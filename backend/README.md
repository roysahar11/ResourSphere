# ResourSphere Backend

## 🏗️ Backend Architecture
The backend service is a FastAPI application that directly interfaces with AWS services, providing:
- Centralized policy enforcement
- Unified audit trail for AWS operations
- AWS API abstraction layer
- Role-based access control

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resoursphere.git
cd resoursphere/backend
```

2. Install the package:
```bash
pip install .
```

3. Configure AWS credentials:
```bash
aws configure --profile resoursphere
```

4. Verify configuration files in `app/config`:
- `users.yml`: User credentials and permissions
- `groups.yml`: Group definitions and permissions
- `security.yml`: JWT token configuration
- `secrets.yml`: Secret keys and passwords

## 🚀 API Reference

### Authentication Endpoints

```
POST /auth/login
```

[Rest of the backend API documentation...] 