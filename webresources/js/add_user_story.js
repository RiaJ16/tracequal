$(document).ready(function(){
    $('.role').on('input', function(){
        let input = $(this).val()
        $('#role_p').html(input);
        $('#article_p').html(determine_article(input));
    });
    $('.action').on('input', function(){
        let input = $(this).val()
        $('#action_p').html(input);
    });
    $('.benefit').on('input', function(){
        let input = $(this).val();
        $('#benefit_p').html(input);
    });
    $('#add_another').click(function(){
        let my_form = $('#form');
        let data = my_form.serialize();
        $.ajax({
            type: 'POST',
            url: '',
            data: data,
            success: function(response){
                alert_appear('.custom-alert.success', 2000);
                my_form[0].reset();
                let key_field = $('#key');
                console.log(key_field.attr('value'))
                let new_max= parseInt(key_field.val()) + 1
                console.log(new_max);
                key_field.attr('value', new_max);
                key_field.attr('min', new_max);
                $('#role_p').html('.');
                $('#action_p').html('.');
                $('#benefit_p').html('.');
            },
            error: function(error){
                alert_appear('.custom-alert.failure', 1500);
            }
        });
    });
});

function alert_appear(selector, ms){
    let alert = $(selector);
    alert.fadeIn();
    setTimeout(function(){
        alert.fadeOut();
    }, ms);
}

function determine_article(user_input){
    let vowels = ['a', 'e', 'i', 'o'];
    if(vowels.some(vowel => user_input.toLowerCase().startsWith(vowel)))
        return "an";
    else
        return"a";
}
