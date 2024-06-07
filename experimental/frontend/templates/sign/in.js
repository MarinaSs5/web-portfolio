function submit(login, password)
{
    login = login.toLowerCase();

    $.post('/sign/in/submit',
    {
        'login': login,
        'password': password
    },
    function(response)
    {
        if(response['result'] == 'invalid')
            alert('Неправильное имя пользователя или пароль.');

        else if(response['result'] == 'ok')
            window.location.href = '/me/' + login + '/info'

        else
            alert('Неизвестная ошибка.');
    }, 'json');
}

function showPassword()
{
    let passwordInput = document.getElementById('password');
    let eyeIcon = document.querySelector('.eye-password');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.add('password-shown');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('password-shown');
    }
}