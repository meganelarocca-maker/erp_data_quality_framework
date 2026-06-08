from faker import Faker
import pandas as pd
import numpy as np
from openpyxl import * 

# J'initialise Faker en français
fake = Faker("fr_FR")

# Je définis mes référentiels avec des listes de valeurs autorisées
familles = ["BETON", "ARMATURE", "ISOLATION"]
unites = ["KG", "M", "L"]
statuts = ["ACTIF", "INACTIF"]
libelles = [
    "Dalle pleine 20cm",
    "Poutre précontrainte T160",
    "Prémur 15cm",
    "Escalier droit 12 marches",
    "Planche de rive 3m",
    "Voile béton 18cm",
    "Linteau préfabriqué 1m20",
    "Plaque de sol 40x40",
    "Poteau carré 25x25",
    "Gaine technique 3m"
]
depots = [
    "DEP_AVIGNON",      # siège social
    "DEP_VERNOUILLET",  # Île-de-France
    "DEP_GRIGNY",       # plateforme logistique IDF
    "DEP_LIMAY",        # logistique régionale
    "DEP_GRAULHET",     # usine Sud
    "DEP_CIEL",         # usine Bourgogne
    "DEP_NORD",
    "DEP_OUEST"
]

priorites_fournisseur=["Basse", "Moyenne", "Haute"]

def generate_articles(n=100):
    # Je crée une liste vide qui va accueillir mes articles
    articles = []
    
    # Je génère n articles avec des données simulées
    for i in range(n):
        # Je crée un dictionnaire pour chaque article
        article = {
            "code_article": f"ART{str(i+1).zfill(3)}",
            "libelle": np.random.choice(libelles),
            "famille": np.random.choice(familles),
            "unite": np.random.choice(unites),
            "prix_standard": round(np.random.uniform(10, 500), 2),
            "statut": np.random.choice(statuts),
            "fournisseur_principal": f"FOUR{str(np.random.randint(1, 20)).zfill(3)}"
        }
        # J'ajoute l'article à ma liste
        articles.append(article)
    
    # Je convertis ma liste en DataFrame et je la retourne
    return pd.DataFrame(articles)

df_articles = generate_articles()
print(df_articles.head())

df_articles.to_csv("data/raw/articles.csv", index=False)

#je réalise les mêmes étapes pour la table de référence fournisseurs
def generate_fournisseurs(n=50):
    fournisseurs= []
    for i in range(n):
        fournisseur= {
        "id_fournisseur": f"FOUR{str(i+1) . zfill(3)}",
        "nom_fournisseur":  fake.company(),
         "pays": fake.country(),
        "statut": np.random.choice(statuts)
            }

        fournisseurs.append(fournisseur)

    return pd.DataFrame(fournisseurs)

df_fournisseurs=generate_fournisseurs()
print(df_fournisseurs.head())
df_articles.to_csv("data/raw/fournisseurs.csv", index=False)

#Maintenant je créé la table transactionnelle "stocks" qui sera jointe à la table article grâce à la clé commune "code_article"

def generate_stocks(df_articles, n=800): #je passe df_article en argument pour que la fonction aille chercher les codes articles pré-existants
    stocks= []
    for i in range(n):
        stock= {
        "code_article": np.random.choice(df_articles["code_article"]),
        "depot":  np.random.choice(depots),
        "quantite_stock": np.random.randint(0,800),
        "date_maj": fake.date_between(start_date="-2y", end_date="today")
            }

        stocks.append(stock)

    return pd.DataFrame(stocks)

df_stocks=generate_stocks(df_articles)
print(df_stocks.head())
df_stocks.to_csv("data/raw/stocks.csv", index=False)


#Pour finir, je créé la table transactionnelle "commandes" qui sera elle aussi jointe à la table article grâce à la clé commune "code_article"

def generate_commandes(df_articles, n=800): #je passe df_article en argument pour que la fonction aille chercher les codes articles pré-existants
    commandes= []
    for i in range(n):
        commande= {
        "numero_commande": f"COM{str(i+1).zfill(3)}",
        "code_article": np.random.choice(df_articles["code_article"]),
        "quantite_commande": np.random.randint(10,500),
        "prix_vente": round(np.random.uniform(10, 500), 2),
        "date_commande": fake.date_between(start_date="-2y", end_date="today")
        }

        commandes.append(commande)

    return pd.DataFrame(commandes)

df_commandes=generate_commandes(df_articles)
print(df_commandes.head())
df_commandes.to_csv("data/raw/commandes.csv", index=False)

#Maintenant, je génère c'est la source qui simule les corrections manuelles des équipes métier.

def generate_corrections_metier(df_articles, n=30) :
        corrections_metier= []
        for i in range(n):
            priorite = np.random.choice(priorites_fournisseur)
            if priorite == "Haute":
                seuil = np.random.choice([120, 150])
            elif priorite == "Moyenne":
                seuil = np.random.choice([80, 100])
            else:
                seuil = np.random.choice([50, 80])
            correction_metier ={
                "code_article": np.random.choice(df_articles["code_article"]),
                "famille_excel": np.random.choice(familles),
                "priorite_fournisseur": priorite,
                "seuil_alerte": seuil
            }

            corrections_metier.append(correction_metier)

        return pd.DataFrame(corrections_metier)

df_corrections_metier=generate_corrections_metier(df_articles)
print(df_corrections_metier.head())
df_corrections_metier.to_excel("data/raw/corrections_metier_articles.xlsx", index=False)

#je vais maintenant introduire des anomalies volontairement correspondant à celles  recensées dans les études sur les données d'entreprises

def generate_anomalies_articles(df_articles):
    df_articles_dirty=df_articles.copy()
    idx = df_articles_dirty.sample(frac=0.08).index #je créée une variable index me permettant d'avoir des prix incohérents différents et non uniforme 
    df_articles_dirty.loc[df_articles_dirty.sample(frac=0.08).index, "famille"] = np.nan
    df_articles_dirty.loc[df_articles_dirty.sample(frac=0.08).index, "prix_standard"] = -np.random.uniform(10, 500, size=len(idx)) #size me permet de créer une valeur différente par ligne
    df_articles_dirty.loc[df_articles_dirty.sample(frac=0.05).index, "prix_standard"] = 0
    df_articles_dirty.loc[df_articles_dirty.sample(frac=0.07).index, "unite"] = np.random.choice(["kilo", "kg"])
    df_articles_dirty.loc[df_articles_dirty.sample(frac=0.15).index, "statut"] = np.random.choice(["inactif", "actif"])
    df_articles_dirty.loc[df_articles_dirty.sample(frac=0.04).index, "fournisseur_principal"] = "FOUR999"

    return df_articles_dirty
df_articles_dirty=generate_anomalies_articles(df_articles)
print(df_articles_dirty.sample(10))
df_articles_dirty.to_csv("data/raw/articles_dirty.csv", index=False)

def generate_anomalies_fournisseurs(df_fournisseurs):
    df_fournisseurs_dirty=df_fournisseurs.copy()
    doublons = df_fournisseurs_dirty.sample(3)  # je prends 3 lignes au hasard
    df_fournisseurs_dirty = pd.concat([df_fournisseurs_dirty, doublons], ignore_index=True)
    df_fournisseurs_dirty.loc[df_fournisseurs_dirty.sample(frac=0.04).index, "id_fournisseur"] ="FOUR999"
    df_fournisseurs_dirty.loc[df_fournisseurs_dirty.sample(frac=0.08).index, "nom_fournisseur"] = np.nan
    idx = df_fournisseurs_dirty.sample(frac=0.10).index
    df_fournisseurs_dirty.loc[idx, "pays"] = df_fournisseurs_dirty.loc[idx, "pays"].str.lower() # Je simule une erreur de casse fréquente : pays saisi en minuscules sans majuscule initiale
    df_fournisseurs_dirty.loc[df_fournisseurs_dirty.sample(frac=0.15).index, "statut"] = np.random.choice(["inactif", "actif"])
  
    return df_fournisseurs_dirty

df_fournisseurs_dirty=generate_anomalies_fournisseurs(df_fournisseurs)
print(df_fournisseurs_dirty.sample(10))
df_fournisseurs_dirty.to_csv("data/raw/fournisseurs_dirty.csv", index=False)

def generate_anomalies_stocks(df_stocks):
    df_stocks_dirty=df_stocks.copy()
    df_stocks_dirty.loc[df_stocks_dirty.sample(frac=0.03).index, "code_article"] = "ART999"
    idx = df_stocks_dirty.sample(frac=0.05).index
    df_stocks_dirty.loc[idx, "quantite_stock"] = -np.random.randint(0, 800, size=len(idx))
    idx = df_stocks_dirty.sample(frac=0.01).index
    df_stocks_dirty.loc[idx, "depot"] = df_stocks_dirty.loc[idx, "depot"].str.lower()
    idx = df_stocks_dirty.sample(frac=0.04).index
    df_stocks_dirty.loc[idx, "date_maj"] = pd.Timestamp("2019-01-01")
            
    return df_stocks_dirty

df_stocks_dirty=generate_anomalies_stocks(df_stocks)
print(df_stocks_dirty[df_stocks_dirty["quantite_stock"] < 0])
print(df_stocks_dirty[df_stocks_dirty["code_article"] == "ART999"])
print(df_stocks_dirty.sample(10))
df_stocks_dirty.to_csv("data/raw/stocks_dirty.csv", index=False)

def generate_anomalies_commandes(df_commandes):
    df_commandes_dirty = df_commandes.copy()
    df_commandes_dirty.loc[df_commandes_dirty.sample(frac=0.05).index, "prix_vente"] = np.nan
    idx = df_commandes_dirty.sample(frac=0.03).index
    df_commandes_dirty.loc[idx, "prix_vente"] = -np.round(np.random.uniform(10, 500, size=len(idx)), 2)
    df_commandes_dirty.loc[df_commandes_dirty.sample(frac=0.03).index, "prix_vente"] = 0
    idx = df_commandes_dirty.sample(frac=0.03).index
    df_commandes_dirty.loc[idx, "date_commande"] = pd.Timestamp("2027-01-01")
    idx = df_commandes_dirty.sample(frac=0.03).index
    df_commandes_dirty.loc[idx, "date_commande"] = pd.Timestamp("2021-06-15") 

    return df_commandes_dirty   


df_commandes_dirty=generate_anomalies_commandes(df_commandes)

#je filtre directement sur les erreurs pour gagner du temps et vérfier mes résultats 
print(df_commandes_dirty[df_commandes_dirty["prix_vente"] < 0])
print(df_commandes_dirty[df_commandes_dirty["prix_vente"].isna()])
print(df_commandes_dirty[pd.to_datetime(df_commandes_dirty["date_commande"]) > pd.Timestamp("2026-06-08")])
df_commandes_dirty.to_csv("data/raw/commandes_dirty.csv", index=False)