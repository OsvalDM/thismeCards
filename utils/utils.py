from flask import session
import qrcode
import os
import urllib.parse

def verifySignIn():
    user = session.get('user', None)
    if user:
        return user
    else:
        return None
    
def logoutAux():
    session.clear()
    return {'result' : 'success'}
    
def get_filename(url):
    parsed_url = urllib.parse.urlparse(url)
    filename = parsed_url.netloc + parsed_url.path.replace('/', '_')
    return filename + '.png'

def generateQr(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = get_filename(url)
    static_folder = os.path.join(os.getcwd(), 'static/data/qr')
    img_path = os.path.join(static_folder, filename)

    img.save(img_path, 'PNG')

    return ('data/qr/' + filename, img_path)
    
def generate_filename(id, field, fileExtension):
    return f"{id}_{field}.{fileExtension}"

def deleteFile(name):
    file_Img = 'static/' + name
    if os.path.exists(file_Img):                        
        os.remove(file_Img)