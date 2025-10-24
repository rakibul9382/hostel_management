from flask import Flask,session
from dotenv import load_dotenv  # ✅ Add this line
import os
from .config import Config
def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes.home import home_bp
    from app.routes.admin import admin_bp
    from app.routes.fees import fees_bp
    from app.routes.room import room_bp
    from app.routes.login import login_bp
    from app.routes.registration import registration_bp
    from app.routes.logout import logout_bp
    from app.routes.complaint import complaint_bp
    from app.routes.mees import mess_bp
    from app.routes.profile import profile_bp
    from app.routes.student import student_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(fees_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(mess_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(student_bp)
    return app