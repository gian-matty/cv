import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GEOAPIFY_KEY = os.getenv('GEOAPIFY_API_KEY')

TITOLI_STUDIO = [
    # --- Scuola dell'Obbligo e Qualifiche Professionali ---
    "Licenza Media / Scuola Secondaria di Primo Grado",
    "Qualifica Professionale triennale (IeFP)",
    "Diploma di Tecnico Professionale (IeFP - 4 anni)",

    # --- Diplomi di Scuola Secondaria Superiore (Licei) ---
    "Diploma Liceo Scientifico",
    "Diploma Liceo Scientifico - Opzione Scienze Applicate",
    "Diploma Liceo Scientifico - Sezione ad Indirizzo Sportivo",
    "Diploma Liceo Classico",
    "Diploma Liceo delle Scienze Umane",
    "Diploma Liceo delle Scienze Umane - Opzione Economico-Sociale",
    "Diploma Liceo Linguistico",
    "Diploma Liceo Artistico",
    "Diploma Liceo Musicale e Coreutico",

    # --- Diplomi di Scuola Secondaria Superiore (Istituti Tecnici) ---
    "Diploma Istituto Tecnico - Amministrazione, Finanza e Marketing (AFM)",
    "Diploma Istituto Tecnico - Relazioni Internazionali per il Marketing (RIM)",
    "Diploma Istituto Tecnico - Sistemi Informativi Aziendali (SIA)",
    "Diploma Istituto Tecnico - Turismo",
    "Diploma Istituto Tecnico - Meccanica, Meccatronica ed Energia",
    "Diploma Istituto Tecnico - Trasporti e Logistica",
    "Diploma Istituto Tecnico - Elettronica ed Elettrotecnica",
    "Diploma Istituto Tecnico - Informatica e Telecomunicazioni",
    "Diploma Istituto Tecnico - Grafica e Comunicazione",
    "Diploma Istituto Tecnico - Chimica, Materiali e Biotecnologie",
    "Diploma Istituto Tecnico - Sistema Moda",
    "Diploma Istituto Tecnico - Agraria, Agroalimentare e Agroindustria",
    "Diploma Istituto Tecnico - Costruzioni, Ambiente e Territorio (Geometra)",

    # --- Formazione Terziaria Non Universitaria ---
    "Diploma ITS (Istituto Tecnico Superiore - Formazione Terziaria)",
    "Diploma AFAM (Alta Formazione Artistica, Musicale e Coreutica)",

    # --- Lauree Triennali (L-1 a L-43) ---
    "Laurea Triennale in Architettura / Scienze dell'Architettura (L-17)",
    "Laurea Triennale in Beni Culturali (L-1)",
    "Laurea Triennale in Biotecnologie (L-2)",
    "Laurea Triennale in Design (L-4)",
    "Laurea Triennale in Discipline delle Arti, della Musica e dello Spettacolo - DAMS (L-3)",
    "Laurea Triennale in Filosofia (L-5)",
    "Laurea Triennale in Fisica (L-30)",
    "Laurea Triennale in Geografia (L-6)",
    "Laurea Triennale in Giurisprudenza / Scienze dei Servizi Giuridici (L-14)",
    "Laurea Triennale in Informatica / Scienze e Tecnologie Informatiche (L-31)",
    "Laurea Triennale in Ingegneria Civile e Ambientale (L-7)",
    "Laurea Triennale in Ingegneria dell'Informazione (L-8)",
    "Laurea Triennale in Ingegneria Industriale (L-9)",
    "Laurea Triennale in Lettere / Lettere e Filosofia (L-10)",
    "Laurea Triennale in Lingue e Culture Moderne (L-11)",
    "Laurea Triennale in Matematica (L-35)",
    "Laurea Triennale in Mediazione Linguistica (L-12)",
    "Laurea Triennale in Psicologia / Scienze e Tecniche Psicologiche (L-24)",
    "Laurea Triennale in Scienza della Nutrizione / Scienze della Nutrizione (L-26)",
    "Laurea Triennale in Scienze Biologiche (L-13)",
    "Laurea Triennale in Scienze Chimiche (L-27)",
    "Laurea Triennale in Scienze della Comunicazione (L-20)",
    "Laurea Triennale in Scienze dell'Economia e della Gestione Aziendale (L-18)",
    "Laurea Triennale in Scienze delle Attività Motorie e Sportive (L-22)",
    "Laurea Triennale in Scienze dell'Educazione e della Formazione (L-19)",
    "Laurea Triennale in Scienze e Tecnologie Agrarie e Forestali (L-25)",
    "Laurea Triennale in Scienze e Tecnologie Alimentari (L-26)",
    "Laurea Triennale in Scienze e Tecnologie Farmaceutiche (L-29)",
    "Laurea Triennale in Scienze e Tecnologie per l'Ambiente e la Natura (L-32)",
    "Laurea Triennale in Scienze Economiche (L-33)",
    "Laurea Triennale in Scienze Geologiche (L-34)",
    "Laurea Triennale in Scienze Politiche e delle Relazioni Internazionali (L-36)",
    "Laurea Triennale in Scienze Sociali / Servizio Sociale (L-39)",
    "Laurea Triennale in Scienze Statistiche (L-41)",
    "Laurea Triennale in Scienza della Formazione Primaria",
    "Laurea Triennale nelle Professioni Sanitarie - Infermieristica (L/SNT1)",
    "Laurea Triennale nelle Professioni Sanitarie - Ostetricia (L/SNT1)",
    "Laurea Triennale nelle Professioni Sanitarie - Fisioterapia (L/SNT2)",
    "Laurea Triennale nelle Professioni Sanitarie - Logopedia (L/SNT2)",
    "Laurea Triennale nelle Professioni Sanitarie - Radiologia / Tecniche di Radiologia (L/SNT3)",
    "Laurea Triennale nelle Professioni Sanitarie - Igiene Dentale (L/SNT3)",
    "Laurea Triennale nelle Professioni Sanitarie - Tecniche di Laboratorio (L/SNT3)",
    "Laurea Triennale nelle Professioni Sanitarie - Prevenzione nell'Ambiente e nei Luoghi di Lavoro (L/SNT4)",

    # --- Lauree Magistrali a Ciclo Unico ---
    "Laurea Magistrale a Ciclo Unico in Architettura e Ingegneria Edile-Architettura (LM-4 c.u.)",
    "Laurea Magistrale a Ciclo Unico in Chimica e Tecnologia Farmaceutiche - CTF (LM-13 c.u.)",
    "Laurea Magistrale a Ciclo Unico in Farmacia (LM-13 c.u.)",
    "Laurea Magistrale a Ciclo Unico in Giurisprudenza (LMG/01)",
    "Laurea Magistrale a Ciclo Unico in Medicina e Chirurgia (LM-41)",
    "Laurea Magistrale a Ciclo Unico in Odontoiatria e Protesi Dentaria (LM-46)",
    "Laurea Magistrale a Ciclo Unico in Medicina Veterinaria (LM-42)",
    "Laurea Magistrale a Ciclo Unico in Conservazione e Restauro dei Beni Culturali (LMR/02)",

    # --- Lauree Magistrali / Specialistiche (2 anni) ---
    "Laurea Magistrale in Antropologia ed Etnologia (LM-1)",
    "Laurea Magistrale in Archeologia (LM-2)",
    "Laurea Magistrale in Biologia (LM-6)",
    "Laurea Magistrale in Biotecnologie Mediche, Veterinarie e Farmaceutiche (LM-9)",
    "Laurea Magistrale in Data Science e Gestione dell'Informazione (LM-91)",
    "Laurea Magistrale in Economia e Management / Scienze Economico-Aziendali (LM-77)",
    "Laurea Magistrale in Finance / Finanza (LM-16)",
    "Laurea Magistrale in Fisica e Astrofisica (LM-17)",
    "Laurea Magistrale in Informatica (LM-18)",
    "Laurea Magistrale in Ingegneria Aerospaziale e Astronautica (LM-20)",
    "Laurea Magistrale in Ingegneria Biomedica (LM-21)",
    "Laurea Magistrale in Ingegneria Chimica (LM-22)",
    "Laurea Magistrale in Ingegneria Civile (LM-23)",
    "Laurea Magistrale in Ingegneria dei Materiali (LM-53)",
    "Laurea Magistrale in Ingegneria delle Telecomunicazioni (LM-27)",
    "Laurea Magistrale in Ingegneria Elettrica (LM-28)",
    "Laurea Magistrale in Ingegneria Elettronica (LM-29)",
    "Laurea Magistrale in Ingegneria Gestionale (LM-31)",
    "Laurea Magistrale in Ingegneria Informatica (LM-32)",
    "Laurea Magistrale in Ingegneria Meccanica (LM-33)",
    "Laurea Magistrale in Ingegneria Meccatronica (LM-33)",
    "Laurea Magistrale in Ingegneria Navale (LM-34)",
    "Laurea Magistrale in Ingegneria Nucleare (LM-36)",
    "Laurea Magistrale in Intelligenza Artificiale / AI & Robotics (LM-18 / LM-32)",
    "Laurea Magistrale in Lingue e Letterature Moderne (LM-37)",
    "Laurea Magistrale in Matematica (LM-40)",
    "Laurea Magistrale in Psicologia (LM-51)",
    "Laurea Magistrale in Relazioni Internazionali (LM-52)",
    "Laurea Magistrale in Scienze Chimiche (LM-54)",
    "Laurea Magistrale in Scienze della Formazione Continua (LM-57)",
    "Laurea Magistrale in Scienze della Comunicazione Pubblica, d'Impresa e Pubblicità (LM-59)",
    "Laurea Magistrale in Scienze delle Pubbliche Amministrazioni (LM-63)",
    "Laurea Magistrale in Scienze Economiche (LM-56)",
    "Laurea Magistrale in Scienze Filosofiche (LM-78)",
    "Laurea Magistrale in Scienze Storiche (LM-84)",
    "Laurea Magistrale in Scienze Politiche (LM-62)",
    "Laurea Magistrale in Sicurezza Informatica / Cybersecurity (LM-66)",
    "Laurea Magistrale in Traduzione Specialistica ed Interpretariato (LM-94)",

    # --- Post-Laurea e Alta Formazione ---
    "Master Universitario di Primo Livello",
    "Master Universitario di Secondo Livello",
    "Scuola di Specializzazione (Area Medica / Legale / Beni Culturali)",
    "Dottorato di Ricerca (Ph.D.)",

    # --- Opzione Personalizzata ---
    "Altro"
]


@app.route('/')
def home():
    return render_template('form.html', geoapify_key=GEOAPIFY_KEY, titoli_studio=TITOLI_STUDIO)

@app.route('/genera_cv', methods=['POST'])
def genera_cv():
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
        'titolo_studio': titoli_selezionati,
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
    
    # Se un campo richiesto o la lista dei titoli è vuota, torna alla home
    if not titoli_selezionati or any(v == '' for k, v in dati_cv.items() if k != 'titolo_studio'):
        return redirect(url_for('home'))

    return render_template('cv.html', dati=dati_cv)

if __name__ == '__main__':
    app.run(debug=True)