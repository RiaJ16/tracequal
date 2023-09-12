$(document).ready(function() {
    $('.extra').on('click', function(event) {
        let id = $(this).data('id');
        let to_hide = $('#hidden_block_' + id);
        to_hide.css('display', to_hide.css('display') === 'table' ? 'none' : 'table');
        let chevron = $('#chevron_' + id);
        if(chevron.hasClass('fa-chevron-down')){
            chevron.removeClass('fa-chevron-down');
            chevron.addClass('fa-chevron-up');
        }
        else{
            chevron.removeClass('fa-chevron-up');
            chevron.addClass('fa-chevron-down');
        }
    });
});
