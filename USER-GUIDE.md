# Application User Guide
This guide provides step-by-step instructions for deploying and running the ITAM (IT Asset Management) application.<br>
There are two deployment methods available:
1. **Manual Deployment** - Deploy infrastructure and application manually
2. **CI/CD Deployment** - Automated deployment via GitHub Actions

## Prerequisites
### Required Software (Manual Deployment Method Only)
**Note**: For CI/CD method, you don't need to install any software locally - everything runs in GitHub Actions. You only need a GitHub account and to configure 5 secrets.

For manual deployment method, ensure you have the following installed on your local machine:
1. **Git** - For cloning the repository
2. **Terraform** - For infrastructure provisioning
3. **Docker** or **Docker Desktop** - For building and pushing container images

### AWS Account Requirements
- AWS Access Key ID, Secret Access Key and AWS Session Token:
  - `aws_access_key_id`, `aws_secret_access_key` and `aws_session_token` values is required to set in `terraform.tfvars` file (manual deployment)
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` will be provisioned to Github Secrets for CI/CD deployment
- Active AWS account with appropriate permissions to create:
  - VPC, Subnets, Internet Gateway
  - EC2 Instances
  - Security Groups
  - Application Load Balancer
  - Key Pairs

### Docker Hub Account
- For manual deployment (used for image pushing to Docker Hub), `docker_repo` value is required to set in `terraform.tfvars` file
- Secrets `DOCKER_USERNAME` and `DOCKER_PASSWORD` provisioning to GitHub (used in CI/CD deployment method)

### GitHub Account
- GitHub account
- Repository access (or fork the repository)

## Method 1: Manual Deployment

## Method 2: CI/CD Deployment