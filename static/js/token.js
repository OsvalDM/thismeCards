import utils from "./utils.js";
const btnToken = document.getElementById('btnToken');

const verifyToken = async ()=> {
    const value = document.getElementById('token').value;
    const url = '/token';

    const body = {
        token: value
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        if (!response.ok){
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const data = await response.json();        
        

        if (data.result == 'success'){            
            utils.removeElement('tokenContainer');
            utils.enableSignUp('mainContainer');
        }else{            
            utils.removeElement('noti')
            utils.makeAlert('Introduce un token valido.', 'tokenContainer')
        }
    }catch(err){
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = verifyToken;