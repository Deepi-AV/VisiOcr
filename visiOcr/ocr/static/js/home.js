document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("upload-form");
    form.addEventListener("submit", () => {
        form.querySelector("button[type='submit']").textContent = "Uploading...";
    });
});
