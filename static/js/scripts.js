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

// Aktivera partiklar automatiskt vid sidladdning (3 gånger)
document.addEventListener("DOMContentLoaded", function() {
    for (let i = 0; i < 3; i++) { // Kör 3 gånger vid sidladdning
        setTimeout(generateParticles, i * 600); // Skjuter iväg partiklar varje 1.5 sekund
    }
});



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


document.addEventListener("DOMContentLoaded", function () {
    const introText = document.querySelector(".intro-text");

    function checkScroll() {
        const rect = introText.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        if (rect.top < windowHeight * 0.75) {
            introText.classList.add("in-view"); // Lägg till klassen när sektionen är i vy
        } else {
            introText.classList.remove("in-view"); // Ta bort klassen om man scrollar upp
        }
    }

    window.addEventListener("scroll", checkScroll);
});


document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".scroll-animation");

    function checkScroll() {
        elements.forEach(element => {
            const rect = element.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            if (rect.top < windowHeight * 0.75) {
                element.classList.add("in-view"); // Lägg till klassen när elementet är i vy
            } else {
                element.classList.remove("in-view"); // Ta bort klassen om man scrollar upp
            }
        });
    }

    window.addEventListener("scroll", checkScroll);
    checkScroll(); // Kör direkt vid start
});

CKEDITOR.on('instanceReady', function(event) {
    // Sätt bakgrundsfärgen till mörk (samma som övriga fält)
    event.editor.document.getBody().setStyle('background-color', '#000000');

    // Sätt textfärgen till gul (FFF002)
    event.editor.document.getBody().setStyle('color', '#FFFFFF');

});


window.addEventListener('load', function() {
    setTimeout(function() {
        // Försök dölja popupen för versionen
        const warningPopup = document.querySelector('.cke_version_warning');
        if (warningPopup) {
            warningPopup.style.display = 'none'; // Döljer varningen
        }
    }, 500); // Vänta en kort stund innan du döljer popupen
});


CKEDITOR.on('instanceReady', function(event) {
    var editorDocument = event.editor.document;

    // Sätt glöd-effekten för hela CKEditor-containeren (icke textinnehållet)
    var editorContainer = event.editor.container;  // Referens till hela CKEditor-behållaren
    editorContainer.setStyle('box-shadow', '0 0 10px #FFFF00, 0 0 20px #FFFF00, 0 0 40px #8A2BE2, 0 0 100px #8A2BE2');
    // Ta bort padding och margin från hela CKEditor-området, inklusive border
    var editorInner = editorContainer.getChild(0);  // Den inre delen av CKEditor, .cke_inner
    editorInner.setStyle('padding', '0');
    editorInner.setStyle('margin', '0');
    editorInner.setStyle('border', '1px solid #FFFF00');  // Ändra till önskad border
});
