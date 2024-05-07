function autoResizeTextarea() {
    var textarea = $(this);
    textarea.height(0);
    var scrollHeight = textarea.prop('scrollHeight');
    textarea.height(scrollHeight);
}

$('#about-input').on('input', autoResizeTextarea);
$('#skills-input').on('input', autoResizeTextarea);

