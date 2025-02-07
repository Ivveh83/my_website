/*!
* Start Bootstrap - Business Casual v7.0.9 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
// Highlights current date on contact page
window.addEventListener('DOMContentLoaded', event => {
    const listHoursArray = document.body.querySelectorAll('.list-hours li');
    listHoursArray[new Date().getDay()].classList.add(('today'));
});

// Funktion som genererar partiklar från bildens kanter
function generateParticles() {
    const particleContainer = document.querySelector('.particles');
    const particleCount = 60; // Antal partiklar som ska genereras

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        // Bestäm slumpmässig startposition längs bildens kanter
        let side = Math.floor(Math.random() * 4); // 0 = vänster, 1 = höger, 2 = topp, 3 = botten
        let xStart = 0, yStart = 0, xMove = 0, yMove = 0;

        switch (side) {
            case 0: // Vänster sida
                xStart = 0;
                yStart = Math.random() * 100 + '%';
                xMove = Math.random() * 200 - 100 + 'px'; // Rörelse åt höger/vänster
                yMove = Math.random() * 200 - 100 + 'px'; // Rörelse upp/ner
                break;
            case 1: // Höger sida
                xStart = '100%';
                yStart = Math.random() * 100 + '%';
                xMove = Math.random() * 200 - 100 + 'px';
                yMove = Math.random() * 200 - 100 + 'px';
                break;
            case 2: // Topp
                xStart = Math.random() * 100 + '%';
                yStart = 0;
                xMove = Math.random() * 200 - 100 + 'px';
                yMove = Math.random() * 200 - 100 + 'px';
                break;
            case 3: // Botten
                xStart = Math.random() * 100 + '%';
                yStart = '100%';
                xMove = Math.random() * 200 - 100 + 'px';
                yMove = Math.random() * 200 - 100 + 'px';
                break;
        }

        // Sätt startposition och rörelse
        particle.style.left = xStart;
        particle.style.top = yStart;
        particle.style.setProperty('--x', xMove);
        particle.style.setProperty('--y', yMove);

        // Lägg till partikeln i containern
        particleContainer.appendChild(particle);

        // Ta bort partikeln efter animationen
        setTimeout(() => {
            particle.remove();
        }, 5000);
    }
}

// Lägg till eventlyssnare för att skapa partiklar vid hover
document.querySelector('.particle-container').addEventListener('mouseenter', generateParticles);


document.addEventListener("DOMContentLoaded", function () {
    const image = document.querySelector(".blur-on-scroll");

    window.addEventListener("scroll", function () {
        const scrollPosition = window.scrollY;
        if (scrollPosition > 250) {  // Justera detta värde beroende på när du vill att effekten ska slå in
            image.classList.add("scrolled");
        } else {
            image.classList.remove("scrolled");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".product-item-img");

    function checkVisibility() {
        images.forEach(img => {
            const rect = img.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8) {  // Justera värdet för att trigga tidigare/senare
                img.classList.add("in-view");
            }
        });
    }

    window.addEventListener("scroll", checkVisibility);
    checkVisibility();  // Kör direkt för bilder som redan är synliga
});


document.addEventListener("DOMContentLoaded", function () {
    const titles = document.querySelectorAll(".product-item-title");
    const images = document.querySelectorAll(".product-item-img");

    function checkVisibility() {
        titles.forEach(title => {
            const rect = title.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8) {
                title.classList.add("in-view");
            }
        });

        images.forEach(img => {
            const rect = img.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8) {
                img.classList.add("in-view");
            }
        });
    }

    window.addEventListener("scroll", checkVisibility);
    checkVisibility();
});


document.addEventListener("DOMContentLoaded", function () {
    const descriptions = document.querySelectorAll(".product-item-description");

    function checkVisibility() {
        descriptions.forEach(desc => {
            const rect = desc.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8) {
                desc.classList.add("in-view");
            }
        });
    }

    window.addEventListener("scroll", checkVisibility);
    checkVisibility();
});
