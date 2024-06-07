// Спрятать элемент: $('#...').attr('hidden', false);





let languages_preloaded =
[
    {% for language in profile.languages %}
    ['{{language[0]}}', '{{language[1]}}'],
    {% endfor %}
];
let languages_count = 0;
for(let iter = 0; iter < languages_preloaded.length; ++iter)
    add_language_html(languages_preloaded[iter][0], languages_preloaded[iter][1]);





function add_language_html(language, level)
{
    $('.profile-language-list').append
    (`\
    <li id="language_${languages_count}">\
        <span>${language} ${level}</span>\
        <div class="remove-language-button" onclick="remove_language(this.parentElement.id)"></div>\
    </li>\
    `);
    ++languages_count;
}
// В остальных language функциях ничего править не надо
function remove_language_html(index)
{
    $('#language_' + index).remove();
    for(let iter = index + 1; iter < languages_count; ++iter)
        $('#language_' + iter).attr('id', 'language_' + (iter - 1));
    --languages_count;
}
function add_language(language, level)
{
    // if(language.length == 0)
    // {
    //     alert('Язык не может быть пустым.');
    //     return;
    // }
    $.post('/me/{{profile.id}}/info/addlanguage',
    {
        'language': language,
        'level': level
    },
    function(response)
    {
        if(response['result'] == 'ok')
            add_language_html(language, level);
            $(".remove-language-button").show();
    }, 'json');
}
function remove_language(id)
{
    let splitstr = id.split('_');
    let index = parseInt(splitstr[splitstr.length - 1]);
    $.post('/me/{{profile.id}}/info/removelanguage',
    {
        'index': index,
    },
    function(response)
    {
        if(response['result'] == 'ok')
            remove_language_html(index)
    }, 'json');
}



function triggerFileInput() {
    document.getElementById('avatar_input').click(); // Симуляция клика по скрытому input
}

function file_updated() {
    let input = document.getElementById('avatar_input');
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

    update_avatar();
}

function update_avatar() {
    let formData = new FormData(document.getElementById('avatar_form'));

    $.ajax({
        url: '/me/{{profile.id}}/info/newavatar',
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response) {
            $('.profile-photo-large').attr('src', `/me/{{profile.id}}/avatar?${new Date().getTime()}`);
            $('.profile-photo-small').attr('src', `/me/{{profile.id}}/avatar?${new Date().getTime()}`);
        }
    });
}






function update_fields(name, surname, specialty, city, job, mail, vk, tg, about, skill)
{
    $.post('/me/{{profile.id}}/info/update',
    {
        'name': name,
        'surname': surname,
        'specialty': specialty,
        'city': city,
        'job': job,
        'mail': mail,
        'vk': vk,
        'tg': tg,
        'about': about,
        'skill': skill,
    },
    function(response)
    {
        if(response['result'] == 'ok')
            ;
    }, 'json');    
}

function make_editable_elements() {
    $("#edit-profile-name").attr("contenteditable", "true");
    $("#edit-profile-surname").attr("contenteditable", "true");
    $("#edit-profile-specialty").attr("contenteditable", "true");
    $("#edit-profile-city").attr("contenteditable", "true");
    $("#edit-profile-job").attr("contenteditable", "true");
    $("#edit-profile-mail").attr("contenteditable", "true");
    $("#edit-profile-tg").attr("contenteditable", "true");
    $("#edit-profile-vk").attr("contenteditable", "true");
    $(".add-language-container").show();
    $(".remove-language-button").show();
    $(".add-avatar-container").show();
    $(".edit-profile-button").hide();
    $(".save-profile-button").show();
}

function save_profile_info() {
    update_fields
    (
        $("#edit-profile-name").text(),
        $("#edit-profile-surname").text(),
        $("#edit-profile-specialty").text(),
        $("#edit-profile-city").text(),
        $("#edit-profile-job").text(),
        $("#edit-profile-mail").text(),
        $("#edit-profile-vk").text(),
        $("#edit-profile-tg").text(),
        $("#about-input").val(),                                   // !!!
        $("#skills-input").val()                                    // !!!
    );

    $("#edit-profile-name").attr("contenteditable", "false");
    $("#edit-profile-name").addClass("not-editable");

    $("#edit-profile-surname").attr("contenteditable", "false");
    $("#edit-profile-surname").addClass("not-editable");

    $("#edit-profile-specialty").attr("contenteditable", "false");
    $("#edit-profile-specialty").addClass("not-editable");

    $("#edit-profile-city").attr("contenteditable", "false");
    $("#edit-profile-cityy").addClass("not-editable");

    $("#edit-profile-job").attr("contenteditable", "false");
    $("#edit-profile-job").addClass("not-editable");

    $("#edit-profile-mail").attr("contenteditable", "false");
    $("#edit-profile-mail").addClass("not-editable");

    $("#edit-profile-tg").attr("contenteditable", "false");
    $("#edit-profile-tg").addClass("not-editable");

    $("#edit-profile-vk").attr("contenteditable", "false");
    $("#edit-profile-vk").addClass("not-editable");

    $(".remove-language-button").hide();

    $(".add-avatar-container").hide();
    $(".add-language-container").hide();
    $(".edit-profile-button").show();
    $(".save-profile-button").hide();
    
    $("#save-about-button").hide();
    $("#save-skills-button").hide();

}

$(document).ready(function() {
    $('#languageSelect').select2({
        placeholder: "Выберите язык",
        language: {
            "noResults": function () {
                return "Ничего не найдено";
            }
        }
    });
    $('#languageSelect').val(null).trigger('change');
});

$(document).ready(function() {
    $('#languageLevel').select2({
        placeholder: "Уровень",
        language: {
            "noResults": function () {
                return "Ничего не найдено";
            }
        }
    });
    $('#languageSelect').val(null).trigger('change');
});

$(document).ready(function() {
    $('#languageLevel').select2({
        placeholder: "Уровень языка",
        minimumResultsForSearch: Infinity
    });
});

let textareaAbout = document.getElementById('about-input');
let saveButtonAbout = document.getElementById('save-about-button');
let originalContentAbout = textareaAbout.value;

textareaAbout.addEventListener('input', function () {
    if (textareaAbout.value !== originalContentAbout) {
        saveButtonAbout.style.display = 'block'; 
    } else {
        saveButtonAbout.style.display = 'none'; 
    }
});

let textareaSkills = document.getElementById('skills-input');
let saveButtonSkills = document.getElementById('save-skills-button');
let originalContentSkills = textareaSkills.value;

textareaSkills.addEventListener('input', function () {
    if (textareaSkills.value !== originalContentSkills) {
        saveButtonSkills.style.display = 'block'; 
    } else {
        saveButtonSkills.style.display = 'none'; 
    }
});


function autoResizeTextarea() {
    var textarea = $(this);
    textarea.height(0);
    var scrollHeight = textarea.prop('scrollHeight');
    textarea.height(scrollHeight);
}

$('textarea').each(function () {
    autoResizeTextarea.call(this);
}).on('input', autoResizeTextarea);

