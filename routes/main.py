import io
import cv2
import numpy as np
import base64

from flask import Blueprint, render_template, request, jsonify

landing = Blueprint("landing", "__name__")

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_bg(img):
    # Remove the background using OpenCV
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    fg = cv2.erode(thresh, None, iterations=1)
    bgt = cv2.dilate(thresh, None, iterations=1)
    ret, bg = cv2.threshold(bgt, 1, 128, 1)
    marker = cv2.add(fg, bg)
    marker32 = np.int32(marker)
    cv2.watershed(img, marker32)
    m = cv2.convertScaleAbs(marker32)
    _, thresh = cv2.threshold(m, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_inv = cv2.bitwise_not(thresh)
    img[thresh_inv == 0] = (255, 255, 255)
    return img


@landing.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if img_file := request.files['image']:
            # if not allowed_file(img_file):
            #     return jsonify({'error': 'No image uploaded'})

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
