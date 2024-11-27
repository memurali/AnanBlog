jQuery(function () {

    jQuery('.navbar-toggle').on('click', function () {
        jQuery('.navbar-main').toggleClass('navbar-toggle-on');
        jQuery('.navbar-main').parents('body').toggleClass('body-overflow-hide');
    });

});