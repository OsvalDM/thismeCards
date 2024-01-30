from flask import session

def getUserData(mysql, userName):
    #Data
    content = { 
        'cardData': None,
        'socials' : None,
        'style' : None,
        'aboutme' : None,   
        'briefcase': None,
        'ubication': None,
        'costumers' : None
    }        

    cur = mysql.connection.cursor()

    try:    
        #get basic data            
        cur.execute('''SELECT id FROM USERCARD WHERE userName = %s''', (userName,))
        id = cur.fetchone()[0]

        cur.execute('''SELECT * FROM CARD WHERE user = %s''', (id,))
        cardData = cur.fetchone()

        if cardData:
            content['cardData'] = cardData

            #get social network data
            cur.execute('SELECT * FROM SOCIAL WHERE user = %s', (id,))
            socials = cur.fetchall()
            if socials:
                content['socials'] = socials

            #get personalization
            cur.execute('SELECT * FROM STYLE WHERE user = %s', (id, ))
            style = cur.fetchone()
            if style:
                content['style'] = style

            #get all data
            #get aboutme
            cur.execute('''SELECT * 
                            FROM COMPONENT AS c
                            NATURAL JOIN ABOUTME AS a
                            WHERE c.user = %s''', (id,))
            aboutme = cur.fetchall()
            if aboutme:
                content['aboutme'] = aboutme
            
            #get briefcase
            cur.execute('''SELECT bi.urlImg 
                            FROM COMPONENT AS c
                            NATURAL JOIN BRIEFCASE AS b
                            JOIN BRIEFCASE_IMAGE AS bi ON b.id = bi.briefcase
                            WHERE c.user = %s''', (id,))
            briefcase = cur.fetchall()
            if briefcase:
                content['briefcase'] = briefcase
            
            #get ubication
            cur.execute('''SELECT * 
                            FROM COMPONENT AS c
                            NATURAL JOIN UBICATION AS u                         
                            WHERE c.user = %s''', (id,))
            ubication = cur.fetchall()
            if ubication:
                content['ubication'] = ubication
            
            #get costumers
            cur.execute('''SELECT cod.name, cod.img
                            FROM COMPONENT AS c
                            NATURAL JOIN COSTUMER AS co
                            JOIN COSTUMER_DATA AS cod ON co.id = cod.costumer
                            WHERE c.user = %s''', (id,))
                        
            costumer = cur.fetchall()            
            if costumer:
                content['costumers'] = costumer
            
            print(content)
            return content
        else:
            return None

    except Exception as e:
        print(e)
        return {'failed' : 'Error en la base de datos'}

    finally:
        cur.close()