# Flask API Endpoint Development Guide

## Project Features & Requirements

Document your specific API requirements and features in one of these locations for AI agents to reference:

1. **README.md** - Main project overview with feature list and API endpoints
2. **docs/features.md** - Detailed feature specifications and business requirements  
3. **docs/api-spec.md** - API endpoint specifications with request/response examples
4. **GitHub Issues** - Individual features as issues with acceptance criteria
5. **This file** - Add a "Current Features" section below for immediate reference

When describing features to an AI agent, include:
- Specific API endpoints needed (GET /api/users, POST /api/orders, etc.)
- Request/response data structures
- Business logic requirements
- Database schema needs
- Authentication/authorization requirements

## Project Architecture

This is a Flask-based API endpoint project following RESTful principles. The project structure should follow these conventions:

```
apiendpoint/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   ├── routes/              # Route handlers organized by resource
│   ├── services/            # Business logic layer
│   └── utils/               # Helper functions and utilities
├── config/
│   ├── __init__.py
│   ├── development.py       # Dev environment config
│   └── production.py        # Prod environment config
├── tests/                   # Unit and integration tests
├── migrations/              # Database migration files (if using Flask-Migrate)
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── app.py                   # Application entry point
```

## Development Workflow

### Environment Setup
- Virtual environment is already created in `venv/`
- Activate with: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- For development: `pip install -r requirements-dev.txt`

### Running the Application
- Development: `flask run` or `python app.py`
- Production: Use WSGI server like Gunicorn
- Environment variables: Use `.env` file with `python-dotenv`

### Key Dependencies to Install
```bash
pip install flask flask-sqlalchemy flask-migrate python-dotenv
pip install pytest pytest-flask black flake8  # dev dependencies
```

## Code Patterns & Conventions

### Flask App Factory Pattern
Use the application factory pattern in `app/__init__.py`:
```python
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api/v1')
    
    return app
```

### Route Organization
- Group related endpoints in blueprints by resource (e.g., `users.py`, `orders.py`)
- Use descriptive route names following REST conventions
- Example blueprint structure in `app/routes/users.py`:
```python
from flask import Blueprint
users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    # Implementation here
```

### Error Handling
- Implement consistent error responses using custom exception handlers
- Return JSON responses with appropriate HTTP status codes
- Example error handler:
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
```

### Database Models
- Use SQLAlchemy with Flask-SQLAlchemy
- Place models in `app/models/` directory
- Follow naming conventions: PascalCase for classes, snake_case for attributes
- Include `__repr__` methods for debugging

### Testing Strategy
- Use pytest with pytest-flask plugin
- Test structure mirrors app structure: `tests/routes/`, `tests/models/`
- Use fixtures for common test data
- Test both success and error scenarios
- Example test structure:
```python
def test_get_users(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 200
```

## Configuration Management

### Environment-Based Config
- Use class-based configuration in `config/`
- Load sensitive data from environment variables
- Example config pattern:
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
```

### Environment Variables
Create `.env` file for development (add to `.gitignore`):
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///dev.db
```

## API Response Patterns

### Consistent JSON Structure
```python
# Success response
{
    "success": true,
    "data": { ... },
    "message": "Operation completed successfully"
}

# Error response
{
    "success": false,
    "error": "Error message",
    "code": "ERROR_CODE"
}
```

### Pagination for List Endpoints
```python
{
    "success": true,
    "data": [...],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "pages": 5
    }
}
```

## Development Commands

### Database Operations
```bash
flask db init          # Initialize migrations
flask db migrate       # Generate migration
flask db upgrade        # Apply migrations
```

### Testing
```bash
pytest                  # Run all tests
pytest -v              # Verbose output
pytest tests/routes/    # Test specific directory
```

### Code Quality
```bash
black .                 # Format code
flake8 .               # Check linting
```

## Security Considerations

- Always validate input data using libraries like Marshmallow or WTForms
- Use CORS properly if serving frontend applications
- Implement authentication/authorization as needed (JWT, Flask-Login)
- Never commit secrets to version control
- Use environment variables for configuration

## Common Debugging Tips

- Use Flask's debug mode for development: `FLASK_ENV=development`
- Add logging throughout the application using Python's logging module
- Use Flask's `current_app.logger` for application-specific logging
- Test API endpoints using tools like Postman or curl
- Use `flask shell` for interactive debugging with application context

Remember to follow RESTful principles, maintain consistent error handling, and write comprehensive tests for all endpoints.

## Getting Started for AI Agents

When starting development:

1. **Check project requirements** in README.md or ask the user for specific features
2. **Create the basic Flask structure** using the architecture pattern above
3. **Set up dependencies** with `pip install flask flask-sqlalchemy python-dotenv`
4. **Create configuration files** in `config/` directory
5. **Implement core models** in `app/models/` based on data requirements
6. **Build API routes** in `app/routes/` following REST conventions
7. **Add error handling** and validation
8. **Write tests** for all endpoints
9. **Create migration files** for database schema

Always ask for clarification on specific business requirements, data models, and API behavior before implementing features.