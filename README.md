# Attendance System API

A dummy RESTful API built with Flask for an attendance management system. Uses fixed/mock data instead of a real database to simulate attendance tracking for employees and managers.

## Features

### Core API Endpoints

1. **Authentication**
   - `POST /api/v1/auth/login` - User login (employee/manager roles)

2. **Employee Attendance**
   - `GET /api/v1/attendance/my` - View own attendance records
   - `GET /api/v1/attendance/my?date=2025-12-05` - View attendance for specific date
   - `PUT /api/v1/attendance/{id}/remark` - Add/update remark for late/early attendance

3. **Manager Functions** 
   - `GET /api/v1/attendance/staff` - View supervised staff attendance
   - `GET /api/v1/attendance/staff?date=2025-12-05` - View staff attendance for specific date
   - `PUT /api/v1/attendance/{id}/verify` - Verify staff remark

### Fixed Data Structure

- **User Objects** (hardcoded employees and managers)
  - `id` (Integer)
  - `username` (String)
  - `email` (String)
  - `role` (String: 'employee' or 'manager')
  - `manager_id` (Integer: for employees)

- **Attendance Records** (hardcoded attendance data)
  - `id` (Integer)
  - `user_id` (Integer)
  - `date` (Date)
  - `check_in` (Time)
  - `check_out` (Time)
  - `status` (String: 'on_time', 'late', 'early_leave')
  - `remark` (String: employee's explanation)
  - `remark_verified` (Boolean: manager verification)
  - `verified_by` (Integer: manager_id)

Note: Data is static and predefined - no actual database persistence.

### Request/Response Examples

#### 1. Login - Employee Success
```json
POST /api/v1/auth/login
{
  "email": "john@company.com",
  "password": "password123"
}

HTTP 200 OK
{
  "success": true,
  "data": {
    "token": "fake-jwt-token-123456",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@company.com",
      "role": "employee",
      "manager_id": 5
    }
  },
  "message": "Login successful"
}

// Login Failure
POST /api/v1/auth/login
{
  "email": "invalid@company.com",
  "password": "wrong"
}

HTTP 401 Unauthorized
{
  "success": false,
  "error": "Invalid email or password",
  "code": "AUTH_FAILED"
}
```

#### 2. View Own Attendance
```json
GET /api/v1/attendance/my
Authorization: Bearer fake-jwt-token-123456

HTTP 200 OK
{
  "success": true,
  "data": [
    {
      "id": 1,
      "date": "2025-12-05",
      "check_in": "09:15:00",
      "check_out": "17:30:00",
      "status": "late",
      "remark": "Traffic jam on highway",
      "remark_verified": false
    },
    {
      "id": 2,
      "date": "2025-12-04",
      "check_in": "09:00:00",
      "check_out": "17:00:00",
      "status": "on_time",
      "remark": null,
      "remark_verified": null
    }
  ]
}

// Unauthorized access
HTTP 401 Unauthorized
{
  "success": false,
  "error": "Invalid or missing token",
  "code": "UNAUTHORIZED"
}
```

#### 3. Add Remark
```json
PUT /api/v1/attendance/1/remark
{
  "remark": "Had to drop kids at school due to wife's emergency"
}

HTTP 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "remark": "Had to drop kids at school due to wife's emergency",
    "remark_verified": false
  },
  "message": "Remark updated successfully"
}

// Attendance record not found
HTTP 404 Not Found
{
  "success": false,
  "error": "Attendance record not found",
  "code": "RECORD_NOT_FOUND"
}

// Not authorized to update this record
HTTP 403 Forbidden
{
  "success": false,
  "error": "Not authorized to update this attendance record",
  "code": "FORBIDDEN"
}
```

#### 4. Manager View Staff (Manager Login)
```json
POST /api/v1/auth/login
{
  "email": "smith@company.com",
  "password": "manager123"
}

HTTP 200 OK
{
  "success": true,
  "data": {
    "token": "fake-jwt-token-789012",
    "user": {
      "id": 5,
      "username": "manager_smith",
      "email": "smith@company.com",
      "role": "manager"
    }
  },
  "message": "Login successful"
}
```

#### 5. Manager View Staff Attendance
```json
GET /api/v1/attendance/staff
Authorization: Bearer fake-jwt-token-789012

HTTP 200 OK
{
  "success": true,
  "data": [
    {
      "id": 1,
      "employee": {
        "id": 1,
        "username": "john_doe",
        "email": "john@company.com"
      },
      "date": "2025-12-05",
      "check_in": "09:15:00",
      "check_out": "17:30:00",
      "status": "late",
      "remark": "Traffic jam on highway",
      "remark_verified": false
    }
  ]
}

// Non-manager trying to access staff data
HTTP 403 Forbidden
{
  "success": false,
  "error": "Manager role required to view staff attendance",
  "code": "INSUFFICIENT_PRIVILEGES"
}
```

#### 6. Manager Verify Remark
```json
PUT /api/v1/attendance/1/verify
{
  "verified": true,
  "manager_note": "Acceptable reason"
}

HTTP 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "remark_verified": true,
    "verified_by": 5,
    "manager_note": "Acceptable reason"
  },
  "message": "Remark verified successfully"
}

// Employee trying to verify (not manager)
HTTP 403 Forbidden
{
  "success": false,
  "error": "Manager role required to verify remarks",
  "code": "INSUFFICIENT_PRIVILEGES"
}

// Invalid request data
HTTP 400 Bad Request
{
  "success": false,
  "error": "Missing required field: verified",
  "code": "VALIDATION_ERROR"
}
```



## Business Requirements

- **Role-based Access Control** - Employee vs Manager permissions
- **Date Filtering** - View attendance by specific date
- **Remark System** - Employees can explain late/early attendance
- **Manager Verification** - Managers can approve/reject remarks
- **Hierarchical Structure** - Employees belong to specific managers
- **Simulation/Dummy API** - Fixed data responses for testing
- **No Database Persistence** - In-memory fixed attendance data

## Getting Started

1. **Setup Environment**
   ```bash
   source venv/bin/activate
   pip install flask
   ```

2. **Run Development Server**
   ```bash
   python app.py
   ```
   or
   ```bash
   flask run
   ```

**No database setup needed** - all data is hardcoded in the application.

## API Documentation

- Base URL: `http://localhost:5000/api/v1`
- Authentication: **Simulated JWT tokens** (role-based)
- Content-Type: `application/json`
- All endpoints return **fixed mock attendance data**
- Role-based access: Employee sees own data, Manager sees staff data
- Date filtering supported via query parameters
- Remark operations are simulated (no actual persistence)

### HTTP Status Codes Used

- `200 OK` - Successful requests
- `400 Bad Request` - Invalid request data/validation errors
- `401 Unauthorized` - Invalid/missing authentication token
- `403 Forbidden` - Insufficient privileges for operation
- `404 Not Found` - Requested resource not found

## Technology Stack

- **Backend**: Flask (minimal setup)
- **Data**: Fixed/hardcoded Python dictionaries and lists
- **Authentication**: Simulated (no real auth)
- **CORS**: Configured for web application consumption
- **Testing**: Basic manual testing

**Minimal Dependencies**: Only Flask required for basic simulation.

## Security Notes

### CORS Configuration

- **Development**: Allows all origins (`*`) when `debug=True`
- **Production**: Only allows specific whitelisted domains
- **Configuration**: Update `ALLOWED_ORIGINS` in `app/__init__.py` for production

### Mobile App Considerations

- **No CORS Issues**: Mobile apps make direct HTTP requests (not browser-based)
- **API Base URL**: Use `http://your-server.com:5001/api/v1` for production
- **Authentication**: Store JWT tokens securely in device storage
- **Network Security**: Always use HTTPS in production
- **Rate Limiting**: Consider implementing API rate limits per user/device

### Client Types Supported

- ✅ **Web Applications** (React, Vue, Angular) - Requires CORS configuration
- ✅ **Mobile Apps** (iOS, Android, React Native, Flutter) - No CORS needed
- ✅ **Desktop Apps** (Electron, .NET, etc.) - No CORS needed
- ✅ **Server-to-Server** API calls - No CORS needed

### For Production Deployment

1. Set `debug=False` in `app.py`
2. Update `ALLOWED_ORIGINS` with your actual web frontend domains (mobile apps don't need this)
3. Use HTTPS for all production domains
4. Consider implementing proper JWT authentication
5. Add rate limiting and input validation
6. Use environment variables for configuration

## Mobile App Integration

### Base URLs

- **Development**: `http://localhost:5001/api/v1`
- **Production**: `https://your-domain.com/api/v1`

### Example Mobile App Usage

#### React Native/Expo

```javascript
// Development
const API_BASE = 'http://localhost:5001/api/v1';
// Production
// const API_BASE = 'https://api.mypisang.info/api/v1';

// Login
const login = async (email, password) => {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
};

// Get attendance with token
const getAttendance = async (token) => {
  const response = await fetch(`${API_BASE}/attendance/my`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
};
```

#### Flutter/Dart

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class AttendanceApi {
  // Development
  static const String baseUrl = 'http://localhost:5001/api/v1';
  // Production
  // static const String baseUrl = 'https://api.mypisang.info/api/v1';
  
  static Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    return jsonDecode(response.body);
  }
  
  static Future<Map<String, dynamic>> getAttendance(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/attendance/my'),
      headers: {'Authorization': 'Bearer $token'},
    );
    return jsonDecode(response.body);
  }
}
```

### Mobile-Specific Considerations

- **No CORS Issues**: Mobile HTTP requests bypass browser CORS restrictions
- **Token Storage**: Store JWT tokens securely (Keychain/Keystore)
- **Network Handling**: Handle offline scenarios gracefully
- **SSL Pinning**: Consider certificate pinning for production
- **Error Handling**: Implement proper error handling for network failures

## Docker Deployment

### Quick Start with Docker Compose

#### Development Mode
```bash
# Start the application in development mode
docker-compose up -d

# View logs
docker-compose logs -f attendance-api

# Stop the application
docker-compose down
```

#### Production Mode (Behind External Proxy)
```bash
# Start the Flask app container (without built-in nginx)
docker-compose up -d

# The Flask API will be available at:
# - Container port: http://localhost:5000
# - Through external proxy: https://api.mypisang.info
```

### Available Docker Commands

```bash
# Build and start services
docker-compose up --build -d

# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f attendance-api

# Scale the application (multiple instances behind proxy)
docker-compose up -d --scale attendance-api=3
# Note: Configure external nginx with multiple upstream servers for load balancing

# Execute commands inside container
docker-compose exec attendance-api python -c "from app.data import USERS; print(len(USERS))"

# Stop all services
docker-compose down

# Remove all containers and networks
docker-compose down --volumes --remove-orphans
```

### Environment Configuration

Create a `.env` file for custom configuration:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000
HOST=0.0.0.0

# Security
SECRET_KEY=your-super-secret-key-here

# Custom allowed origins for CORS (production)
ALLOWED_ORIGINS=https://api.mypisang.info,https://mypisang.info,https://www.mypisang.info
```

### Production Deployment Checklist

1. **Environment Variables**
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=false
   ```

2. **SSL Certificates** (for HTTPS)
   - Place certificates in `./ssl/` directory
   - Update `nginx.conf` with your domain
   - Uncomment HTTPS server block in `nginx.conf`

3. **Domain Configuration**
   - Domain: `api.mypisang.info` (already configured)
   - Configure DNS A record to point to your server IP
   - SSL certificates should be placed in `./ssl/cert.pem` and `./ssl/key.pem`

4. **Security Hardening**
   - Change default secret key
   - Enable firewall rules
   - Regular security updates
   - Monitor logs

### Container Specifications

- **Base Image**: Python 3.11 slim
- **Port**: 5000 (internal), 5001 (external)
- **Health Check**: Automatic API health monitoring
- **Restart Policy**: Unless stopped manually
- **Network**: Isolated bridge network
- **Volume**: Optional app directory mounting for development
- **Proxy Ready**: Configured to work behind external nginx proxy

## External Nginx Proxy Configuration

This container is designed to run behind an external nginx proxy. Use the provided `nginx-proxy.conf` configuration:

### Setup External Nginx

1. **Copy proxy configuration**:
   ```bash
   sudo cp nginx-proxy.conf /etc/nginx/sites-available/api.mypisang.info
   sudo ln -s /etc/nginx/sites-available/api.mypisang.info /etc/nginx/sites-enabled/
   ```

2. **Update SSL certificate paths in the config**:
   ```bash
   sudo nano /etc/nginx/sites-available/api.mypisang.info
   # Update ssl_certificate and ssl_certificate_key paths
   ```

3. **Test and reload nginx**:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Proxy Benefits
- ✅ **SSL Termination** handled by external nginx
- ✅ **Load Balancing** across multiple container instances
- ✅ **Rate Limiting** and security headers
- ✅ **Static File Serving** (if needed)
- ✅ **Centralized Logging** and monitoring

### Monitoring and Logging

```bash
# Monitor resource usage
docker stats attendance-api

# View health check status
docker inspect --format='{{.State.Health.Status}}' attendance-api

# Export logs
docker-compose logs attendance-api > app.log 2>&1
```