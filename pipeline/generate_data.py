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










