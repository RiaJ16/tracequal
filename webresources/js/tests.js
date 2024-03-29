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
        menu.removeClass('btn_inconclusive');
        switch(option){
            case 0:
                verdict = "Not tested";
                menu.addClass('btn-secondary');
                break;
            case 1:
                verdict = "Pass";
                menu.addClass('btn-success');
                menu.addClass('btn_pass');
                break;
            case 2:
                verdict = "Inconclusive";
                menu.addClass('btn_inconclusive');
                break;
            case 3:
                verdict = "Fail";
                menu.addClass('btn-danger');
                break;
        }
        menu.text(verdict);
    });
    $('.delete_testapp').on('click', function(event){
        let confirmation_dialog= $('#confirmation_dialog');
        event.preventDefault();
        event.stopPropagation();
        let id = $(this).data('id');
        let test_id = $(this).data('testid');
        confirmation_dialog.data('id', id);
        confirmation_dialog.data('testid', test_id);
        confirmation_dialog.data('url', $(this).data('url')).show();
        $('.custom-alert-info').html('Are you sure you want to delete this test application?');
        $('#confirm_button').off('click').click(function(){
            let id = confirmation_dialog.data('id');
            let test_id = confirmation_dialog.data('testid');
            let url = confirmation_dialog.data('url');
            let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
            $.ajax({
                headers:{
                    'X-CSRFToken': csrf_token
                },
                type: 'POST',
                url: window.location.origin + url,
                data: JSON.stringify({
                    'ta_id': id,
                }),
                success: function (response){
                    $('#tapp_' + id).fadeOut();
                    $('#hidden_block_ta_' + id).fadeOut();
                    $.ajax({
                        headers:{
                            'X-CSRFToken': csrf_token
                        },
                        type: 'POST',
                        url: window.location.origin + '/test/' + test_id + '/',
                        data: {
                        },
                        success: function(response){
                            $("#number_of_ta"+response.id).html(response.test_applications);
                            $("#current_verdict"+response.id).html(
                                '<b title="'+response.application_date+'" class="verdict_title '+response.verdict+'">'+response.verdict_cap+'</b>'
                            );
                        },
                        error: function(error){
                        }
                    });
                },
                error: function (error){
                }
            });
            confirmation_dialog.hide();
        });
        $('#cancel_button').off('click').click(function(){
            confirmation_dialog.hide();
        });
    });
});
