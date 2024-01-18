from flask import session

def createCardBase(mysql, data):
    cur = mysql.connection.cur()

    try:
        cur.execute('''INSERT INTO CARD (user, name, lastFat, lastMot, imgProfile)
                    VALUES (%s, %s, %s, %s, %s)''', (data['user'],data['name'],data['lastFat'],
                                                     data['lastMot'],data['imgProfile']));
        mysql.connection.commit()
        
        cur.execute('SELECT id FROM tarjeta WHERE usuario = %s', (id,))
        cardData = cur.fetchone()



            profilePictureMain = request.files['profilePictureMain']      
            if profilePictureMain:      
                file_extension = profilePictureMain.filename.rsplit('.', 1)[1].lower()
                filename_profilePictureMain = generate_filename(id,'profilePictureMain' ,file_extension)
                filename_profilePictureMain = 'data/profilePictureMain/' + filename_profilePictureMain
                profilePictureMain.save(f'static/{filename_profilePictureMain}')

                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO imgPerfil VALUES (%s, %s)', (cardData[0], filename_profilePictureMain) )
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
    
    except Exception as e:
        print(e)
        return {'failed' : 'Error en la base de datos'}

    finally:
        cur.close()