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
            document.getElementById('btnSignup').onclick = validatePasswords
        }else{            
            utils.removeElement('noti')
            utils.makeAlert('Introduce un token valido.', 'tokenContainer')
        }
    }catch(err){
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = verifyToken;

const verifySignup = async (psw)=> {
    const userName = document.getElementById('name').value
    const email = document.getElementById('email').value


    const body = {
        userName : userName,
        email : email,
        psw : psw
    }

    try {                        
        const response = await fetch('/signup', {
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
            window.location.href = '/login';
        }else{            
            utils.removeElement('noti')
            utils.makeAlert(data.msg, 'signupContainer')
        }
    }catch(err){
        console.log('Error en la solicitud: ', err.message);
    }
};

const validatePasswords = () => {
    var password = document.getElementById("password").value;
    var passwordVerify = document.getElementById("passwordVerify").value;

    if (password === passwordVerify && password != '') {
        verifySignup(password);
    } else {
        alert("Las contraseñas no coinciden, por favor verifícalas.");
    }
}