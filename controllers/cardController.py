def createCardBase(mysql, data, socials):
    cur = mysql.connection.cursor()

    try:

        cur.execute('''INSERT INTO CARD(user, name, lastFat, lastMot, imgProfile, charge, email, cellphone, tittle) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (data['user'], data['name'], data['lastFat'], data['lastMot'], data['file'], data['charge'], data['email'], data['cellphone'], data['tittle']) )
        mysql.connection.commit()
        
        cur.execute('SELECT id FROM CARD WHERE user = %s', (id,))
        cardData = cur.fetchone()

        #Redes sociales        
        if socials['facebook'] != '':                
            cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (cardData[0], 'facebook', socials['facebook']) )
            mysql.connection.commit()
        
        if socials['instagram'] != '':                
            cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (cardData[0], 'instagram', socials['instagram']) )
            mysql.connection.commit()
        
        if socials['twitter'] != '':                
            cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (cardData[0], 'twitter', socials['twitter']) )
            mysql.connection.commit()
        
        if socials['linkedin'] != '':                
            cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (cardData[0], 'linkedin', socials['linkedin']) )
            mysql.connection.commit()
        
        cur.execute('INSERT INTO LOGS(user, detail) VALUES (%s, %s)', (id, 'Create card - ' + str(cardData[0]) ) )            
        mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False

    finally:
        cur.close()

def addAboutme(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('INSERT INTO COMPONENT (user, category) VALUES (%s, %s)',
                    (data['user'], 'ABOUTME'))
        mysql.connection.commit()    
    
        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'ABOUTME'))
        idRow = cur.fetchone()[0]
    
        cur.execute('INSERT INTO ABOUTME VALUES(%s, %s, %s)', 
                    (idRow, data['user'], data['content']))
        mysql.connection.commit()
        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def addUbication(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('INSERT INTO COMPONENT (user, category) VALUES (%s, %s)',
                    (data['user'], 'UBICATION'))
        mysql.connection.commit()    

        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'UBICATION'))
        idRow = cur.fetchone()[0]

        cur.execute('INSERT INTO UBICATION VALUES(%s, %s, %s, %s, %s, "")', 
                    (idRow, data['user'], data['lat'], data['lon'], data['address']))
        mysql.connection.commit()
        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def addClient(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('INSERT INTO COMPONENT (user, category) VALUES (%s, %s)',
                    (data['user'], 'COSTUMER'))
        mysql.connection.commit()    

        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'COSTUMER'))
        idRow = cur.fetchone()[0]

        cur.execute('INSERT INTO COSTUMER VALUES(%s, %s)', 
                    (idRow, data['user']))
        mysql.connection.commit()
        
        cur.execute('INSERT INTO COSTUMER_DATA(costumer, name, img) VALUES(%s, %s, %s)', 
                    (idRow, data['name'], data['img']))
        mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()