// Get the modal elements
let modal = document.getElementById("delete-account-modal");  // Main Modal div
let btn = document.getElementById("delete-account-modal-button");  //  The button to open the modal
let span = document.getElementsByClassName("close")[0];  // The 'button' to close the modal
let input = document.getElementById("input-block");  // The <input> element that the user has to type in
let confirmDeleteButton = document.getElementById("confirm-delete-account-button");

// Set up input box's regex
input.pattern = CONFIRM_DELETE_REGEX;

// When the user clicks the button, open the modal
btn.onclick = () => {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = () => {
    modal.style.display = "none";
    input.value = "";
    confirmDeleteButton.disabled = true;
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
        input.value = "";
        confirmDeleteButton.disabled = true;
    }
}

// Check if the user has entered the correct string into the delete account popup
input.onkeyup = () => {
    // Get the current value
    let currentValue = input.value;

    // If it matches what we expected, then enable the delete button
    confirmDeleteButton.disabled = !(new RegExp(CONFIRM_DELETE_REGEX)).test(currentValue);
}
