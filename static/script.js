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

    const scena3d = document.getElementById('hero3d-scene');
    const traccia3d = document.getElementById('hero3d');

    if (scena3d && traccia3d) {
        const almenoTouch = matchMedia('(pointer: coarse)').matches;
        const riduci = matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (almenoTouch || riduci) {
            scena3d.style.setProperty('--advance', '-60px');
            scena3d.style.setProperty('--tilt-x', '8deg');
            scena3d.style.setProperty('--tilt-y', '-4deg');
        } else {
            let progresso = 0;
            let obiettivo = 0;
            let raf = null;

            const aggiorna = () => {
                const avanzamento = traccia3d.offsetHeight - window.innerHeight;
                const p = Math.min(1, Math.max(0, (window.scrollY - traccia3d.offsetTop) / (avanzamento || 1)));
                obiettivo = p;

                progresso += (obiettivo - progresso) * 0.09;
                if (Math.abs(obiettivo - progresso) > 0.0005) {
                    scena3d.style.setProperty('--advance', `${-420 + progresso * 1120}px`);
                    scena3d.style.setProperty('--tilt-x', `${14 - progresso * 17}deg`);
                    scena3d.style.setProperty('--tilt-y', `${-6 + progresso * 4}deg`);
                    raf = requestAnimationFrame(aggiorna);
                } else {
                    raf = null;
                }
            };

            const suScroll = () => {
                if (raf === null) raf = requestAnimationFrame(aggiorna);
            };

            window.addEventListener('scroll', suScroll, { passive: true });
            suScroll();
        }
    }

    const anteprimaDialog = document.getElementById('anteprima-dialog');
    const anteprimaFrame = document.getElementById('anteprima-frame');

    if (anteprimaDialog && anteprimaFrame) {
        const anteprimaNome = document.getElementById('anteprima-nome');
        const chiudiAnteprima = () => {
            if (anteprimaDialog.open) anteprimaDialog.close();
        };

        document.querySelectorAll('.hero3d-card').forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                anteprimaFrame.src = card.getAttribute('href');
                if (anteprimaNome) anteprimaNome.textContent = card.dataset.nome || '';
                anteprimaDialog.showModal();
            });
        });

        const stampaAnteprima = () => {
            if (anteprimaFrame.contentWindow) anteprimaFrame.contentWindow.print();
        };

        const chiudiBtn = document.getElementById('anteprima-chiudi');
        if (chiudiBtn) chiudiBtn.addEventListener('click', chiudiAnteprima);

        anteprimaDialog.addEventListener('click', (e) => {
            if (e.target === anteprimaDialog) chiudiAnteprima();
        });

        anteprimaDialog.addEventListener('close', () => {
            anteprimaFrame.src = 'about:blank';
        });

        const pdfBtn = document.getElementById('anteprima-pdf');
        if (pdfBtn) pdfBtn.addEventListener('click', stampaAnteprima);

        const stampaBtn = document.getElementById('anteprima-stampa');
        if (stampaBtn) stampaBtn.addEventListener('click', stampaAnteprima);
    }
});