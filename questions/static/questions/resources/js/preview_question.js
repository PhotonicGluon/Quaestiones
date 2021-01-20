// Define a ShowDown markdown converter
const converter = new showdown.Converter();

// Get the text area element
let textArea = document.getElementById("question-content");

// Get the preview area
let previewArea = document.getElementById("question-preview-area");

// Every time something was typed in the box, we update the preview area
textArea.onkeyup = () => {
    // Update the preview area
    previewArea.innerHTML = converter.makeHtml(textArea.value);
}
