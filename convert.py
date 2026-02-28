from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_xls_to_xlsx():
    file = request.files.get('file')
    if not file:
        return {'error': 'No file provided'}, 400

    # Save uploaded file to a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, file.filename)
        file.save(input_path)

        # Use LibreOffice headless to convert to xlsx
        result = subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'xlsx',
            '--outdir', tmpdir, input_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            return {'error': 'LibreOffice conversion failed', 'details': result.stderr}, 500

        # Find the output file
        output_filename = os.path.splitext(file.filename)[0] + '.xlsx'
        output_path = os.path.join(tmpdir, output_filename)

        if not os.path.exists(output_path):
            return {'error': 'Converted file not found'}, 500

        # Read and return before tempdir is deleted
        with open(output_path, 'rb') as f:
            data = f.read()

    import io
    return send_file(
        io.BytesIO(data),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='converted.xlsx'
    )

if __name__ == '__main__':
    app.run(debug=True)
