function alert_appear(message, selector, ms){
    let alert = $(selector);
    $(selector+' .message').html(message)
    alert.fadeIn();
    setTimeout(function(){
        alert.fadeOut();
    }, ms);
}