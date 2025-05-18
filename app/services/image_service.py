import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file, folder=None, resize=None):
    """
    Save an image to the upload folder.
    
    Args:
        file: The file object from request.files
        folder: Sub-folder within uploads to save to (optional)
        resize: Tuple of (width, height) to resize image (optional)
        
    Returns:
        Saved filename or None if failed
    """
    if not file or not allowed_file(file.filename):
        return None
        
    # Generate secure filename with UUID to avoid collisions
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    new_filename = f"{uuid.uuid4().hex}{ext}"
    
    # Determine upload path
    upload_dir = current_app.config['UPLOAD_FOLDER']
    if folder:
        upload_dir = os.path.join(upload_dir, folder)
        os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, new_filename)
    
    # Process and save the image
    try:
        if resize:
            img = Image.open(file)
            img = img.resize(resize, Image.LANCZOS)
            img.save(file_path)
        else:
            file.save(file_path)
        return new_filename
    except Exception as e:
        current_app.logger.error(f"Error saving image: {str(e)}")
        return None

def delete_image(filename, folder=None):
    """Delete an image from the upload folder."""
    if not filename:
        return False
        
    upload_dir = current_app.config['UPLOAD_FOLDER']
    if folder:
        upload_dir = os.path.join(upload_dir, folder)
    
    file_path = os.path.join(upload_dir, filename)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        current_app.logger.error(f"Error deleting image: {str(e)}")
    
    return False

def get_image_url(filename, folder=None):
    """Get URL for an image."""
    if not filename:
        return None
        
    if folder:
        return f"/static/images/uploads/{folder}/{filename}"
    return f"/static/images/uploads/{filename}"
