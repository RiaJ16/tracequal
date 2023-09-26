$(document).ready(function(){
    $(".diagram_button").click(function(event){
        event.preventDefault(); // Prevent the default behavior of the link
        let img_url = $(this).attr('data-rel');
        let container = $("#floating-container");
        container.html("<a href='" + img_url + "' target='_blank'><img src='" + img_url + "' alt='description' /></a>");
        if (container.is(':hidden')){
            container.fadeIn();
        }
    });

    $(document).mouseup(function(e) {
        let container = $("#floating-container");
        // If the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if (!$(e.target).is('i.fas.fa-image')) {
                container.fadeOut(); // Hide the floating container
            }
        }
    });
});
