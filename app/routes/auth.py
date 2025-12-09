from flask import Blueprint, request, jsonify
from app.data import find_user_by_username, find_user_by_email
import uuid

auth_bp = Blueprint('auth', __name__)

# Store active tokens (in a real app, use Redis or database)
ACTIVE_TOKENS = {}

def generate_token(user):
    """Generate a fake JWT token"""
    token = f"fake-jwt-token-{uuid.uuid4().hex[:12]}"
    ACTIVE_TOKENS[token] = user
    return token

def get_user_from_token(token):
    """Get user from token"""
    if not token:
        return None
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    return ACTIVE_TOKENS.get(token)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required",
                "code": "VALIDATION_ERROR"
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                "success": False,
                "error": "Email and password are required",
                "code": "VALIDATION_ERROR"
            }), 400
        
        # Find user
        user = find_user_by_email(email)
        
        if not user or user['password'] != password:
            return jsonify({
                "success": False,
                "error": "Invalid email or password",
                "code": "AUTH_FAILED"
            }), 401
        
        # Generate token
        token = generate_token(user)
        
        # Prepare user data (exclude password)
        user_data = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
        
        # Add manager_id for employees
        if user["role"] == "employee":
            user_data["manager_id"] = user["manager_id"]
        
        return jsonify({
            "success": True,
            "data": {
                "token": token,
                "user": user_data
            },
            "message": "Login successful"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }), 500