// Get the DOM elements
const fileInput = document.getElementById("fileInput");
const progressContainer = document.getElementById("uploadProgressContainer");
const progressBar = document.getElementById("uploadProgressBar");
const progressText = document.getElementById("uploadProgressText");
const path = document.getElementById("uploadPath").value;
const sortSelect = document.getElementById("sortSelect");
const createFolderButton = document.getElementById("createFolderButton");

// Functions
function uploadFile() {
    const file = fileInput.files[0];
    if (!file) return alert("No file selected");

    const form = new FormData();
    form.append("file", file);
    form.append("path", path);

    progressContainer.classList.remove("hidden");
    progressBar.style.width = "0%";
    progressText.textContent = "Uploading...";

    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = function (e) {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percent + "%";
            progressText.textContent = `Uploading... ${percent}%`;
        }
    };

    xhr.onload = function () {
        if (xhr.status === 204) {
            progressText.textContent = "Upload complete!";
            setTimeout(() => location.reload(), 500);
        } else {
            progressText.textContent = "Upload failed.";
        }
    };

    xhr.onerror = function () {
        progressText.textContent = "Upload error.";
    };

    xhr.open("POST", "/upload", true);
    xhr.send(form);
}

function deleteFile(path) {
    const confirmed = confirm(`Are you sure you want to delete "${path}"?`);
    if (!confirmed) return;
    fetch(`/delete/${path}`, {method: "POST"}).then(() => location.reload());
}

function createFolder() {
    const name = prompt("Enter folder name:");
    if (!name || name.trim() === "") return;

    const path = document.getElementById("uploadPath").value;
    const form = new FormData();
    form.append("name", name);
    form.append("path", path);

    fetch("/mkdir", {method: "POST", body: form}).then(() => location.reload());
}

function onSortChange() {
    const sort = sortSelect.value;

    const url = new URL(window.location);
    url.searchParams.set("sort", sort);
    window.location = url.toString();
}

//Attach event listeners
sortSelect.addEventListener("change", onSortChange);
fileInput.addEventListener("change", uploadFile);
createFolderButton.addEventListener("click", createFolder);
