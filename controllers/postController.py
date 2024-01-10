from flask import render_template

def verifySignToken(mysql, token):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM TOKEN WHERE content = %s', (token,))
        token = cur.fetchone()

        # todo: manejar resultados
        return {'result' : 'success', 'token' : token}
    except Exception as e:
        print(e)        
        return {'result' : 'failed', 'token' : None}
    finally:
        cur.close()