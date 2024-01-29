const btnToken = document.getElementById('btnLogout');

const logout = async ()=> {    

    const url = '/logout';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },            
        });

        if (!response.ok){
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const data = await response.json();
        window.location.href = '';
    }catch(err){
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = logout;