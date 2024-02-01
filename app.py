from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
from flask_mysqldb import MySQL
import hashlib

from controllers.tokenController import *
from controllers.loginController import signup as signupCtrl, login as loginCtrl
from controllers.userController import *
from controllers.cardController import *
from utils.utils import *

app = Flask(__name__)

#Configuración de la base de datos
app.config['MYSQL_HOST'] = '198.12.240.41'
app.config['MYSQL_USER'] = 'adminRE'
app.config['MYSQL_PASSWORD'] = 'R0str03mP%'
app.config['MYSQL_DB'] = 'rostroempresarial'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'esta es la mejor clave secreta del universo'

mysql = MySQL(app)

#Methods get
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup')
def signup():        
    return render_template('signup.html')
        
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/dashboard')
def dashboard():
    user = verifySignIn()
    if user:
        urlQr = generateQr( 'https://rostroempresarial.com/mycard/' + user[2] )
        data = getUserData(mysql, user[2])
        return render_template('dashboard.html', content = data, urlQr = urlQr[0], user = user)
    else:
        return redirect(url_for('login'))

@app.route('/mycard/<id>')
def mycard(id):            
    data = getUserData(mysql, id)
    return render_template('mycard.html', content = data)

@app.route('/createCard')
def createCard():
    user = verifySignIn()
    if user:        
            return render_template('createCard.html', user = user)
    else:
        return redirect(url_for('login'))

@app.route('/editCard')
def editCard():
    user = verifySignIn()
    if user:        
            urlQr = generateQr( 'https://rostroempresarial.com/mycard/' + user[2] )
            data = getUserData(mysql, user[2], True)
            return render_template('editCard.html', user = user, content = data, urlQr = urlQr[0])
    else:
        return redirect(url_for('login'))

@app.route('/component')
def component():
    user = verifySignIn()
    if user:        
        urlQr = generateQr( 'https://rostroempresarial.com/mycard/' + user[2] )
        data = getUserData(mysql, user[2])
        return render_template('components.html', user = user, data = data, urlQr = urlQr[0])
    else:
        return redirect(url_for('login'))

#Methods post

@app.route('/token', methods=['POST'])
def postToken():
    data = request.get_json()    
    token = data['token']
    result = verifySignToken(mysql, token)
    return jsonify(result)

@app.route('/signup', methods=['POST'])
def signupPost():
    data = request.get_json()    
    result = signupCtrl(mysql, data)

    return jsonify(result)  

@app.route('/login', methods=['POST'])
def postLogin():
    data = request.get_json()        
    result = loginCtrl(mysql, data)
    return jsonify(result)

@app.route('/logout', methods=['POST'])
def postLogout():
    result = logoutAux()
    return jsonify(result)

@app.route('/createCard', methods=['POST'])
def createCardPost():
    user = verifySignIn()
    if user:        
        cur = mysql.connection.cursor()
        try:
            id  = user[0]                                                

            #profile picture
            profilePictureMain = request.files['profilePictureMain']      
            if profilePictureMain:
                file_extension = profilePictureMain.filename.rsplit('.', 1)[1].lower()
                filename_profilePictureMain = generate_filename(id,'profilePictureMain' ,file_extension)
                filename_profilePictureMain = 'data/profilePictureMain/' + filename_profilePictureMain
                profilePictureMain.save(f'static/{filename_profilePictureMain}')                
            
            data = {
                'name' : request.form['name'],
                'lastFat' : request.form['lastNameFather'],
                'lastMot' : request.form['lastNameMother'],
                'email' : request.form['email'],
                'cellphone' : request.form['telephone'],
                'tittle' : request.form['titulo'],
                'charge' : request.form['cargo'],
                'user' : id,
                'file' : filename_profilePictureMain
            }

            socials = {
                'facebook' : request.form['facebook'],
                'instagram' : request.form['instagram'],
                'twitter' : request.form['twitter'],
                'linkedin' : request.form['linkedin']
            }

            createCardBase(mysql, data, socials)
            return  redirect(url_for('dashboard'))

        except Exception as e:
            print(e)
            return  redirect(url_for('createCard'))

        finally:            
            cur.close()
    else:        
        return redirect(url_for('login'))    
    
@app.route('/aboutme', methods=['POST'])
def aboutmePost():
    user = verifySignIn()
    if user:        
        data = {        
            'content' : request.form['content'],
            'url' : request.form['url'],
            'user' : user[0]
        }    
        addAboutme(mysql, data)        
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/ubication', methods=['POST'])
def ubicationPost():
    user = verifySignIn()
    if user:        
        data = {                    
            'user' : user[0],
            'lat' : request.form['latitude'],
            'lon' : request.form['longitude'],
            'address' : request.form['ubication']
        }    
        addUbication(mysql, data)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/costumers', methods=['POST'])
def costumersPost():
    user = verifySignIn()
    if user:                        
        id  = user[0]
        urlCostumer = saveFile(request.files['logo'], 'imgLogo', id, True)

        data = {
            'user' : user[0],
            'name' : request.form['name'],
            'img' : urlCostumer
        }
        
        addClient(mysql,data)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/briefcase', methods=['POST'])
def briefcasePost():
    user = verifySignIn()
    if user:                        
        id  = user[0]

        urlConten = []
        nameFields = ['content1', 'content2', 'content3', 'content4', 'content5', 'content6']
        
        n = 0
        for name in nameFields:
            content = request.files[name]

            if content:
                urlConten.append( saveFile(content, 'content', id, True, n) )            
            n += 1

        data = {
            'user' : user[0],
            'content' : urlConten            
        }
        
        addBriefcase(mysql,data)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/editAboutme', methods=['POST'])
def editAboutme():
    user = verifySignIn()
    if user:                        
        id  = user[0]
        
        data = {
            'content' : request.form['message'],
            'url' : request.form['url'],
            'id' : id
        }

        editAboutmeF(mysql, data)
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))       

#Verified endpoint
@app.route('/editProfile', methods=['POST'])
def editProfile():
    user = verifySignIn()
    if user:                        
        id  = user[0]     
        profilePictureMain = request.files['profilePictureMain']      
        filename_profilePictureMain = request.form['profilePictureMainId']

        if profilePictureMain:
            deleteFile(filename_profilePictureMain)
            filename_profilePictureMain = saveFile(profilePictureMain, 'profilePictureMain', id)        
        #Campos extra
        data = {
            'name' : request.form['name'],
            'lastFat' : request.form['lastNameFather'],
            'lastMot' : request.form['lastNameMother'],
            'email' : request.form['email'],
            'cellphone' : request.form['telephone'],
            'tittle' : request.form['titulo'],
            'charge' : request.form['cargo'],
            'user' : id,
            'file' : filename_profilePictureMain
        }

        socials = {
            'facebook' : request.form['facebook'],
            'instagram' : request.form['instagram'],
            'twitter' : request.form['twitter'],
            'linkedin' : request.form['linkedin']
        }

        editCardF(mysql, data, socials)
    
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))   

@app.route('/editUbication', methods=['POST'])
def editUbication():
    user = verifySignIn()
    if user:                                
        data = {                    
            'user' : user[0],
            'lat' : request.form['latitude'],
            'lon' : request.form['longitude'],
            'address' : request.form['ubication']
        }    
        editUbicationF(mysql, data)        
    
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))       

@app.route('/editBriefcase', methods=['POST'])
def editBriefcase():
    user = verifySignIn()
    if user:                        
        id  = user[0]                

        urlConten = []
        urlUpdate = []
        previousContent = []
        nameFields = ['content1', 'content2', 'content3', 'content4', 'content5', 'content6']
        
        n = 0
        for name in nameFields:
            content = request.files[name]
            previous = request.form[name + 'id']            
            if previous != '' and content:
                deleteFile(previous)
                previousContent.append( previous)
                urlUpdate.append( saveFile(content, 'content', id, True, n) )
            elif previous == '' and content:
                urlConten.append( saveFile(content, 'content', id, True, n) )
            n += 1

        data = {
            'user' : user[0],
            'content' : urlUpdate,
            'previous' : previousContent,
            'new' : urlConten
        }
        
        editBriefcaseF(mysql,data)
        
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))       

@app.route('/editClient/<id>', methods=['POST'])
def editClient(id):
    user = verifySignIn()
    if user:
        file = request.files['logo']      
        urlCostumer = request.form['logoid']
        
        if file:
            deleteFile(urlCostumer)
            urlCostumer = saveFile(file, 'imgLogo', user[0], True)
        
        data = {
            'id' : id,
            'name' : request.form['name'],
            'img' : urlCostumer
        }
        
        editClientF(mysql,data)
        
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))       


@app.route('/newCostumer', methods=['POST'])
def newCostumer():
    user = verifySignIn()
    if user:                        
        id  = user[0]
        urlCostumer = saveFile(request.files['logo'], 'imgLogo', id, True)

        data = {
            'user' : user[0],
            'name' : request.form['name'],
            'img' : urlCostumer
        }
        
        addClientItem(mysql,data)
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))

@app.route('/deleteClient/<id>')
def deleteCostumer(id):
    user = verifySignIn()
    if user:        
        deleteClientF(mysql, id)
        
        return redirect(url_for('editCard'))
    else:
        return redirect(url_for('login'))       


#Error handler
#Verified endpoint
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

#----------------------------------------------------------------------

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