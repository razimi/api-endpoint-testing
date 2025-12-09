from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'attendance-system-secret-key'
    
    # Allowed origins - UPDATE THESE FOR PRODUCTION
    ALLOWED_ORIGINS = [
        'http://localhost:3000',  # React dev server
        'http://localhost:8080',  # Vue dev server
        'http://localhost:4200',  # Angular dev server
        'http://127.0.0.1:3000',
        'http://127.0.0.1:8080',
        'http://127.0.0.1:4200',
        # Production domains
        'https://api.mypisang.info',
        'https://mypisang.info',
        'https://www.mypisang.info',
        'http://api.mypisang.info',  # For development/testing
    ]
    
    # Add CORS headers to all responses (for web apps only - mobile apps don't need CORS)
    @app.after_request
    def after_request(response):
        from flask import request
        origin = request.headers.get('Origin')
        
        # CORS headers are only needed for browser-based requests
        # Mobile apps, desktop apps, and server-to-server calls don't need CORS
        if origin:  # Only add CORS headers if Origin header is present (browser requests)
            # For development/testing, allow all origins
            if app.debug:
                response.headers['Access-Control-Allow-Origin'] = '*'
            # For production, only allow specific origins
            elif origin in ALLOWED_ORIGINS:
                response.headers['Access-Control-Allow-Origin'] = origin
            
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        return response
    
    # Handle preflight OPTIONS requests (browser CORS preflight)
    @app.before_request
    def handle_preflight():
        from flask import request
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            origin = request.headers.get('Origin')
            
            # Only handle CORS for browser requests (with Origin header)
            if origin:
                # For development/testing, allow all origins
                if app.debug:
                    response.headers['Access-Control-Allow-Origin'] = '*'
                # For production, only allow specific origins
                elif origin in ALLOWED_ORIGINS:
                    response.headers['Access-Control-Allow-Origin'] = origin
                    
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.attendance import attendance_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/v1/attendance')
    
    return app