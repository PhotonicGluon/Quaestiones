// Get the modal elements
let modal = document.getElementById("reset-input-modal");  // Main modal div
let successModal = document.getElementById("reset-input-success-modal");  // Success modal div
let btn = document.getElementById("reset-input-modal-button");  //  The button to open the modal
let closeButton1 = document.getElementById("reset-input-success-modal-close");
let closeButton2 = document.getElementById("success-modal-close");
let noButton = document.getElementById("reset-input-no");
let yesButton = document.getElementById("reset-input-yes");

// When the user clicks the button, open the modal
btn.onclick = () => {
    modal.style.display = "block";
}

// When the user clicks on the first close button, close the reset input modal
closeButton1.onclick = () => {
    modal.style.display = "none";
}

// When the user clicks on the first close button, close the success message modal
closeButton2.onclick = () => {
    successModal.style.display = "none";
}


// When the user clicks on the "no" button, close the reset input modal
noButton.onclick = () => {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close both modals
window.onclick = (event) => {
    if (event.target === modal || event.target === successModal) {
        modal.style.display = "none";
        successModal.style.display = "none"
    }
}

// If the user clicks on the "yes" button, then send a request to the reset input page
yesButton.onclick = () => {
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
            modal.style.display = "none";

            // Show the success message modal
            successModal.style.display = "block";
        }
    });
}
