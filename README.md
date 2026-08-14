# vibe-kpi-demo

Run commands (assume virtual environment is activated):

Install requirements:

```
pip install -r requirements.txt
```

Run ETL to create the SQLite DB:

```
python src/etl_load_sqlite.py
```

Run the KPI script:

```
python src/kpi_city.py
```

Run tests:

```
pytest -q
```
# vide-kpi-demo