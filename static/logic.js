const POINT_VALUES = [20, 40, 60, 80, 100];
let keyBuffer = [];
let bufferTimeout = null;

document.addEventListener('keydown', (event) => {
    const key = event.key;

    // Shortcut: Z -> Zurück zur Hauptseite
    if (key.toUpperCase() === 'H') {
        window.location.href = '/';
        return;
    }

    // Shortcut: A -> Frage auflösen (nur wenn der Button existiert)
    if (key.toUpperCase() === 'A') {
        const resolveButton = document.querySelector('a.button:not(.secondary)');

        if (resolveButton && resolveButton.text === 'Auflösen') {
            resolveButton.click();
        }
        return;
    }

    // Zahlen-Shortcuts für Kategorie und Punktwert
    if (/^\d$/.test(key)) {
        // Vorhandenen Timer löschen, falls der User schnell tippt
        if (bufferTimeout) clearTimeout(bufferTimeout);

        keyBuffer.push(parseInt(key) - 1);

        if (keyBuffer.length === 2) {
            const topicId = keyBuffer[0];
            const pointIdx = keyBuffer[1];

            // Prüfen, ob die Indizes innerhalb der gültigen Bereiche liegen
            if (pointIdx < POINT_VALUES.length) {
                const pointValue = POINT_VALUES[pointIdx];
                window.location.href = `/question/${topicId}/${pointValue}`;
            }

            keyBuffer = []; // Buffer leeren
        } else {
            // Wenn nach der ersten Zahl eine gewisse Zeit vergeht, 
            // wird der Buffer geleert, damit keine "versehentlichen" Kombis entstehen.
            bufferTimeout = setTimeout(() => {
                keyBuffer = [];
            }, 1000); 
        }
    } else {
        // Bei jeder anderen Taste wird der Buffer geleert
        keyBuffer = [];
    }
});

