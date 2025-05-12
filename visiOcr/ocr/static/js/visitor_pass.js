document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        const phoneNumberInput = document.querySelector('input[name="phone_number"]');
        const phoneNumber = phoneNumberInput.value;

        // Check if the phone number is exactly 10 digits
        if (phoneNumber.length !== 10 || !/^\d{10}$/.test(phoneNumber)) {
            event.preventDefault(); // Prevent form submission
            alert("Please enter a valid 10-digit phone number.");
            return;
        }
    });

    // Generate and display QR Code if visitor pass exists
    const visitorPass = document.getElementById("visitor-pass");
    if (visitorPass) {
        const name = document.querySelector("#visitor-pass .name").textContent.trim();
        const dob = document.querySelector("#visitor-pass .dob").textContent.trim();
        const phoneNumber = document.querySelector("#visitor-pass .phone-number").textContent.trim();

        // Generate QR Code data with 6 hours validity
        const validityTimestamp = new Date(new Date().getTime() + 6 * 60 * 60 * 1000).toISOString();  // 6 hours from now
        const qrData = {
            name,
            dob,
            phone_number: phoneNumber,
            valid_until: validityTimestamp
        };

        // Display the QR Code
        const qrContainer = document.getElementById("qr-container");
        qrContainer.innerHTML = ''; // Clear existing QR code if any
        new QRCode(qrContainer, {
            text: JSON.stringify(qrData), // Stringify the data
            width: 128,
            height: 128,
        });
    }

    const downloadBtn = document.getElementById("download-pass-btn");
    downloadBtn.addEventListener("click", function () {
        const passElement = document.getElementById("visitor-pass");

        // Use html2canvas to capture the visitor pass and QR code
        html2canvas(passElement, {
            scale: 5,
            useCORS: true, // Higher resolution
            onrendered: function (canvas) {
                const imgData = canvas.toDataURL("image/png");

                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF();

                const imgWidth = 180;
                const imgHeight = canvas.height * imgWidth / canvas.width;

                const pageWidth = pdf.internal.pageSize.width;
                const pageHeight = pdf.internal.pageSize.height;
                const xOffset = (pageWidth - imgWidth) / 2;
                const yOffset = (pageHeight - imgHeight) / 2;

                // Add the pass details image
                pdf.addImage(imgData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);

                // Save the PDF
                pdf.save("Visitor_Pass_with_QR.pdf");
            }
        });
    });
});
