# 🌬️ Pipeline SIG — Prospection Éolienne Onshore

> Pipeline géospatial open source reproduisant et améliorant l'architecture SIG  
> utilisée en prospection éolienne onshore chez un opérateur européen majeur.  
> Développé dans le cadre du TFE Ingénieur ESGT (wpd, 2026) par **Christ Ivane KOUADIO**.

---

## 🎯 Objectif

Construire un pipeline **bout-en-bout, automatisé et cloud-ready** pour la gestion des données géospatiales en prospection éolienne :

- Ingestion automatique de **46 sources open data** géographiques
- Stockage et traitement dans **PostgreSQL/PostGIS**
- Orchestration des mises à jour avec **Apache Airflow**
- Publication cartographique via **GeoServer + Lizmap**
- API géospatiale REST avec **FastAPI**
- Déploiement cloud sur **AWS** (S3, RDS, Lambda)
- Intégration **IA (Claude API)** pour l'analyse automatique des couches

---

## 🧱 Stack technique

| Couche | Technologie |
|--------|------------|
| **Base de données** | PostgreSQL 15 · PostGIS 3.4 |
| **Traitement géospatial** | Python · GeoPandas · GDAL/OGR · Shapely · SQLAlchemy |
| **Orchestration pipelines** | Apache Airflow · pgAgent |
| **Transformation données** | dbt (data build tool) |
| **Visualisation web** | QGIS Server · Lizmap · GeoServer · pg_tileserv |
| **API REST** | FastAPI · Uvicorn |
| **Cloud** | AWS S3 · AWS RDS PostGIS · AWS Lambda |
| **Conteneurisation** | Docker · docker-compose |
| **IA géospatiale** | Claude API (Anthropic) · YOLOv11 (détection objets) |
| **MLOps** | MLflow · Weights & Biases |
| **Formats cloud-native** | COG (Cloud Optimized GeoTIFF) · STAC |

---

## 📡 Sources de données — 46 sources documentées

| Thème | Sources |
|-------|---------|
| **Foncier** | Cadastre DGFiP (×95 dép.) · MAJIC personnes morales · RPG PAC |
| **Infrastructure** | RTE réseau électrique · Enedis/ORE · IGN BD TOPO · Géorisques ICPE · PPRNi |
| **Environnement** | INPN ZNIEFF · Natura 2000 · Zones humides · BRGM géologie · Haies IGN |
| **Aviation** | SIA/DGAC obstacles · Faisceaux hertziens ANFR · Contraintes aéro |
| **Contexte éolien** | Éoliennes DREALs (×12 régions) · ZAER · ZAER arrêtées |
| **Vent** | Cerema/Météo France 140m · ADEME 100m · UL spd100/140m |
| **Paysage** | Monuments historiques · Sites classés/inscrits · Atlas patrimoines |
| **Administratif** | RNE Élus (API) · Admin Express IGN · Communes/Départements/Régions |

> 📊 Grille complète de scoring et gouvernance : `data/suivi_sources_sig.xlsx`  
> Modèle multicritères (MCDM/ELECTRE TRI) documenté dans `docs/scoring_model.md`

---

## 🏗️ Architecture du projet

```
pipeline-prosp-eolien/
│
├── docker-compose.yml           # Stack complète : PostGIS + Airflow + GeoServer + Lizmap
│
├── dags/                        # Apache Airflow — orchestration pipelines
│   ├── dag_cadastre.py          # Pipeline Cadastre DGFiP (×95 départements)
│   ├── dag_bdtopo.py            # Pipeline BD TOPO IGN (routes, haies, végétation)
│   ├── dag_enedis.py            # Pipeline Enedis / Agence ORE
│   ├── dag_obstacles_sia.py     # Pipeline Obstacles SIA/DGAC
│   ├── dag_elus_rne.py          # Pipeline RNE Élus (API mensuelle)
│   ├── dag_zaer.py              # Pipeline ZAER arrêtées
│   └── dag_monuments_histo.py   # Pipeline Atlas patrimoines (WFS)
│
├── scripts/                     # Scripts Python standalone
│   ├── 01_download_data.py      # Téléchargement sources open data
│   ├── 02_load_postgis.py       # Chargement ogr2ogr → PostGIS
│   ├── 03_transform_dbt.py      # Lancement transformations dbt
│   ├── 04_api_fastapi.py        # API géospatiale REST
│   └── 05_qgis_claude_plugin.py # Plugin QGIS + Claude API (analyse IA)
│
├── dbt/                         # Modèles de transformation SQL versionnés
│   └── models/
│       ├── staging/             # Données brutes nettoyées
│       └── marts/               # Données métier (contexte éolien, contraintes)
│
├── aws/                         # Déploiement cloud AWS
│   ├── s3_raster_store.py       # Stockage rasters COG sur S3
│   ├── rds_postgis_connect.py   # Connexion RDS PostGIS managé
│   └── lambda_pipeline.py       # Déclenchement pipeline serverless
│
├── ml/                          # IA géospatiale
│   ├── yolo_detection.py        # Détection éoliennes par YOLOv11 (satellite)
│   └── claude_analysis.py       # Analyse automatique couches via Claude API
│
├── qgis-projects/               # Projets QGIS publiés sur Lizmap
│   └── contexte_eolien.qgz
│
├── data/
│   ├── suivi_sources_sig.xlsx   # Gouvernance 46 sources (scoring A/B/C/D)
│   └── sample/                  # Données exemples (département test)
│
├── docs/
│   ├── scoring_model.md         # Modèle MCDM/ELECTRE TRI documenté
│   ├── architecture.md          # Schéma architecture complète
│   └── pipelines/               # Notices techniques par source
│
└── README.md
```

---

## 🚀 Démarrage rapide

```bash
# Cloner le repo
git clone https://github.com/christivanekouadio/pipeline-prosp-eolien.git
cd pipeline-prosp-eolien

# Lancer la stack complète
docker-compose up -d

# Vérifier que PostGIS est up
docker exec -it postgis psql -U lizmap -c "SELECT PostGIS_Version();"

# Charger un département test (Oise - 60)
python scripts/01_download_data.py --source cadastre --dept 60
python scripts/02_load_postgis.py --source cadastre --dept 60
```

---

## 🤖 Intégration IA — Claude API dans QGIS

```python
# Plugin QGIS : analyse automatique d'une couche éolienne
import anthropic
import geopandas as gpd

def analyser_contexte_eolien(gpkg_path: str) -> str:
    gdf = gpd.read_file(gpkg_path)
    stats = {
        "nb_projets": len(gdf),
        "statuts": gdf["statut"].value_counts().to_dict(),
        "puissance_totale_mw": gdf["puissance_parc_max_mw"].sum()
    }
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"Analyse ce contexte éolien régional et identifie les tendances : {stats}"
        }]
    )
    return response.content[0].text
```

---

## 📊 Modèle de scoring multicritères

Le projet intègre un modèle **MCDM/ELECTRE TRI** pour prioriser l'automatisation des sources :

- **8 critères** pondérés (accessibilité, criticité métier, stabilité format...)
- **Coefficients validés** par sondage Delphi auprès d'experts SIG
- **Seuils déterminés** par 3 méthodes convergentes : Jenks (1967), partition équidistante, fuzzy sets (Zadeh, 1965)
- **Classification** : A (automatiser) · B (planifier) · C (semi-auto) · D (manuel)

> 📄 Documentation complète : `docs/scoring_model.md`

---

## 📈 Résultats et objectifs

| Métrique | Avant (manuel) | Après (pipeline) | Gain |
|----------|---------------|------------------|------|
| MAJ Cadastre ×95 dép. | ~40h | ~2h | **−95 %** |
| MAJ Obstacles SIA | ~3h | ~15 min | **−92 %** |
| MAJ Élus RNE | ~2h | automatique | **−100 %** |
| MAJ BD TOPO ×6 tables | ~20h | ~3h | **−85 %** |
| Inventaire sources | non documenté | 46 sources scorées | ✅ |

---

## 🗺️ Roadmap

- [x] Architecture BDD PostGIS documentée (TFE wpd)
- [x] 46 sources inventoriées et scorées (Excel + modèle MCDM)
- [x] Application Flask gouvernance SIG
- [x] Docker PostGIS local opérationnel
- [ ] DAGs Airflow (Cadastre, BD TOPO, Enedis)
- [ ] dbt models (staging + marts)
- [ ] API FastAPI géospatiale
- [ ] Déploiement AWS (S3 + RDS)
- [ ] Plugin QGIS + Claude API
- [ ] Détection éoliennes YOLOv11 (images satellite)
- [ ] STAC catalog + COG rasters
- [ ] Dashboard Streamlit / Grafana

---

## 👤 Auteur

**Christ Ivane KOUADIO**  
Ingénieur Géomètre-Topographe · Géomatique & Data Géospatiale — ESGT (2026)  
Spécialisation : Geospatial Data Engineering · Énergie · IA géospatiale

[![Kaggle](https://img.shields.io/badge/Kaggle-Geospatial_Analysis-blue)](https://www.kaggle.com/learn/certification/christivanekouadio/geospatial-analysis)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-christ--ivane--kouadio-blue)](https://linkedin.com/in/christ-ivane-kouadio)

---

## 📄 Licence

MIT — libre d'utilisation, d'adaptation et de redistribution avec attribution.
