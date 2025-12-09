import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Configure for proxy deployment
    behind_proxy = os.getenv('BEHIND_PROXY', 'false').lower() == 'true'
    
    if behind_proxy:
        # When behind proxy, trust proxy headers
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    app.run(debug=debug, host=host, port=port)