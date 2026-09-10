const inputCitta = document.getElementById('citta');
const dataList = document.getElementById('citta-list');

// Sostituisci con la tua API Key Geoapify
const API_KEY = '17da1441495b4bc895f8c734bcaa2400'; 

let timerDebounce;

if (inputCitta && dataList) {
    inputCitta.addEventListener('input', function() {
        const query = this.value;

        // Annulla il timer precedente ad ogni nuovo carattere digitato
        clearTimeout(timerDebounce);

        if (query.length < 3) {
            dataList.innerHTML = '';
            return;
        }

        // Attende 400 millisecondi prima di inviare la richiesta API
        timerDebounce = setTimeout(async () => {
            const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(query)}&filter=countrycode:it&type=city&apiKey=${API_KEY}`;

            try {
                const response = await fetch(url);
                const data = await response.json();
                
                dataList.innerHTML = ''; // Svuota i vecchi suggerimenti
                
                if (data.features) {
                    data.features.forEach(feature => {
                        const option = document.createElement('option');
                        option.value = feature.properties.city || feature.properties.name; 
                        dataList.appendChild(option);
                    });
                }
            } catch (error) {
                console.error("Errore nel recupero città con Geoapify:", error);
            }
        }, 400); // 0,4 secondi di attesa
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const selectTitolo = document.getElementById('titolo_professionale');
    const boxAltro = document.getElementById('box_altro');
    const inputAltro = document.getElementById('titolo_altro');

    if (selectTitolo) {
        selectTitolo.addEventListener('change', () => {
            if (selectTitolo.value === 'Altro') {
                boxAltro.style.display = 'block';
                inputAltro.required = true;
            } else {
                boxAltro.style.display = 'none';
                inputAltro.required = false;
                inputAltro.value = '';
            }
        });
    }
});