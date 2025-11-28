from sqlalchemy import create_engine, text

DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"

def publish():
    print("📤 Creating Looker Studio Views...")

    engine = create_engine(DB_URI)

    with engine.begin() as conn:   # ใช้ begin() เพื่อ auto-commit

        conn.execute(text("""
            CREATE OR REPLACE VIEW public.vw_best_selling_products AS
            SELECT
                description AS product_name,
                SUM(quantity) AS total_quantity,
                SUM(unitprice * quantity) AS total_revenue
            FROM production.fact_sales
            WHERE quantity > 0
            GROUP BY description
            ORDER BY total_quantity DESC;
        """))

        conn.execute(text("""
            CREATE OR REPLACE VIEW public.vw_sales_by_country AS
            SELECT
                country,
                SUM(unitprice * quantity) AS total_revenue
            FROM production.fact_sales
            WHERE quantity > 0
            GROUP BY country
            ORDER BY total_revenue DESC;
        """))

        conn.execute(text("""
            CREATE OR REPLACE VIEW public.vw_monthly_sales_trend AS
            SELECT
                month,
                SUM(unitprice * quantity) AS total_revenue
            FROM production.fact_sales
            WHERE quantity > 0
            GROUP BY month
            ORDER BY month ASC;
        """))

        conn.execute(text("""
            CREATE OR REPLACE VIEW public.vw_top_customer AS
            SELECT
                customerid,
                SUM(unitprice * quantity) AS total_spent
            FROM production.fact_sales
            WHERE quantity > 0
            GROUP BY customerid
            ORDER BY total_spent DESC;
        """))

        conn.execute(text("""
            CREATE OR REPLACE VIEW public.vw_cancel_rate_by_product AS
            SELECT
                description AS product_name,
                SUM(CASE WHEN quantity < 0 THEN 1 ELSE 0 END) AS cancel_count
            FROM production.fact_sales
            GROUP BY description
            ORDER BY cancel_count DESC;
        """))

    print("✅ All Views Created Successfully!")

if __name__ == "__main__":
    publish()
