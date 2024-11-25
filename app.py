from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '1245678'
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_year=2023)

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['resume']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and file.filename.endswith('.pdf'):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('options'))

    flash('Invalid file format. Please upload a PDF file.')
    return redirect(url_for('index'))

@app.route('/options')
def options():
    return render_template('options.html', current_year=2023)

if __name__ == '__main__':
    app.run(debug=True)
