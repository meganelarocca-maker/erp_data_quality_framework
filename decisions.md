# Journal des décisions techniques

---

## Phase 1 — Génération et simulation des données

## Décision 1 — Génération des données simulées

### Contexte
Aucune donnée réelle d'ERP n'étant disponible, j'ai choisi de simuler
des exports ERP réalistes en Python plutôt que d'utiliser des jeux de
données génériques trouvés en ligne.

### Choix techniques
- Faker avec locale `fr_FR` pour des noms d'entreprises et données crédibles
- Numpy pour les valeurs numériques et les choix aléatoires
- Référentiels métier calés sur un contexte BTP préfabriqué béton
- 100 articles, 50 fournisseurs, 800 stocks, 800 commandes, 30 corrections métier

### Justification
Ces volumes permettent d'avoir des patterns statistiques visibles
sans alourdir les temps de traitement sur un environnement local.

---

## Décision 2 — Architecture multi-source

### Contexte
Un ERP réel ne suffit jamais seul — les équipes métier maintiennent
toujours des fichiers Excel parallèles pour corriger ou enrichir les données.

### Choix techniques
- CSV : simulation des exports ERP (articles, fournisseurs, stocks, commandes)
- Excel : corrections manuelles métier (famille, priorité fournisseur, seuil alerte)
- API Open Meteo : enrichissement saisonnier (impact météo sur commandes BTP)
- API INSEE : indice d'activité BTP pour contextualiser les performances

### Justification
Cette architecture reproduit fidèlement ce qu'on trouve dans un service BI
industriel : une source système + des sources métier + des sources externes.

---

## Décision 3 — Introduction d'anomalies intentionnelles

### Contexte
Les données ERP réelles contiennent systématiquement des erreurs de saisie.
Selon The Warehousing Institute, 76% des problèmes de qualité des données
trouvent leur origine dans les saisies utilisateurs.

### Taux retenus par anomalie

| Table | Anomalie | Taux | Justification |
|---|---|---|---|
| Articles | famille manquante | 8% | oubli fréquent à la création |
| Articles | prix négatif | 8% | erreur de saisie |
| Articles | prix à 0 | 5% | article créé sans prix |
| Articles | unité hors référentiel | 7% | incohérence de codification |
| Articles | statut casse incorrecte | 15% | erreur systémique |
| Articles | fournisseur inexistant | 4% | référentiel non mis à jour |
| Fournisseurs | nom manquant | 8% | saisie incomplète |
| Fournisseurs | pays en minuscules | 10% | erreur de casse |
| Fournisseurs | statut casse incorrecte | 15% | erreur systémique |
| Fournisseurs | doublons | 3 lignes fixes | duplication accidentelle |
| Stocks | quantité négative | 5% | erreur d'inventaire |
| Stocks | code article inexistant | 3% | référentiel désynchronisé |
| Stocks | date antérieure à 2020 | 4% | erreur de saisie de date |
| Stocks | dépôt en minuscules | 1% | incohérence de casse |
| Commandes | prix manquant | 5% | commande créée sans tarif |
| Commandes | prix négatif | 3% | erreur de saisie |
| Commandes | date future | 3% | erreur de saisie |
| Commandes | date antérieure à 2022 | 3% | donnée historique incohérente |

### Justification
Les taux ont été calibrés pour reproduire un niveau d'anomalies réaliste —
ni trop propre (irréaliste), ni trop dégradé (les équipes métier ne sont pas
des amateurs). La table corrections_metier reste volontairement propre :
c'est la source de vérité métier.

---

## Décision 4 — Séparation raw / clean

### Contexte
Les fichiers bruts avec anomalies sont conservés dans `data/raw/`
sous le suffixe `_dirty`. Les données nettoyées iront dans `data/clean/`
en Phase 3.

### Justification
Cette séparation reproduit la logique d'un vrai pipeline data :
on ne détruit jamais la donnée source, on la transforme dans une couche séparée.
C'est un principe fondamental de gouvernance des données.