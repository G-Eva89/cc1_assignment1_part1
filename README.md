# AWS S3 Image Gallery

NYU Cloud Computing Assignment 1 - Part I

## Description
A Flask web application that allows users to upload, view, and delete images stored in AWS S3.

## Technologies Used
- **AWS EC2** (SUSE Linux)
- **AWS S3** (Storage)
- **Python 3** with Flask
- **Boto3** (AWS SDK)

## Features
- Upload images to S3 bucket
- Display gallery of uploaded images
- Delete images from S3
- Responsive web interface

## Setup Instructions

### Prerequisites
- AWS Account with EC2 and S3 access
- Python 3 installed
- Flask and Boto3 libraries

### Installation

1. Clone this repository
2. Install dependencies:
```bash
pip3 install flask boto3
```

3. Update `app.py` with your S3 bucket name:
```python
S3_BUCKET = 'cc1part1'
S3_REGION = 'us-east-2'
```

4. Configure AWS credentials (IAM role on EC2 or `aws configure`)

5. Run the application:
```bash
python3 app.py
```

6. Access at `http://your-ec2-ip:8080`

## Configuration

### S3 Bucket Policy
Add this policy to your S3 bucket for public read access:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::cc1part1/*"
        }
    ]
}
```

### EC2 Security Group
Allow inbound traffic on port 8080 (Custom TCP)
