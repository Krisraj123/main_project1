from flask import Flask, render_template, request, redirect, url_for, flash
import os
from helpers import polish_resume_ai

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

@app.route('/polish_resume', methods=['GET', 'POST'])
def polish_resume():
    polished_content = None

    if request.method == "POST":
        position_name = request.form['position_name']
        polish_prompt = request.form.get('polish_prompt', '')
        resume_file = request.files.get('resume_file')
        if resume_file and resume_file.filename.endswith('.pdf'):
            try:
                polished_content = polish_resume_ai(position_name, resume_file , polish_prompt)
            except Exception as e:
                flash(f'Error occurred while processing the resume: {str(e)}')
        else:
            flash('Invalid file format. Please upload a PDF file.')
    return render_template('polish_resume.html', polished_content = polished_content)



if __name__ == '__main__':
    app.run(debug=True)
