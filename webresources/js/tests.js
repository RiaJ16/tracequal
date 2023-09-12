$(document).ready(function() {
    $('.change_option').on('click', function(event) {
        event.preventDefault();
        let option = $(this).data('option');
        let id = $(this).data('buttonid');
        let menu = $('#verdict_menu_' + id);
        let verdict = "";
        menu.removeClass('verdict');
        menu.removeClass('btn-success');
        menu.removeClass('btn_pass');
        menu.removeClass('btn-secondary');
        menu.removeClass('btn-danger');
        menu.removeClass('btn_not_tested');
        switch(option){
            case 0:
                verdict = "Not tested";
                menu.addClass('btn_not_tested');
                break;
            case 1:
                verdict = "Pass";
                menu.addClass('btn-success');
                menu.addClass('btn_pass');
                break;
            case 2:
                verdict = "Inconclusive";
                menu.addClass('btn-secondary');
                break;
            case 3:
                verdict = "Fail";
                menu.addClass('btn-danger');
                break;
        }
        menu.text(verdict);
    });
});