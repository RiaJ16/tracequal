$(document).ready(function(){
    let password = $('#id_password1');
    password.removeAttr('required');
    $('#id_password2').removeAttr('required');
    password.on('change', function(){
        $('#current_password').show();
    });
    $('#btn_editar').click(function(event){
        $('#user_form').show();
        $('.card').hide();
    });
});
