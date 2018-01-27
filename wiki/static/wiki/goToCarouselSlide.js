$(document).ready(function () {
    function qs(key) {
        key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
        var match = location.search.match(new RegExp("[?&]" + key + "=([^&]+)(&|$)"));
        var slide = match && decodeURIComponent(match[1].replace(/\+/g, " "));
        var id = parseInt(slide);
        if (isNaN(id)) {
            return "pause";
        }
        return id;
    }

    $('#wikiCarousel').carousel(qs('slide'));
});
