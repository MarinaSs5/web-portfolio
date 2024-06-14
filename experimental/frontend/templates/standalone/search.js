$(document).ready(function() {
    $('.main-search-button').on('click', function() {
        var query = $('.main-search-field').val().trim(); 
        var searchProfiles = $('#prof').is(':checked'); 
        var searchProjects = $('#proj').is(':checked'); 

        if (query.length < 3) {
            alert('Запрос не может быть короче трёх символов.');
            return; 
        }

        if (!searchProfiles && !searchProjects) {
            alert('Критерии поиска должны содержать хотя бы одну категорию.');
            return; 
        }

        var options = 'profiles'; 
        if (searchProfiles && searchProjects) {
            options = 'profiles+projects'; 
        } else if (!searchProfiles && searchProjects) {
            options = 'projects';
        }

        var searchUrl = `/search/${query}/${options}`; 
        window.location.href = searchUrl; 
    });
});
