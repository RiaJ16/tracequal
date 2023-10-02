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
});

function determine_article(user_input){
    let vowels = ['a', 'e', 'i', 'o'];
    if(vowels.some(vowel => user_input.toLowerCase().startsWith(vowel)))
        return "an";
    else
        return"a";
}
