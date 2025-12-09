from flask import Blueprint, request, jsonify
from app.routes.auth import get_user_from_token
from app.data import (
    get_user_attendance, 
    get_staff_attendance, 
    find_attendance_by_id,
    update_attendance_remark,
    verify_attendance_remark,
    find_user_by_id
)

attendance_bp = Blueprint('attendance', __name__)

def require_auth():
    """Helper function to get authenticated user from request"""
    auth_header = request.headers.get('Authorization', '')
    user = get_user_from_token(auth_header)
    
    if not user:
        return None, jsonify({
            "success": False,
            "error": "Invalid or missing token",
            "code": "UNAUTHORIZED"
        }), 401
    
    return user, None, None

@attendance_bp.route('/my', methods=['GET'])
def get_my_attendance():
    """Get current user's attendance records"""
    try:
        user, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        # Get date filter if provided
        date_filter = request.args.get('date')
        
        # Get user's attendance records
        records = get_user_attendance(user["id"], date_filter)
        
        return jsonify({
            "success": True,
            "data": records
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }), 500

@attendance_bp.route('/<int:attendance_id>/remark', methods=['PUT'])
def update_remark(attendance_id):
    """Update remark for attendance record"""
    try:
        user, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required",
                "code": "VALIDATION_ERROR"
            }), 400
        
        remark = data.get('remark')
        if remark is None:
            return jsonify({
                "success": False,
                "error": "Missing required field: remark",
                "code": "VALIDATION_ERROR"
            }), 400
        
        # Find attendance record
        attendance = find_attendance_by_id(attendance_id)
        if not attendance:
            return jsonify({
                "success": False,
                "error": "Attendance record not found",
                "code": "RECORD_NOT_FOUND"
            }), 404
        
        # Check if user owns this record
        if attendance["user_id"] != user["id"]:
            return jsonify({
                "success": False,
                "error": "Not authorized to update this attendance record",
                "code": "FORBIDDEN"
            }), 403
        
        # Update remark
        updated_record = update_attendance_remark(attendance_id, remark)
        
        return jsonify({
            "success": True,
            "data": {
                "id": updated_record["id"],
                "remark": updated_record["remark"],
                "remark_verified": updated_record["remark_verified"]
            },
            "message": "Remark updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }), 500

@attendance_bp.route('/staff', methods=['GET'])
def get_staff_attendance():
    """Get attendance records for staff (manager only)"""
    try:
        user, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        # Check if user is a manager
        if user["role"] != "manager":
            return jsonify({
                "success": False,
                "error": "Manager role required to view staff attendance",
                "code": "INSUFFICIENT_PRIVILEGES"
            }), 403
        
        # Get date filter if provided
        date_filter = request.args.get('date')
        
        # Get staff attendance records
        records = get_staff_attendance(user["id"], date_filter)
        
        return jsonify({
            "success": True,
            "data": records
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }), 500

@attendance_bp.route('/<int:attendance_id>/verify', methods=['PUT'])
def verify_remark(attendance_id):
    """Verify attendance remark (manager only)"""
    try:
        user, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        # Check if user is a manager
        if user["role"] != "manager":
            return jsonify({
                "success": False,
                "error": "Manager role required to verify remarks",
                "code": "INSUFFICIENT_PRIVILEGES"
            }), 403
        
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required",
                "code": "VALIDATION_ERROR"
            }), 400
        
        verified = data.get('verified')
        manager_note = data.get('manager_note', '')
        
        if verified is None:
            return jsonify({
                "success": False,
                "error": "Missing required field: verified",
                "code": "VALIDATION_ERROR"
            }), 400
        
        # Find attendance record
        attendance = find_attendance_by_id(attendance_id)
        if not attendance:
            return jsonify({
                "success": False,
                "error": "Attendance record not found",
                "code": "RECORD_NOT_FOUND"
            }), 404
        
        # Check if the employee belongs to this manager
        employee = find_user_by_id(attendance["user_id"])
        if not employee or employee.get("manager_id") != user["id"]:
            return jsonify({
                "success": False,
                "error": "Not authorized to verify this attendance record",
                "code": "FORBIDDEN"
            }), 403
        
        # Verify remark
        updated_record = verify_attendance_remark(attendance_id, verified, user["id"], manager_note)
        
        return jsonify({
            "success": True,
            "data": {
                "id": updated_record["id"],
                "remark_verified": updated_record["remark_verified"],
                "verified_by": updated_record["verified_by"],
                "manager_note": updated_record["manager_note"]
            },
            "message": "Remark verified successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }), 500