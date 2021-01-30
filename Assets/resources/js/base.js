function createAlert(alertInfo, level = 20) {
    // Determine the alert level based on the `level` given
    switch (level) {
        case 10:
            level = "debug";
            break;
        case 20:
            level = "info";
            break;
        case 25:
            level = "success";
            break;
        case 30:
            level = "warning";
            break;
        case 40:
            level = "error";
            break;
        default:
            level = "info";
    }

    // Prevent XSS by replacing angled brackets with special characters
    alertInfo = DOMPurify.sanitize(alertInfo);

    // Craft alert HTML
    let alertHTML = `<div class="alert"><div class="alert-box alert-` + level + `"><span class="alert-box-close-button" id="alert-temp">&times;</span>${alertInfo}</div></div>`;

    // Prepend the HTML code to the `parentElement`
    document.getElementById("alerts-box").insertAdjacentHTML("beforeend", alertHTML);

    // Get the new alert close button element
    let alertCloseButton = document.getElementById("alert-temp");

    // Remove the id from the alert close button element
    alertCloseButton.removeAttribute("id");

    // Add an 'onclick' event to the alert
    alertCloseButton.onclick = function () {
        // Get the div element of the alert
        let div = this.parentElement;

        // Set the opacity of div to 0%
        div.style.opacity = "0";

        // Wait for 600 ms before executing this code
        setTimeout(function () {
            // Hide the div
            div.style.display = "none";

            // Remove the div after the `div`'s display has been set to "none".
            div.remove();
        }, 600);
    }
}
