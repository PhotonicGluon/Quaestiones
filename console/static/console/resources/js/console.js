// FUNCTIONS
function sendCommandToServer(cmd, args) {
    // Create a form so that the command and its arguments can be sent to the URL
    let commandForm = new FormData();
    commandForm.append("command", cmd);
    commandForm.append("args", args);

    const request = new Request(
        EXECUTE_COMMAND_URL,
        {
            headers: {"X-CSRFToken": Cookies.get("csrftoken")},
        }
    );

    // Send the command to the server
    return fetch(request, {
        method: "POST",
        mode: "same-origin",
        body: commandForm
    }).then((response) => {
        return response.text();
    });
}

function handleOutput(output) {
    // Get the first line of the output
    let splitOutput = output.split("\n");
    let firstLine = splitOutput[0];

    console.log(output);

    // Handle the output based on the first line
    if (firstLine === "SUCCESSFULLY EXECUTED") {
        // Then just return whatever else was sent along the response
        return splitOutput.slice(1).join("\n");
    } else if (firstLine === "HAS EXCEPTION") {
        // Return the exception to the screen
        return splitOutput[1];
    } else if (firstLine === "HANDLE IN JS") {
        // Get the command to be executed
        let cmd = splitOutput[1];

        // Get the arguments
        let args = JSON.parse(splitOutput[2]);

        // Execute the command and return its response
        return commands[cmd](...args);
    } else if (firstLine === "CSRF VALIDATION FAILED") {
        return "The Cross-Site Request Forgery Validation failed.";
    } else if (firstLine === "EXECUTE ANOTHER IN JS") {
        // Get the command to be executed
        let cmd = splitOutput[1];

        // Get the arguments
        let args = JSON.parse(splitOutput[2]);
        console.log(splitOutput + "\n---\n" + args);

        // Execute the command and return its response
        return commands[cmd](...args);
    } else {
        return "How did it reach here?";
    }
}

function get_output_cmd_before() {
    return curr_dir + " > ";
}

// MAIN CONSOLE FUNCTIONS
function input() {
    // Display the typed input to the console
    let cmd = DOMPurify.sanitize(consoleInput.val());
    $("#outputs").append("<div class=\"output-cmd\" output-cmd-before=\"" + get_output_cmd_before() + "\">" + cmd +
        "</div>");

    // Hide and disable the input area
    consoleInput.hide();
    consoleInput.parent().parent().attr("output-cmd-before", "");  // Hide the ">"
    consoleInput.disabled = true;

    // Reset the input area and force update the size of the input area
    consoleInput.val("");
    autosize.update(consoleInput);

    // Scroll the page down to the bottom
    $("html, body").animate({
        scrollTop: $(document).height()
    }, 300);  // 300 ms = 0.3 s

    // Return the entered command
    return cmd;
}

function output(string) {
    // Parse the `string`
    let output = "<p>" + (typeof (string) !== "undefined" ? string : "") + "</p>";  // Parse any undefined outputs as ""

    // Replace any linebreaks with the <br> tag
    output = output.replace(/\n/g, "<br />");

    // Append the HTML code of `output` to the outputs div
    $("#outputs").append(output);

    // Scroll to the bottom of the page
    $(document).scrollTop(consoleDiv.height());
}

// JAVASCRIPT IMPLEMENTED CONSOLE COMMANDS
function cd(dir_path) {
    console.log(dir_path)
    curr_dir = dir_path;
}

function clear() {
    // Clear console output
    $("#outputs").html("");
}

// SET UP JQUERY SELECTORS
let consoleDiv = $(".console");
let consoleInput = $(".console-input");

// SET UP CONSOLE
// Define `output-cmd-before`
consoleInput.parent().parent().attr("output-cmd-before", get_output_cmd_before());

// Auto size the text area
autosize(consoleInput);

// Output the start up message
output("Welcome to the Quaestiones console.");
output("Please note that this session will only last for <b>10 minutes</b>.");

// CONSOLE CODE
// Other Commands
let commands = {
    cd,
    clear
};

// Set focus to the console's input whenever the user clicks anywhere in the console div
consoleDiv.click(() => {
    $(".console-input").focus();
});

// Handle command executing and command history
let commandsHistory = [];
let commandPointer = -1;

consoleInput.on("keydown", async (event) => {
    // Handle command history
    if (event.which === 38) { // Up Arrow
        // Get the command pointer's new value
        commandPointer = Math.min(++commandPointer, commandsHistory.length - 1);

        // Get the corresponding command
        consoleInput.val(commandsHistory[commandPointer]);

    } else if (event.which === 40) { // Down Arrow
        // Get the command pointer's new value
        commandPointer = Math.max(--commandPointer, -1);

        // Get the corresponding command
        if (commandPointer === -1) {
            consoleInput.val("");  // Set it to nothing
        } else {
            consoleInput.val(commandsHistory[commandPointer]);
        }

        // Handle command execution
    } else if (event.which === 13) {  // Enter/Return Key
        // Prevent the default action of the enter key from taking place (i.e. the "new line" action)
        event.preventDefault();

        // Reset the command pointer's value
        commandPointer = -1

        // Get what the user has entered into the console
        let text = input();

        // Only parse the input if something was entered
        if (text !== "") {
            // Parse the input
            let args = getTokens(text)[0];
            let cmd = args.shift().value;  // Note: `shift()` is like `pop()` in Python

            // Get the value of all the non-whitespace arguments
            args = JSON.stringify(args.filter(x => x.type !== "whitespace").map(x => x.value));

            // Add the current command to the command history
            commandsHistory.unshift(text);

            // Send the command and its arguments to the server
            let response = sendCommandToServer(cmd, args);

            await response.then((r) => {
                output(handleOutput(r));
            });
        }

        // Show and re-enable the input area
        consoleInput.show();
        consoleInput.parent().parent().attr("output-cmd-before", get_output_cmd_before());
        consoleInput.disabled = false;
        consoleInput.focus();
    }
});

// HELPER FUNCTIONS
function getNumber(input) {
    // Get the length of the 'number' portion of the input
    let containsNumber = 0;
    while (containsNumber < input.length && "-.0123456789".includes(input[containsNumber])) containsNumber++;

    // If there is no number in the input return nothing
    if (containsNumber === 0) return [[], input];

    // If there is a number, return it as such
    let token = {
        type: "number",
        value: Number(input.slice(0, containsNumber))
    };

    return [[token], input.slice(containsNumber)];
}

function getQuotedString(input) {
    // If the input is nothing then there is no quoted string
    if (input.length === 0) return [[], input];

    // Check if the first character is a quote
    let i = 0;
    let quoteChar = input[i++];
    if (!"'\"".includes(quoteChar)) return [[], input];  // Does not include either a single quote or a double quote

    // Get the length of the string portion
    while (i < input.length) {
        if (input[i] === quoteChar) break;  // It is the end of the string
        i++;
    }

    // Process the token to be returned
    let token = {
        type: "string",
        value: input.slice(1, i)
    };

    return [[token], input.slice(i + 1)];
}

function getWhitespace(input) {
    // Get the length of the whitespace
    let whitespaceLength = 0;
    while (whitespaceLength < input.length && " \t\n\r".includes(input[whitespaceLength])) whitespaceLength++;

    // If the `whitespaceLength` is 0 then there is no whitespace
    if (whitespaceLength === 0) return [[], input];

    // Process the token to be returned
    let token = {
        type: "whitespace",
        value: input.slice(0, whitespaceLength)
    };

    return [[token], input.slice(whitespaceLength)];
}

function getRawString(input) {
    // If the input is nothing then there is no raw string
    if (input.length === 0) return [[], input];

    // Try and find the length of the raw string
    let strLen = 0;
    while (strLen < input.length && !" \t\n\r".includes(input[strLen])) strLen++;

    // If the raw string's length is 0 then there is no raw string
    if (strLen === 0) return [[], input];

    // Process the token to be returned
    let token = {
        type: "word",
        value: input.slice(0, strLen)
    };

    return [[token], input.slice(strLen)];
}

function getTokens(input) {
    // Set up variables
    let parsers = [getQuotedString, getRawString, getNumber, getWhitespace];
    let result = [];
    let lastInputSize = Infinity;
    let token;

    // Tokenize the input
    while (input.length > 0 && input.length < lastInputSize) {
        lastInputSize = input.length;
        let parser;

        for (parser of parsers) {
            // Parse the current input
            [token, input] = parser(input);

            // Append the parses input to the back of the `result` array
            result = [...result, ...token];  // Note: `...result` is the same as `*result` or `**result` in Python
        }
    }

    // Return the result
    return [result, input];
}

setTimeout(() => {
    window.location.replace(CONSOLE_LOGIN_URL);
}, 10 * 60 * 1000);  // 10 Minutes
