const images = ['../../static/img/landingimage1.jpg','../../static/img/landingimage2.jpg','../../static/img/landingimage3.jpg'];
    let index = 0;
    const hero = document.querySelector('.hero');
 
    function changeImage() {
        console.log(images[index]);
        hero.style.backgroundImage = `url('${images[index]}')`;
        console.log(hero.style.backgroundImage);
        index = (index + 1) % images.length;
    }
 
    // Change image every 5 seconds
    setInterval(changeImage, 2000);
