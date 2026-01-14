from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return "❌ No file part in the request."
    
    files = request.files.getlist('files')
    if not files:
        return "❌ No files selected."
    
    saved_files = []
    for file in files:
        if file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            saved_files.append(file.filename)
    
    if not saved_files:
        return "⚠️ No valid files uploaded."
    
    uploaded_list = "<br>".join(saved_files)
    return f"✅ Uploaded {len(saved_files)} files successfully!<br><br>{uploaded_list}"

@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return "<h3>No files uploaded yet.</h3>"
    return '<br>'.join([f"<a href='/download/{file}'>{file}</a>" for file in files])

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    # Run on all network interfaces so mobile can access
    app.run(host='0.0.0.0', port=5173, debug=True)
