$(document).ready(function() {
    $("#formButton").click(function() {
        $("#update_form").toggle();
    });
});


var scroll = new SmoothScroll('a[href*="#"]', {
    speed: 1500,
    speedAsDuration: true
});


var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            })

$(function () {
    $('[data-toggle="popover"]').popover()
        })
