from flask import Flask, redirect, url_for
from config import Config
from models import db
from models.user import User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    # Inisialisasi Database
    db.init_app(app)

    # Inisialisasi Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu untuk mengakses halaman admin.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.survey import survey_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(survey_bp)
    app.register_blueprint(auth_bp, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix='/admin/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Global 404 Error Handler
    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('survey.landing'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
