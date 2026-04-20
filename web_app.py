import os
from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from detect import detect_objects
from predict import predict_image

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'outputs')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    result = None
    image_url = None
    output_image_url = None
    selected_task = 'detection'

    if request.method == 'POST':
        file = request.files.get('image')
        selected_task = request.form.get('task', 'detection')
        if file is None or file.filename == '':
            error = 'Please select an image file to upload.'
            return render_template('index.html', error=error, selected_task=selected_task)

        if not allowed_file(file.filename):
            error = 'Only JPG, JPEG, and PNG files are supported.'
            return render_template('index.html', error=error, selected_task=selected_task)

        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        image_url = url_for('uploaded_file', filename=filename)

        if selected_task == 'classification':
            label, confidence = predict_image(input_path)
            result = {
                'task_name': 'Food Freshness Analysis',
                'label': label,
                'confidence': confidence,
            }
        else:
            output_name = f'detected_{filename}'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_name)
            detections, saved_path = detect_objects(input_path, output_path)
            output_image_url = url_for('output_file', filename=os.path.basename(saved_path)) if saved_path else None
            largest_object = detections[0] if detections else None
            result = {
                'task_name': 'Object Inspection Analysis',
                'objects': detections,
                'total_objects': len(detections),
                'largest_object': largest_object,
            }

    return render_template(
        'index.html',
        error=error,
        result=result,
        image_url=image_url,
        output_image_url=output_image_url,
        selected_task=selected_task,
    )


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/outputs/<path:filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
    )
