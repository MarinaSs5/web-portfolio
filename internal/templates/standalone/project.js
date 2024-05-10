document.querySelector('.edit-project-button').addEventListener('click', function() {
    document.querySelector('.edit-project-button').style.display = 'none';
    document.querySelector('.save-project-button').style.display = 'block';
    document.querySelector('.add-project-cover-button').style.display = 'block';
    document.querySelector('.attach-file-button').style.display = 'block';

    document.querySelector('.project-title').setAttribute('contenteditable', 'true');
    document.querySelector('.project-type').setAttribute('contenteditable', 'true');
    document.querySelector('.project-description').setAttribute('contenteditable', 'true');
    document.querySelector('.project-original-lang').setAttribute('contenteditable', 'true');
    document.querySelector('.project-translation-lang').setAttribute('contenteditable', 'true');
});

document.querySelector('.save-project-button').addEventListener('click', function() {
    update_fields
    (
        document.querySelector('.project-title').textContent,
        document.querySelector('.project-type').textContent,
        document.querySelector('.project-original-lang').textContent,
        document.querySelector('.project-translation-lang').textContent,
        document.querySelector('.project-description').textContent,                               
    );


    document.querySelector('.edit-project-button').style.display = 'block';
    document.querySelector('.save-project-button').style.display = 'none';
    document.querySelector('.add-project-cover-button').style.display = 'none';
    document.querySelector('.attach-file-button').style.display = 'none';

    document.querySelector('.project-title').setAttribute('contenteditable', 'false');
    document.querySelector('.project-type').setAttribute('contenteditable', 'false');
    document.querySelector('.project-description').setAttribute('contenteditable', 'false');
    document.querySelector('.project-original-lang').setAttribute('contenteditable', 'false');
    document.querySelector('.project-translation-lang').setAttribute('contenteditable', 'false');
});

function update_fields(name, type, original, translation, description)
{
    $.post('/project/{{project_id}}/update',
    {
        'name': name,
        'type': type,
        'original': original,
        'translation': translation,
        'description': description,
    },
    function(response)
    {
        if(response['result'] == 'ok')
            ;
    }, 'json');    
}




function triggerFileInput() {
    document.getElementById('cover_input').click(); // Симуляция клика по скрытому input
}

function file_updated() {
    let input = document.getElementById('cover_input');
    let file = input.files[0];
    if (!file) return;

    if (file.type !== 'image/jpeg') {
        alert('Файл должен быть изображением с расширением JPEG.');
        return;
    }
    if (file.size > 1024 * 1024 * 2) { 
        alert('Размер файла не должен превышать 2 МБ.');
        return;
    }

    update_cover();
}

function update_cover() {
    let formData = new FormData(document.getElementById('cover_form'));

    $.ajax({
        url: '/project/{{project_id}}/newthumbnail',
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response) {
            location.reload();
        }
    });
}


