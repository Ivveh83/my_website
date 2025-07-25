/*!
* Start Bootstrap - Business Casual v7.0.9 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
//console.log("JavaScript file is loaded.");


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("morseForm");
    const recordingTimeInput = document.getElementById("recording_time"); // Hämta dropdown
    const choiceInput = document.querySelector('input[name="choice"]:checked');
    let mediaRecorder;
    let recordedChunks = [];

    console.log("JavaScript file is loaded."); // Kontrollera att scriptet är laddat

    // Lyssna på submit-eventet
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Stoppa formuläret från att skicka direkt

        // Lägg till logg här för att bekräfta att submit-eventet fångas upp
        console.log("Form submit intercepted.");

        // Kontrollera vilket val användaren har gjort
        const choiceInput = document.querySelector('input[name="choice"]:checked');
        console.log("Form submitted, selected choice: ", choiceInput ? choiceInput.value : "None");

        if (choiceInput && choiceInput.value === "analyze") {
            console.log("Analyze chosen, starting recording...");
            startRecording(); // Starta inspelning om "analyze" är valt
        } else {
            console.log("Play chosen, submitting form...");
            setTimeout(() => {
                form.submit(); // Skicka formuläret manuellt efter en kort fördröjning
            }, 100); // Fördröj formulärskickningen så att preventDefault får effekt
        }
    });

    function startRecording() {
        const recordingTime = recordingTimeInput ? parseInt(recordingTimeInput.value) * 1000 : 5000;
        console.log("Recording for ", recordingTime / 1000, " seconds");

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                recordedChunks = [];

                mediaRecorder.ondataavailable = event => {
                    if (event.data.size > 0) {
                        recordedChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = sendAudioFile;

                mediaRecorder.start();

                // Stoppa inspelning efter valt antal sekunder
                setTimeout(() => {
                    console.log("Stopping recording...");
                    mediaRecorder.stop();
                }, recordingTime);
            })
            .catch(error => {
                console.error("Error accessing microphone:", error);
            });
    }

    function sendAudioFile() {
        
        const audioBlob = new Blob(recordedChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "audio_recording.wav");

        // Hämta och skicka CSRF-token
        const csrfToken = document.querySelector("input[name='csrf_token']").value;
        formData.append("csrf_token", csrfToken);

        // Hämta och skicka valda alternativ från formuläret
        const choice = document.querySelector('input[name="choice"]:checked');
        if (choice) {
            formData.append("choice", choice.value);
        } else {
            console.error("Choice is missing!");
        }

        const recordingTime = document.getElementById("recording_time");
        if (recordingTime) {
            formData.append("recording_time", recordingTime.value);
        } else {
            console.error("Recording time is missing!");
        }

        console.log("Sending audio file with form data...");
        for (const [key, value] of formData.entries()) {
            console.log(key, value);
        }


        fetch("/morse_decoder", {
            method: "POST",
            body: formData
        })
        .then(response => response.text()) // Flask returnerar HTML
        .then(responseText => {
            document.getElementById("text").innerHTML = responseText;
        })
        .catch(error => console.error("Error uploading audio:", error));
    }
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
        setTimeout(generateParticles, i * 600); // Skjuter iväg partiklar varje 0.6 sekund
    }
});



//document.addEventListener("DOMContentLoaded", function () {
//    const image = document.querySelector(".blur-on-scroll");
//
//    window.addEventListener("scroll", function () {
//        const scrollPosition = window.scrollY;
//        if (scrollPosition > 250) {  // Justera detta värde beroende på när du vill att effekten ska slå in
//            image.classList.add("scrolled");
//        } else {
//            image.classList.remove("scrolled");
//        }
//    });
//});

document.addEventListener("DOMContentLoaded", function () {
    const image = document.querySelector('.blur-on-scroll');
    let isInView = false;  // Håller koll på om bilden är i "in-view"-läge

    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            // Om inte redan i-view och minst 50% synligt, lägg till klassen
            if (!isInView && entry.intersectionRatio >= 0.5) {
                image.classList.add("scrolled");
                isInView = true;
            }
            // Om redan in-view men synligheten sjunker under 0.3, ta bort klassen
            else if (isInView && entry.intersectionRatio < 0.7) {
                image.classList.remove("scrolled");
                isInView = false;
            }
        });
    }, { threshold: [0.7, 0.5] });  // Använder en array med tröskelvärden

    observer.observe(image);
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

        const img = document.querySelector('.blur-on-scroll');
        if (!img) return; // Kör inte vidare om bilden inte finns!

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

        const img = document.querySelector('.blur-on-scroll');
        if (!img) return; // Kör inte vidare om bilden inte finns!


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








