const btnToken = document.getElementById('btnToken');

const alertErrorMsg = `
    <div class="flex items-center p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
        <svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <span class="sr-only">Info</span>
        <div>
            <span class="font-medium">Mensaje: </span> El token ingresado no es valido
        </div>
    </div>
`;

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
            console.log('Respuesta del servidor Ok ', data);
        }else{
            console.log('Respuesta del servidor ', data);
            document.getElementById('tokenContainer').innerHTML += alertErrorMsg;
        }
    }catch(err){
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = verifyToken;