const inputCitta = document.getElementById('citta');
const dataListCitta = document.getElementById('citta-list');
const inputCap = document.querySelector('input[name="cap"]');
const inputLuogo = document.getElementById('luogo_nascita');
const dataListLuogo = document.getElementById('luogo-list');

const normalizzaNome = (s) => (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();

const precompilaCap = (nomeCitta, features) => {
    if (!inputCap) return;
    const cercato = normalizzaNome(nomeCitta);
    if (!cercato) return;
    for (const feature of features || []) {
        const nome = normalizzaNome(feature.properties.city || feature.properties.name);
        if (nome === cercato) {
            const cap = feature.properties.postcode;
            const valore = Array.isArray(cap) ? cap[0] : cap;
            if (valore) inputCap.value = valore;
            return;
        }
    }
};

const abilitaAutocomplete = (input, dataList, options = {}) => {
    const { soloCitta = false, dopoRisposta = null } = options;
    if (!input || !dataList) return;

    let timerDebounce;
    let risultatiCorrenti = [];

    input.addEventListener('input', function() {
        const query = this.value;

        clearTimeout(timerDebounce);

        if (query.length < 3) {
            dataList.innerHTML = '';
            return;
        }

        if (dopoRisposta) dopoRisposta(query, risultatiCorrenti);

        timerDebounce = setTimeout(async () => {
            const filtroTipo = soloCitta ? '&type=city' : '';
            const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(query)}&filter=countrycode:it${filtroTipo}&apiKey=${API_KEY}`;

            try {
                const response = await fetch(url);
                const data = await response.json();

                risultatiCorrenti = data.features || [];
                dataList.innerHTML = '';

                risultatiCorrenti.forEach(feature => {
                    const option = document.createElement('option');
                    option.value = feature.properties.city || feature.properties.name;
                    dataList.appendChild(option);
                });

                if (dopoRisposta) dopoRisposta(input.value, risultatiCorrenti);
            } catch (error) {
                console.error("Errore nel recupero città con Geoapify:", error);
            }
        }, 400);
    });
};

abilitaAutocomplete(inputCitta, dataListCitta, { soloCitta: true, dopoRisposta: precompilaCap });

abilitaAutocomplete(inputLuogo, dataListLuogo);

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('cv-theme');

    const applyTheme = (theme, animate = false) => {
        document.documentElement.dataset.theme = theme;
        if (themeToggle) {
            const dark = theme === 'dark';
            themeToggle.setAttribute('aria-pressed', String(dark));
            
            if (animate) {
                themeToggle.classList.add('animate');
                setTimeout(() => {
                    themeToggle.querySelector('.theme-icon').textContent = dark ? '☀' : '☾';
                    themeToggle.classList.remove('animate');
                }, 250);
            } else {
                themeToggle.querySelector('.theme-icon').textContent = dark ? '☀' : '☾';
            }
        }
    };

    applyTheme(savedTheme === 'dark' ? 'dark' : 'light', false);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('cv-theme', nextTheme);
            applyTheme(nextTheme, true);
        });
    }

    const telefonoInput = document.getElementById('telefono');

    if (telefonoInput) {
        telefonoInput.addEventListener('input', () => {
            const cifre = telefonoInput.value.replace(/\D/g, '').slice(0, 10);
            const gruppi = [cifre.slice(0, 3)];
            if (cifre.length > 3) gruppi.push(cifre.slice(3, 6));
            if (cifre.length > 6) gruppi.push(cifre.slice(6, 10));
            telefonoInput.value = gruppi.join(' ');
        });
    }

    const imageInput = document.getElementById('foto_profilo');
    const imagePreview = document.getElementById('image-preview');
    const imagePreviewImg = document.getElementById('image-preview-img');
    const removeImage = document.getElementById('remove-image');
    const uploadZone = document.getElementById('upload-zone');
    const uploadError = document.getElementById('upload-error');

    const MAX_FOTO = 5 * 1024 * 1024;

    const mostraErroreFoto = (msg) => {
        if (!uploadError) return;
        if (msg) {
            uploadError.textContent = msg;
            uploadError.hidden = false;
        } else {
            uploadError.hidden = true;
        }
    };

    const mostraAnteprima = (file) => {
        mostraErroreFoto(null);
        if (!file) {
            imagePreview.hidden = true;
            imagePreviewImg.removeAttribute('src');
            return;
        }
        if (!file.type.startsWith('image/')) {
            imageInput.value = '';
            mostraErroreFoto('Formato non supportato: carica un\'immagine (JPG, PNG, WebP).');
            return;
        }
        if (file.size > MAX_FOTO) {
            imageInput.value = '';
            mostraErroreFoto('File troppo grande: massimo 5 MB.');
            return;
        }
        imagePreviewImg.src = URL.createObjectURL(file);
        imagePreview.hidden = false;
    };

    if (imageInput && imagePreview && imagePreviewImg) {
        imageInput.addEventListener('change', () => {
            mostraAnteprima(imageInput.files[0]);
        });
    }

    if (uploadZone) {
        ['dragenter', 'dragover'].forEach(evt => {
            uploadZone.addEventListener(evt, (e) => {
                e.preventDefault();
                uploadZone.classList.add('upload-active');
            });
        });

        ['dragleave', 'drop'].forEach(evt => {
            uploadZone.addEventListener(evt, (e) => {
                e.preventDefault();
                uploadZone.classList.remove('upload-active');
            });
        });

        uploadZone.addEventListener('drop', (e) => {
            const file = e.dataTransfer.files && e.dataTransfer.files[0];
            if (!file) return;
            imageInput.files = e.dataTransfer.files;
            mostraAnteprima(file);
        });
    }

    if (removeImage) {
        removeImage.addEventListener('click', () => {
            imageInput.value = '';
            imagePreview.hidden = true;
            imagePreviewImg.removeAttribute('src');
            mostraErroreFoto(null);
        });
    }

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

    const filtroTitoli = document.getElementById('titolo_filtro');
    const listaTitoli = document.getElementById('titoli_lista');

    if (filtroTitoli && listaTitoli) {
        const righe = Array.from(listaTitoli.querySelectorAll('div[data-titolo]'));

        const normalizza = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

        filtroTitoli.addEventListener('input', () => {
            const query = normalizza(filtroTitoli.value.trim());

            righe.forEach(riga => {
                const corrisponde = !query || normalizza(riga.dataset.titolo).includes(query);
                riga.style.display = corrisponde ? 'flex' : 'none';
            });
        });
    }

    const abilitaRigheDinamiche = (container, nomeCampo) => {
        if (!container) return;
        const esempio = (container.querySelector('input') || {}).placeholder || '';

        const aggiungiRiga = () => {
            const input = document.createElement('input');
            input.type = 'text';
            input.name = nomeCampo;
            input.placeholder = esempio;
            container.appendChild(input);
            input.addEventListener('input', gestisciRighe);
        };

        const rimuoviRigheVuote = () => {
            const righe = container.querySelectorAll('input');
            for (let i = righe.length - 1; i > 0; i--) {
                if (!righe[i].value.trim()) righe[i].remove();
            }
        };

        const gestisciRighe = () => {
            rimuoviRigheVuote();
            const righe = container.querySelectorAll('input');
            const ultima = righe[righe.length - 1];
            if (ultima && ultima.value.trim()) aggiungiRiga();
        };

        container.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', gestisciRighe);
        });
    };

    abilitaRigheDinamiche(document.getElementById('lingue-container'), 'lingue');
    abilitaRigheDinamiche(document.getElementById('patente-container'), 'patente');
    abilitaRigheDinamiche(document.getElementById('hobby-container'), 'hobby');
});