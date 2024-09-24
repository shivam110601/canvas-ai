var width = 1500;
var height = 2000;

var stage = new Konva.Stage({
    container: 'canvas-container',
    width: width,
    height: height,
});

var layer = new Konva.Layer();
stage.add(layer);

var canvas = document.createElement('canvas');
canvas.width = stage.width();
canvas.height = stage.height();

var image = new Konva.Image({
    image: canvas,
    x: 0,
    y: 0,
    shadowEnabled: 'true',
});
layer.add(image);

var context = canvas.getContext('2d');
context.strokeStyle = '#f00000';  // Set default brush color
context.lineJoin = 'round';
context.lineWidth = 5;

var isPaint = false;
var lastPointerPosition;
var mode = 'brush';

//============== Section for zoom implementation in canvas ============== //

//*** Edit necessary: now modify code for scrolling and zooming for touch
// input where zoom happens only when pinch in or out action is performed
// and dragging using 2 fingers performs the scrolling action

// Set initial scale and maximum/minimum zoom levels
var scaleBy = 1.01;  // Adjust zoom sensitivity
var minScale = 0.1;
var maxScale = 3;

// Add zoom functionality (mouse wheel)
stage.on('wheel', function (e) {
    e.evt.preventDefault(); // Prevent default scrolling behavior

    var oldScale = stage.scaleX(); // Get current scale
    var pointer = stage.getPointerPosition(); // Get mouse pointer position

    // Calculate zoom direction
    var direction = e.evt.deltaY > 0 ? -1 : 1;
    var newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;

    // Limit zoom range
    newScale = Math.max(minScale, Math.min(maxScale, newScale));

    // Calculate the position before and after scaling to keep the zoom centered
    var mousePointTo = {
        x: (pointer.x - stage.x()) / oldScale,
        y: (pointer.y - stage.y()) / oldScale
    };

    // Apply new scale
    stage.scale({ x: newScale, y: newScale });

    var newPos = {
        x: pointer.x - mousePointTo.x * newScale,
        y: pointer.y - mousePointTo.y * newScale
    };

    // Update stage position
    stage.position(newPos);

    stage.batchDraw(); // Redraw the stage with new scale
});

stage.on('mousedown touchstart', function (e) {
    if (e.evt && e.evt.button === 1) {
        stage.draggable(true);  // Enable dragging when middle mouse button is pressed
    } else if (e.evt && e.evt.button === 0) {
        stage.draggable(false);  // Disable dragging for other mouse buttons
        isPaint = true;
        // Set lastPointerPosition when the drawing starts (on mousedown or touchstart)
        var pos = stage.getPointerPosition();

        // Adjust for transformations (zoom, pan)
        var transform = stage.getAbsoluteTransform().copy();
        transform.invert();
        lastPointerPosition = transform.point(pos);

        //=========== try Update the position display
        updatePointerPosition(lastPointerPosition.x, lastPointerPosition.y);
    }
});

stage.on('mouseup touchend', function () {
    isPaint = false;
    stage.draggable(false);  // Always disable dragging after mouse release
});

//=========== pointer position display
// Add this function to update the position display
function updatePointerPosition(x, y) {
    var positionElement = document.getElementById('pointer-position');
    positionElement.textContent = Math.round(x) + ', ' + Math.round(y);
}
//===========

stage.on('mousemove touchmove', function (e) {
    if (!isPaint) {
        return;
    }

    // Ensure that only left mouse button continues drawing
    if (e.evt && e.evt.buttons !== undefined && !(e.evt.buttons & 1)) {
        isPaint = false;  // If the left mouse button is no longer pressed, stop painting
        return;
    }

    e.evt.preventDefault();

    if (mode === 'brush') {
        context.globalCompositeOperation = 'source-over';
    }
    if (mode === 'eraser') {
        context.globalCompositeOperation = 'destination-out';
    }

    // Get the pointer position relative to the canvas, adjusted for zoom and stage position
    var pos = stage.getPointerPosition();

    // Adjust the position to account for stage scale and position
    var transform = stage.getAbsoluteTransform().copy();
    transform.invert();  // Invert the transform to get the real drawing position
    var localPos = transform.point(pos);

    context.beginPath();
    // Move to the last pointer position and draw a line to the current position
    context.moveTo(lastPointerPosition.x, lastPointerPosition.y);
    context.lineTo(localPos.x, localPos.y);
    context.closePath();
    context.stroke();

    // Update the last pointer position
    lastPointerPosition = localPos;

    //=========== try Update the position display
    updatePointerPosition(localPos.x, localPos.y);

    layer.batchDraw();
});

//=================== tools changed ================
// Replace the toolSelect event listener with the following:
var brushTool = document.getElementById('brush-tool');
var eraserTool = document.getElementById('eraser-tool');

function setActiveTool(activeTool) {
    mode = activeTool;
    brushTool.classList.toggle('active', activeTool === 'brush');
    eraserTool.classList.toggle('active', activeTool === 'eraser');
}

brushTool.addEventListener('click', function() {
    setActiveTool('brush');
});

eraserTool.addEventListener('click', function() {
    setActiveTool('eraser');
});

// Initialize with brush as the active tool
setActiveTool('brush');

//====================================================

var colorPicker = document.getElementById('color-picker');
colorPicker.addEventListener('change', function () {
    context.strokeStyle = colorPicker.value;
});

var sizeSlider = document.getElementById('size-slider');
sizeSlider.addEventListener('input', function () {
    context.lineWidth = sizeSlider.value;
});

document.getElementById('generate-button').onclick = function() {
    var loadingElement = document.getElementById('loading');
    var geminiOutputElement = document.getElementById('gemini-output');
    var plotOutputElement = document.getElementById('plot-output');

    // Show loading indicator
    loadingElement.style.display = 'block';
    geminiOutputElement.innerHTML = '';
    plotOutputElement.innerHTML = '';

    // Get the canvas data as a base64-encoded string
    var tempCanvas = document.createElement('canvas');
    tempCanvas.width = stage.width();
    tempCanvas.height = stage.height();
    var tempContext = tempCanvas.getContext('2d');
    // Fill the canvas with the background color
    tempContext.fillStyle = '#f0f0f0';
    tempContext.fillRect(0, 0, canvas.width, canvas.height);

    // Draw the background
    tempContext.drawImage(canvas, 0, 0);

    var imageData = tempCanvas.toDataURL('image/png');

    // Send the image data to the backend
    fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(`HTTP error! status: ${response.status}, message: ${err.error}`);
            });
        }
        return response.json();
    })
    .then(data => {
        // Hide loading indicator
        loadingElement.style.display = 'none';

        // Log the entire response for debugging
        console.log('Backend response:', data);

        geminiOutputElement.innerHTML = data.solutions

        // Update the Gemini output
        if (data.solutions && Array.isArray(data.solutions) && data.solutions.length > 0) {
            let outputHtml = '';
            data.solutions.forEach((solution, index) => {
                outputHtml += `<strong>Question ${index + 1}:</strong> ${solution.question || 'N/A'}\n\n`;
                outputHtml += `<strong>Explanation:</strong> ${solution.explanation || 'N/A'}\n\n`;
                outputHtml += `<strong>Solution:</strong> ${solution.solution || 'N/A'}\n\n`;
                if (solution.equations && Array.isArray(solution.equations) && solution.equations.length > 0) {
                    outputHtml += `<strong>Equations:</strong> ${solution.equations.join(', ')}\n\n`;
                }
                outputHtml += '---\n\n';
            });
            geminiOutputElement.innerHTML = outputHtml;
        } else {
            geminiOutputElement.innerHTML = 'No solutions found or invalid response format.';
        }

        // Handle plotting the equations
        if (data.equations && Array.isArray(data.equations) && data.equations.length > 0) {
            plotOutputElement.innerHTML = `Equations to plot: ${data.equations.join(', ')}`;
        } else {
            plotOutputElement.innerHTML = 'No equations to plot.';
        }

    })
    .catch((error) => {
        console.error('Error:', error);
        loadingElement.style.display = 'none';
        geminiOutputElement.innerHTML = `An error occurred while processing the image: ${error.message}`;
        if (error.message.includes('raw_response')) {
            plotOutputElement.innerHTML = `Raw response from Gemini: ${error.raw_response}`;
        }
    });
};