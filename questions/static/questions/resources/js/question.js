// Define a ShowDown markdown converter
const converter = new showdown.Converter();

// Parse the markdown and show the content of the question
document.getElementById("question-body").innerHTML = converter.makeHtml(QUESTION_CONTENT);
