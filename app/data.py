from datetime import datetime, date

# Mock users data
USERS = [
    {
        "id": 1,
        "username": "john_doe",
        "password": "password123",
        "email": "john@company.com",
        "role": "employee",
        "manager_id": 5
    },
    {
        "id": 2,
        "username": "jane_smith",
        "password": "password123",
        "email": "jane@company.com",
        "role": "employee", 
        "manager_id": 5
    },
    {
        "id": 3,
        "username": "bob_wilson",
        "password": "password123",
        "email": "bob@company.com",
        "role": "employee",
        "manager_id": 6
    },
    {
        "id": 4,
        "username": "alice_brown",
        "password": "password123",
        "email": "alice@company.com",
        "role": "employee",
        "manager_id": 6
    },
    {
        "id": 5,
        "username": "manager_smith",
        "password": "manager123",
        "email": "smith@company.com",
        "role": "manager"
    },
    {
        "id": 6,
        "username": "manager_jones",
        "password": "manager123",
        "email": "jones@company.com",
        "role": "manager"
    }
]

# Mock attendance data
ATTENDANCE = [
    {
        "id": 1,
        "user_id": 1,
        "date": "2025-12-05",
        "check_in": "09:15:00",
        "check_out": "17:30:00",
        "status": "late",
        "remark": "Traffic jam on highway",
        "remark_verified": False,
        "verified_by": None,
        "manager_note": None
    },
    {
        "id": 2,
        "user_id": 1,
        "date": "2025-12-04",
        "check_in": "09:00:00",
        "check_out": "17:00:00",
        "status": "on_time",
        "remark": None,
        "remark_verified": None,
        "verified_by": None,
        "manager_note": None
    },
    {
        "id": 3,
        "user_id": 1,
        "date": "2025-12-03",
        "check_in": "08:55:00",
        "check_out": "16:45:00",
        "status": "early_leave",
        "remark": "Doctor appointment",
        "remark_verified": True,
        "verified_by": 5,
        "manager_note": "Acceptable reason"
    },
    {
        "id": 4,
        "user_id": 2,
        "date": "2025-12-05",
        "check_in": "08:45:00",
        "check_out": "17:15:00",
        "status": "on_time",
        "remark": None,
        "remark_verified": None,
        "verified_by": None,
        "manager_note": None
    },
    {
        "id": 5,
        "user_id": 2,
        "date": "2025-12-04",
        "check_in": "09:30:00",
        "check_out": "17:00:00",
        "status": "late",
        "remark": "Child was sick, had to take to hospital",
        "remark_verified": False,
        "verified_by": None,
        "manager_note": None
    },
    {
        "id": 6,
        "user_id": 3,
        "date": "2025-12-05",
        "check_in": "09:00:00",
        "check_out": "17:00:00",
        "status": "on_time",
        "remark": None,
        "remark_verified": None,
        "verified_by": None,
        "manager_note": None
    },
    {
        "id": 7,
        "user_id": 4,
        "date": "2025-12-05",
        "check_in": "09:10:00",
        "check_out": "17:00:00",
        "status": "late",
        "remark": "Train delay due to signal problem",
        "remark_verified": True,
        "verified_by": 6,
        "manager_note": "Valid reason - public transport issue"
    }
]

# Helper functions
def find_user_by_username(username):
    """Find user by username"""
    return next((user for user in USERS if user["username"] == username), None)

def find_user_by_email(email):
    """Find user by email"""
    return next((user for user in USERS if user["email"] == email), None)

def find_user_by_id(user_id):
    """Find user by ID"""
    return next((user for user in USERS if user["id"] == user_id), None)

def get_user_attendance(user_id, date_filter=None):
    """Get attendance records for a specific user"""
    user_records = [record for record in ATTENDANCE if record["user_id"] == user_id]
    
    if date_filter:
        user_records = [record for record in user_records if record["date"] == date_filter]
    
    return user_records

def get_staff_attendance(manager_id, date_filter=None):
    """Get attendance records for all staff under a manager"""
    # Get all employees under this manager
    staff_ids = [user["id"] for user in USERS if user.get("manager_id") == manager_id]
    
    staff_records = []
    for record in ATTENDANCE:
        if record["user_id"] in staff_ids:
            # Add employee info to record
            employee = find_user_by_id(record["user_id"])
            record_with_employee = record.copy()
            record_with_employee["employee"] = {
                "id": employee["id"],
                "username": employee["username"],
                "email": employee["email"]
            }
            staff_records.append(record_with_employee)
    
    if date_filter:
        staff_records = [record for record in staff_records if record["date"] == date_filter]
    
    return staff_records

def find_attendance_by_id(attendance_id):
    """Find attendance record by ID"""
    return next((record for record in ATTENDANCE if record["id"] == attendance_id), None)

def update_attendance_remark(attendance_id, remark):
    """Update remark for attendance record"""
    for record in ATTENDANCE:
        if record["id"] == attendance_id:
            record["remark"] = remark
            record["remark_verified"] = False  # Reset verification when remark is updated
            record["verified_by"] = None
            record["manager_note"] = None
            return record
    return None

def verify_attendance_remark(attendance_id, verified, manager_id, manager_note=None):
    """Verify attendance remark by manager"""
    for record in ATTENDANCE:
        if record["id"] == attendance_id:
            record["remark_verified"] = verified
            record["verified_by"] = manager_id
            record["manager_note"] = manager_note
            return record
    return None