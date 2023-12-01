$(document).ready(function() {

    let lastScrollTop = 0;
    const navbar = $('.navbar');

    $(window).scroll(function () {
        const scrollTop = $(this).scrollTop();
        if (scrollTop > lastScrollTop) {
            navbar.css('top', `-${navbar.outerHeight()}px`);
        } else {
            navbar.css('top', '0');
        }
        lastScrollTop = scrollTop;
    });
});