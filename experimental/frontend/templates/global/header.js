$(document).ready(function(){
    $('.search-field').keypress(function(e){
        if(e.which == 13){ // Проверка нажатия на клавишу Enter, которая имеет код 13
            e.preventDefault(); // Предотвратить стандартное поведение при нажатии на Enter
            var query = $(this).val(); 
            if(query.length >= 3){ 
                window.location.href = '/search/' + query + '/profiles'; // Перенаправление на нужный URL
            } else {
                alert("Пожалуйста, введите минимум 3 символа для поиска."); // Уведомление пользователя, если введено менее 3 символов
            }
        }
    });
});