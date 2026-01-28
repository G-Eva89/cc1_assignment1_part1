from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from botocore.exceptions import NoCredentialsError
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
S3_BUCKET = 'cc1part1'  # S3 Bucket that I created
S3_REGION = 'us-east-2' 

# Initialize S3 client
s3_client = boto3.client('s3', region_name=S3_REGION)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Display gallery of images from S3"""
    try:
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        
        images = []
        if 'Contents' in response:
            for obj in response['Contents']:
                # Generate public URL for each image
                image_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{obj['Key']}"
                images.append({
                    'name': obj['Key'],
                    'url': image_url,
                    'size': obj['Size'],
                    'date': obj['LastModified']
                })
        
        return render_template('index.html', images=images)
    
    except Exception as e:
        flash(f'Error loading images: {str(e)}', 'danger')
        return render_template('index.html', images=[])

@app.route('/upload', methods=['POST'])
def upload():
    """Handle image upload to S3"""
    if 'file' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{file.filename}"
            
            # Upload to S3
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                filename,
                ExtraArgs={
                    'ContentType': file.content_type,
                }
            )
            
            flash(f'Successfully uploaded {file.filename}!', 'success')
        
        except NoCredentialsError:
            flash('AWS credentials not configured properly', 'danger')
        except Exception as e:
            flash(f'Upload failed: {str(e)}', 'danger')
    else:
        flash('Invalid file type. Please upload an image.', 'warning')
    
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    """Delete image from S3"""
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=filename)
        flash(f'Deleted {filename}', 'success')
    except Exception as e:
        flash(f'Delete failed: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
