$(document).ready(function(){
    $('#keep_editing').click(function(){
        let my_form = $('#form');
        let data = my_form.serialize();
        $.ajax({
            type: 'POST',
            url: '',
            data: data,
            success: function(response){
                alert_appear(
                    'The artifact was successfully updated',
                    '.custom-alert.success',
                    2000,
                );
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
