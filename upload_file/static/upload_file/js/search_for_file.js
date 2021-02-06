// Get elements
let table = document.getElementById("file-table");
let tr = table.getElementsByTagName("tr");
let input = document.getElementById("file-search");

// Functions
function copyToClipboard(text) {
    let dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
}

function search() {
    // Declare variables
    let filter = input.value.toUpperCase();

    // Loop through all table rows, and hide those who don't match the search query
    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            let textValue = td.innerText;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// Click events
window.onclick = e => {
    // Get the target element
    let target = e.target;

    // Check if it is an element with the class `file-name`
    if (target.className === "file-name") {
        // Get the file name
        let fileName = target.innerText;

        // Encode the file name
        fileName = encodeURI(fileName);

        // Generate the final file url
        let url = UPLOADED_FILES_ROOT + fileName;
        console.log(url);

        // "Copy" it to the clipboard
        copyToClipboard(url);

        // Show a success alert
        createAlert("Copied URL to the file!", 25);
    }

}
