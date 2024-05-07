function submit(login, name, surname, password, repeat)
{
    login = login.toLowerCase();

    // Разрешить в логине только латинские буквы нижнего регистра, цифры, точку и подчёркивание
    //                       regex (regular expression)      проверяем строку на соответствие
    let login_in_range =          /^[a-z0-9._]*$/                     .test(login);
    // и проверить длину
    let login_lengthy = (login.length >= 5) && (login.length <= 30);
    // Я знаю, что регулярные выражения это боль, я сам их не до конца понимаю, но они будут попадаться часто.
    
    let name_lengthy = name.length >= 1
    let surname_lengthy = surname.length >= 1

    // Разрешить в пароле символы только с пробела (0x20) до тильды (0x7F)
    let password_in_range = /^[\x20-\x7E]*$/.test(password);
    let password_lengthy = (password.length >= 10) && (password.length <= 100);

    // Проверить, что пароль введён правильно дважды
    let password_match = (password == repeat);





    // Вывести ошибки пользователю, если они есть
    if(!login_in_range)
    {
        alert('Логин может содержать только латинские буквы, цифры, точки и подчёркивания.');
        return;
    }
    if(!login_lengthy)
    {
        alert('Длина логина должна быть не меньше 5 и не больше 30 символов.');
        return;
    }
    if(!name_lengthy)
    {
        alert('Имя не может быть пустым.');
        return;
    }
    if(!surname_lengthy)
    {
        alert('Фамилия не может быть пустой.');
        return;
    }
    if(!password_in_range)
    {
        alert('Пароль может содержать только ASCII символы.');
        return;
    }
    if(!password_lengthy)
    {
        alert('Длина пароля должна быть не меньше 10 и не больше 100 символов.');
        return;
    }
    if(!password_match)
    {
        alert('Пароли должны совпадать.');
        return;
    }





    $.post('/sign/up/submit',
    {
        'login': login,
        'password': password,
        'name': name,
        'surname': surname,
    },
    function(response)
    {
        if(response['result'] == 'already')
            alert('Пользователь с таким логином уже есть.');

        else if(response['result'] == 'ok')
            window.location.href = '/me/' + login + '/info';

        else
            alert('Неизвестная ошибка.');
    }, 'json');
     
}
