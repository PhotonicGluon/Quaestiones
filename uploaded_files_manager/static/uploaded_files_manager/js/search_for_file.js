// GET ELEMENTS
// Search function elements
let list = document.getElementById("file-list");
let list_items = list.getElementsByTagName("li");
let search_box = document.getElementById("file-search");

// Delete File modal's elements
let deleteFileModal = document.getElementById("delete-file-modal");
let deleteFileModalClose = document.getElementById("delete-file-modal-close");
let deleteFileModalNoButton = document.getElementById("delete-file-modal-no");
let deleteFileModalYesButton = document.getElementById("delete-file-modal-yes");

// FILES LIST
function copyToClipboard(text) {
    let dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
}

function copyFileURL(target) {
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
    createAlert("Copied the file's URL!", 25);
}

function search() {
    // Declare variables
    let filter = search_box.value.toUpperCase();

    // Loop through all table rows, and hide those who don't match the search query
    for (let i = 0; i < list_items.length; i++) {
        let file_name = list_items[i].getElementsByTagName("a")[0];
        if (file_name) {
            file_name = file_name.innerText;
            if (file_name.toUpperCase().indexOf(filter) > -1) {
                list_items[i].style.display = "";
            } else {
                list_items[i].style.display = "none";
            }
        }
    }
}

// DELETE FILE MODAL
function showConfirmDeleteModal(listItem) {
    // Get the file name
    let fileName = listItem.getElementsByTagName("a")[0].innerText;

    // Replace all elements of the class `delete-file-name` with the file name
    let deleteFileNameElements = deleteFileModal.getElementsByClassName("delete-file-name")

    for (let i = 0; i < deleteFileNameElements.length; i++) {
        deleteFileNameElements[i].innerHTML = fileName;
    }

    // Show the delete file modal
    deleteFileModal.style.display = "block";
}

// When the user clicks on the close button, close the modal
deleteFileModalClose.onclick = () => {
    deleteFileModal.style.display = "none";
}

// When the user clicks on the "no" button, close the reset input modal
deleteFileModalNoButton.onclick = () => {
    deleteFileModal.style.display = "none";
}

deleteFileModalYesButton.onclick = () => {
    // Create a new request
    const request = new Request(
        DELETE_FILE_URL,
        {
            headers: {"X-CSRFToken": Cookies.get("csrftoken")},
        }
    );

    // Create the delete file form
    let deleteFileForm = new FormData();
    deleteFileForm.append("file_name", document.getElementsByClassName("delete-file-name")[0].innerHTML);

    // Send a request to the reset input page
    fetch(request, {
        method: "POST",
        mode: "same-origin",
        body: deleteFileForm
    }).then((response) => {
        return response.text()
    }).then((text) => {
        if (text === "Operation Complete") {
            location.reload();
        }
    });
}

// When the user clicks anywhere outside of the modal, close the modal
window.onclick = (event) => {
    if (event.target === deleteFileModal) {
        deleteFileModal.style.display = "none";
    }
}
