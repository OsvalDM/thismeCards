from flask import session

def verifySignToken(mysql, token):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM TOKEN WHERE content = %s', (token,))
        token = cur.fetchone()        

        # todo: manejar resultados
        if token != None:
            session['token'] = token
            return {'result' : 'success'}
        else:
            return {'result' : 'failed'}
    except Exception as e:
        print(e)        
        return {'result' : 'failed'}
    finally:
        cur.close()