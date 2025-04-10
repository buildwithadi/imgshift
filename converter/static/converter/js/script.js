document.getElementById('fileInput').addEventListener('change', function () {
  const fileListDiv = document.getElementById('fileList');
  const files = this.files;
  
  if (files.length === 0) {
    fileListDiv.innerHTML = "<i>No files selected</i>";
    return;
  }

  let list = "<strong>Selected files:</strong><ul>";
  for (let i = 0; i < files.length; i++) {
    list += `<li>${files[i].name}</li>`;
  }
  list += "</ul>";
  fileListDiv.innerHTML = list;
});

let dropArea = document.getElementById('drop-area');
let fileInput = document.getElementById('fileInput');
let fileList = document.getElementById('fileList');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, e => e.preventDefault());
  dropArea.addEventListener(eventName, e => e.stopPropagation());
});

// Highlight on drag
['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'));
});
['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'));
});

// Handle dropped files
dropArea.addEventListener('drop', handleDrop);

function handleDrop(e) {
  let dt = e.dataTransfer;
  let files = dt.files;
  fileInput.files = files; // Sets dropped files to file input
  displayFileNames(files);
}

// Display file names
function displayFileNames(files) {
  fileList.innerHTML = "";
  Array.from(files).forEach(file => {
    fileList.innerHTML += `<div>📄 ${file.name}</div>`;
  });
}

// Also show names when selected using Choose File
fileInput.addEventListener('change', () => {
  displayFileNames(fileInput.files);
});