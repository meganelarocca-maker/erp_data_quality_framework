import pandas as pd
from sqlalchemy import create_engine,text

# Je crée mon moteur de connexion vers PostgreSQL
# il contient mes identifiants et l'adresse de ma base erp_data_quality

engine = create_engine("postgresql://megane:erp251125@localhost:5433/erp_data_quality")

#je crée le schéma raw dans PostgreSQL s'il n'existe pas dejà
#raw = la couche qui stocke les données brutes avec anomalies, telles quelles

with engine.connect() as conn: 
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    conn.commit()

#je charge mes CSV en DataFrame
df_articles=pd.read_csv("data/raw/articles_dirty.csv", encoding='utf-8')
df_commandes=pd.read_csv("data/raw/commandes_dirty.csv", encoding='utf-8')
df_corrections_articles= pd.read_excel("data/raw/corrections_metier_articles.xlsx")
df_fournisseurs=pd.read_csv("data/raw/fournisseurs_dirty.csv", encoding='utf-8')
df_stocks=pd.read_csv("data/raw/stocks_dirty.csv", encoding='utf-8')

#j'écris df_articles dans PostgreSQL dans le schéma raw 
#if_exists="replace" : si la table existe dejà je la remplace 
#index=False : je n'écris pas l'index Pandas comme colonne, cela m'est inutile 
df_articles.to_sql("articles", engine, schema="raw", if_exists="replace", index=False)
df_commandes.to_sql("commandes", engine, schema="raw", if_exists="replace", index=False)
df_corrections_articles.to_sql("corrections_articles", engine,schema="raw", if_exists="replace", index=False)
df_fournisseurs.to_sql("fournisseurs", engine, schema="raw", if_exists="replace", index=False)
df_stocks.to_sql("stocks", engine, schema="raw", if_exists="replace", index=False)

#j'effectue un text en lisant la table article depuis PGSQL pour vérifier qu'elle existe 
df_test= pd.read_sql("SELECT * FROM raw.articles LIMIT 5", engine)
print(df_test)