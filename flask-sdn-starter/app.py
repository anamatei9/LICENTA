from flask import Flask, render_template
from .extensions import db, jwt, api
from .config import Config
from .resources.auth import auth_blp
from .resources.sdn_api import firewall_blp, openflow_blp
from flask_jwt_extended import JWTManager
from .blocklist import BLOCKLIST
from .models.user import UserModel
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, redirect, url_for
from .resources.role_required import viewer_required, operator_required, admin_required


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if not UserModel.query.filter_by(username="ana").first():
            admin = UserModel(
                username="ana",
                password=generate_password_hash("admin123", method="pbkdf2:sha256", salt_length=8),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user 'ana' created.")


    jwt.init_app(app)
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = UserModel.query.get(identity)
        if user:
            return {"role": user.role}
        return {"role": "viewer"}  # fallback, just in case

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            {"message": "The token has been revoked.", "error": "token_revoked"},
            401,
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return redirect(url_for('index'))

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return redirect(url_for('index'))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('index'))
        
    api.init_app(app)
    @app.before_request
    def check_jwt_cookie():
        from flask import request
        
        # Skip for login and static routes
        if request.path == '/' or request.path == '/login' or request.path.startswith('/static'):
            return
            
        # Check for token in cookies
        token = request.cookies.get('access_token')
        if token:
            # Add to request headers
            request.environ['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    # Register blueprints
    app.register_blueprint(auth_blp)
    app.register_blueprint(firewall_blp)
    app.register_blueprint(openflow_blp)

    @app.route('/')
    def index():
        return render_template('login.html')
    @app.route('/ui')
    def api_ui():
        return render_template('api_ui.html')
    @app.route('/login')
    def login():
        return render_template('login.html')


    # ✅ Main Pages
    @app.route("/dashboard", methods=["GET", "POST"])
    @viewer_required
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/stats")
    @viewer_required 
    def stats():
        return render_template("stats.html")

    @app.route("/flow_table")
    @operator_required
    def flow_table():
        return render_template("flow_table.html")

    @app.route("/firewall")
    @operator_required
    def firewall():
        return render_template("firewall.html")

    @app.route("/meter_group")
    @operator_required
    def meter_group():
        return render_template("meter_group.html")

    @app.route("/user_management")
    @admin_required
    def user_management():
        return render_template("user_management.html")

    @app.route("/logout")
    def logout():
        return redirect('/')  # Directly redirects to the root URL

    return app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
