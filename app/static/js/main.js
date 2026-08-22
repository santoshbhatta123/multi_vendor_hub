$(document).ready(function() {
    setTimeout(function() {
        $('.alert-dismissible').fadeOut('slow');
    }, 5000);

    $('[data-toggle="tooltip"]').tooltip();

    $('.product-card').each(function() {
        $(this).on('mouseenter', function() {
            $(this).find('.btn').addClass('btn-hover');
        }).on('mouseleave', function() {
            $(this).find('.btn').removeClass('btn-hover');
        });
    });

    $('input[type="number"]').on('input', function() {
        var max = parseInt($(this).attr('max'));
        var min = parseInt($(this).attr('min')) || 1;
        var val = parseInt($(this).val());
        if (max && val > max) {
            $(this).val(max);
        }
        if (val < min) {
            $(this).val(min);
        }
    });

    $('.table-responsive').on('click', '.btn-delete', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    if (window.location.hash) {
        $('html, body').animate({
            scrollTop: $(window.location.hash).offset().top - 100
        }, 500);
    }

    $('.navbar-toggler').on('click', function() {
        $('#navbarNav').toggleClass('show');
    });
});

function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}
