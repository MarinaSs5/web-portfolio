$(document).ready(function () {

    $('#languageSelectOriginal, #languageSelectTranslation').select2({
        language: {
            noResults: function () {
                return "Ничего не найдено";
            }
        }
    });

    $('#languageSelectOriginal, #languageSelectTranslation').next('.select2-container').hide();

    $('.edit-project-button').click(function () {
        $('.edit-project-button').hide();
        $('.save-project-button, .add-project-cover-button, .attach-file-button').show();
        $('.project-title, .project-type, .project-description').attr('contenteditable', 'true');


        $('#languageSelectOriginal').val($('.original-lang').text()).trigger('change').next('.select2-container').css('display', 'block');
        $('#languageSelectTranslation').val($('.translation-lang').text()).trigger('change').next('.select2-container').css('display', 'block');

        $('.original-lang, .translation-lang').hide();
    });

    $('.save-project-button').click(function () {
        update_fields(
            $('.project-title').text(),
            $('.project-type').text(),
            $('#languageSelectOriginal').val(),
            $('#languageSelectTranslation').val(),
            $('.project-description').text()
        );

        $('.edit-project-button').show();
        $(this).hide();
        $('.add-project-cover-button, .attach-file-button').hide();
        $('.project-title, .project-type, .project-description').removeAttr('contenteditable');

        $('#languageSelectOriginal, #languageSelectTranslation').next('.select2-container').css('display', 'none');

        $('.original-lang').text($('#languageSelectOriginal').val()).show();
        $('.translation-lang').text($('#languageSelectTranslation').val()).show();
    });


    function update_fields(name, type, original, translation, description) {
        $.post('/project/{{project_id}}/update', {
            name: name,
            type: type,
            original: original,
            translation: translation,
            description: description,
        }, function (response) {
            if (response.result == 'ok') {

            }
        }, 'json');
    }

    function triggerFileInputCover() {
        $('#cover_input').click();
    }

    function file_updated_cover() {
        let file = $('#cover_input')[0].files[0];
        if (!file) return;

        if (file.type !== 'image/jpeg') {
            alert('Файл должен быть изображением с расширением JPEG.');
            return;
        }
        if (file.size > 2 * 1024 * 1024) { 
            alert('Размер файла не должен превышать 2 МБ.');
            return;
        }

        update_cover();
    }

    function update_cover() {
        let formData = new FormData($('#cover_form')[0]);

        $.ajax({
            url: '/project/{{project_id}}/newthumbnail',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                $('.project-cover-img').attr('src', `/project/{{project_id}}/thumbnail?${new Date().getTime()}`);
            }
        });
    }

    $('#add-project-cover-button').click(triggerFileInputCover);
    $('#cover_input').change(file_updated_cover);



    function triggerFileInputContent() {
        $('#file_input').click(); 
    }

    function file_updated_content() {
        let file = $('#file_input')[0].files[0]; 
        if (!file) return;

        if (file.type !== 'application/pdf') {
            alert('Файл должен быть PDF.');
            return;
        }
        if (file.size > 1024 * 1024 * 5) { 
            alert('Размер файла не должен превышать 5 МБ.');
            return;
        }

        update_file();
    }

    function update_file() {
        let formData = new FormData($('#file_form')[0]); 

        $.ajax({
            url: '/project/{{project_id}}/newcontent',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.result === 'ok') {
                    $('#project_file_link').attr('href', '/project/{{project_id}}/content').show();
                    alert('Файл успешно загружен!');
                } else {
                    alert('Не удалось загрузить файл.');
                }
            },
            error: function () {
                alert('Ошибка при загрузке файла.');
            }
        });
    }

    $('.attach-file-button').click(triggerFileInputContent);
    $('#file_input').change(file_updated_content);




    $('.add-translation-fragment-button').click(function () {
        $('.edit-translation-fragment-button, .save-translation-fragment-button, .remove-translation-fragment-button').show();
        $(this).hide();
        $.post('/project/{{project_id}}/addpreview', {
            original: '',
            translation: ''
        }, function (response) {
            if (response.result === 'ok') {
                $('.translation-fragment').show();
            } else {
                alert('Ошибка при создании фрагмента.');
            }
        });
    });

    $('.edit-translation-fragment-button').click(function () {
        $('.original-text, .translation-text').attr('contenteditable', 'true');
    });

    $('.save-translation-fragment-button').click(function () {
        let originalText = $('.original-text').text();
        let translationText = $('.translation-text').text();
        $.post('/project/{{project_id}}/updatepreview', {
            index: 0,
            original: originalText,
            translation: translationText
        }, function (response) {
            if (response.result === 'ok') {
                alert('Фрагмент успешно обновлен!');
                $('.original-text, .translation-text').attr('contenteditable', 'false');
            } else {
                alert('Ошибка обновления.');
            }
        });
    });

    $('.remove-translation-fragment-button').click(function () {
        if (confirm('Вы уверены, что хотите удалить этот фрагмент?')) {
            $.post('/project/{{project_id}}/removepreview', {
                index: 0
            }, function (response) {
                if (response.result === 'ok') {
                    $('.translation-fragment').hide();
                    $('.edit-translation-fragment-button, .save-translation-fragment-button, .remove-translation-fragment-button').hide();
                    $('.add-translation-fragment-button').show();
                } else {
                    alert('Ошибка удаления.');
                }
            });
        }
    });

});
