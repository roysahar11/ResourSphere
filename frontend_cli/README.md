# ResourSphere CLI

Command-line interface for managing AWS resources through ResourSphere.

## 🔧 Installation

```bash
git clone https://github.com/yourusername/resourcesphere-cli.git
cd resourcesphere-cli
pip install -e .
```

## 🚀 Usage Guide

### Authentication
```bash
# Login with interactive prompt
resourcesphere auth login

# Login with username provided
resourcesphere auth login -u yourusername

# Logout
resourcesphere auth logout
```

### EC2 Management
```bash
# Create instance
resourcesphere ec2 create --ami ubuntu-x86 --type t3.nano --name my-server

# List instances
resourcesphere ec2 list

# Start/Stop/Delete instance
resourcesphere ec2 start my-test-server
resourcesphere ec2 stop my-test-server
resourcesphere ec2 delete my-test-server
```

## 🛠️ Configuration
The CLI stores configuration in the `~/resourcesphere` directory:
- `.user`: Your username
- `.permissions`: Your user permissions
- `.tmp/.token`: Authentication token
- `.token_expires_at`: Token expiration time 