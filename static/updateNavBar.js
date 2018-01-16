$(document).ready(function () {
    var pathname = window.location.pathname;
    if (pathname !== '/') {
        $('nav a[href^="/' + pathname.split("/")[1] + '"]').addClass('active');
    }
});
