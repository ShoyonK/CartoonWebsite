var minPerSlide = 3;
function slideCarousel() {
    var next = $(this).next();
    if (!next.length) {
        next = $(this).siblings(':first');
    }

    next.children(':first-child').clone().appendTo($(this));

    for (var i = 0; i < minPerSlide; i++) {
        next = next.next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }
        
        next.children(':first-child').clone().appendTo($(this));
    }
}

$('.carousel .carousel-item').each(slideCarousel);

module.exports = {
    slideCarousel : slideCarousel,
    minPerSlide: minPerSlide
};