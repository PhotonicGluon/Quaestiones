// Get the countdown <span> element
let countdownElement = document.getElementById("confirmation-email-wait");

// Get the resend email 'button' (<a> element)
let resendEmailButton = document.getElementById("resend-email-button");

function sendConfirmationEmail() {
    const request = new Request(
        SEND_CONFIRMATION_EMAIL_URL,
        {
            headers: {"X-CSRFToken": Cookies.get("csrftoken")},
        }
    );

    // Send the email again
    fetch(request, {
        method: "POST",
        mode: "same-origin",
        body: emailForm
    }).then((response) => {
        return response.text()
    }).then((text) => {
        if (text === "Sent Email") {
            // Start the countdown again
            startCountdown();
        }
    });
}

function updateCountdown(secondsLeft) {
    if (secondsLeft <= 0) {
        // Clear whatever is shown in the span element
        countdownElement.innerHTML = "";

        // Also update the <a> element
        resendEmailButton.removeAttribute("class");
    } else {
        if (secondsLeft === 1) {  // Grammar is important
            countdownElement.innerHTML = " in <em>1</em> second";
        } else {
            countdownElement.innerHTML = " in <em>" + secondsLeft + "</em> seconds";
        }

        // Also update the <a> element
        resendEmailButton.setAttribute("class", "disabled");
    }
}

function startCountdown() {
    let timeLeft = 60;
    let countdownInterval = setInterval(() => {
        updateCountdown(timeLeft);
        timeLeft--;

        if (timeLeft === -1) {
            clearInterval(countdownInterval);
        }
    }, 1000);  // Update every second
}

window.onload = () => {
    startCountdown();
}
