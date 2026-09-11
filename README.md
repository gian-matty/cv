# Cursus

Generatore di curriculum vitae basato su Flask: compili un form unico e scegli tra 5 template per ottenere un CV pronto da stampare o esportare.

---

## Funzionalità

- **Landing pubblica** con hero section, login e registrazione (autenticazione demo in memoria, nessun database)
- **Area personale** con dashboard dei tuoi curriculum
- **5 template** di CV (Aurora, Editorial, Executive, Creative, Minimal) con stile coerente
- **Autocompletamento città** tramite API Geoapify (gratuita) con **CAP precompilato automaticamente** dalla città selezionata
- **Foto profilo** con drag & drop (max 5 MB, salvata in base64 direttamente nel CV)
- **Ricerca dei titoli di studio** (elenco lungo con filtro live)
- **Tema chiaro/scuro** e navbar sticky con effetto liquid glass
- Design responsive (mobile, tablet, desktop) con supporto stampa

## Requisiti

- Python 3.8+
- Una chiave API gratuita di [Geoapify](https://www.geoapify.com) (nessun abbonamento richiesto)

## Installazione

1. Clona o scarica il progetto e spostati nella cartella:

```bash
cd curriculum
```

2. Crea e attiva un ambiente virtuale:

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

4. Crea il file `.env` nella cartella del progetto e incolla la tua chiave:

```
GEOAPIFY_API_KEY=LA_TUA_CHIAVE
```

> La chiave si ottiene gratis dal sito ufficiale creando un nuovo progetto; non serve alcun abbonamento a pagamento.

5. Avvia l'app:

```bash
python app.py
```

6. Apri nel browser: <http://127.0.0.1:5000>

Account demo: `demo@cursus.it` / `demo123`.

## Struttura del progetto

```
curriculum/
├── app.py                  # Applicazione Flask: route, auth demo, validazione
├── requirements.txt        # Dipendenze
├── .env                    # Chiave API Geoapify (non committare mai)
├── templates/
│   ├── landing.html        # Landing pubblica con hero
│   ├── login.html          # Accesso
│   ├── register.html       # Registrazione
│   ├── dashboard.html      # Area personale
│   ├── form.html           # Form di compilazione CV
│   ├── cv.html             # Rendering dei 5 template CV
│   ├── _nav.html           # Navbar sticky condivisa
│   └── _macros.html        # Macro condivise (head, ecc.)
└── static/
    ├── style.css           # Stili, tema chiaro/scuro, glass e responsive
    └── script.js           # Autocomplete città, foto, lingue, formattazione
```

## Note

- I CV e gli utenti sono salvati **in memoria**: si azzerano al riavvio dell'app. È un prototipo, nessun database.
- La foto profilo viene incorporata come **data URI base64**: non supera i 5 MB e il CV resta un singolo documento HTML.
- I campi obbligatori sono validati sia dal browser sia lato server (`campi_obbligatori` in `app.py`).

---