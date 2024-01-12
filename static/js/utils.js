const utils = {};

utils.makeAlert = (msg, containerId) => {    
    const alertDiv = document.createElement('div');
    alertDiv.className = 'flex items-center p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 animate__bounceIn';
    alertDiv.role = 'alert';
    alertDiv.id = 'noti'
    alertDiv.innerHTML = `        
            <svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <span class="sr-only">Info</span>
            <div>
                <span class="font-medium">Mensaje: </span> ${msg}
            </div>        
    `;
    
    document.getElementById(containerId).appendChild(alertDiv);
}

utils.enableSignUp = (containerId) => {
    const signupDiv = document.createElement('div');
    signupDiv.className = 'flex justify-center flex-col px-8 py-4 h-fit animate__bounceIn';    
    signupDiv.id = 'signupContainer'
    signupDiv.innerHTML = `
    <!-- create account -->    
        <h3 class="font-bold text-3xl w-full text-center mb-2 text-white">Registrate</h3>        

        <form class="flex justify-center items-center flex-col w-96" action="/signup" method="post" id="signupForm">
            <div class="mb-5">
                <label for="name" class="block mb-2 text-sm font-medium text-white">Nombre de usuario</label>
                <input type="text" id="name" name="name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-96 p-2.5 " required>
            </div>
            <div class="mb-5">
                <label for="email" class="block mb-2 text-sm font-medium text-white">Correo electronico</label>
                <input type="email" id="email" name="email" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-96 p-2.5 " required>
            </div>
            <div class="mb-5">
                <label for="password" class="block mb-2 text-sm font-medium text-white">Contraseña</label>
                <input type="password" id="password" name="password" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block  w-96 p-2.5 " required>
            </div>

            <div class="mb-5">
                <label for="passwordVerify" class="block mb-2 text-sm font-medium text-white">Verifica contraseña</label>
                <input type="password" id="passwordVerify" name="passwordVerify" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block  w-96 p-2.5 " required>
            </div>
            
            <button type="button" onclick="validatePasswords()" class="text-white bg-[#ff4a4a] hover:bg-red-600 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center w-40">Aceptar</button>
        </form>                        
    `;
    document.getElementById(containerId).appendChild(signupDiv);
}

utils.removeElement = (id) => {
    const existingAlert = document.getElementById(id);
    if (existingAlert && existingAlert.parentNode) {
        existingAlert.parentNode.removeChild(existingAlert);
    }
};

export default utils;