from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
ETL_PATH = ROOT / "src" / "etl_load_sqlite.py"
KPI_PATH = ROOT / "src" / "kpi_city.py"


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


etl = _load_module(ETL_PATH, "etl_load_sqlite")
kpi = _load_module(KPI_PATH, "kpi_city")


def setup_module():
    # Ensure the DB exists for tests
    etl.load_csv_to_sqlite(csv_path=ROOT / "data" / "raw" / "customers_raw.csv", db_path=ROOT / "data" / "db" / "analytics.db")


def test_happy_path():
    res = kpi.city_kpi("Mumbai", db_path=ROOT / "data" / "db" / "analytics.db")
    assert res["customers"] == 3


def test_sql_injection_attempt():
    res = kpi.city_kpi("Mumbai' OR 1=1 --", db_path=ROOT / "data" / "db" / "analytics.db")
    # injection attempt should not return rows for other cities
    assert res["customers"] == 0
