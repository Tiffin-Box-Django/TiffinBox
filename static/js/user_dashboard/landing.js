const images = ['../../static/img/landingimage1.jpg','../../static/img/landingimage2.jpg','../../static/img/landingimage3.jpg'];
    let index = 0;
    const hero = document.querySelector('.hero');
 
    function changeImage() {
        hero.style.backgroundImage = `url('${images[index]}')`;
        index = (index + 1) % images.length;
    }
 
    // Change image every 5 seconds
    setInterval(changeImage, 2000);
