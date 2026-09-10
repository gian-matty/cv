import os
import base64
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GEOAPIFY_KEY = os.getenv('GEOAPIFY_API_KEY')

TITOLI_STUDIO = {
    "Scuola dell'Obbligo e Diplomi": [
        "Licenza Media / Scuola Secondaria di Primo Grado",
        "Diploma Liceo Scientifico / Classico / Linguistico",
        "Diploma Istituto Tecnico (Informatica / Economia / Meccanica)",
        "Diploma Istituto Professionale / Qualifica IeFP",
        "Diploma ITS (Istituto Tecnico Superiore)"
    ],
    "Area Tecnico-Scientifica e Ingegneria": [
        "Laurea in Informatica / Ingegneria Informatica",
        "Laurea in Ingegneria (Industriale / Civile / Gestionale)",
        "Laurea in Biologia / Biotecnologie / Chimica",
        "Laurea in Matematica / Fisica / Data Science",
        "Laurea in Scienze Agrarie / Alimentari"
    ],
    "Area Economico-Giuridica e Sociale": [
        "Laurea in Economia / Economia Aziendale / Management",
        "Laurea in Giurisprudenza",
        "Laurea in Scienze Politiche / Relazioni Internazionali",
        "Laurea in Psicologia",
        "Laurea in Scienze della Comunicazione / Digital Marketing"
    ],
    "Area Medico-Sanitaria e Formazione": [
        "Laurea in Medicina e Chirurgia",
        "Laurea nelle Professioni Sanitarie (Infermieristica, Fisioterapia, ecc.)",
        "Laurea in Scienze dell'Educazione / Formazione Primaria"
    ],
    "Area Umanistica, Artistica e Design": [
        "Laurea in Architettura / Design",
        "Laurea in Lettere / Filosofia / Storia",
        "Laurea in Lingue e Culture Moderne"
    ],
    "Post-Laurea e Altro": [
        "Master Universitario di Primo Livello",
        "Master Universitario di Secondo Livello",
        "Dottorato di Ricerca (Ph.D.)",
        "Altro"
    ]
}

@app.route('/')
def home():
    return render_template('form.html', geoapify_key=GEOAPIFY_KEY, titoli_studio=TITOLI_STUDIO)

@app.route('/genera_cv', methods=['POST'])
def genera_cv():
    # Gestione Upload Foto in Base64
    foto_b64 = None
    if 'foto' in request.files:
        file = request.files['foto']
        if file and file.filename != '':
            foto_bytes = file.read()
            foto_b64 = base64.b64encode(foto_bytes).decode('utf-8')

    # Gestione 'Altro' per il titolo professionale
    titolo = request.form.get('titolo_professionale', '').strip()
    if titolo == 'Altro':
        titolo = request.form.get('titolo_altro', '').strip()

    # Gestione titoli di studio multipli
    titoli_selezionati = request.form.getlist('titolo_studio')
    if 'Altro' in titoli_selezionati:
        titoli_selezionati.remove('Altro')
        altro_titolo = request.form.get('titolo_studio_altro', '').strip()
        if altro_titolo:
            titoli_selezionati.append(altro_titolo)

    return render_template(
        'cv.html',
        foto_b64=foto_b64,
        nome=request.form.get('nome', '').strip(),
        cognome=request.form.get('cognome', '').strip(),
        codice_fiscale=request.form.get('codice_fiscale', '').strip(),
        data_nascita=request.form.get('data_nascita', '').strip(),
        sesso=request.form.get('sesso', '').strip(),
        email=request.form.get('email', '').strip(),
        prefisso=request.form.get('prefisso', '').strip(),
        telefono=request.form.get('telefono', '').strip(),
        citta=request.form.get('citta', '').strip(),
        linkedin=request.form.get('linkedin', '').strip(),
        github=request.form.get('github', '').strip(),
        instagram=request.form.get('instagram', '').strip(),
        facebook=request.form.get('facebook', '').strip(),
        titolo_professionale=titolo,
        descrizione=request.form.get('descrizione', '').strip(),
        titoli_selezionati=titoli_selezionati,
        anno_diploma=request.form.get('anno_diploma', '').strip(),
        ultimo_ruolo=request.form.get('ultimo_ruolo', '').strip(),
        azienda=request.form.get('azienda', '').strip(),
        periodo_lavoro=request.form.get('periodo_lavoro', '').strip(),
        descrizione_lavoro=request.form.get('descrizione_lavoro', '').strip(),
        competenze_tecniche=request.form.get('competenze_tecniche', '').strip(),
        lingue=request.form.get('lingue', '').strip(),
        patenti=request.form.get('patenti', '').strip(),
        certificazioni=request.form.get('certificazioni', '').strip(),
        hobby=request.form.get('hobby', '').strip()
    )

if __name__ == '__main__':
    app.run(debug=True)