// GETTING THE ELEMENTS
// Get the reset all inputs modal's elements
let resetAllInputsModal = document.getElementById("reset-all-inputs-modal");
let resetAllInputsModalButton = document.getElementById("reset-all-inputs-modal-button");
let resetAllInputsModalClose = document.getElementById("reset-all-inputs-modal-close");
let resetAllInputsModalInput = document.getElementById("reset-all-inputs-modal-input");
let resetAllInputsModalConfirm = document.getElementById("reset-all-inputs-confirm-button");

// Get the reset all input success modal's elements
let resetAllInputsSuccessModal = document.getElementById("reset-all-inputs-success-modal");
let resetAllInputsModalSuccessClose = document.getElementById("reset-all-inputs-success-modal-close");

// RESET ALL INPUTS MODAL
// Open the reset all inputs modal if the button was pressed
resetAllInputsModalButton.onclick = () => {
    resetAllInputsModal.style.display = "block";
    resetAllInputsModalInput.value = "";
}

// When the user clicks on the close button, close the modal
resetAllInputsModalClose.onclick = () => {
    resetAllInputsModal.style.display = "none";
}

// Check if the user has entered the correct string into the delete question popup
resetAllInputsModalInput.onkeyup = () => {
    // Get the current value
    let currentValue = resetAllInputsModalInput.value;

    // If it matches what we expected, then enable the delete button
    resetAllInputsModalConfirm.disabled = !(new RegExp("[rR][eE][sS][eE][tT] [aA][lL][lL] [iI][nN][pP][uU][tT][sS]")).test(currentValue);
}

// If the user clicks on the reset input modal's "yes" button, then send a request to the reset input page
resetAllInputsModalConfirm.onclick = () => {
    console.log("Button clicked");
    const request = new Request(
        RESET_INPUT_URL,
        {
            headers: {"X-CSRFToken": Cookies.get("csrftoken")},
        }
    );

    // Send a request to the reset input page
    fetch(request, {
        method: "POST",
        mode: "same-origin"
    }).then((response) => {
        return response.text()
    }).then((text) => {
        if (text === "Operation Complete") {
            // Close the current modal
            resetAllInputsModal.style.display = "none";

            // Show the success message modal
            resetAllInputsSuccessModal.style.display = "block";
        }
    });
}

// RESET ALL INPUTS SUCCESS MODAL
// When the user clicks on the close button, close the modal
resetAllInputsModalSuccessClose.onclick = () => {
    resetAllInputsSuccessModal.style.display = "none";
}

// FOR ALL MODALS
// When the user clicks anywhere outside of any modal, close all modals
window.onclick = (event) => {
    if (event.target === resetAllInputsModal || event.target === resetAllInputsSuccessModal) {
        resetAllInputsModal.style.display = "none";
        resetAllInputsSuccessModal.style.display = "none"
    }
}
