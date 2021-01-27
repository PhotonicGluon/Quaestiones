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
    let parsers = [getNumber, getQuotedString, getRawString, getWhitespace];
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

// MAIN CONSOLE FUNCTIONS
function input() {
    // Display the typed input to the console
    let cmd = consoleInput.val();
    $("#outputs").append("<div class=\"output-cmd\">" + cmd + "</div>");

    // Reset the input area and force update the size of the input area
    consoleInput.val("")
    autosize.update(textArea);

    // Scroll the page down to the bottom
    $("html, body").animate({
        scrollTop: $(document).height()
    }, 300);  // 300 ms = 0.3 s

    // Return the entered command
    return cmd;
}

function output(string) {
    // Set up the markdown parser
    if (!window.md) {
        window.md = window.markdownit({
            linkify: true,
            breaks: true
        });
    }
    
    // Parse the markdown of the `string`
    let output = window.md.render(string);
    
    // Append the HTML code of `output` to the outputs div
    $("#outputs").append(output);
    
    // Scroll to the bottom of the page
    $(document).scrollTop(consoleDiv.height());
}

// CONSOLE COMMANDS
function echo(...a) {
    // Join all entered arguments together with the space character
    return a.join(" ")
}

function clear() {
    // Clear console output
    $("#outputs").html("");
}

function help() {
    let result = "**Commands:**\n";
    
    let print = Object.keys(commands);
    for (let p of print) result += "- " + p + "\n";
    
    return result;
}

// SET UP JQUERY SELECTORS
let textArea = $("textarea");
let consoleDiv = $(".console");
let consoleInput = $(".console-input");

// SET UP CONSOLE
// Auto size the text area
autosize(textArea);

// Output the start up message
output("Welcome to the Quaestiones console.");

// CONSOLE CODE
// User Commands
let commands = {
    help,
    clear,
    echo
};

// Set focus to the console's input whenever the user clicks anywhere in the console div
consoleDiv.click(() => {
    $(".console-input").focus()
});

// Handle command executing and command history
let commandsHistory = [];
let commandPointer = -1;

consoleInput.on("keydown", (event) => {
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

        // Parse the input
        let args = getTokens(text)[0];
        let cmd = args.shift().value;  // Note: `shift()` is like `pop()` in Python

        // Get the value of all the non-whitespace arguments
        args = args.filter(x => x.type !== "whitespace").map(x => x.value);

        // Add the current command to the command history
        commandsHistory.unshift(text);

        // Handle the different possible cases
        if (typeof commands[cmd] === "function") {  // There exists such a command
            // Execute the command and handle the output
            let result = commands[cmd](...args);

            if (result === void (0)) {  // Returns nothing
                // So output nothing
            } else if (result instanceof Promise) {  // Need to wait for completion
                // Wait for completion, then output the result
                result.then(output);
            } else {
                // Directly output the result
                output(result);
            }
        } else if (cmd.trim() === "") {  // Nothing was entered
            output("");
        } else {
            output("Command not found: `" + cmd + "`");
            output("Use `help` for list of commands.");
        }
    }
});

