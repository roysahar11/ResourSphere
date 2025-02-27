# ResourSphere Backend

## 🏗️ Backend Architecture
The backend service is a FastAPI application that directly interfaces with AWS services, providing:
- Centralized policy enforcement
- Unified audit trail for AWS operations
- AWS API abstraction layer
- Role-based access control

## 🔧 Backend Installation

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

4. Verify configuration files in `app/config` (see instructions ahead ):
- `users.yml`: User credentials and permissions
- `groups.yml`: Group definitions and permissions
- `security.yml`: JWT token configuration
- `secrets.yml`: Secret keys and passwords

## 🛠️ Backend Configuration

### User Configuration
```yaml
# app/config/users.yml
roysahar:
  username: roysahar
  group: developers
  password_hash: $2b$12$IRjsxvDUqr1GICJB/sVsb.uOCZDP3YkQk.nD4L618Al7PVXiPo.Fu
```

### Group Configuration
```yaml
# app/config/groups.yml
developers:
  permissions:
    ec2_max_running: 3
    ec2_instance_types:
      - t3.nano
      - t4g.nano
    ami_choice:
      ubuntu-x86: "ami-04b4f1a9cf54c11d0"
      amazon-x86: "ami-053a45fff0a704a47"
```


## 🚀 Backend API Reference

### Authentication Endpoints

```
POST /auth/login
```

**Request body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_at_utc": "2025-02-26T21:00:00.000000Z",
  "user_permissions": {
    "ec2_max_running": 3,
    "ec2_instance_types": ["t3.nano", "t4g.nano"],
    "ami_choice": {
      "ubuntu-x86": "ami-04b4f1a9cf54c11d0",
      "amazon-x86": "ami-053a45fff0a704a47",
      "ubuntu-arm": "ami-0a7a4e87939439934",
      "amazon-arm": "ami-0f37c4a1ba152af46"
    }
  }
}
```