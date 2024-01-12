import utils from "./utils.js";
const btnToken = document.getElementById('btnToken');

const verifyToken = async ()=> {
    const email = document.getElementById('email').value;
    const psw = document.getElementById('password').value;

    const url = '/login';

    const body = {
        email: email,
        psw: psw
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
            window.location.href = 'dashboard';
        }else{            
            utils.removeElement('noti')
            utils.makeAlert('Email o contraseña incorrecto.', 'loginContainer')
        }
    }catch(err){
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = verifyToken;