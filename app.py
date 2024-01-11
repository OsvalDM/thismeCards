from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
from flask_mysqldb import MySQL
import hashlib
import os
from datetime import datetime

from controllers.postController import *
from utils.utils import *

app = Flask(__name__)

#Configuración de la base de datos
app.config['MYSQL_HOST'] = '198.12.240.41'
app.config['MYSQL_USER'] = 'adminRE'
app.config['MYSQL_PASSWORD'] = 'R0str03mP%'
app.config['MYSQL_DB'] = 'rostroempresarial'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

mysql = MySQL(app)

#Methods get
#Verified endpoint +
@app.route('/')
def landing():
    return render_template('landing.html')

#Verified endpoint +
@app.route('/signup')
def signup():        
    return render_template('signup.html')
        
#Verified endpoint +
@app.route('/login')
def login():
    return render_template('login.html')

#Verified endpoint +
@app.route('/example')
def example():
    return render_template('example.html')



#Methods post

@app.route('/token', methods=['POST'])
def postToken():
    data = request.get_json()    
    token = data['token']
    result = verifySignToken(mysql, token)
    return jsonify(result)


#Error handler
#Verified endpoint
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404


#----------------------------------------------------------------------
#Verified endpoint
@app.route('/restore')
def restore():
    return render_template('restorePSW.html')

#Verified endpoint
@app.route('/user')
def home():
    userInfo = getUserCookie()
    if userInfo:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (userInfo[0],))
        cardData = cur.fetchone()

        urlQr = generateQr( 'http://cardscarnival.com/mycard/' + userInfo[0] )


        ##Traer datos
        content = { 
            'cardData': None,
            'profilePicData': None,
            'imgPortafolio': None,
            'redSocial': None,
            'clientes' : None
        }
        
        cardData = None  # Initialize cardData here

        try:
            cur = mysql.connection.cursor()

            cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (userInfo[0],))
            cardData = cur.fetchone()

            if cardData:
                content['cardData'] = cardData

                cur.execute('SELECT * FROM imgPerfil WHERE tarjeta = %s', (cardData[0],))
                profilePicData = cur.fetchall()
                if profilePicData:
                    content['profilePicData'] = profilePicData

                cur.execute('SELECT * FROM imgPortafolio WHERE tarjeta = %s', (cardData[0],))
                imgPortafolio = cur.fetchall()
                if imgPortafolio:
                    content['imgPortafolio'] = imgPortafolio

                cur.execute('SELECT * FROM redSocial WHERE tarjeta = %s', (cardData[0],))
                redSocial = cur.fetchall()
                if redSocial:
                    content['redSocial'] = redSocial

                cur.execute('SELECT * FROM cliente WHERE tarjeta = %s', (cardData[0],))
                clientes = cur.fetchall()
                if clientes:
                    content['clientes'] = clientes

        except Exception as e:
            print(e)
            return redirect(url_for('restore'))

        finally:
            cur.close()

        if cardData != None:
            return render_template('home.html', haveCard = True, userName = userInfo[1], qrSource = urlQr, content = content)
        else:
            return render_template('home.html', haveCard = False, userName = userInfo[1], qrSource = urlQr, content = content)
    else:        
        return redirect(url_for('login'))

#Verified endpoint
@app.route('/createCard')
def createCard():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'False':
            return render_template('createCard.html', userName = userInfo[1])
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

#Verified endpoint
@app.route('/editCard')
def editCard():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            content = { 
                'cardData': None,
                'profilePicData': None,
                'imgPortafolio': None,
                'redSocial': None,
                'clientes' : None
            }
            
            cardData = None
            
            try:
                cur = mysql.connection.cursor()

                cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (userInfo[0],))
                cardData = cur.fetchone()

                if cardData:
                    content['cardData'] = cardData

                    cur.execute('SELECT * FROM imgPerfil WHERE tarjeta = %s', (cardData[0],))
                    profilePicData = cur.fetchall()
                    if profilePicData:
                        content['profilePicData'] = profilePicData

                    cur.execute('SELECT * FROM imgPortafolio WHERE tarjeta = %s', (cardData[0],))
                    imgPortafolio = cur.fetchall()
                    if imgPortafolio:
                        noImgPath = 'img/noImg.png'
                        imgs = [noImgPath, noImgPath, noImgPath, noImgPath, noImgPath, noImgPath]

                        for img in imgPortafolio:
                            if 'content1' in img[1]:
                                imgs[0] = img[1]
                            elif 'content2' in img[1]:
                                imgs[1] = img[1]
                            elif 'content3' in img[1]:
                                imgs[2] = img[1]
                            elif 'content4' in img[1]:
                                imgs[3] = img[1]
                            elif 'content5' in img[1]:
                                imgs[4] = img[1]
                            elif 'content6' in img[1]:
                                imgs[5] = img[1]

                        content['imgPortafolio'] = imgs

                    cur.execute('SELECT * FROM redSocial WHERE tarjeta = %s', (cardData[0],))
                    redSocial = cur.fetchall()
                    if redSocial:
                        socials = ['','','','']
                        for redSocialData in redSocial:
                            if redSocialData[1] == 'facebook':
                                socials[0] = redSocialData[2]
                            elif redSocialData[1] == 'instagram':
                                socials[1] = redSocialData[2]
                            elif redSocialData[1] == 'twitter':
                                socials[2] = redSocialData[2]
                            elif redSocialData[1] == 'linkedin':
                                socials[3] = redSocialData[2]
                            
                        content['redSocial'] = socials

                    cur.execute('SELECT * FROM cliente WHERE tarjeta = %s', (cardData[0],))
                    clientes = cur.fetchall()
                    if clientes:
                        content['clientes'] = clientes

            except Exception as e:
                print(e)
                return redirect(url_for('restore'))

            finally:
                cur.close()

            return render_template('editCard.html', userName = userInfo[1], content = content)
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

#Verified endpoint
@app.route('/mycard/<id>')
def mycard(id):
    content = { 
        'cardData': None,
        'profilePicData': None,
        'imgPortafolio': None,
        'redSocial': None,
        'clientes' : None
    }
    
    cardData = None

    try:
        cur = mysql.connection.cursor()

        cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (id,))
        cardData = cur.fetchone()

        if cardData:
            content['cardData'] = cardData

            cur.execute('SELECT * FROM imgPerfil WHERE tarjeta = %s', (cardData[0],))
            profilePicData = cur.fetchall()
            if profilePicData:
                content['profilePicData'] = profilePicData

            cur.execute('SELECT * FROM imgPortafolio WHERE tarjeta = %s', (cardData[0],))
            imgPortafolio = cur.fetchall()
            if imgPortafolio:
                content['imgPortafolio'] = imgPortafolio

            cur.execute('SELECT * FROM redSocial WHERE tarjeta = %s', (cardData[0],))
            redSocial = cur.fetchall()
            if redSocial:
                content['redSocial'] = redSocial

            cur.execute('SELECT * FROM cliente WHERE tarjeta = %s', (cardData[0],))
            clientes = cur.fetchall()
            if clientes:
                content['clientes'] = clientes

        else:
            return redirect(url_for('login'))

    except Exception as e:
        print(e)
        return redirect(url_for('login'))

    finally:
        cur.close()

    return render_template('mycard.html', content=content)

#Methods get admin

#Verified endpoint
@app.route('/admin/login')
def loginAdmin():
    return render_template('admin/login.html')

#Verified endpoint
@app.route('/admin/')
def homeAdmin():
    userInfo = getUserCookie()
    if userInfo and userInfo[3] == '1':
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT nombre, apellidoPat, usuario FROM tarjeta')
            user_data = cur.fetchall()

            if user_data:
                return render_template('admin/homeAdmin.html', cards= user_data, userName = userInfo[1])
            else:
                return render_template('admin/homeAdmin.html', cards= None, userName = userInfo[1])

        except Exception as e:
            print(e)
            return redirect(url_for('login'))

        finally:
            cur.close()
    
    else:        
        return redirect(url_for('login'))

#Verified endpoint 
@app.route('/admin/logs')
def logs():
    userInfo = getUserCookie()
    if userInfo and userInfo[3] == '1':
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM movimientos')
            logs = cur.fetchall()

            if logs:
                return render_template('admin/logs.html', logs= logs, userName = userInfo[1])
            else:
                return render_template('admin/logs.html', logs= None, userName = userInfo[1])

        except Exception as e:
            print(e)
            return redirect(url_for('login'))

        finally:
            cur.close()
    
    else:        
        return redirect(url_for('login'))

#Midleware routes get
        
#Verified endpoint
@app.route('/logout')
def logout():
    userInfo = getUserCookie()
    if userInfo:
        resp = make_response(redirect(url_for('login')))
        resp.delete_cookie('user')
        return resp
    else:
        return redirect(url_for('login'))

#Methods post
    
#Verified endpoint
@app.route('/login', methods=['POST'])
def loginPost():
    try:
        idWorker = request.form['idWorker']
        password = request.form['password']
        hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE id = %s', (idWorker,))
        user_data = cur.fetchone()

        cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (idWorker,))
        card_data = cur.fetchone()

        haveCard = False
        if card_data:
            haveCard = True

        if user_data:
            if user_data[2] == hashedPassword:                
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('user', f'{user_data[0]}:{user_data[1]}:{haveCard}:{user_data[3]}', max_age=7200)
                return resp
            else:
                return redirect(url_for('login'))
        else:            
            return redirect(url_for('login'))

    except Exception as e:
        print(e)
        return  redirect(url_for('login'))

    finally:
        cur.close()

#Verified endpoint
@app.route('/signup', methods=['POST'])
def signupPost():
    cur = None
    try:
        idWorker = request.form['idWorker']
        name = request.form['name']
        password = request.form['password']
        pregunta = request.form['pregunta']
        respuesta = request.form['respuesta']
        hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()        

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuario(id, nombreUsuario, psw) VALUES (%s, %s, %s)', (idWorker, name, hashedPassword) )
        mysql.connection.commit()

        cur.execute('INSERT INTO recuperacionContrasena(usuario, pregunta, respuesta) VALUES (%s, %s, %s)', (idWorker, pregunta, respuesta) )
        mysql.connection.commit()

    except Exception as e:
        print(e)
        return  redirect(url_for('signup'))

    finally:
        if cur:
            cur.close()

    return  redirect(url_for('login'))

#Verified endpoint
@app.route('/createCard', methods=['POST'])
def createCardPost():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'False':
            cur = None
            try:
                id  = userInfo[0]            
                
                #Campos extra

                nombre = request.form['name']
                apellidoPat = request.form['lastNameFather']
                apellidoMat = request.form['lastNameMother']
                correo = request.form['email']
                telefono = request.form['telephone']
                sobreMi = request.form['message']
                ubicacion = request.form['ubication']
                titulo = request.form['titulo']
                cargo = request.form['cargo']
                lat = request.form['latitude']
                lng = request.form['longitude']
                usuario = userInfo[0]

                cur = mysql.connection.cursor()
                cur.execute('''INSERT INTO tarjeta(nombre, apellidoPat, apellidoMat, correo, telefono, sobreMi, ubicacion, usuario, titulo, cargo, lat, lng) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                            (nombre, apellidoPat, apellidoMat, correo, telefono, sobreMi, ubicacion, usuario, titulo, cargo, lat, lng) )
                mysql.connection.commit()

                cur.execute('SELECT id FROM tarjeta WHERE usuario = %s', (id,))
                cardData = cur.fetchone()

                cur.execute('INSERT INTO movimientos(usuario, accion) VALUES (%s, %s)', (str(usuario) + "_" + nombre + apellidoPat, 'Create card - ' + str(cardData[0]) ) )            
                mysql.connection.commit()
            except Exception as e:
                print(e)
                return  redirect(url_for('createCard'))

            #Imagenes
            try:
                cur.execute('SELECT id FROM tarjeta WHERE usuario = %s', (id,))
                cardData = cur.fetchone()

                if cardData:
                    #profile picture
                    profilePictureMain = request.files['profilePictureMain']      
                    if profilePictureMain:      
                        file_extension = profilePictureMain.filename.rsplit('.', 1)[1].lower()
                        filename_profilePictureMain = generate_filename(id,'profilePictureMain' ,file_extension)
                        filename_profilePictureMain = 'data/profilePictureMain/' + filename_profilePictureMain
                        profilePictureMain.save(f'static/{filename_profilePictureMain}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPerfil VALUES (%s, %s)', (cardData[0], filename_profilePictureMain) )
                        mysql.connection.commit()

                    profilePictureSecond = request.files['profilePictureSecond']            
                    if profilePictureSecond:
                        file_extension = profilePictureSecond.filename.rsplit('.', 1)[1].lower()
                        filename_profilePictureSecond = generate_filename(id,'profilePictureSecond' ,file_extension)
                        filename_profilePictureSecond = 'data/profilePictureSecond/' + filename_profilePictureSecond
                        profilePictureSecond.save(f'static/{filename_profilePictureSecond}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPerfil VALUES (%s, %s)', (cardData[0], filename_profilePictureSecond) )
                        mysql.connection.commit()

                    #portafolio
                    content1 = request.files['content1']            
                    if content1:
                        file_extension = content1.filename.rsplit('.', 1)[1].lower()
                        filename_content1 = generate_filename(id,'content1' ,file_extension)
                        filename_content1 = 'data/content1/' + filename_content1
                        content1.save(f'static/{filename_content1}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content1) )
                        mysql.connection.commit()

                    content2 = request.files['content2']            
                    if content2:
                        file_extension = content2.filename.rsplit('.', 1)[1].lower()
                        filename_content2 = generate_filename(id,'content2' ,file_extension)
                        filename_content2 = 'data/content2/' + filename_content2
                        content2.save(f'static/{filename_content2}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content2) )
                        mysql.connection.commit()

                    content3 = request.files['content3']            
                    if content3:
                        file_extension = content3.filename.rsplit('.', 1)[1].lower()
                        filename_content3 = generate_filename(id,'content3' ,file_extension)
                        filename_content3 = 'data/content3/' + filename_content3
                        content3.save(f'static/{filename_content3}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content3) )
                        mysql.connection.commit()

                    content4 = request.files['content4']            
                    if content4:
                        file_extension = content4.filename.rsplit('.', 1)[1].lower()
                        filename_content4 = generate_filename(id,'content4' ,file_extension)
                        filename_content4 = 'data/content4/' + filename_content4
                        content4.save(f'static/{filename_content4}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content4) )
                        mysql.connection.commit()

                    content5 = request.files['content5']            
                    if content5:
                        file_extension = content5.filename.rsplit('.', 1)[1].lower()
                        filename_content5 = generate_filename(id,'content5' ,file_extension)
                        filename_content5 = 'data/content5/' + filename_content5
                        content5.save(f'static/{filename_content5}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content5) )
                        mysql.connection.commit()

                    content6 = request.files['content6']            
                    if content6:
                        file_extension = content6.filename.rsplit('.', 1)[1].lower()
                        filename_content6 = generate_filename(id,'content6' ,file_extension)
                        filename_content6 = 'data/content6/' + filename_content6
                        content6.save(f'static/{filename_content6}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content6) )
                        mysql.connection.commit()


                    #Redes sociales
                    facebook = request.form['facebook']
                    if facebook != '':
                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'facebook', facebook) )
                        mysql.connection.commit()

                    instagram = request.form['instagram']
                    if instagram != '':
                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'instagram', instagram) )
                        mysql.connection.commit()

                    twitter = request.form['twitter']
                    if twitter != '':
                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'twitter', twitter) )
                        mysql.connection.commit()

                    linkedin = request.form['linkedin']
                    if linkedin != '':
                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'linkedin', linkedin) )
                        mysql.connection.commit()

                    #Update cookie                        
                    resp = make_response(redirect(url_for('home')))
                    resp.set_cookie('user', f'{userInfo[0]}:{userInfo[1]}:{True}:{userInfo[3]}', max_age=7200)
                    return resp

                else:
                    return redirect(url_for('createCard'))
            except Exception as e:
                print(e)
                return  redirect(url_for('createCard'))

            finally:
                if cur:
                    cur.close()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))    

#Verified endpoint
@app.route('/addClient', methods=['POST'])
def addClientPost():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            cur = None
            try:
                id  = userInfo[0]
                cur = mysql.connection.cursor()
                cur.execute('SELECT id FROM tarjeta WHERE usuario = %s', (id,))
                cardData = cur.fetchone()

                if cardData:                    
                    nombre = request.form['name']
                    imgLogo = request.files['logo']
                    extTime = datetime.now().strftime("%Y%m%d%H%M%S")

                    if imgLogo:
                        file_extension = imgLogo.filename.rsplit('.', 1)[1].lower()
                        filename_imgLogo = generate_filename(id,'imgLogo' + extTime ,file_extension)
                        filename_imgLogo = 'data/imgLogo/' + filename_imgLogo
                        imgLogo.save(f'static/{filename_imgLogo}')

                        cur = mysql.connection.cursor()
                        cur.execute('INSERT INTO cliente(nombre, imgLogo, tarjeta) VALUES (%s, %s, %s)', (nombre, filename_imgLogo, cardData[0]) )
                        mysql.connection.commit()

            except Exception as e:
                print(e)
                return  redirect(url_for('createCard'))

            finally:
                if cur:
                    cur.close()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('home'))

#Verified endpoint
@app.route('/editContent', methods=['POST'])
def editContent():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            cur = None
            id  = userInfo[0]      

            try:
                cur = mysql.connection.cursor()    
                cur.execute('SELECT id FROM tarjeta WHERE usuario = %s', (id,))
                cardData = cur.fetchone()

                if cardData:
                    #portafolio
                    content1 = request.files['content1']            
                    if content1:
                        actualImg = request.form['content1id']
                        file_extensionImg = actualImg.rsplit('.', 1)[1].lower()                    
                        file_extensionImg = 'static/data/content1/' + generate_filename(id,'content1' ,file_extensionImg)
                        if os.path.exists(file_extensionImg):                        
                            os.remove(file_extensionImg)

                        file_extension = content1.filename.rsplit('.', 1)[1].lower()
                        filename_content1 = generate_filename(id,'content1' ,file_extension)
                        filename_content1 = 'data/content1/' + filename_content1
                        content1.save(f'static/{filename_content1}')                    

                        cur = mysql.connection.cursor()                    
                        cur.execute('DELETE FROM imgPortafolio where rutaPortafolio = %s', (request.form['content1id'],) )
                        mysql.connection.commit()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content1) )
                        mysql.connection.commit()

                    content2 = request.files['content2']            
                    if content2:
                        actualImg = request.form['content2id']
                        file_extensionImg = actualImg.rsplit('.', 1)[1].lower()                    
                        file_extensionImg = 'static/data/content2/' + generate_filename(id,'content2' ,file_extensionImg)
                        if os.path.exists(file_extensionImg):                        
                            os.remove(file_extensionImg)

                        file_extension = content2.filename.rsplit('.', 1)[1].lower()
                        filename_content2 = generate_filename(id,'content2' ,file_extension)
                        filename_content2 = 'data/content2/' + filename_content2
                        content2.save(f'static/{filename_content2}')

                        cur = mysql.connection.cursor()
                        cur.execute('DELETE FROM imgPortafolio where rutaPortafolio = %s', (request.form['content2id'],) )
                        mysql.connection.commit()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content2) )
                        mysql.connection.commit()

                    content3 = request.files['content3']            
                    if content3:
                        actualImg = request.form['content3id']
                        file_extensionImg = actualImg.rsplit('.', 1)[1].lower()                    
                        file_extensionImg = 'static/data/content3/' + generate_filename(id,'content3' ,file_extensionImg)
                        if os.path.exists(file_extensionImg):                        
                            os.remove(file_extensionImg)

                        file_extension = content3.filename.rsplit('.', 1)[1].lower()
                        filename_content3 = generate_filename(id,'content3' ,file_extension)
                        filename_content3 = 'data/content3/' + filename_content3
                        content3.save(f'static/{filename_content3}')

                        cur = mysql.connection.cursor()
                        cur.execute('DELETE FROM imgPortafolio where rutaPortafolio = %s', (request.form['content3id'],) )
                        mysql.connection.commit()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content3) )
                        mysql.connection.commit()

                    content4 = request.files['content4']            
                    if content4:
                        actualImg = request.form['content4id']
                        file_extensionImg = actualImg.rsplit('.', 1)[1].lower()                    
                        file_extensionImg = 'static/data/content4/' + generate_filename(id,'content4' ,file_extensionImg)
                        if os.path.exists(file_extensionImg):                        
                            os.remove(file_extensionImg)

                        file_extension = content4.filename.rsplit('.', 1)[1].lower()
                        filename_content4 = generate_filename(id,'content4' ,file_extension)
                        filename_content4 = 'data/content4/' + filename_content4
                        content4.save(f'static/{filename_content4}')

                        cur = mysql.connection.cursor()
                        cur.execute('DELETE FROM imgPortafolio where rutaPortafolio = %s', (request.form['content4id'],) )
                        mysql.connection.commit()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content4) )
                        mysql.connection.commit()

                    content5 = request.files['content5']            
                    if content5:
                        actualImg = request.form['content5id']
                        file_extensionImg = actualImg.rsplit('.', 1)[1].lower()                    
                        file_extensionImg = 'static/data/content5/' + generate_filename(id,'content5' ,file_extensionImg)
                        if os.path.exists(file_extensionImg):                        
                            os.remove(file_extensionImg)

                        file_extension = content5.filename.rsplit('.', 1)[1].lower()
                        filename_content5 = generate_filename(id,'content5' ,file_extension)
                        filename_content5 = 'data/content5/' + filename_content5
                        content5.save(f'static/{filename_content5}')

                        cur = mysql.connection.cursor()
                        cur.execute('DELETE FROM imgPortafolio where rutaPortafolio = %s', (request.form['content5id'],) )
                        mysql.connection.commit()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content5) )
                        mysql.connection.commit()

                    content6 = request.files['content6']            
                    if content6:
                        actualImg = request.form['content6id']
                        file_extensionImg = actualImg.rsplit('.', 1)[1].lower()                    
                        file_extensionImg = 'static/data/content6/' + generate_filename(id,'content6' ,file_extensionImg)
                        if os.path.exists(file_extensionImg):                        
                            os.remove(file_extensionImg)

                        file_extension = content6.filename.rsplit('.', 1)[1].lower()
                        filename_content6 = generate_filename(id,'content6' ,file_extension)
                        filename_content6 = 'data/content6/' + filename_content6
                        content6.save(f'static/{filename_content6}')

                        cur = mysql.connection.cursor()
                        cur.execute('DELETE FROM imgPortafolio where rutaPortafolio = %s', (request.form['content6id'],) )
                        mysql.connection.commit()
                        cur.execute('INSERT INTO imgPortafolio VALUES (%s, %s)', (cardData[0], filename_content6) )
                        mysql.connection.commit()

            except Exception as e:
                print(e)
                return  redirect(url_for('createCard'))

            finally:
                if cur:
                    cur.close()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('editCard'))

#Verified endpoint
@app.route('/editClient/<idClient>', methods=['POST'])
def editClient(idClient):
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            cur = None
            id  = userInfo[0]      

            try:
                name = request.form['name']
                logo = request.files['logo']   
                actualImg = request.form['logoid']  
                extTime = datetime.now().strftime("%Y%m%d%H%M%S")
                if logo:
                        file_Img = 'static/' + actualImg
                        if os.path.exists(file_Img):                        
                            os.remove(file_Img)

                        file_extension = logo.filename.rsplit('.', 1)[1].lower()
                        filename_imgLogo = generate_filename(id,'imgLogo' + extTime ,file_extension)
                        filename_imgLogo = 'data/imgLogo/' + filename_imgLogo
                        logo.save(f'static/{filename_imgLogo}')
                        actualImg = filename_imgLogo
                        
                cur = mysql.connection.cursor()    
                cur.execute('UPDATE cliente SET nombre = %s, imgLogo = %s WHERE id = %s', (name,actualImg,idClient))
                mysql.connection.commit()

            except Exception as e:
                print(e)
                return  redirect(url_for('createCard'))

            finally:
                if cur:
                    cur.close()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('editCard'))

#Verified endpoint
@app.route('/deleteClient/<idClient>')
def deleteClient(idClient):
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            try:
                cur = mysql.connection.cursor()    
                cur.execute('SELECT imgLogo FROM cliente WHERE id = %s', (idClient,))
                clientData = cur.fetchone()

                file_Img = 'static/' + clientData[0]
                if os.path.exists(file_Img):                        
                    os.remove(file_Img)

                cur = mysql.connection.cursor()    
                cur.execute('DELETE FROM cliente WHERE id = %s', (idClient, ))
                mysql.connection.commit()
                
            except Exception as e:
                print(e)
                return  redirect(url_for('createCard'))

            finally:
                if cur:
                    cur.close()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('editCard'))

#Verified endpoint
@app.route('/editProfile', methods=['POST'])
def editProfile():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            id  = userInfo[0]            
                
            #Campos extra
            nombre = request.form['name']
            apellidoPat = request.form['lastNameFather']
            apellidoMat = request.form['lastNameMother']
            correo = request.form['email']
            telefono = request.form['telephone']
            titulo = request.form['titulo']
            cargo = request.form['cargo']

            cur = mysql.connection.cursor()    
            cur.execute('UPDATE tarjeta SET nombre = %s, apellidoPat = %s, apellidoMat = %s, correo = %s, telefono = %s, titulo = %s, cargo = %s WHERE usuario = %s', (nombre,apellidoPat,apellidoMat,correo,telefono, titulo ,cargo,id))
            mysql.connection.commit()

            #Redes sociales
            #clean table
            cur = mysql.connection.cursor()    
            cur.execute('SELECT id FROM tarjeta WHERE usuario = %s', (id,))
            cardData = cur.fetchone()
            
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM redSocial where tarjeta = %s', (cardData[0],) )
            mysql.connection.commit()

            facebook = request.form['facebook']
            if facebook != '':
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'facebook', facebook) )
                mysql.connection.commit()

            instagram = request.form['instagram']
            if instagram != '':
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'instagram', instagram) )
                mysql.connection.commit()

            twitter = request.form['twitter']
            if twitter != '':
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'twitter', twitter) )
                mysql.connection.commit()

            linkedin = request.form['linkedin']
            if linkedin != '':
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO redSocial VALUES (%s, %s, %s)', (cardData[0], 'linkedin', linkedin) )
                mysql.connection.commit()

            #profile pictures
            profilePictureMain = request.files['profilePictureMain']     
            profilePictureMainId = request.form['profilePictureMainId'] 
            if profilePictureMain:      
                file_Img = 'static/' + profilePictureMainId
                if os.path.exists(file_Img):                        
                    os.remove(file_Img)

                file_extension = profilePictureMain.filename.rsplit('.', 1)[1].lower()
                filename_profilePictureMain = generate_filename(id,'profilePictureMain' ,file_extension)
                filename_profilePictureMain = 'data/profilePictureMain/' + filename_profilePictureMain
                profilePictureMain.save(f'static/{filename_profilePictureMain}')

                cur = mysql.connection.cursor()
                cur.execute('UPDATE imgPerfil SET rutaPerfil = %s WHERE tarjeta = %s AND rutaPerfil = %s', (filename_profilePictureMain, cardData[0], profilePictureMainId) )
                mysql.connection.commit()

            profilePictureSecond = request.files['profilePictureSecond']      
            profilePictureSecondId = request.form['profilePictureSecondId']          
            if profilePictureSecond:
                if profilePictureSecondId != '':
                    file_Img = 'static/' + profilePictureSecondId
                    if os.path.exists(file_Img):                        
                        os.remove(file_Img)
                
                    file_extension = profilePictureSecond.filename.rsplit('.', 1)[1].lower()
                    filename_profilePictureSecond = generate_filename(id,'profilePictureSecond' ,file_extension)
                    filename_profilePictureSecond = 'data/profilePictureSecond/' + filename_profilePictureSecond
                    profilePictureSecond.save(f'static/{filename_profilePictureSecond}')

                    cur = mysql.connection.cursor()
                    cur.execute('UPDATE imgPerfil SET rutaPerfil = %s WHERE tarjeta = %s AND rutaPerfil = %s', (filename_profilePictureSecond, cardData[0], profilePictureSecondId) )
                    mysql.connection.commit()
                else:
                    file_extension = profilePictureSecond.filename.rsplit('.', 1)[1].lower()
                    filename_profilePictureSecond = generate_filename(id,'profilePictureSecond' ,file_extension)
                    filename_profilePictureSecond = 'data/profilePictureSecond/' + filename_profilePictureSecond
                    profilePictureSecond.save(f'static/{filename_profilePictureSecond}')

                    cur = mysql.connection.cursor()
                    cur.execute('INSERT INTO imgPerfil VALUES (%s, %s)', (cardData[0], filename_profilePictureSecond) )
                    mysql.connection.commit()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('editCard'))

#Verified endpoint
@app.route('/editUbication', methods=['POST'])
def editUbication():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            id  = userInfo[0]

            ubicacion = request.form['ubication']
            lat = request.form['latitude']
            lng = request.form['longitude']

            cur = mysql.connection.cursor()    
            cur.execute('UPDATE tarjeta SET ubicacion = %s, lat = %s, lng = %s WHERE usuario = %s', (ubicacion, lat, lng, id))
            mysql.connection.commit()
        
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('editCard'))

#Verified endpoint
@app.route('/editAboutme', methods=['POST'])
def editAboutme():
    userInfo = getUserCookie()
    if userInfo:
        if userInfo[2] == 'True':
            id  = userInfo[0]
            sobreMi = request.form['message']

            cur = mysql.connection.cursor()    
            cur.execute('UPDATE tarjeta SET sobreMi = %s WHERE usuario = %s', (sobreMi, id))
            mysql.connection.commit()
        else:
            return redirect(url_for('home'))
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('editCard'))

#Methods post - admin

#Verified endpoint
@app.route('/admin/login', methods=['POST'])
def loginPostAdmin():
    try:
        idWorker = request.form['idWorker']
        password = request.form['password']
        hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE id = %s', (idWorker,))
        user_data = cur.fetchone()

        cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (idWorker,))
        card_data = cur.fetchone()

        haveCard = False
        if card_data:
            haveCard = True

        if user_data:
            if user_data[2] == hashedPassword and user_data[3] == True:                
                resp = make_response(redirect(url_for('homeAdmin')))
                resp.set_cookie('user', f'{user_data[0]}:{user_data[1]}:{haveCard}:{user_data[3]}', max_age=7200)
                return resp
            else:
                return redirect(url_for('loginAdmin'))
        else:            
            return redirect(url_for('loginAdmin'))

    except Exception as e:
        print(e)
        return  redirect(url_for('loginAdmin'))

    finally:
        cur.close()

#Verified endpoint
@app.route('/addAdmin', methods=['POST'])
def addAdminPost():
    userInfo = getUserCookie()
    if userInfo and userInfo[3] == '1':
        cur = None
        try:
            idWorker = request.form['idWorker']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuario WHERE id = %s', (idWorker,))
            cardData = cur.fetchone()

            if cardData:                
                cur = mysql.connection.cursor()
                cur.execute('UPDATE usuario SET admin = 1 WHERE id = %s', (idWorker,) )
                mysql.connection.commit()

                cur.execute('INSERT INTO movimientos(usuario, accion) VALUES (%s, %s)', (userInfo[0] + "_" + userInfo[1], 'Add admin - ' + idWorker))
                mysql.connection.commit()

        except Exception as e:
            print(e)
            return  redirect(url_for('createCard'))

        finally:
            if cur:
                cur.close()
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('homeAdmin'))

#Verified endpoint
@app.route('/deleteAdmin', methods=['POST'])
def deleteAdminPost():
    userInfo = getUserCookie()
    if userInfo and userInfo[3] == '1':
        cur = None
        try:
            idWorker = request.form['idWorker']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuario WHERE id = %s', (idWorker,))
            cardData = cur.fetchone()

            if cardData:                
                cur = mysql.connection.cursor()
                cur.execute('UPDATE usuario SET admin = 0 WHERE id = %s', (idWorker,) )
                mysql.connection.commit()

                cur.execute('INSERT INTO movimientos(usuario, accion) VALUES (%s, %s)', (userInfo[0] + "_" + userInfo[1], 'Delete admin - ' + idWorker))
                mysql.connection.commit()

        except Exception as e:
            print(e)
            return  redirect(url_for('createCard'))

        finally:
            if cur:
                cur.close()
    else:        
        return redirect(url_for('login'))

    return  redirect(url_for('homeAdmin'))

#Verified endpoint
@app.route('/deleteCard/<id>')
def deleteCard(id):
    userInfo = getUserCookie()
    if userInfo and userInfo[3] == '1':
        cur = None
        try:                        
            data = None
            cur = mysql.connection.cursor()                

            #card
            cur.execute('SELECT * FROM tarjeta WHERE usuario = %s', (id,))
            data = cur.fetchone()
            idCard = data[0]

            #client
            cur.execute('SELECT imgLogo FROM cliente WHERE tarjeta = %s', (idCard,))
            data = cur.fetchall()

            if data:
                for element in data:                    
                    deleteFile(element[0])                    

            cur.execute('DELETE FROM cliente WHERE tarjeta = %s', (idCard,))
            mysql.connection.commit()

            #img perfil
            cur.execute('SELECT rutaPerfil FROM imgPerfil WHERE tarjeta = %s', (idCard,))
            data = cur.fetchall()

            if data:
                for element in data:                    
                    deleteFile(element[0])  

            cur.execute('DELETE FROM imgPerfil WHERE tarjeta = %s', (idCard,))
            mysql.connection.commit()

            #img portafolio
            cur.execute('SELECT rutaPortafolio FROM imgPortafolio WHERE tarjeta = %s', (idCard,))
            data = cur.fetchall()

            if data:
                for element in data:                    
                    deleteFile(element[0])  

            cur.execute('DELETE FROM imgPortafolio WHERE tarjeta = %s', (idCard,))
            mysql.connection.commit()

            #social
            cur.execute('DELETE FROM redSocial WHERE tarjeta = %s', (idCard,))
            mysql.connection.commit()

            #card            
            cur.execute('DELETE FROM tarjeta WHERE id = %s', (idCard,))
            mysql.connection.commit()

            cur.execute('DELETE FROM recuperacionContrasena WHERE usuario = %s', (id,))
            mysql.connection.commit()

            cur.execute('DELETE FROM usuario WHERE id = %s', (id,))
            mysql.connection.commit()

            cur.execute('INSERT INTO movimientos(usuario, accion) VALUES (%s, %s)', (str(userInfo[0]) + "_" + str(userInfo[1]), 'Delete card - ' + str(idCard)))
            mysql.connection.commit()  

            if userInfo[0] == id:
                resp = make_response(redirect(url_for('login')))
                resp.delete_cookie('user')
                return resp

        except Exception as e:
            print(e)
            return  redirect(url_for('loginAdmin'))

        finally:
            if cur:
                cur.close()
    else:        
        return redirect(url_for('loginAdmin'))

    return  redirect(url_for('homeAdmin'))

if __name__ == '__main__':
    app.run()