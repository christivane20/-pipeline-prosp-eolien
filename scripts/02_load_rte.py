import geopandas as gpd
from sqlalchemy import create_engine
import requests

engine = create_engine(
    "postgresql+psycopg://eolien:eolien123@localhost:5433/eolien_db"
)

# LIGNES AERIENNES RTE nouveau decoupage
print("Telechargement lignes aeriennes RTE...")
url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/lignes-aeriennes-rte-nv/exports/geojson"
response = requests.get(url, timeout=180)

print("Status : " + str(response.status_code))

if response.status_code == 200:
    filepath = "data/rte_lignes.geojson"
    with open(filepath, "wb") as f:
        f.write(response.content)
    print("Telecharge : " + filepath)

    gdf = gpd.read_file(filepath)
    print("Lignes brut : " + str(len(gdf)))
    print("Colonnes : " + str(list(gdf.columns)))

    gdf = gdf[gdf.geometry.notna()]
    gdf = gdf[~gdf.geometry.is_empty]
    print("Lignes valides : " + str(len(gdf)))

    if len(gdf) > 0:
        gdf = gdf.to_crs(epsg=2154)
        gdf.to_postgis("rte_lignes", engine, if_exists="replace", index=False)
        print("Succes !")
    else:
        print("Aucune geometrie valide")
else:
    print("Erreur : " + str(response.status_code))
