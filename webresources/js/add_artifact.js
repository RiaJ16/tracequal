$(document).ready(function(){
    $('#add_another').click(function(event){
        event.preventDefault();
        let my_form = $('#form')[0];
        let data = new FormData(my_form);
        $.ajax({
            type: 'POST',
            url: '',
            data: data,
            processData: false,
            contentType: false,
            success: function(response){
                alert_appear(
                    'The artifact was successfully added',
                    '.custom-alert.success',
                    2000,
                );
                my_form.reset();
                let key_field = $('#key');
                let new_max= parseInt(key_field.val()) + 1;
                key_field.attr('value', new_max);
                key_field.attr('min', new_max);
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
