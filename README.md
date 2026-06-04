# ERP Data Quality Framework

> Contrôle qualité, standardisation et exploitation analytique de données ERP
> Simulation d'un environnement industriel BTP — projet personnel et démonstration de compétences Data

---

## Contexte et problématique

Les données issues d'un ERP industriel sont rarement exploitables telles quelles.
Doublons, valeurs manquantes, incohérences de codification, référentiels non harmonisés :
ces anomalies rendent toute analyse fiable impossible sans une étape de qualification préalable.

Ce projet simule le workflow complet d'un Data Analyst intégré à un service BI industriel :
de l'extraction des données brutes jusqu'à la production d'indicateurs de pilotage fiables.

**Problématique centrale**
Comment fiabiliser des données issues d'un ERP et de sources externes
afin de produire des indicateurs pertinents pour le pilotage des stocks,
des fournisseurs et de l'activité commerciale ?

---

## Architecture

Sources                  Traitement                  Restitution
────────────────────────────────────────────────────────────────
CSV ERP simulé   ──┐
Excel métier     ──┼──► Ingestion ──► Audit qualité ──► Nettoyage ──► PostgreSQL ──► Power BI
API Open Meteo   ──┤
API INSEE BTP    ──┘

---

## Stack technique

| Couche | Outil |
|---|---|
| Ingestion & transformation | Python, Pandas |
| Stockage | PostgreSQL |
| Qualité & audit | Python, règles métier custom |
| Visualisation | Power BI, DAX |
| Sources externes | API Open Meteo, API INSEE |

---

## Structure du projet

erp_data_quality_framework/
│
├── data/
│   ├── raw/          # Fichiers sources bruts (CSV, Excel)
│   └── clean/        # Données transformées
│
├── notebooks/        # Exploration et audit qualité
├── pipeline/         # Scripts d'ingestion et de nettoyage
├── sql/              # Schéma PostgreSQL et requêtes analytiques
├── powerbi/          # Fichier .pbix
├── decisions.md      # Journal des choix techniques
└── README.md

---

## Périmètre fonctionnel

- Simulation d'exports ERP : articles, fournisseurs, stocks, commandes
- Intégration de corrections manuelles issues de fichiers Excel métier
- Enrichissement via API météo et indice BTP INSEE
- L'enrichissement via API répond à une logique analytique précise :
  - Open Meteo fournit les températures quotidiennes par région —
    permettant de corréler les volumes de commandes avec la saisonnalité climatique,
    un facteur réel dans le secteur BTP
  - L'indice INSEE d'activité BTP permet de distinguer une baisse de performance
    interne d'un ralentissement global du marché de la construction
- Audit qualité avec table d'anomalies graduée (critique / moyenne / faible)
- Modélisation en schéma étoile
- Dashboard Power BI : qualité master data, pilotage stock, activité commerciale

---

## Limites assumées

- Les données sont entièrement simulées — elles ne proviennent pas d'un ERP réel
- Le périmètre est volontairement réduit pour rester démontrable en solo
- L'API INSEE nécessite une clé d'accès gratuite à créer sur api.insee.fr

---

## Statut

🚧 En cours de développement