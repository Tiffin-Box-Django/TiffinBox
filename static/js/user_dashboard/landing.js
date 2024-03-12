$(document).ready(function () {
    $('.testimonial-slider').slick({
        autoplay: true,
        autoplaySpeed: 2000,
        arrows: false,
        dots: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        cssEase: 'linear',
        adaptiveHeight: true
    });
});

const images = ['../../static/img/lunch.jpeg', '../../static/img/dinner.jpg', '../../static/img/breakfast.jpg'];
    let index = 0;
    const hero = document.querySelector('.hero');
 
    function changeImage() {
        console.log(images[index]);
        hero.style.backgroundImage = `url('${images[index]}')`;
        console.log(hero.style.backgroundImage);
        index = (index + 1) % images.length;
    }
 
    // Change image every 5 seconds
    setInterval(changeImage, 5000);