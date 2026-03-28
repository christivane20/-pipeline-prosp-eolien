import geopandas as gpd
import psycopg
from sqlalchemy import create_engine, text
import requests

print("Test connexion PostGIS...")
conn = psycopg.connect("host=localhost port=5433 dbname=eolien_db user=eolien password=eolien123")
cur = conn.cursor()
cur.execute("SELECT PostGIS_Version();")
version = cur.fetchone()[0]
print("PostGIS OK : " + version[:30])
conn.close()

engine = create_engine(
    "postgresql+psycopg://eolien:eolien123@localhost:5433/eolien_db"
)

print("Telechargement cadastre departement 60...")
url = "https://cadastre.data.gouv.fr/bundler/cadastre-etalab/departements/60/geojson/parcelles"
response = requests.get(url, timeout=120)

if response.status_code == 200:
    filepath = "data/cadastre_60.geojson"
    with open(filepath, "wb") as f:
        f.write(response.content)
    print("Telecharge : " + filepath)

    print("Chargement PostGIS...")
    gdf = gpd.read_file(filepath)
    print("Parcelles : " + str(len(gdf)))
    gdf = gdf.to_crs(epsg=2154)
    gdf.to_postgis("cadastre_parcelles", engine, if_exists="replace", index=False)
    print("Succes !")
else:
    print("Erreur : " + str(response.status_code))