document.getElementById("uploadForm").addEventListener("submit", function(event) {
  event.preventDefault();

  let fileInput = document.getElementById("imageInput");
  if (fileInput.files.length === 0) {
      alert("Please choose a file before submitting.");
      return;
  }

  let formData = new FormData();
  formData.append("image", fileInput.files[0]);

  console.log("📤 Sending file:", fileInput.files[0]);  // Debugging log

  fetch("/convert/", {
      method: "POST",
      headers: {
          "X-CSRFToken": getCookie("csrftoken")
      },
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      console.log("📩 Response received:", data);
      if (data.error) {
          document.getElementById("message").innerText = "Error: " + data.error;
      } else {
          document.getElementById("message").innerText = "Conversion successful!";
          document.getElementById("convertedImage").src = data.image_url;
          document.getElementById("convertedImage").style.display = "block";
      }
  })
  .catch(error => console.error("❌ Fetch Error:", error));
});
