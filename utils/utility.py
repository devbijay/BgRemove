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