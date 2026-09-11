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

    const footerTop = document.getElementById('footer-top');
    if (footerTop) {
        footerTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
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
    const MAX_DIM = 900;
    const QUALITA_JPEG = 0.82;

    const mostraErroreFoto = (msg) => {
        if (!uploadError) return;
        if (msg) {
            uploadError.textContent = msg;
            uploadError.hidden = false;
        } else {
            uploadError.hidden = true;
        }
    };

    const sostituisciFile = (file) => {
        if (!window.DataTransfer) return;
        const dt = new DataTransfer();
        dt.items.add(file);
        imageInput.files = dt.files;
    };

    const mostraAnteprima = (blob) => {
        if (!blob) {
            imagePreview.hidden = true;
            imagePreviewImg.removeAttribute('src');
            return;
        }
        imagePreviewImg.src = URL.createObjectURL(blob);
        imagePreview.hidden = false;
    };

    const elaboraFotoHq = async (file) => {
        mostraErroreFoto(null);
        if (!file) {
            if (imageInput) imageInput.value = '';
            mostraAnteprima(null);
            return;
        }
        if (!file.type.startsWith('image/')) {
            if (imageInput) imageInput.value = '';
            mostraErroreFoto('Formato non supportato: carica un\'immagine (JPG, PNG, WebP).');
            return;
        }
        if (file.size > MAX_FOTO) {
            if (imageInput) imageInput.value = '';
            mostraErroreFoto('File troppo grande: massimo 5 MB.');
            return;
        }
        try {
            const bitmap = await createImageBitmap(file);
            const scala = Math.min(1, MAX_DIM / Math.max(bitmap.width, bitmap.height));
            const larghezza = Math.max(1, Math.round(bitmap.width * scala));
            const altezza = Math.max(1, Math.round(bitmap.height * scala));
            const canvas = document.createElement('canvas');
            canvas.width = larghezza;
            canvas.height = altezza;
            canvas.getContext('2d').drawImage(bitmap, 0, 0, larghezza, altezza);
            bitmap.close();
            canvas.toBlob((blob) => {
                if (!blob) {
                    mostraErroreFoto('Impossibile elaborare l\'immagine: riprova.');
                    return;
                }
                const nome = file.name.replace(/\.[^.]+$/, '') + '.jpg';
                const compresso = new File([blob], nome, { type: 'image/jpeg', lastModified: Date.now() });
                if (imageInput) sostituisciFile(compresso);
                mostraAnteprima(blob);
            }, 'image/jpeg', QUALITA_JPEG);
        } catch (error) {
            console.error('Impossibile decodificare l\'immagine:', error);
            if (imageInput) imageInput.value = '';
            mostraErroreFoto('Formato non supportato: carica un\'immagine (JPG, PNG, WebP).');
        }
    };

    if (imageInput && imagePreview && imagePreviewImg) {
        imageInput.addEventListener('change', () => {
            elaboraFotoHq(imageInput.files[0]);
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
            elaboraFotoHq(file);
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
            const on = selectTitolo.value === 'Altro';
            boxAltro.classList.toggle('is-open', on);
            inputAltro.required = on;
            if (!on) inputAltro.value = '';
        });
    }

    const checkboxes = document.querySelectorAll('input[name="titolo_studio"]');
    const boxAltroTitolo = document.getElementById('box_altro_titolo');
    const inputAltroTitolo = document.getElementById('titolo_studio_altro');

    checkboxes.forEach(cb => {
        if (cb.value === 'Altro') {
            cb.addEventListener('change', () => {
                const on = cb.checked;
                boxAltroTitolo.classList.toggle('is-open', on);
                inputAltroTitolo.required = on;
                if (!on) inputAltroTitolo.value = '';
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

    const form = document.querySelector('form');
    if (form) {
        let primoInvalido = null;
        let timerScroll;
        form.addEventListener('invalid', (e) => {
            if (!primoInvalido) primoInvalido = e.target;
            clearTimeout(timerScroll);
            timerScroll = setTimeout(() => {
                if (primoInvalido && !form.checkValidity()) {
                    primoInvalido.scrollIntoView({ block: 'center' });
                    try { primoInvalido.focus({ preventScroll: true }); } catch (err) { primoInvalido.focus(); }
                }
                primoInvalido = null;
            }, 60);
        }, true);
        form.addEventListener('submit', () => { primoInvalido = null; });
    }

    const track = document.getElementById('browser-track');
    const browserKey = document.getElementById('browser-key');
    const tabs = document.querySelectorAll('.btab[data-tpl]');
    const browser = document.getElementById('hero-browser');

    if (track && tabs.length) {
        const riduci = matchMedia('(prefers-reduced-motion: reduce)').matches;
        let timer = null;
        let idx = 0;

        const switchTo = (i) => {
            tabs.forEach((t, n) => {
                const attivo = n === i;
                t.classList.toggle('is-active', attivo);
                t.setAttribute('aria-selected', attivo ? 'true' : 'false');
            });
            track.style.transform = `translateX(-${i * 20}%)`;
            if (browserKey) browserKey.textContent = tabs[i].dataset.tpl;
            idx = i;
        };

        const startAutoplay = () => {
            clearInterval(timer);
            timer = setInterval(() => switchTo((idx + 1) % tabs.length), 6000);
        };

        tabs.forEach(tab => tab.addEventListener('click', () => {
            switchTo([...tabs].indexOf(tab));
            if (!riduci) startAutoplay();
        }));

        if (browser) {
            browser.addEventListener('mouseenter', () => clearInterval(timer));
            browser.addEventListener('mouseleave', () => { if (!riduci) startAutoplay(); });
            browser.addEventListener('focusin', () => clearInterval(timer));
            browser.addEventListener('focusout', () => { if (!riduci) startAutoplay(); });
        }

        if (!riduci) startAutoplay();
    }
});