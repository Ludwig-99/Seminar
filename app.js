// app.js handles user interactions and sends AJAX requests to the FastAPI backend

// OCR for prescription image upload
function uploadPrescription() {
    const fileInput = document.getElementById("ocr-file");
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    fetch("http://localhost:8000/ocr/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("ocr-result").innerText = data.ocr_text || "No text found.";
    });
}

// Drug Compatibility Check
function checkCompatibility() {
    const drug1 = document.getElementById("drug1").value;
    const drug2 = document.getElementById("drug2").value;

    fetch("http://localhost:8000/check_compatibility/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ drugs: [drug1, drug2] })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("compatibility-result").innerText = data.compatibility_check;
    });
}

// Drug Recommendation based on symptoms
function recommendDrug() {
    const symptoms = document.getElementById("symptoms").value;

    fetch("http://localhost:8000/recommend/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptoms })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("recommendation-result").innerText = data.recommendation;
    });
}

// Medication Purchase
function purchaseMedication() {
    const medication = document.getElementById("medication").value;

    fetch("http://localhost:8000/purchase/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ medication: medication })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("purchase-result").innerText = data.purchase_status;
    });
}
