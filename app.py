import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GEOAPIFY_KEY = os.getenv('GEOAPIFY_API_KEY')

@app.route('/')
def home():
    return render_template('form.html', geoapify_key=GEOAPIFY_KEY)

@app.route('/genera_cv', methods=['POST'])
def genera_cv():
    # Gestione 'Altro' per il titolo professionale
    titolo = request.form.get('titolo_professionale', '').strip()
    if titolo == 'Altro':
        titolo = request.form.get('titolo_altro', '').strip()

    dati_cv = {
        # --- Dati Anagrafici e Contatti ---
        'nome': request.form.get('nome', '').strip(),
        'cognome': request.form.get('cognome', '').strip(),
        'email': request.form.get('email', '').strip(),
        'prefisso': request.form.get('prefisso', '').strip(),
        'telefono': request.form.get('telefono', '').strip(),
        'citta': request.form.get('citta', '').strip(),

        # --- Profilo Personale ---
        'titolo_professionale': titolo,
        'descrizione': request.form.get('descrizione', '').strip(),

        # --- Istruzione e Formazione ---
        'titolo_studio': request.form.get('titolo_studio', '').strip(),
        'anno_diploma': request.form.get('anno_diploma', '').strip(),

        # --- Esperienze Lavorative ---
        'ultimo_ruolo': request.form.get('ultimo_ruolo', '').strip(),
        'azienda': request.form.get('azienda', '').strip(),
        'periodo_lavoro': request.form.get('periodo_lavoro', '').strip(),
        'descrizione_lavoro': request.form.get('descrizione_lavoro', '').strip(),

        # --- Competenze e Lingue ---
        'competenze_tecniche': request.form.get('competenze_tecniche', '').strip(), 
        'lingue': request.form.get('lingue', '').strip(),
        'hobby': request.form.get('hobby', '').strip()
    }
    
    # Se anche un solo valore è vuoto, ricarica la home
    if any(valore == '' for valore in dati_cv.values()):
        return redirect(url_for('home'))

    return render_template('cv.html', dati=dati_cv)

if __name__ == '__main__':
    app.run(debug=True)