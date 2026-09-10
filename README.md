# CV Creator

Generatore di curriculum vitae basato su Flask: compili un form unico e scegli tra 5 template premium per ottenere un CV pronto da stampare o esportare.

---

## Funzionalità

- **5 template** di CV (Aurora, Editorial, Executive, Creative, Minimal) con stile coerente
- **Autocompletamento città** tramite API Geoapify (gratuita) con **CAP precompilato automaticamente** dalla città selezionata (modificabile)
- **Foto profilo** con drag & drop (max 5 MB, salvata in base64 direttamente nel CV)
- **Ricerca dei titoli di studio** (elenco lungo con filtro live)
- **Tema chiaro/scuro**
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

## Struttura del progetto

```
curriculum/
├── app.py                  # Applicazione Flask, route e validazione
├── requirements.txt        # Dipendenze
├── .env                    # Chiave API Geoapify (non committare mai)
├── templates/
│   ├── form.html           # Form di compilazione
│   └── cv.html             # Rendering dei 5 template CV
└── static/
    ├── style.css           # Stili, tema chiaro/scuro e responsive
    └── script.js           # Autocomplete città, foto, lingue, formattazione
```

## Note

- La foto profilo viene incorporata come **data URI base64**: non supera i 5 MB e il CV resta un singolo documento HTML.
- Il file `.env` e la cartella `venv/` sono esclusi da git (vedi `.gitignore`).
- I campi obbligatori sono validati sia dal browser sia lato server (`campi_obbligatori` in `app.py`).

---

# CV Creator

A Flask-based curriculum vitae generator: fill in a single form and pick one of 5 premium templates to get a CV ready to print or export.

---

## Features

- **5 CV templates** (Aurora, Editorial, Executive, Creative, Minimal) with a consistent style
- **City autocomplete** via the Geoapify API (free) with **CAP/postal code auto-filled** from the selected city (editable)
- **Profile photo** with drag & drop (max 5 MB, embedded as base64 directly in the CV)
- **Dynamic languages**: a new field appears once all the previous ones are filled in
- **Study title search** (long list with live filtering)
- **Automatic mobile phone formatting** (3-3-4 digits)
- **Light/dark theme**
- Responsive design (mobile, tablet, desktop) with print support

## Requirements

- Python 3.8+
- A free [Geoapify](https://www.geoapify.com) API key (no paid subscription needed)

## Installation

1. Clone or download the project and move into the folder:

```bash
cd curriculum
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project folder and paste your key:

```
GEOAPIFY_API_KEY=YOUR_KEY
```

> You can get a free key from the official site by creating a new project; no paid subscription is required.

5. Run the app:

```bash
python app.py
```

6. Open your browser at: <http://127.0.0.1:5000>

## Project structure

```
curriculum/
├── app.py                  # Flask application, routes and validation
├── requirements.txt        # Dependencies
├── .env                    # Geoapify API key (never commit this)
├── templates/
│   ├── form.html           # Submission form
│   └── cv.html             # Rendering of the 5 CV templates
└── static/
    ├── style.css           # Styles, light/dark theme and responsive
    └── script.js           # City autocomplete, photo, languages, formatting
```

## Notes

- The profile photo is embedded as a **base64 data URI**: it is limited to 5 MB and the CV stays a single HTML document.
- The `.env` file and the `venv/` folder are excluded from git (see `.gitignore`).
- Required fields are validated both in the browser and on the server side (`campi_obbligatori` in `app.py`).