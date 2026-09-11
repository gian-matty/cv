import base64
import os
from datetime import date
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, abort, session
from flask_babel import Babel, gettext
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.secret_key = os.getenv('SECRET_KEY', 'cursus-demo-secret')
GEOAPIFY_KEY = os.getenv('GEOAPIFY_API_KEY')
SITE_NAME = 'Cursus'

LANGUAGES = ['it', 'en', 'fr', 'de', 'es']
LANGUAGE_NAMES = {
    'it': 'Italiano',
    'en': 'English',
    'fr': 'Français',
    'de': 'Deutsch',
    'es': 'Español',
}

app.config['BABEL_DEFAULT_LOCALE'] = 'it'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'locale'


def seleziona_locale():
    return session.get('lang', 'it')


babel = Babel(app, locale_selector=seleziona_locale)

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
    "Laurea Magistrale in Statistica (LM-82)",
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

TEMPLATE_OPTIONS = {
    'aurora': 'Aurora',
    'editorial': 'Editorial',
    'executive': 'Executive',
    'creative': 'Creative',
    'minimal': 'Minimal'
}


MOCK_CVS = [
    {
        'id': 1,
        'nome': 'Giulia', 'cognome': 'Rossi',
        'email': 'giulia.rossi@example.it', 'prefisso': '+39', 'telefono': '3331234567',
        'citta': 'Milano', 'cap': '20121', 'indirizzo': 'Via Dante 12',
        'data_nascita': '1998-05-14', 'luogo_nascita': 'Torino, Italia', 'nazionalita': 'Italiana',
        'codice_fiscale': 'RSSGLI98M54L219P',
        'linkedin': 'https://linkedin.com/in/giuliarossi', 'portfolio': 'https://giuliarossi.dev', 'github': 'https://github.com/giuliarossi',
        'titolo_professionale': 'Web Developer (Front-end / Back-end / Full-stack)',
        'descrizione': 'Web developer con 4 anni di esperienza in progetti web, specializzata in interfacce moderne, accessibili e ad alte prestazioni.',
        'obiettivo_professionale': 'Entrare in un team di prodotto per costruire esperienze digitali di qualità e crescere come sviluppatrice senior.',
        'anni_esperienza': '4', 'contratto_desiderato': 'Tempo indeterminato', 'disponibilita_immediata': 'Dopo preavviso',
        'titolo_studio': ['Diploma Istituto Tecnico - Informatica e Telecomunicazioni'],
        'anno_diploma': '2020', 'istituto_formazione': 'ITIS C. Zuccante, Venezia', 'voto_formazione': '92/100', 'tesi_titolo': '',
        'corsi_certificazioni': 'React e TypeScript (Corso online) · AWS Cloud Practitioner',
        'ultimo_ruolo': 'Front-end Developer', 'azienda': 'StudioNova', 'periodo_lavoro': '2022 - Presente', 'settore_lavoro': 'IT',
        'descrizione_lavoro': 'Sviluppo di applicazioni React/TypeScript per clienti enterprise, collaborando con i team di design e prodotto.',
        'risultati_raggiunti': 'Riduzione del 35% dei tempi di caricamento delle pagine principali.',
        'esperienze_precedenti': 'Junior Developer, WebAgency Roma (2021-2022): sviluppo di siti vetrina e piccole web app.',
        'progetti': 'Dashdo, app open source di gestione spese in React',
        'volontariato': 'Volontaria di programmazione per l\'associazione CodingForGood (2021-oggi)',
        'competenze_tecniche': 'JavaScript, TypeScript, React, Node.js, SQL',
        'competenze_trasversali': 'Team working, problem solving, comunicazione, autonomia',
        'strumenti_software': 'Git, GitHub, Figma, VS Code, Docker',
        'lingue': 'Italiano C2, Inglese B1',
        'patente': 'B', 'hobby': 'fotografia, trekking, cucina',
        'referenze': 'Silvia Neri - Head of Product @ StudioNova, +39 333 000 0000',
        'foto_profilo': 'https://randomuser.me/api/portraits/women/44.jpg', 'template_cv': 'aurora', 'modificato': '2026-09-08',
    },
    {
        'id': 2,
        'nome': 'Marco', 'cognome': 'Bianchi',
        'email': 'marco.bianchi@example.it', 'prefisso': '+39', 'telefono': '3279876543',
        'citta': 'Bologna', 'cap': '40121', 'indirizzo': 'Via Rizzoli 21',
        'data_nascita': '1996-02-20', 'luogo_nascita': 'Bologna, Italia', 'nazionalita': 'Italiana',
        'codice_fiscale': 'BNCMRC96B20A944H',
        'linkedin': 'https://linkedin.com/in/marcobianchi', 'portfolio': 'https://marcobianchi.it', 'github': 'https://github.com/marcobianchi',
        'titolo_professionale': 'Data Analyst / Data Scientist',
        'descrizione': 'Analista dati con esperienza in modellazione statistica e business intelligence per il settore retail e finanziario.',
        'obiettivo_professionale': 'Una posizione in cui mettere a frutto le capacità analitiche e contribuire alle decisioni basate sui dati.',
        'anni_esperienza': '6', 'contratto_desiderato': 'Tempo determinato', 'disponibilita_immediata': 'Immediata',
        'titolo_studio': ['Laurea Magistrale in Statistica (LM-82)', 'Laurea Triennale in Matematica (L-35)'],
        'anno_diploma': '2021', 'istituto_formazione': 'Università di Bologna', 'voto_formazione': '110/110 e lode', 'tesi_titolo': 'Modelli predittivi per la customer retention',
        'corsi_certificazioni': 'Google Data Analytics · Certificazione Tableau Desktop Specialist',
        'ultimo_ruolo': 'Data Analyst', 'azienda': 'DataCorp Italia', 'periodo_lavoro': '2023 - Presente', 'settore_lavoro': 'Consulenza IT',
        'descrizione_lavoro': 'Dashboard e analisi predittive per clienti retail; gestione pipeline ETL con SQL e Python.',
        'risultati_raggiunti': 'Aumento del 18% del margine su una linea prodotto grazie alle segnalazioni automatiche.',
        'esperienze_precedenti': 'Business Analyst, GDO Partner (2021-2023): analisi vendite e forecast di magazzino.',
        'progetti': 'Portfolio di analisi pubblico su GitHub con dataset open',
        'volontariato': 'Tutor di statistica per studenti universitari (2022-oggi)',
        'competenze_tecniche': 'Python, R, SQL, Excel, Spark',
        'competenze_trasversali': 'Analisi critica, presentazione dei risultati, lavoro in team',
        'strumenti_software': 'Tableau, Power BI, Jupyter, Git',
        'lingue': 'Italiano C2, Inglese B2',
        'patente': 'B', 'hobby': 'scacchi, trail running, lettura',
        'referenze': 'Davide Serra - CIO @ DataCorp Italia, davide.serra@datacorp.it',
        'foto_profilo': 'https://randomuser.me/api/portraits/men/32.jpg', 'template_cv': 'minimal', 'modificato': '2026-09-09',
    },
    {
        'id': 3,
        'nome': 'Sofia', 'cognome': 'Marchetti',
        'email': 'sofia.marchetti@example.it', 'prefisso': '+39', 'telefono': '3458765432',
        'citta': 'Firenze', 'cap': '50122', 'indirizzo': 'Borgo San Frediano 8',
        'data_nascita': '1994-11-02', 'luogo_nascita': 'Firenze, Italia', 'nazionalita': 'Italiana',
        'codice_fiscale': 'MRCSFO94S42D612L',
        'linkedin': 'https://linkedin.com/in/sofiamarchetti', 'portfolio': 'https://sofiamarchetti.it', 'github': 'https://github.com/sofiamarchetti',
        'titolo_professionale': 'Graphic Designer / Art Director',
        'descrizione': 'Art director con 8 anni di esperienza tra brand identity, editoria e campagne digitali per marchi di moda e cibo.',
        'obiettivo_professionale': 'Guidare un team creativo in uno studio internazionale e portare una visione editoriale autentica.',
        'anni_esperienza': '8', 'contratto_desiderato': 'Freelance / Consulenza', 'disponibilita_immediata': 'Immediata',
        'titolo_studio': ['Laurea Triennale in Design (L-4)', 'Master Universitario di Secondo Livello'],
        'anno_diploma': '2017', 'istituto_formazione': 'ISIA Firenze', 'voto_formazione': '108/110', 'tesi_titolo': 'Identità visiva per piccoli produttori toscani',
        'corsi_certificazioni': 'Adobe Creative Cloud Specialist · Masterclass di direzione creativa',
        'ultimo_ruolo': 'Art Director', 'azienda': 'Studio Meridiana', 'periodo_lavoro': '2021 - Presente', 'settore_lavoro': 'Design & Branding',
        'descrizione_lavoro': 'Direzione creativa di progetti di branding e packaging; gestione del team grafico e dei clienti.',
        'risultati_raggiunti': 'Rebranding premiato con due riconoscimenti nazionali e +40% di notorietà del marchio cliente.',
        'esperienze_precedenti': 'Senior Designer, EDIT Milano (2018-2021): campagne editoriali e digitali per il settore moda.',
        'progetti': 'Tipografia sperimentale open source, collezione di poster con stampa artigianale',
        'volontariato': 'Progetti di comunicazione no-profit per musei civici (2020-oggi)',
        'competenze_tecniche': 'Illustrator, Photoshop, InDesign, Figma, After Effects',
        'competenze_trasversali': 'Leadership creativa, storytelling visivo, gestione della clientela',
        'strumenti_software': 'Adobe CC, Figma, Procreate, Notion',
        'lingue': 'Italiano C2, Inglese C1, Spagnolo B1',
        'patente': 'B', 'hobby': 'ceramica, fotografia analogica, cicloturismo',
        'referenze': 'Luca Moretti - Direttore Creativo @ Studio Meridiana, +39 055 000 0000',
        'foto_profilo': 'https://randomuser.me/api/portraits/women/68.jpg', 'template_cv': 'creative', 'modificato': '2026-09-07',
    },
    {
        'id': 4,
        'nome': 'Alessandro', 'cognome': 'Conti',
        'email': 'alessandro.conti@example.it', 'prefisso': '+39', 'telefono': '3394561230',
        'citta': 'Torino', 'cap': '10100', 'indirizzo': 'Corso Vittorio Emanuele II 33',
        'data_nascita': '1985-03-17', 'luogo_nascita': 'Torino, Italia', 'nazionalita': 'Italiana',
        'codice_fiscale': 'CNTLSN85C17L219T',
        'linkedin': 'https://linkedin.com/in/alessandroconti', 'portfolio': '', 'github': '',
        'titolo_professionale': 'Chief Operating Officer (COO)',
        'descrizione': 'Direttore operativo con 15 anni di esperienza nella manifattura: lean management, ottimizzazione delle supply chain e trasformazione digitale dei processi.',
        'obiettivo_professionale': 'Un ruolo di leadership per guidare la crescita operativa di un gruppo industriale in espansione.',
        'anni_esperienza': '15', 'contratto_desiderato': 'Tempo indeterminato', 'disponibilita_immediata': 'Dopo preavviso',
        'titolo_studio': ['Laurea Magistrale in Ingegneria Gestionale (LM-31)'],
        'anno_diploma': '2009', 'istituto_formazione': 'Politecnico di Torino', 'voto_formazione': '110/110 e lode', 'tesi_titolo': 'Ottimizzazione dei flussi produttivi in ambiente JIT',
        'corsi_certificazioni': 'Executive MBA · Certificazione Lean Six Sigma Black Belt',
        'ultimo_ruolo': 'Chief Operating Officer', 'azienda': 'NordVent S.p.A.', 'periodo_lavoro': '2019 - Presente', 'settore_lavoro': 'Manifatturiero',
        'descrizione_lavoro': 'Responsabile delle operations globali: produzione, logistica, acquisti e qualità su tre stabilimenti.',
        'risultati_raggiunti': 'Riduzione del 22% dei costi operativi e lead time ridotto di 8 giorni a parità di qualità.',
        'esperienze_precedenti': 'Plant Manager, Meccanica Vercelli (2014-2019): riorganizzazione completa dello stabilimento.',
        'progetti': 'Progetto di digitalizzazione delle linee produttive (sensori IoT e MES)',
        'volontariato': 'Mentor per giovani imprenditori presso la Fondazione Filiera (2021-oggi)',
        'competenze_tecniche': 'Lean Manufacturing, Supply Chain, Excel avanzato, SAP, Power BI',
        'competenze_trasversali': 'Gestione dei team, negoziazione, decision making, orientamento ai risultati',
        'strumenti_software': 'SAP S/4HANA, Microsoft Power BI, Jira, MS Project',
        'lingue': 'Italiano C2, Inglese C1, Tedesco B1',
        'patente': 'B', 'hobby': 'vela, economia, bridge',
        'referenze': 'Anna Ferrero - CFO @ NordVent S.p.A., anna.ferrero@nordvent.it',
        'foto_profilo': 'https://randomuser.me/api/portraits/men/75.jpg', 'template_cv': 'executive', 'modificato': '2026-09-06',
    },
    {
        'id': 5,
        'nome': 'Lorenzo', 'cognome': 'Ferrari',
        'email': 'lorenzo.ferrari@example.it', 'prefisso': '+39', 'telefono': '3476543210',
        'citta': 'Roma', 'cap': '00187', 'indirizzo': 'Via del Corso 120',
        'data_nascita': '1990-07-25', 'luogo_nascita': 'Perugia, Italia', 'nazionalita': 'Italiana',
        'codice_fiscale': 'FRRLNZ90L25G478Q',
        'linkedin': 'https://linkedin.com/in/lorenzoferrari', 'portfolio': 'https://lorenzoferrari.medium.com', 'github': '',
        'titolo_professionale': 'Giornalista / Editor',
        'descrizione': 'Giornalista con 10 anni di esperienza tra testate nazionali e newsletter indipendenti, specializzato in economia e innovazione.',
        'obiettivo_professionale': 'Dirigere una redazione digitale e costruire un prodotto editoriale sostenibile e di qualità.',
        'anni_esperienza': '10', 'contratto_desiderato': 'Collaborazione / Progetto', 'disponibilita_immediata': 'Immediata',
        'titolo_studio': ['Laurea Magistrale in Scienze Politiche (LM-62)', 'Master Universitario di Primo Livello'],
        'anno_diploma': '2014', 'istituto_formazione': 'Sapienza di Roma', 'voto_formazione': '105/110', 'tesi_titolo': 'Data journalism e nuove redazioni digitali',
        'corsi_certificazioni': 'Master di giornalismo d\'indagine · Corso di data visualization',
        'ultimo_ruolo': 'Editor', 'azienda': 'Rivista Meridiano', 'periodo_lavoro': '2020 - Presente', 'settore_lavoro': 'Editoria / Media',
        'descrizione_lavoro': 'Coordinamento della redazione, editing dei contributi e gestione della newsletter quotidiana.',
        'risultati_raggiunti': 'Crescita degli abbonati del 60% in due anni e premio giornalistico per l\'inchiesta "Costi nascosti".',
        'esperienze_precedenti': 'Cronista, Agenzia Nazionale (2016-2020): economia e pubblica amministrazione.',
        'progetti': 'Newsletter indipendente settimanale con 12.000 iscritti',
        'volontariato': 'Insegnante volontario di laboratorio di scrittura in un carcere romano (2019-oggi)',
        'competenze_tecniche': 'Editing, Scrittura giornalistica, SEO, Analisi dati (Excel, R base)',
        'competenze_trasversali': 'Comunicazione, gestione redazionale, fact-checking, public speaking',
        'strumenti_software': 'WordPress, Notion, Google Analytics, RSS aggregators',
        'lingue': 'Italiano C2, Inglese C1, Francese B2',
        'patente': 'B', 'hobby': 'cestistica, giardinaggio, storia moderna',
        'referenze': 'Giorgia Rinaldi - Direttrice @ Rivista Meridiano, +39 06 000 0000',
        'foto_profilo': 'https://randomuser.me/api/portraits/men/11.jpg', 'template_cv': 'editorial', 'modificato': '2026-09-05',
    },
]

USERS = {
    'demo@cursus.it': {'nome': 'Demo', 'password': 'demo123'},
}


def trova_cv(cv_id):
    for i, rec in enumerate(MOCK_CVS):
        if rec.get('id') == cv_id:
            return i
    return None


def cv_vuoto():
    return {
        'nome': '', 'cognome': '', 'email': '', 'prefisso': '+39', 'telefono': '',
        'citta': '', 'cap': '', 'indirizzo': '', 'data_nascita': '', 'luogo_nascita': '',
        'nazionalita': '', 'codice_fiscale': '', 'linkedin': '', 'portfolio': '', 'github': '',
        'titolo_professionale': '', 'descrizione': '', 'obiettivo_professionale': '',
        'anni_esperienza': '', 'contratto_desiderato': '', 'disponibilita_immediata': '',
        'titolo_studio': [], 'anno_diploma': '', 'istituto_formazione': '', 'voto_formazione': '',
        'tesi_titolo': '', 'corsi_certificazioni': '', 'ultimo_ruolo': '', 'azienda': '',
        'periodo_lavoro': '', 'settore_lavoro': '', 'descrizione_lavoro': '',
        'risultati_raggiunti': '', 'esperienze_precedenti': '', 'progetti': '',
        'volontariato': '', 'competenze_tecniche': '', 'competenze_trasversali': '',
        'strumenti_software': '', 'lingue': '', 'patente': '', 'hobby': '', 'referenze': '',
        'foto_profilo': '', 'template_cv': 'aurora',
    }


@app.after_request
def senza_cache(resp):
    resp.headers['Cache-Control'] = 'no-store'
    return resp


@app.context_processor
def inietta_i18n():
    return {
        'LANGUAGES': LANGUAGES,
        'LANGUAGE_NAMES': LANGUAGE_NAMES,
        'get_locale': seleziona_locale,
        'template_options': TEMPLATE_OPTIONS,
        'anno': date.today().year,
    }


@app.route('/set-lang/<lang>')
def set_lang(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
    prossima = request.args.get('prossima')
    if prossima and prossima.startswith('/'):
        return redirect(prossima)
    return redirect(request.referrer or url_for('index'))


def login_richiesto(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('utente'):
            return redirect(url_for('login', prossima=request.path))
        return f(*args, **kwargs)
    return wrapper


ESEMPI = {
    rec['template_cv']: {
        'nome': f"{rec['nome']} {rec['cognome']}",
        'foto': rec['foto_profilo']
    } for rec in MOCK_CVS
}


@app.route('/')
def index():
    return render_template('landing.html', template_options=TEMPLATE_OPTIONS, esempi=ESEMPI)


@app.route('/esempi/<template>')
def esempi(template):
    for rec in MOCK_CVS:
        if rec.get('template_cv') == template:
            return render_template(
                'cv.html',
                dati=rec,
                template_cv=template,
                template_name=TEMPLATE_OPTIONS[template],
                anteprima=True
            )
    abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('utente'):
        return redirect(url_for('dashboard'))
    errore = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        utente = USERS.get(email)
        if utente and utente['password'] == password:
            session['utente'] = email
            prossima = request.args.get('prossima')
            return redirect(prossima or url_for('dashboard'))
        errore = gettext('Email o password non corretti.')
    return render_template('login.html', errore=errore)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('utente'):
        return redirect(url_for('dashboard'))
    errore = None
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        conferma = request.form.get('conferma', '')
        if not nome or not email or not password:
            errore = gettext('Compila tutti i campi.')
        elif password != conferma:
            errore = gettext('Le password non coincidono.')
        elif email in USERS:
            errore = gettext('Esiste già un account con questa email.')
        else:
            USERS[email] = {'nome': nome, 'password': password}
            session['utente'] = email
            return redirect(url_for('dashboard'))
    return render_template('register.html', errore=errore)


@app.route('/logout')
def logout():
    session.pop('utente', None)
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_richiesto
def dashboard():
    return render_template(
        'dashboard.html',
        cvs=MOCK_CVS,
        template_options=TEMPLATE_OPTIONS
    )

@app.route('/cv/nuovo')
@login_richiesto
def cv_nuovo():
    return render_template(
        'form.html',
        dati=cv_vuoto(),
        cv_id=None,
        geoapify_key=GEOAPIFY_KEY,
        titoli_studio=TITOLI_STUDIO,
        template_options=TEMPLATE_OPTIONS
    )

@app.route('/cv/<int:cv_id>/modifica')
@login_richiesto
def cv_modifica(cv_id):
    idx = trova_cv(cv_id)
    if idx is None:
        abort(404)
    return render_template(
        'form.html',
        dati=MOCK_CVS[idx],
        cv_id=cv_id,
        geoapify_key=GEOAPIFY_KEY,
        titoli_studio=TITOLI_STUDIO,
        template_options=TEMPLATE_OPTIONS
    )

@app.route('/cv/<int:cv_id>')
@login_richiesto
def cv_anteprima(cv_id):
    idx = trova_cv(cv_id)
    if idx is None:
        abort(404)
    rec = MOCK_CVS[idx]
    template_cv = rec.get('template_cv', 'aurora')
    if template_cv not in TEMPLATE_OPTIONS:
        template_cv = 'aurora'
    return render_template(
        'cv.html',
        dati=rec,
        template_cv=template_cv,
        template_name=TEMPLATE_OPTIONS[template_cv]
    )

@app.route('/genera_cv', methods=['POST'])
@login_richiesto
def genera_cv():
    titolo = request.form.get('titolo_professionale', '').strip()
    if titolo == 'Altro':
        titolo = request.form.get('titolo_altro', '').strip()

    titoli_selezionati = request.form.getlist('titolo_studio')
    if 'Altro' in titoli_selezionati:
        titoli_selezionati.remove('Altro')
        altro_titolo = request.form.get('titolo_studio_altro', '').strip()
        if altro_titolo:
            titoli_selezionati.append(altro_titolo)

    foto = request.files.get('foto_profilo')
    foto_profilo = None
    if foto and foto.filename:
        if not foto.mimetype or not foto.mimetype.startswith('image/'):
            return redirect(url_for('dashboard'))
        foto_profilo = (
            f"data:{foto.mimetype};base64,"
            f"{base64.b64encode(foto.read()).decode('ascii')}"
        )

    def campo(nome):
        return request.form.get(nome, '').strip()

    dati_cv = {
        'nome': campo('nome'),
        'cognome': campo('cognome'),
        'email': campo('email'),
        'prefisso': campo('prefisso'),
        'telefono': campo('telefono'),
        'citta': campo('citta'),
        'cap': campo('cap'),
        'indirizzo': campo('indirizzo'),
        'data_nascita': campo('data_nascita'),
        'luogo_nascita': campo('luogo_nascita'),
        'nazionalita': campo('nazionalita'),
        'codice_fiscale': campo('codice_fiscale'),
        'linkedin': campo('linkedin'),
        'portfolio': campo('portfolio'),
        'github': campo('github'),
        'titolo_professionale': titolo,
        'descrizione': campo('descrizione'),
        'obiettivo_professionale': campo('obiettivo_professionale'),
        'anni_esperienza': campo('anni_esperienza'),
        'contratto_desiderato': campo('contratto_desiderato'),
        'disponibilita_immediata': campo('disponibilita_immediata'),
        'titolo_studio': titoli_selezionati,
        'anno_diploma': campo('anno_diploma'),
        'istituto_formazione': campo('istituto_formazione'),
        'voto_formazione': campo('voto_formazione'),
        'tesi_titolo': campo('tesi_titolo'),
        'corsi_certificazioni': campo('corsi_certificazioni'),
        'ultimo_ruolo': campo('ultimo_ruolo'),
        'azienda': campo('azienda'),
        'periodo_lavoro': campo('periodo_lavoro'),
        'settore_lavoro': campo('settore_lavoro'),
        'descrizione_lavoro': campo('descrizione_lavoro'),
        'risultati_raggiunti': campo('risultati_raggiunti'),
        'esperienze_precedenti': campo('esperienze_precedenti'),
        'progetti': campo('progetti'),
        'volontariato': campo('volontariato'),
        'competenze_tecniche': campo('competenze_tecniche'),
        'competenze_trasversali': campo('competenze_trasversali'),
        'strumenti_software': campo('strumenti_software'),
        'lingue': ', '.join(filter(None, request.form.getlist('lingue'))),
        'patente': ', '.join(filter(None, request.form.getlist('patente'))),
        'hobby': ', '.join(filter(None, request.form.getlist('hobby'))),
        'referenze': campo('referenze'),
        'foto_profilo': foto_profilo
    }
    template_cv = request.form.get('template_cv', 'aurora')
    if template_cv not in TEMPLATE_OPTIONS:
        template_cv = 'aurora'
    
    cv_id = request.form.get('cv_id', '').strip()
    if cv_id.isdigit():
        idx = trova_cv(int(cv_id))
        if idx is not None:
            if not dati_cv['foto_profilo']:
                dati_cv['foto_profilo'] = MOCK_CVS[idx].get('foto_profilo')
            MOCK_CVS[idx] = {
                **dati_cv,
                'id': int(cv_id),
                'template_cv': template_cv,
                'modificato': date.today().isoformat(),
            }

    campi_obbligatori = (
        'nome', 'cognome', 'email', 'telefono', 'citta',
        'titolo_professionale', 'descrizione', 'anno_diploma',
        'ultimo_ruolo', 'azienda', 'periodo_lavoro',
        'descrizione_lavoro', 'competenze_tecniche', 'lingue', 'hobby'
    )
    if not titoli_selezionati or any(not dati_cv[campo_nome] for campo_nome in campi_obbligatori):
        return redirect(url_for('dashboard'))

    return render_template(
        'cv.html',
        dati=dati_cv,
        template_cv=template_cv,
        template_name=TEMPLATE_OPTIONS[template_cv]
    )

if __name__ == '__main__':
    app.run(debug=True)