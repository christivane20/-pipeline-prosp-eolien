import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
import requests

engine = create_engine(
    "postgresql+psycopg://eolien:eolien123@localhost:5433/eolien_db"
)

BASE_URL = "https://www.data.gouv.fr/api/1/datasets/"

tables = {
    "conseillers_departementaux": "5c34c4d1634f4173183a7b6b",
    "conseillers_regionaux":      "5c34c4d1634f4173183a7b6c",
    "deputes":                    "5c34c4d1634f4173183a7b6d",
    "senateurs":                  "5c34c4d1634f4173183a7b6e",
}

# API RNE directe
print("Telechargement elus nationaux via API RNE...")

# Deputes
url_dep = "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"
response = requests.get(url_dep, timeout=60)
print("Deputes status : " + str(response.status_code))

if response.status_code == 200:
    filepath = "data/deputes.csv"
    with open(filepath, "wb") as f:
        f.write(response.content)
    df = pd.read_csv(filepath, sep=";", encoding="utf-8")
    print("Deputes : " + str(len(df)) + " lignes")
    print("Colonnes : " + str(list(df.columns)[:5]))
    df.to_sql("deputes", engine, if_exists="replace", index=False)
    print("Succes deputes !")
else:
    print("Erreur deputes")

# Senateurs
url_sen = "https://www.data.gouv.fr/fr/datasets/r/efea5e6d-1fc9-4f14-9e43-4e3cf3c3cf9a"
response2 = requests.get(url_sen, timeout=60)
print("Senateurs status : " + str(response2.status_code))

if response2.status_code == 200:
    filepath2 = "data/senateurs.csv"
    with open(filepath2, "wb") as f:
        f.write(response2.content)
    df2 = pd.read_csv(filepath2, sep=";", encoding="utf-8")
    print("Senateurs : " + str(len(df2)) + " lignes")
    df2.to_sql("senateurs", engine, if_exists="replace", index=False)
    print("Succes senateurs !")
else:
    print("Erreur senateurs")
