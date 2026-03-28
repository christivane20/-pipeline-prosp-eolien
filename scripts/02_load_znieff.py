import geopandas as gpd
from sqlalchemy import create_engine
import requests
import zipfile
import os

engine = create_engine(
    "postgresql+psycopg://eolien:eolien123@localhost:5433/eolien_db"
)

# ZNIEFF TYPE 1 et TYPE 2 - INPN
print("Telechargement ZNIEFF type 1...")
url_z1 = "https://inpn.mnhn.fr/docs/Shape/znieff1.zip"
response = requests.get(url_z1, timeout=180)

if response.status_code == 200:
    zip_path = "data/znieff1.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)
    print("Telecharge : " + zip_path)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall("data/znieff1")
    print("Extrait dans data/znieff1")

    shp_files = [f for f in os.listdir("data/znieff1") if f.endswith(".shp")]
    print("Fichiers SHP : " + str(shp_files))

    if shp_files:
        gdf = gpd.read_file("data/znieff1/" + shp_files[0])
        print("ZNIEFF1 : " + str(len(gdf)) + " zones")
        gdf = gdf[gdf.geometry.notna()]
        gdf = gdf[~gdf.geometry.is_empty]
        gdf = gdf.to_crs(epsg=2154)
        gdf.to_postgis("znieff_type1", engine, if_exists="replace", index=False)
        print("Succes ZNIEFF type 1 !")
else:
    print("Erreur ZNIEFF1 : " + str(response.status_code))

print("Telechargement ZNIEFF type 2...")
url_z2 = "https://inpn.mnhn.fr/docs/Shape/znieff2.zip"
response2 = requests.get(url_z2, timeout=180)

if response2.status_code == 200:
    zip_path2 = "data/znieff2.zip"
    with open(zip_path2, "wb") as f:
        f.write(response2.content)
    print("Telecharge : " + zip_path2)

    with zipfile.ZipFile(zip_path2, "r") as z:
        z.extractall("data/znieff2")
    print("Extrait dans data/znieff2")

    shp_files2 = [f for f in os.listdir("data/znieff2") if f.endswith(".shp")]

    if shp_files2:
        gdf2 = gpd.read_file("data/znieff2/" + shp_files2[0])
        print("ZNIEFF2 : " + str(len(gdf2)) + " zones")
        gdf2 = gdf2[gdf2.geometry.notna()]
        gdf2 = gdf2[~gdf2.geometry.is_empty]
        gdf2 = gdf2.to_crs(epsg=2154)
        gdf2.to_postgis("znieff_type2", engine, if_exists="replace", index=False)
        print("Succes ZNIEFF type 2 !")
else:
    print("Erreur ZNIEFF2 : " + str(response2.status_code))
