const POINT_VALUES = [20, 40, 60, 80, 100];
let keyBuffer = [];
let bufferTimeout = null;

function isAnswered(topicId, pointValue) {
    const cookies = document.cookie.split('; ');
    const answeredCookie = cookies.find(row => row.startsWith('answered_questions='));
    if (!answeredCookie) return false;

    const answeredList = answeredCookie.split('=')[1].split(',');
    return answeredList.includes(`${topicId}-${pointValue}`);
}

document.addEventListener('keydown', (event) => {
    const key = event.key;

    if (key.toUpperCase() === 'H') {
        window.location.href = '/';
        return;
    }

    if (key.toUpperCase() === 'A') {
        const resolveButton = document.querySelector('a.button:not(.secondary)');
        if (resolveButton) {
            resolveButton.click();
        }
        return;
    }

    if (/^\d$/.test(key)) {
        if (bufferTimeout) clearTimeout(bufferTimeout);
        keyBuffer.push(parseInt(key) - 1);

        if (keyBuffer.length === 2) {
            const topicId = keyBuffer[0];
            const pointIdx = keyBuffer[1];

            if (pointIdx < POINT_VALUES.length) {
                const pointValue = POINT_VALUES[pointIdx];

                if (!isAnswered(topicId, pointValue)) {
                    window.location.href = `/question/${topicId}/${pointValue}`;
                } else {
                    console.log("Frage bereits beantwortet!");
                }
            }
            keyBuffer = [];
        } else {
            bufferTimeout = setTimeout(() => { keyBuffer = []; }, 1000); 
        }
    } else {
        keyBuffer = [];
    }
});

