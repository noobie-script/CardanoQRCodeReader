const resultBox = document.getElementById("result");
let html5QrcodeScanner;

function onScanSuccess(decodedText, decodedResult) {
    // Ferma lo scanner temporaneamente
    html5QrcodeScanner.clear();
    
    // Valida il QR
    validateQR(decodedText);
}

function onScanError(errorMessage) {
    // Ignora gli errori di scansione continui
}

function startScanner() {
    html5QrcodeScanner = new Html5QrcodeScanner(
        "reader",
        { 
            fps: 10, 
            qrbox: { width: 250, height: 250 },
            aspectRatio: 1.0
        },
        false
    );
    
    html5QrcodeScanner.render(onScanSuccess, onScanError);
}

async function validateQR(qrText) {
    resultBox.innerHTML = "<p>Verifica in corso...</p>";
    
    try {
        const response = await fetch("/validate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ qr_text: qrText })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultBox.innerHTML = `
                <h2> QR Riconosciuto!</h2>
                <p><b>Nome:</b> ${data.nome}</p>
                <p><b>Cognome:</b> ${data.cognome}</p>
                <p><b>Gruppo:</b> ${data.gruppo}</p>
            `;
        } else {
            resultBox.innerHTML = `
                <h2 style="color:red;"> Errore</h2>
                <p>${data.error}</p>
            `;
        }
    } catch (error) {
        resultBox.innerHTML = `
            <h2 style="color:red;"> Errore di connessione</h2>
            <p>${error.message}</p>
        `;
    }
    
    // Riparte lo scanner dopo 3 secondi
    setTimeout(startScanner, 3000);
}

document.addEventListener("DOMContentLoaded", startScanner);