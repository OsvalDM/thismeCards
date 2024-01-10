from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify, send_file, abort
from flask_mysqldb import MySQL
import hashlib
import qrcode
import os
import urllib.parse
from PIL import Image
from datetime import datetime
from flask_cors import CORS

def getUserCookie():
    myCookie = request.cookies.get('user')

    if myCookie:        
        userId, userName, haveCard, admin = myCookie.split(':')
        return (userId, userName, haveCard, admin)
    else:
        return None
    
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
    static_folder = os.path.join(os.getcwd(), 'static/data')
    img_path = os.path.join(static_folder, filename)

    img.save(img_path, 'PNG')

    return ('data/' + filename, img_path)
    
def generate_filename(id, field, fileExtension):
    return f"{id}_{field}.{fileExtension}"

def deleteFile(name):
    file_Img = 'static/' + name
    if os.path.exists(file_Img):                        
        os.remove(file_Img)