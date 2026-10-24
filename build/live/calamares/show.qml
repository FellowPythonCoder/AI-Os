/* AURA OS installer slideshow (Calamares slideshow API 2) */
import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation {
    id: presentation

    Timer {
        interval: 9000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        Image {
            id: bg1
            source: "welcome.png"
            width: parent.width; height: parent.height
            fillMode: Image.PreserveAspectCrop
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 40
            text: "Welcome to AURA OS — a blue mountain desktop"
            color: "#ffffff"
            font.pixelSize: 26
            font.bold: true
        }
    }

    Slide {
        centeredText: "<h1>Celestia Shell</h1>" +
            "<p>AURA's terminal speaks plain English: <b>aura help</b>, " +
            "<b>aura install blender</b>, <b>aura doctor</b> — plus every " +
            "standard Linux tool.</p>"
    }

    Slide {
        centeredText: "<h1>Yours to shape</h1>" +
            "<p>Wallpapers, accent colors, dock, fonts, effects — " +
            "personalize everything in AURA Settings, with live previews.</p>"
    }

    Slide {
        centeredText: "<h1>Real applications</h1>" +
            "<p>Tens of thousands of free apps from Debian and Flathub, " +
            "one click away in the AURA App Center.</p>" +
            "<p>Thank you for choosing AURA OS.</p>"
    }

    function onActivate() {
        presentation.currentSlide = 0;
    }
}
