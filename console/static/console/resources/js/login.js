// SET UP JQUERY SELECTORS
let consoleDiv = $(".console");
let usernameInput = $("#username-input input");
let passwordInput = $("#password-input input");

// SET UP CONSOLE
// Auto size the input fields
autosize(usernameInput);
autosize(passwordInput);

// Handle text entering in the username input field
usernameInput.on("keydown", async (event) => {
    if (event.which === 13) {  // Enter/Return Key
        // Disable default function
        event.preventDefault();

        // Un-hide the password field
        passwordInput.parent().parent().show();

        // Move onto the password field
        passwordInput.prop("disabled", false);
        usernameInput.prop("disabled", true);

        // Give focus to the password field
        passwordInput.focus();
    }
});

// Handle text entering in the password input field
passwordInput.on("keydown", async (event) => {
    if (event.which === 13) {  // Enter/Return Key
        // Disable default function
        event.preventDefault();

        // Enable both fields for a split second
        usernameInput.prop("disabled", false);

        // Submit the form
        $("#login-form").submit();
    }
});
