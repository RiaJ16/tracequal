$(document).ready(function(){
    $('#toggle_panel').click(function(){
        toggle_panel();
    });

    $('#close_button').click(function(){
        toggle_panel();
    });
});

function toggle_panel(){
    $('.panel').toggleClass('open');
    let chevron = $('#chevron');
    chevron.toggleClass('fa-chevron-left');
    chevron.toggleClass('fa-chevron-right');
}

function open_panel(){
    $('.panel').addClass('open');
    let chevron = $('#chevron');
    chevron.removeClass('fa-chevron-left');
    chevron.addClass('fa-chevron-right');
}
