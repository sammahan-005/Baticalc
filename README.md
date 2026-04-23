BatiCalc 🏗️ — Calculateur BIM pour le Gros Œuvre

BatiCalc est une application desktop developpée en Python permettant l'analyse automatique de fichiers IFC (BIM) pour la génération de devis quantitatifs de matériaux de construction, spécifiquement adaptée au contexte du bâtiment au Cameroun. 
📋 Présentation du Projet

Dans le secteur du BTP au Cameroun, l'estimation des matériaux est encore souvent manuelle, lente et sujette aux erreurs. BatiCalc résout ce problème en extrayant les données géométriques des maquettes numériques (murs, poteaux, dalles) pour les convertir instantanément en quantités réelles de matériaux (sacs de ciment, barres de fer, parpaings). 

L'objectif est de réduire le temps de chiffrage d'un bâtiment standard de plusieurs jours à moins de 3 minutes. 
✨ Fonctionnalités Clés

    Importation IFC : Support des normes ISO 16739 (IFC2x3 et IFC4). 

    Analyse Structurelle Automatique : Extraction des quantités pour les murs (IfcWall), fondations (IfcFooting), poteaux (IfcColumn) et toitures (IfcRoof). 

    Conversion Métier : Calcul automatique des besoins en ciment (dosage 350kg/m³), sable, gravier, ferraillage (HA06 à HA12) et parpaings. 

    Estimation Financière : Intégration des prix unitaires du marché local (Yaoundé, Douala, Bafoussam). 

    Génération de Rapports : Exportation de devis professionnels au format PDF. 

    Gestion de Projets : Système d'authentification et historique des analyses par utilisateur. 

🛠️ Stack Technique

    Langage : Python 3.10+ 

    Interface Graphique : PySide6 (Qt6) pour une expérience desktop moderne. 

    Analyse BIM : IfcOpenShell pour le parsing des fichiers IFC. 

    Base de Données : SQLite (stockage local et sécurisé). 

    Export PDF : ReportLab. 

📂 Structure du Projet
Plaintext

BatiCalc/
├── data/               # Base de données SQLite (utilisateurs, prix, projets) [cite: 139]
├── generated/          # Fichiers d'interface générés par Qt Designer [cite: 136]
├── src/                # Code source principal [cite: 133]
│   ├── analyseurs/     # Modules d'extraction IFC (walls, foundations, etc.) [cite: 134]
│   ├── ui_handlers/    # Logique des fenêtres et navigation [cite: 135]
│   ├── export/         # Logique de génération des rapports PDF [cite: 137]
│   └── calculateur_materiaux.py  # Formules de conversion BTP [cite: 138]
└── requirements.txt    # Dépendances du projet

🚀 Installation & Utilisation

    Cloner le dépôt :
    Bash

    git clone https://github.com/votre-compte/BatiCalc.git
    cd BatiCalc

    Installer les dépendances :
    Bash

    pip install -r requirements.txt

    Lancer l'application :
    Bash

    python src/main.py

📊 Formules de Calcul (Contexte Cameroun)

L'application intègre des ratios basés sur les pratiques de construction locales : 

    Béton armé : 8 sacs de ciment, 0.40m³ de sable et 0.80m³ de gravier par m³. 

    Maçonnerie : 12.5 parpaings (20x20x40) par m². 

    Ferraillage : Moyenne de 80kg/m³ pour les armatures principales. 

🛡️ Sécurité & Confidentialité

    Mode Offline : L'application est 100% locale, aucune donnée n'est envoyée sur internet. 

    Protection des données : Les mots de passe sont hachés en base de données. 

🗺️ Roadmap

    [x] Architecture et base de données 

    [x] Interface graphique et navigation 

    [x] Parseurs IFC (Murs, Poteaux, Fondations) 

    [x] Finalisation du module de calcul des matériaux 

    [x] Export PDF et rapports détaillés
