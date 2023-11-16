$(document).ready(function(){
    $('.archive').click(function(){
        let confirmation_dialog= $('#confirmation_dialog');
        let id = $(this).data('id');
        let archive = $(this).data('archive');
        let is_link = $(this).data('is_link');
        let element = "artifact";
        if(is_link)
            element = "link";
        confirmation_dialog.data('id', id).show();
        confirmation_dialog.data('archive', archive).show();
        if(archive)
            $('.custom-alert-info').html('Are you sure you want to delete this '+element+'?');
        else
            $('.custom-alert-info').html('Are you sure you want to restore this '+element+'?');
        $('#confirm_button').click(function(){
            confirmation_dialog.hide();
            let id = confirmation_dialog.data('id');
            let archive = confirmation_dialog.data('archive');
            $.ajax({
                headers:{
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                type: 'POST',
                url: window.location.origin + $(this).data('url'),
                data: JSON.stringify({
                    'id': id,
                    'archive': archive,
                }),
                success: function (response){
                    $('#artifact' + id).fadeOut();
                    $('#link' + id).fadeOut();
                },
                error: function (error){
                }
            });
        });
        $('#cancel_button').click(function(){
            confirmation_dialog.hide();
        });
    });
});
