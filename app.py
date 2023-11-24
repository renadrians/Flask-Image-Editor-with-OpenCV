from flask import Flask, render_template, request, redirect, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import cv2
from werkzeug.utils import secure_filename
import numpy as np
import requests

app = Flask(__name__)

load_dotenv()

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg'}
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)

def init_db():
    db.create_all()

def remove_background(image_path, selected_option):
    api_key = 'w5N54GfnT11719grEdve5G9Q'
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},
        headers={'X-Api-Key': api_key},
    )
    
    if response.status_code == requests.codes.ok:
        edited_filename = f'edited_{selected_option}_{os.path.basename(image_path)}'
        edited_path = os.path.join(app.config['UPLOAD_FOLDER'], edited_filename)
        
        with open(edited_path, 'wb') as out:
            out.write(response.content)
        
        return cv2.imread(edited_path)
    else:
        print(f"Error: {response.status_code}, {response.content}")
        return None


def flip_vertical(image_path):
    image = cv2.imread(image_path)
    flipped_image = cv2.flip(image, 0)
    return flipped_image

def flip_horizontal(image_path):
    image = cv2.imread(image_path)
    flipped_image = cv2.flip(image, 1)
    return flipped_image

def apply_sharpen(image_path):
    image = cv2.imread(image_path)
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image

def apply_blur(image_path):
    image = cv2.imread(image_path)
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
    return blurred_image

def apply_bnw(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bnw_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    return bnw_image

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    init_db()
    images = Image.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        new_image = Image(filename=filename)
        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/edit/<int:image_id>', methods=['GET', 'POST'])
def edit_image(image_id):
    image = Image.query.get(image_id)

    if request.method == 'POST':
        selected_options = request.form.getlist('options')

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        edited_image = None

        for option in selected_options:
            if option == 'flip_vertical':
                edited_image = flip_vertical(image_path)
            elif option == 'flip_horizontal':
                edited_image = flip_horizontal(image_path)
            elif option == 'sharpen':
                edited_image = apply_sharpen(image_path)
            elif option == 'blur':
                edited_image = apply_blur(image_path)
            elif option == 'bnw':
                edited_image = apply_bnw(image_path)
            elif option == 'removeBackground':
                edited_image = remove_background(image_path, option)  
        if edited_image is not None:
            edited_filename = f'edited_{selected_options[0]}_{image.filename}'
            edited_path = os.path.join(app.config['UPLOAD_FOLDER'], edited_filename)
            cv2.imwrite(edited_path, edited_image)

            new_edited_image = Image(filename=edited_filename)
            db.session.add(new_edited_image)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('edit.html', image=image)

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        edited_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'edited_{image.filename}')
        
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(edited_image_path):
            os.remove(edited_image_path)
            
        db.session.delete(image)
        db.session.commit()
        
    return redirect(url_for('index'))

@app.route('/download/<filename>', methods=['GET'])
def download_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)