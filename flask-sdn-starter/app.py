from flask import Flask, render_template
from .extensions import db, jwt, api
from .config import Config
from .resources.auth import auth_blp
from .resources.sdn_api import firewall_blp, openflow_blp
from flask_jwt_extended import JWTManager
from .blocklist import BLOCKLIST
from .models.user import UserModel
from werkzeug.security import generate_password_hash


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

    
    api.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_blp)
    app.register_blueprint(firewall_blp)
    app.register_blueprint(openflow_blp)

    @app.route("/login")
    def login():
        return render_template("login.html")
    @app.route("/")
    def home():
        return '<a href="/docs">Go to Swagger API Documentation</a>'
    @app.route('/ui')
    def api_ui():
        return render_template('api_ui.html')

    # ✅ Main Pages
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/stats")
    def stats():
        return render_template("stats.html")

    @app.route("/flow_table")
    def flow_table():
        return render_template("flow_table.html")

    @app.route("/firewall")
    def firewall():
        return render_template("firewall.html")

    @app.route("/meter_group")
    def meter_group():
        return render_template("meter_group.html")

    @app.route("/user_management")
    def user_management():
        return render_template("user_management.html")

    # ✅ Logout Route
    @app.route("/logout")
    def logout():
        return redirect(url_for('login'))  # Redirects to login page

    return app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
