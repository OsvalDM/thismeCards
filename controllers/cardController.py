import re

def createCardBase(mysql, data, socials):
    cur = mysql.connection.cursor()

    try:

        cur.execute('''INSERT INTO CARD(user, name, lastFat, lastMot, imgProfile, charge, email, cellphone, tittle) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (data['user'], data['name'], data['lastFat'], data['lastMot'], data['file'], data['charge'], data['email'], data['cellphone'], data['tittle']) )
        mysql.connection.commit()
        
        cur.execute('SELECT id FROM CARD WHERE user = %s', (data['user'],))
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
        
        cur.execute('INSERT INTO STYLE(user) VALUES (%s)', (data['user'], ))
        mysql.connection.commit()

        cur.execute('INSERT INTO LOGS(user, detail) VALUES (%s, %s)', (data['user'], 'Create card - ' + str(cardData[0]) ) )            
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
        pattern = re.compile(r'watch\?v=([^\&]+)')

        match = pattern.search(data['url'])

        if match:
            url = match.group(1)
            print("ID del video:", url)
        else:
            print("No se encontró ningún ID de video en la URL.")
            return False

        cur.execute('INSERT INTO COMPONENT (user, category) VALUES (%s, %s)',
                    (data['user'], 'ABOUTME'))
        mysql.connection.commit()    
    
        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'ABOUTME'))
        idRow = cur.fetchone()[0]        

        cur.execute('INSERT INTO ABOUTME VALUES(%s, %s, %s, %s)', 
                    (idRow, data['user'], data['content'], url))
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
        
        cur.execute('INSERT INTO COSTUMER_DATA(costumer, name, img, description) VALUES(%s, %s, %s, %s)', 
                    (idRow, data['name'], data['img'], data['desc']))
        mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def addClientItem(mysql, data):
    cur = mysql.connection.cursor()

    try:                
        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'COSTUMER'))
        idRow = cur.fetchone()[0]
        
        cur.execute('INSERT INTO COSTUMER_DATA(costumer, name, img, description) VALUES(%s, %s,%s, %s)', 
                    (idRow, data['name'], data['img'], data['desc']))
        mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def addBriefcase(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('INSERT INTO COMPONENT (user, category) VALUES (%s, %s)',
                    (data['user'], 'BRIEFCASE'))
        mysql.connection.commit()    

        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'BRIEFCASE'))
        idRow = cur.fetchone()[0]

        cur.execute('INSERT INTO BRIEFCASE VALUES(%s, %s)', 
                    (idRow, data['user']))
        mysql.connection.commit()
        
        for url in data['content']:
            cur.execute('INSERT INTO BRIEFCASE_IMAGE(briefcase, urlImg) VALUES(%s, %s)', 
                        (idRow, url))
            mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

#-----------------------------------------------------------------------------------------
#Edit functions

def editAboutmeF(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        pattern = re.compile(r'watch\?v=([^\&]+)')

        match = pattern.search(data['url'])

        if match:
            url = match.group(1)
            print("ID del video:", url)
        else:
            print("No se encontró ningún ID de video en la URL.")
            return False  

        cur.execute('UPDATE ABOUTME SET content = %s, url = %s WHERE user = %s', 
                    (data['content'], url, data['id']))
        mysql.connection.commit()
        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()


def verifySocial(mysql, name, user):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('SELECT * FROM SOCIAL WHERE name = %s and user = %s', (name, user))
        result = cur.fetchone()
        if result: return True
        else: return False
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def editStyleFun(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('UPDATE STYLE SET template = %s WHERE user = %s', (data['template'], data['user']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def editCardF(mysql, data, socials):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''UPDATE CARD SET name = %s , lastFat = %s, lastMot = %s, imgProfile = %s, charge = %s, email = %s, cellphone = %s, tittle = %s WHERE user = %s''', 
                    (data['name'], data['lastFat'], data['lastMot'], data['file'], data['charge'], data['email'], data['cellphone'], data['tittle'], data['user']) )
        mysql.connection.commit()

        #Redes sociales        
        if socials['facebook'] != '':                            
            if verifySocial(mysql,'facebook', data['user']):
                cur.execute('UPDATE SOCIAL SET link = %s WHERE name = %s and user = %s', (socials['facebook'], 'facebook', data['user']) )                
            else:
                cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (data['user'], 'facebook', socials['facebook']) )
            
            mysql.connection.commit()
        
        if socials['instagram'] != '':                
            if verifySocial(mysql, 'instagram', data['user']):
                cur.execute('UPDATE SOCIAL SET link = %s WHERE name = %s and user = %s', (socials['instagram'], 'instagram', data['user']) )
            else:
                cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (data['user'], 'instagram', socials['instagram']) )
            mysql.connection.commit()
        
        if socials['twitter'] != '':    
            if verifySocial(mysql,'twitter', data['user']):            
                cur.execute('UPDATE SOCIAL SET link = %s WHERE name = %s and user = %s', (socials['twitter'], 'twitter', data['user']) )
            else:
                cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (data['user'], 'twitter', socials['twitter']) )
            mysql.connection.commit()
        
        if socials['linkedin'] != '':                
            if verifySocial(mysql, 'linkedin', data['user']):
                cur.execute('UPDATE SOCIAL SET link = %s WHERE name = %s and user = %s', (socials['linkedin'], 'linkedin', data['user']) )
            else:
                cur.execute('INSERT INTO SOCIAL(user, name, link) VALUES (%s, %s, %s)', (data['user'], 'linkedin', socials['linkedin']) )
            mysql.connection.commit()        

        return True
    
    except Exception as e:
        print(e)
        return False

    finally:
        cur.close()        


def editUbicationF(mysql, data):
    cur = mysql.connection.cursor()

    try:        
        cur.execute('UPDATE UBICATION SET lat = %s, lon = %s, address = %s WHERE user = %s', 
                    (data['lat'], data['lon'], data['address'],data['user']))
        mysql.connection.commit()
        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def editBriefcaseF(mysql, data):
    cur = mysql.connection.cursor()

    try:                
        cur.execute('SELECT id FROM COMPONENT WHERE user = %s and category = %s', (data['user'], 'BRIEFCASE'))
        idRow = cur.fetchone()[0]        
        
        print(data)
        for i in range(len(data['previous'])):
            cur.execute('UPDATE BRIEFCASE_IMAGE SET urlImg = %s WHERE urlImg = %s', 
                        (data['content'][i], data['previous'][i]))
            mysql.connection.commit()

        for url in data['new']:
            cur.execute('INSERT INTO BRIEFCASE_IMAGE(briefcase, urlImg) VALUES(%s, %s)', 
                        (idRow, url))
            mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def editClientF(mysql, data):
    cur = mysql.connection.cursor()

    try:            
        cur.execute('UPDATE COSTUMER_DATA SET name = %s, img = %s, description = %s WHERE id = %s', 
                    (data['name'], data['img'], data['desc'], data['id']))
        mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()

def deleteClientF(mysql, id):
    cur = mysql.connection.cursor()

    try:            
        cur.execute('DELETE FROM COSTUMER_DATA WHERE id = %s', 
                    (id, ))
        mysql.connection.commit()

        return True
    
    except Exception as e:
        print(e)
        return False
    
    finally:
        cur.close()