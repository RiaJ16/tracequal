$(document).ready(function(){
    $('#add_another').click(function(){
        let my_form = $('#form');
        let data = my_form.serialize();
        $.ajax({
            type: 'POST',
            url: '',
            data: data,
            success: function(response){
                alert_appear(
                    'The artifact was successfully added',
                    '.custom-alert.success',
                    2000,
                );
                my_form[0].reset();
                let key_field = $('#key');
                let new_max= parseInt(key_field.val()) + 1;
                key_field.attr('value', new_max);
                key_field.attr('min', new_max);
                $('#role_p').html('.');
                $('#action_p').html('.');
                $('#benefit_p').html('.');
            },
            error: function(error){
                alert_appear(
                    'Verify that all fields have been correctly filled',
                    '.custom-alert.failure',
                    1500,
                );
            }
        });
    });
});
