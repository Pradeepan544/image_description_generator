document.getElementById("imageForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const imageInput = document.getElementById("imageInput");
    const imageFile = imageInput.files[0];

    if (!imageFile) {
        alert("Please select an image file.");
        return;
    }

    const reader = new FileReader();

    reader.onload = async function() {
        // Get Base64 encoded string (removes data URL prefix)
        const base64Image = reader.result.split(",")[1];

        // Send Base64 encoded image to the server
        const response = await fetch("/upload", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", // Set content type to JSON
            },
            body: JSON.stringify({ image: base64Image }) // Send Base64 image data in JSON format
        });

        const result = await response.json();
        document.getElementById("description").textContent = result.description || "No description available.";
    };

    reader.readAsDataURL(imageFile); // Encode the image file as Base64
});