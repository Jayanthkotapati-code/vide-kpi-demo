import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB_DEFAULT = BASE / "data" / "db" / "analytics.db"


def city_kpi(city: str, db_path=DB_DEFAULT):
    """Compute simple KPIs for a given city using parameterized SQL."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    query = (
        "SELECT COUNT(*) as customers, AVG(monthly_spend) as avg_spend, "
        "SUM(churned) as total_churn FROM customers_raw WHERE city = ?"
    )
    cur.execute(query, (city,))
    row = cur.fetchone()
    conn.close()
    customers = int(row[0]) if row and row[0] is not None else 0
    avg_spend = float(row[1]) if row and row[1] is not None else 0.0
    total_churn = int(row[2]) if row and row[2] is not None else 0
    result = {"customers": customers, "avg_spend": avg_spend, "total_churn": total_churn}
    print(f"city_kpi({city!r}) -> {result}")
    return result


if __name__ == "__main__":
    city_kpi("Mumbai")
    # injection attempt should NOT return all rows because we use parameterized SQL
    city_kpi("Mumbai' OR 1=1 --")
