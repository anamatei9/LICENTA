from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_app.models.user import UserModel
from flask_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort  # in case you want to use it for cleaner error handling
from flask_app.blocklist import BLOCKLIST
from flask_jwt_extended import  get_jwt_identity
from flask_jwt_extended import  create_refresh_token
from flask_app.resources.role_required import admin_required

auth_blp = Blueprint("auth", __name__, url_prefix="/auth", description="Authentication endpoints")

@auth_blp.route("/secret")
class SecretRoute(MethodView):
    @jwt_required()
    @auth_blp.response(200, description="Returns a secret message")
    def get(self):
        current_user = get_jwt_identity()
        return {"message": f"Welcome, user #{current_user}! 🔒 This is protected data."}
    
@auth_blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @auth_blp.response(200, description="Logs out the current user")
    def post(self):
        jti = get_jwt()["jti"]  # Unique token ID
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}

@auth_blp.route("/register")
class UserRegister(MethodView):
    @auth_blp.response(201, description="User created")
    def post(self):
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return {"message": "Username and password required."}, 400

        if UserModel.query.filter_by(username=data["username"]).first():
            return {"message": "User already exists."}, 409

        new_user = UserModel(
            username=data["username"],
            password=generate_password_hash(data["password"])
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully."}, 201

@auth_blp.route("/users")
class UserList(MethodView):
    @jwt_required()
    @admin_required
    @auth_blp.response(200)
    def get(self):
        users = UserModel.query.all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
            for user in users
        ]
@auth_blp.route("/users/<int:user_id>")
class UserRoleUpdate(MethodView):
    @jwt_required()
    @admin_required
    @auth_blp.response(200)
    def put(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return {"message": "User not found."}, 404

        data = request.get_json()  # ✅ Get JSON manually
        new_role = data.get("role")  

        if new_role not in ["viewer", "operator", "admin"]:
            return {"message": "Invalid role. Must be viewer, operator, or admin."}, 400

        user.role = new_role
        db.session.commit()
        return {"message": f"User '{user.username}' role updated to '{new_role}'."}

@auth_blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @auth_blp.response(200, description="Returns new access token")
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}
        
@auth_blp.route("/login", methods=["POST"])
class UserLogin(MethodView):
    def post(self):
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return {"message": "Username and password required."}, 400

        # ✅ Check if the user already exists
        user = UserModel.query.filter_by(username=data["username"]).first()

        # ✅ If user doesn't exist, create a new one
        if not user:
            user = UserModel(
                username=data["username"],
                password=generate_password_hash(data["password"]),  # ✅ Hash the password
                role="viewer"
            )
            db.session.add(user)
            db.session.commit()  # ✅ Ensure user is saved

        # ✅ Now verify the login
        if check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "Invalid credentials."}, 401