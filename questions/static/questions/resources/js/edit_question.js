// GETTING THE ELEMENTS
// Get the reset input modal's elements
let resetInputModal = document.getElementById("reset-input-modal");
let resetInputModalButton = document.getElementById("reset-input-modal-button");
let resetInputModalClose = document.getElementById("reset-input-modal-close");
let resetInputNoButton = document.getElementById("reset-input-no");
let resetInputYesButton = document.getElementById("reset-input-yes");

// Get the reset input success modal's elements
let resetInputSuccessModal = document.getElementById("reset-input-success-modal");
let resetInputModalSuccessClose = document.getElementById("reset-input-success-modal-close");

// Get the delete question modal's elements
let deleteQuestionModal = document.getElementById("delete-question-modal");
let deleteQuestionModalButton = document.getElementById("delete-question-modal-button");
let deleteQuestionModalClose = document.getElementById("delete-question-modal-close");
let deleteQuestionModalInput = document.getElementById("delete-question-modal-input");
let deleteQuestionModalConfirm = document.getElementById("confirm-delete-question-button");

// SETUP
// Set up input box's regex
deleteQuestionModalInput.pattern = CONFIRM_DELETE_REGEX;

// RESET INPUT MODAL
// Open the reset input modal if the button was pressed
resetInputModalButton.onclick = () => {
    resetInputModal.style.display = "block";
}

// When the user clicks on the close button, close the modal
resetInputModalClose.onclick = () => {
    resetInputModal.style.display = "none";
}

// When the user clicks on the "no" button, close the reset input modal
resetInputNoButton.onclick = () => {
    resetInputModal.style.display = "none";
}

// If the user clicks on the reset input modal's "yes" button, then send a request to the reset input page
resetInputYesButton.onclick = () => {
    const request = new Request(
        RESET_INPUT_URL,
        {
            headers: {"X-CSRFToken": Cookies.get("csrftoken")},
        }
    );

    // Send a request to the reset input page
    fetch(request, {
        method: "POST",
        mode: "same-origin",
        body: resetInputForm
    }).then((response) => {
        return response.text()
    }).then((text) => {
        if (text === "Operation Complete") {
            // Close the current modal
            resetInputModal.style.display = "none";

            // Show the success message modal
            resetInputSuccessModal.style.display = "block";
        }
    });
}

// RESET INPUT SUCCESS MODAL
// When the user clicks on the close button, close the modal
resetInputModalSuccessClose.onclick = () => {
    resetInputSuccessModal.style.display = "none";
}

// DELETE QUESTION MODAL
// Open the delete question modal if the button was pressed
deleteQuestionModalButton.onclick = () => {
    deleteQuestionModal.style.display = "block";
}

// When the user clicks on the close button, close the modal
deleteQuestionModalClose.onclick = () => {
    deleteQuestionModal.style.display = "none";
}

// Check if the user has entered the correct string into the delete question popup
deleteQuestionModalInput.onkeyup = () => {
    // Get the current value
    let currentValue = deleteQuestionModalInput.value;

    // If it matches what we expected, then enable the delete button
    deleteQuestionModalConfirm.disabled = !(new RegExp(CONFIRM_DELETE_REGEX)).test(currentValue);
}

// FOR ALL MODALS
// When the user clicks anywhere outside of the modal, close all modals
window.onclick = (event) => {
    if (event.target === resetInputModal || event.target === resetInputSuccessModal || event.target === deleteQuestionModal) {
        resetInputModal.style.display = "none";
        resetInputSuccessModal.style.display = "none";
        deleteQuestionModal.style.display = "none";
    }
}
