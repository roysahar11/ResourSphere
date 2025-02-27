# ResourSphere - Simplified AWS Resource Management

ResourSphere is a comprehensive solution for simplifying AWS resource management in your organization. Consisting of a FastAPI backend service and a command-line interface (CLI) tool, this integrated system allows your developers to easily provision AWS resources as they need, while giving your DevOps team complete control over the process with role-based access control policies.

![Version](https://img.shields.io/badge/version-0.0.5-blue)

## 🎯 Why ResourSphere?

### For Developers
- **Simple Resource Creation**: Get the cloud resources you need in seconds through CLI commands
- **No AWS Expertise Required**: Abstract away complex AWS configurations into simple commands
- **Quick Setup**: Install the CLI tool and start creating resources immediately

### For DevOps Teams
- **Centralized Control**: Maintain control over resource creation policies via simple configurations
- **Automatic Compliance**: Enforce tagging, naming conventions, and security policies automatically

## 🌟 Key Features

- **Unified Access Control**: Role-based permissions that integrate with your existing team structure
- **Secure by Design**: JWT authentication, encrypted communication, and no local AWS credentials
- **Automated Best Practices**: Built-in resource tagging, naming conventions, and security policies

## Components
1. **ResouSphere Backend**: A FastAPI server that handles AWS interactions, authentication, and policy enforcement
Backend documentation: [View Backend Documentation](backend/README.md)
2. **ResourSphere CLI**: A simple command-line tool for requesting and managing resources
CLI documentation: [View CLI Documentation](frontend_cli/README.md)


### Supported AWS Services
- **EC2 Management**: Create, list, start, stop, and terminate EC2 instances
- **S3 Storage**: Create buckets, upload files, and manage storage with configurable public access
- **DNS Management**: Create and manage Route53 DNS zones and records

## 🔒 Security Considerations
- Authentication tokens are stored securely
- No passwords are stored locally in the CLI
- All communication uses token-based authentication
- Permissions are enforced at the backend level

## 📝 License
[MIT License](LICENSE)

## 👥 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact
For any questions or support, please open an issue in the repository.

## Author
Roy Sahar