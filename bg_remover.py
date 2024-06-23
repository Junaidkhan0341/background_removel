import io
from flask import Flask, request, jsonify, send_file
from PIL import Image
from rembg import remove
import zipfile
from pathlib import Path
import uuid

app = Flask(__name__)

MAX_FILES = 5
ALLOWED_TYPES = ["png", "jpg", "jpeg"]

def remove_background(image_bytes):
    """Removes the background from an image."""
    result = remove(image_bytes)
    return Image.open(io.BytesIO(result)).convert("RGBA")

def img_to_bytes(img):
    """Converts an Image object to bytes."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

@app.route('/api/background-remover/remove', methods=['POST'])
def remove_background_api():
    """API endpoint to remove background from uploaded images."""
    uploaded_files = request.files.getlist('images')
    
    if not uploaded_files:
        return jsonify({'error': 'No files uploaded.'}), 400
    
    if len(uploaded_files) > MAX_FILES:
        return jsonify({'error': f'Maximum {MAX_FILES} files allowed.'}), 400
    
    results = []
    
    for uploaded_file in uploaded_files:
        image_bytes = uploaded_file.read()
        result_image = remove_background(image_bytes)
        results.append(result_image)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for idx, result in enumerate(results):
            result_bytes = img_to_bytes(result)
            zip_file.writestr(f"image_{idx+1}_nobg.png", result_bytes)
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="background_removed_images.zip",
        mimetype="application/zip"
    )

if __name__ == '__main__':
    app.run(debug=True)
