# ResourSphere Backend

## 🏗️ Backend Architecture
The backend service is a FastAPI application that directly interfaces with AWS services, providing:
- Centralized policy enforcement
- Unified audit trail for AWS operations
- AWS API abstraction layer
- Role-based access control

## 📋 Prerequisites

Before installing and running the backend, ensure you have:

1. Python 3.8 or higher installed
2. pip package manager
3. AWS account with appropriate permissions
4. AWS CLI installed and configured
5. Git installed


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

4. Verify configuration files in `app/config` (see instructions ahead ):
- `users.yml`: User credentials and permissions
- `groups.yml`: Group definitions and permissions
- `security.yml`: JWT token configuration
- `secrets.yml`: Holds a secret jwt key

## 🛠️ Backend Configuration

### 1. AWS Credentials
You'll need to create an access key for an IAM user that has sufficient permissions to manage the resources you wish to manage with ResourSphere (EC2, S3, and Route53).

Then, run this command to configure the "resousphere" AWS profile on your machine:
```bash
aws configure --profile resoursphere
```

### Secret JWT key
JWT uses a *secret key* to encode and decode the user access token used for users authentication in API requests.

Choost your own strong key, or you can use _dev/secret_key_generator.py_ for quickly generating a random strong key.
Then, you can store it in a _secrets.yml_ file in _app/config/_:
```yaml
#app/config/secrets.yml
---
jwt_secret_key: your-super-strong-key
```

*Alternatively*, you can use a secrets manager of your choice and retrieve the secret key whe the service starts up. 
In _app/config.py_, look for the _load_jwt_secret_key()_ function, and modify it to retrieve your secret key:
```python
#app/config.py
def load_jwt_secret_key():
    secret_key = #code to retrieve your secret key from a secrets manager
    return secret_key
```



### 2. Users, Groups & Permisisons
Users and groups can be configured in these files:
- app/config/users.yml
- app/config/groups.yml

###Permissions/Constraints
There are currently 3 permissions/constraints you can control using ResourSphere:
- ec2_max_running: the maximum number of running EC2 instances the user is allowed to have at once (if this limit is reached, ResourSphere will not allow to create or start more EC2 instances)
- ec2_instance_types: a list of EC2 instance types the user is allowed to create.
- ami_choice: a dictionary of AMIs that the user is allowed to use when creating an EC2 instance

example of permissions definition for a user/group:
```yaml
permissions:
  ec2_max_running: 3 #An integer number.
  ec2_instance_types:
    - t3.nano #Instance type names exactly as they appear in AWS
    - t4g.nano
  ami_choice:
    ubuntu-x86: #include an AMI id, for example: "ami-04b4f1a9cf54c11d0"
    amazon-x86: #include an AMI id, for example: "ami-04b4f1a9cf54c11d0"
```
This _permissions_ dictionary can appear both in user and group definitions, when user-defined permission will always override group permissions. You can specify all of these permissions

#### Defining Groups
You an *optionaly* define groups to easily manage permissions for multiple users at once.

Group definition example:
```yaml
# app/config/groups.yml
developers:
  permissions: #A dictionary of permissions
```

#### Defining Users
To define a user you currently need to manually hash the password and store it in the configuration file. Run _app/setup/hashing_passwords.py_ to hash the desired password.

User definition example:
```yaml
# app/config/users.yml
roysahar:
  username: roysahar
  group: developers #Optional: put the user in a group
  password_hash: #Hashed password
  permissions: #An optional dictionary of permissions
```


## 🚀 Backend API Reference

### Authentication Endpoint

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

For additional API documentation, run ResorSphere Backend and visit the automatically generated FastAPI docs at:

- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation

These interactive documentation pages are automatically generated from the FastAPI code and provide detailed information about all available endpoints, request/response schemas, and authentication requirements.