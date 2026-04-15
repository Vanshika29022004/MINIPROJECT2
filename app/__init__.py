from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

# Initialize extensions
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    """Factory function to build the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = 'code-blue-secret-key!@#'
    
    # Initialize SocketIO with this app
    socketio.init_app(app)
    
    # Attach socket to Timer System
    from app.core.timer_system import timers
    timers.init_app(socketio)
    
    # Register blueprints 
    from app.api.routes import bp as api_bp
    app.register_blueprint(api_bp)
    
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
        
    return app
