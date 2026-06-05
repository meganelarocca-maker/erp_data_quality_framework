from faker import Faker
import pandas as pd
import numpy as np

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

#Maintenant je créé la table transactionnelle qui sera jointe à la table article grâce à la clé commune "code_article"

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









