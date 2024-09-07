const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const outputBox = document.getElementById('output-box');
let drawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);
document.getElementById('clear-btn').addEventListener('click', clearCanvas);
document.getElementById('save-btn').addEventListener('click', saveCanvas);

function startDrawing(e) {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function stopDrawing() {
    drawing = false;
    ctx.closePath();
}

function draw(e) {
    if (!drawing) return;
    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    outputBox.textContent = "Math output will be displayed here"; // Reset the output box
}

function getCanvasImage() {
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');

    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;

    tempCtx.fillStyle = "white";
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    tempCtx.drawImage(canvas, 0, 0);

    return tempCanvas.toDataURL('image/png');
}

function saveCanvas() {
    const dataURL = getCanvasImage();

    fetch('http://127.0.0.1:5000/process-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataURL }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Display the Gemini output in the output box
        outputBox.textContent = data.message;
    })
    .catch((error) => {
        console.error('Error:', error);
        outputBox.textContent = 'Error processing the image. Please try again.';
    });
}
