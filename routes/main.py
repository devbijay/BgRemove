import io
import cv2
import numpy as np
import base64

from flask import Blueprint, render_template, request, jsonify

from utils.utility import remove_bg, allowed_file

landing = Blueprint("landing", "__name__")


@landing.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if img_file := request.files['image']:
            img_bytes = img_file.read()

            # Read the image using OpenCV
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = remove_bg(img)

            # Convert the result to base64 format
            _, img_encoded = cv2.imencode('.png', img)
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')

            return render_template('index.html', image=img_base64)

        print(img_file)
    return render_template('index.html')
