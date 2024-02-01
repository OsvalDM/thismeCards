from flask import session

def signup(mysql, data):
    token = session.get('token', None)

    if token:
        cur = mysql.connection.cursor()
        try:
            print(data)
            userName = data['userName'].replace(" ", "_")

            cur.execute('SELECT * FROM USERCARD WHERE email = %s or userName = %s', (data['email'], userName))
            result = cur.fetchone()
            if result:
                return {'result' : 'failed', 'msg' : 'El usuario o email ya existe por favor ingrese otro.'}

            cur.execute('INSERT INTO USERCARD(email, userName, psw) VALUES (%s, %s, %s)', (data['email'], userName, data['psw']) )
            mysql.connection.commit()            

            cur.execute('SELECT id FROM USERCARD WHERE email = %s', (data['email'], ) )
            userId = cur.fetchone()            
                        
            cur.execute('DELETE FROM TOKEN WHERE content = %s', (token[2], ) )
            mysql.connection.commit()
            session.pop('token', None)

            detail = 'User signup using token: ' + token[2]
            cur.execute('INSERT INTO LOGS (user, detail) VALUES (%s, %s)', (userId[0], detail) )
            mysql.connection.commit()

            return {'result' : 'success', 'msg' : 'Usuario registrado correctamente'}
        
        except Exception as e:
            print(e)
            return {'result' : 'failed', 'msg' : 'Error en la base de datos.'}

        finally:            
                cur.close()
        
    else:
        return {'result' : 'failed', 'msg' : 'No eexiste un token de registro.'}
    

def login(mysql, data):
    cur = mysql.connection.cursor()
    try:        
        cur.execute('SELECT * FROM USERCARD WHERE email = %s and psw = %s and state = "ACTIVE" ', (data['email'], data['psw']))
        user = cur.fetchone()        

        # todo: manejar resultados
        if user != None:
            session['user'] = [user[0], user[1], user[2], user[5] ]
            return {'result' : 'success'}
        else:
            return {'result' : 'failed'}
    except Exception as e:
        print(e)        
        return {'result' : 'failed'}
    finally:
        cur.close()
