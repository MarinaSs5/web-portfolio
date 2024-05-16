function add_project() {
    const projectName = prompt("Введите название нового проекта:");
    if (!projectName) return;  // Если название не введено, прекратить выполнение

    fetch(`/me/{{ profile_id }}/projects/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `name=${encodeURIComponent(projectName)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.result !== 'invalid') {
            const projectsList = document.querySelector('.projects-list'); 
            const newProject = document.createElement('div');
            newProject.id = `project-item-${data.result}`; // Важно добавить ID здесь
            newProject.className = 'projects-item';
            newProject.innerHTML = `
                <a class="project-link" href="/project/${data.result}">
                    <img class="project-img" onerror="this.src='/static/project-default.png'" src="/project/${data.result}/thumbnail">
                    <p class="project-title">${projectName}</p>
                </a>
                <div class="delete-button" onclick="remove_project(event, '${data.result}'); return false;">&#10006;</div>`;
            projectsList.appendChild(newProject);
        } else {
            alert('Ошибка при добавлении проекта');
        }
    })
    .catch(error => alert('Ошибка: ' + error));
}


// function add_project(name)
// {
//     $.post('/me/{{profile_id}}/projects/add',
//     {
//         'name': name,
//     },
//     function(response)
//     {
//     }, 'json');    
// }

function remove_project(event, id) {
    event.preventDefault();  // Предотвратить действие по умолчанию (переход по ссылке)
    event.stopPropagation(); // Остановить всплытие события
    $.post('/me/{{profile_id}}/projects/remove', {
        'id': id,
    }, function(response) {
        if (response.result === 'ok') {
            // Удаление элемента проекта из DOM
            document.getElementById('project-item-' + id).remove();
        } else {
            alert('Не удалось удалить проект. Попробуйте еще раз.');
        }
    }, 'json').fail(function() {
        alert("Ошибка выполнения запроса.");
    });
}

