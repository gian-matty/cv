const inputCitta = document.getElementById('citta');
const dataList = document.getElementById('citta-list');
const API_KEY = "{{ geoapify_key }}";

let timerDebounce;

if (inputCitta && dataList) {
    inputCitta.addEventListener('input', function() {
        const query = this.value;

        clearTimeout(timerDebounce);

        if (query.length < 3) {
            dataList.innerHTML = '';
            return;
        }

        timerDebounce = setTimeout(async () => {
            const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(query)}&filter=countrycode:it&type=city&apiKey=${API_KEY}`;

            try {
                const response = await fetch(url);
                const data = await response.json();
                
                dataList.innerHTML = ''; 
                
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
        }, 400);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('cv-theme');
    const applyTheme = (theme) => {
        document.documentElement.dataset.theme = theme;
        if (themeToggle) {
            const dark = theme === 'dark';
            themeToggle.setAttribute('aria-pressed', String(dark));
            themeToggle.innerHTML = `<span class="theme-icon">${dark ? '☀' : '☾'}</span> ${dark ? 'Modalità chiara' : 'Modalità scura'}`;
        }
    };
    applyTheme(savedTheme === 'dark' ? 'dark' : 'light');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('cv-theme', nextTheme);
            applyTheme(nextTheme);
        });
    }

    const imageInput = document.getElementById('foto_profilo');
    const imagePreview = document.getElementById('image-preview');
    const imagePreviewImg = document.getElementById('image-preview-img');
    const removeImage = document.getElementById('remove-image');

    if (imageInput && imagePreview && imagePreviewImg) {
        imageInput.addEventListener('change', () => {
            const file = imageInput.files[0];
            if (!file) {
                imagePreview.hidden = true;
                imagePreviewImg.removeAttribute('src');
                return;
            }
            if (!file.type.startsWith('image/')) {
                imageInput.value = '';
                return;
            }
            imagePreviewImg.src = URL.createObjectURL(file);
            imagePreview.hidden = false;
        });
    }

    if (removeImage) {
        removeImage.addEventListener('click', () => {
            imageInput.value = '';
            imagePreview.hidden = true;
            imagePreviewImg.removeAttribute('src');
        });
    }

    // Gestione campo "Altro" per Titolo Professionale
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

    // Gestione checkbox "Altro" per Titolo di Studio
    const checkboxes = document.querySelectorAll('input[name="titolo_studio"]');
    const boxAltroTitolo = document.getElementById('box_altro_titolo');
    const inputAltroTitolo = document.getElementById('titolo_studio_altro');

    checkboxes.forEach(cb => {
        if (cb.value === 'Altro') {
            cb.addEventListener('change', () => {
                if (cb.checked) {
                    boxAltroTitolo.style.display = 'block';
                    inputAltroTitolo.required = true;
                } else {
                    boxAltroTitolo.style.display = 'none';
                    inputAltroTitolo.required = false;
                    inputAltroTitolo.value = '';
                }
            });
        }
    });
});