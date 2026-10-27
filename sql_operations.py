"""
Electric Vehicle Market Performance & Insights
SQL Operations Module
Executes tailored queries for Emily Johnson, David Chen, Dr. Sarah Williams,
as well as dynamic filtering and executive summaries.
"""

import sqlite3
import os
from typing import Dict, List, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Creates a database connection with dict-like row access."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class EVMarketAnalytics:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Helper to run a read query and return list of dictionaries."""
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def _execute_scalar(self, query: str, params: tuple = ()) -> Any:
        """Helper to fetch a single scalar value."""
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return row[0] if row else None

    # ==========================================
    # Global Executive KPI Summary
    # ==========================================
    def get_global_kpis(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates global market KPIs with optional filter parameters."""
        where_clauses, params = self._build_where_clause(filters)
        where_sql = f"WHERE { ' AND '.join(where_clauses) }" if where_clauses else ""

        query = f"""
        SELECT 
            COUNT(*) AS total_models,
            COALESCE(SUM(annual_sales), 0) AS total_sales,
            ROUND(COALESCE(AVG(driving_range), 0), 1) AS avg_range_km,
            ROUND(COALESCE(AVG(price), 0), 0) AS avg_price_usd,
            ROUND(COALESCE(AVG(battery_capacity), 0), 1) AS avg_capacity_kwh,
            ROUND(COALESCE(AVG(customer_rating), 0), 2) AS avg_customer_rating,
            ROUND(COALESCE(AVG(charging_speed), 0), 1) AS avg_charging_speed
        FROM ev_market
        {where_sql};
        """
        result = self._execute_query(query, tuple(params))[0]

        # Top Manufacturer by Sales in this slice
        top_mfr_query = f"""
        SELECT manufacturer, SUM(annual_sales) as total_sales
        FROM ev_market
        {where_sql}
        GROUP BY manufacturer
        ORDER BY total_sales DESC
        LIMIT 1;
        """
        top_mfr_res = self._execute_query(top_mfr_query, tuple(params))
        result['top_manufacturer'] = top_mfr_res[0]['manufacturer'] if top_mfr_res else "N/A"

        # Dominant Battery Tech
        top_bat_query = f"""
        SELECT battery_tech, SUM(annual_sales) as total_sales
        FROM ev_market
        {where_sql}
        GROUP BY battery_tech
        ORDER BY total_sales DESC
        LIMIT 1;
        """
        top_bat_res = self._execute_query(top_bat_query, tuple(params))
        result['top_battery_tech'] = top_bat_res[0]['battery_tech'] if top_bat_res else "N/A"

        return result

    # =========================================================================
    # PERSONA 1: Emily Johnson (EV Market Strategy Director)
    # Focus: Battery Tech Adoption, Capacity vs. Price & Market Share
    # =========================================================================
    def get_emily_battery_analysis(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Provides strategic battery intelligence:
        - Battery Technology Market Share (% of sales & unit volume)
        - Average range, capacity, and cost efficiency ($/kWh) by battery tech
        - Battery tech distribution across vehicle categories
        """
        where_clauses, params = self._build_where_clause(filters)
        where_sql = f"WHERE { ' AND '.join(where_clauses) }" if where_clauses else ""

        # 1. Battery tech market share & performance metrics
        tech_summary_query = f"""
        SELECT 
            battery_tech,
            COUNT(*) AS model_count,
            SUM(annual_sales) AS total_sales,
            ROUND(AVG(battery_capacity), 1) AS avg_capacity,
            ROUND(AVG(driving_range), 1) AS avg_range,
            ROUND(AVG(price), 0) AS avg_price,
            ROUND(AVG(price / battery_capacity), 1) AS avg_cost_per_kwh,
            ROUND(AVG(driving_range / battery_capacity), 2) AS avg_km_per_kwh
        FROM ev_market
        {where_sql}
        GROUP BY battery_tech
        ORDER BY total_sales DESC;
        """
        tech_summary = self._execute_query(tech_summary_query, tuple(params))

        # 2. Battery Tech across Vehicle Categories (Adoption matrix)
        category_matrix_query = f"""
        SELECT 
            vehicle_category,
            battery_tech,
            COUNT(*) AS count,
            SUM(annual_sales) AS sales
        FROM ev_market
        {where_sql}
        GROUP BY vehicle_category, battery_tech
        ORDER BY vehicle_category, sales DESC;
        """
        category_matrix = self._execute_query(category_matrix_query, tuple(params))

        # 3. Top flagship models by battery tech
        flagships_query = f"""
        SELECT manufacturer, model, vehicle_category, battery_tech, battery_capacity, driving_range, price, annual_sales
        FROM ev_market
        {where_sql}
        ORDER BY annual_sales DESC
        LIMIT 6;
        """
        flagships = self._execute_query(flagships_query, tuple(params))

        return {
            "tech_summary": tech_summary,
            "category_matrix": category_matrix,
            "flagships": flagships
        }

    # =========================================================================
    # PERSONA 2: David Chen (Business Intelligence Manager)
    # Focus: Manufacturing Distribution, Country Analysis & Manufacturer Dominance
    # =========================================================================
    def get_david_manufacturing_analysis(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Provides manufacturing & BI footprint:
        - Country-wise sales, model counts, and avg vehicle prices
        - Top 10 Manufacturers by sales & market share
        - Vehicle category production distribution by country
        """
        where_clauses, params = self._build_where_clause(filters)
        where_sql = f"WHERE { ' AND '.join(where_clauses) }" if where_clauses else ""

        # 1. Country distribution
        country_query = f"""
        SELECT 
            manufacturing_country,
            COUNT(*) AS total_models,
            SUM(annual_sales) AS total_sales,
            ROUND(AVG(price), 0) AS avg_price,
            ROUND(AVG(driving_range), 0) AS avg_range
        FROM ev_market
        {where_sql}
        GROUP BY manufacturing_country
        ORDER BY total_sales DESC;
        """
        country_data = self._execute_query(country_query, tuple(params))

        # 2. Top Manufacturers
        mfr_query = f"""
        SELECT 
            manufacturer,
            manufacturing_country,
            COUNT(*) AS models_offered,
            SUM(annual_sales) AS total_sales,
            ROUND(AVG(price), 0) AS avg_price,
            MAX(driving_range) AS max_range
        FROM ev_market
        {where_sql}
        GROUP BY manufacturer
        ORDER BY total_sales DESC
        LIMIT 10;
        """
        mfr_data = self._execute_query(mfr_query, tuple(params))

        # 3. Country vs Category breakdown
        country_category_query = f"""
        SELECT 
            manufacturing_country,
            vehicle_category,
            SUM(annual_sales) AS sales_volume,
            COUNT(*) AS model_count
        FROM ev_market
        {where_sql}
        GROUP BY manufacturing_country, vehicle_category
        ORDER BY manufacturing_country, sales_volume DESC;
        """
        country_cat_data = self._execute_query(country_category_query, tuple(params))

        return {
            "country_summary": country_data,
            "top_manufacturers": mfr_data,
            "country_category": country_cat_data
        }

    # =========================================================================
    # PERSONA 3: Dr. Sarah Williams (Sustainable Mobility Research Analyst)
    # Focus: Driving Range, Charging Speed & Customer Satisfaction Ratings
    # =========================================================================
    def get_sarah_mobility_analysis(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Provides sustainable mobility insights:
        - Driving range distribution across categories
        - Charging speed tiers and impact on customer satisfaction
        - Customer rating vs driving range & price correlation points
        - High efficiency sustainable champions
        """
        where_clauses, params = self._build_where_clause(filters)
        where_sql = f"WHERE { ' AND '.join(where_clauses) }" if where_clauses else ""

        # 1. Category range and rating benchmarks
        category_benchmarks_query = f"""
        SELECT 
            vehicle_category,
            COUNT(*) AS model_count,
            ROUND(AVG(driving_range), 1) AS avg_range,
            MIN(driving_range) AS min_range,
            MAX(driving_range) AS max_range,
            ROUND(AVG(charging_speed), 1) AS avg_charging_speed,
            ROUND(AVG(customer_rating), 2) AS avg_rating,
            ROUND(AVG(annual_sales), 0) AS avg_sales
        FROM ev_market
        {where_sql}
        GROUP BY vehicle_category
        ORDER BY avg_range DESC;
        """
        category_benchmarks = self._execute_query(category_benchmarks_query, tuple(params))

        # 2. Charging speed tiers vs Customer Satisfaction
        charging_tier_query = f"""
        SELECT 
            CASE 
                WHEN charging_speed < 50 THEN 'Standard AC / Slow DC (<50 kW)'
                WHEN charging_speed BETWEEN 50 AND 149.9 THEN 'Fast DC (50-149 kW)'
                WHEN charging_speed BETWEEN 150 AND 249.9 THEN 'Ultra-Fast DC (150-249 kW)'
                ELSE 'Hyper-Charge DC (250+ kW)'
            END AS speed_tier,
            COUNT(*) AS models_in_tier,
            ROUND(AVG(customer_rating), 2) AS avg_rating,
            ROUND(AVG(driving_range), 1) AS avg_range,
            ROUND(AVG(price), 0) AS avg_price,
            SUM(annual_sales) AS total_sales
        FROM ev_market
        {where_sql}
        GROUP BY speed_tier
        ORDER BY avg_rating DESC;
        """
        charging_tiers = self._execute_query(charging_tier_query, tuple(params))

        # 3. Top Customer Satisfaction Champions (Sustainable Mobility Leaders)
        leaders_query = f"""
        SELECT 
            manufacturer, model, vehicle_category, battery_tech,
            driving_range, charging_speed, customer_rating, price, annual_sales
        FROM ev_market
        {where_sql}
        ORDER BY customer_rating DESC, driving_range DESC
        LIMIT 8;
        """
        leaders = self._execute_query(leaders_query, tuple(params))

        # 4. Scatter data points for (Range, Rating, Charging Speed, Model, Manufacturer)
        scatter_query = f"""
        SELECT 
            model, manufacturer, vehicle_category, battery_tech,
            driving_range, customer_rating, charging_speed, price
        FROM ev_market
        {where_sql}
        ORDER BY annual_sales DESC
        LIMIT 50;
        """
        scatter_data = self._execute_query(scatter_query, tuple(params))

        return {
            "category_benchmarks": category_benchmarks,
            "charging_tiers": charging_tiers,
            "satisfaction_leaders": leaders,
            "scatter_points": scatter_data
        }

    # ==========================================
    # Filtered Models Explorer Table & Export
    # ==========================================
    def get_models_table(self, filters: Optional[Dict[str, Any]] = None,
                         page: int = 1, page_size: int = 15,
                         sort_by: str = 'annual_sales', sort_order: str = 'DESC') -> Dict[str, Any]:
        """Fetches paginated, sorted, and filtered vehicle models."""
        where_clauses, params = self._build_where_clause(filters)
        where_sql = f"WHERE { ' AND '.join(where_clauses) }" if where_clauses else ""

        # Validate sorting column to prevent injection
        valid_cols = {
            'manufacturer': 'manufacturer',
            'model': 'model',
            'vehicle_category': 'vehicle_category',
            'battery_tech': 'battery_tech',
            'battery_capacity': 'battery_capacity',
            'driving_range': 'driving_range',
            'price': 'price',
            'charging_speed': 'charging_speed',
            'manufacturing_country': 'manufacturing_country',
            'customer_rating': 'customer_rating',
            'annual_sales': 'annual_sales'
        }
        order_col = valid_cols.get(sort_by, 'annual_sales')
        direction = 'ASC' if str(sort_order).upper() == 'ASC' else 'DESC'

        # Total count
        count_query = f"SELECT COUNT(*) FROM ev_market {where_sql};"
        total_records = self._execute_scalar(count_query, tuple(params)) or 0

        # Query records
        offset = (max(1, page) - 1) * page_size
        data_query = f"""
        SELECT 
            id, manufacturer, model, vehicle_category, battery_tech,
            battery_capacity, driving_range, price, charging_speed,
            manufacturing_country, customer_rating, annual_sales
        FROM ev_market
        {where_sql}
        ORDER BY {order_col} {direction}
        LIMIT ? OFFSET ?;
        """
        query_params = list(params) + [page_size, offset]
        models = self._execute_query(data_query, tuple(query_params))

        total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1

        return {
            "models": models,
            "total_records": total_records,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    def get_filter_options(self) -> Dict[str, List[Any]]:
        """Returns distinct filter values available in the database."""
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            categories = [r[0] for r in cursor.execute("SELECT DISTINCT vehicle_category FROM ev_market ORDER BY vehicle_category;").fetchall()]
            battery_techs = [r[0] for r in cursor.execute("SELECT DISTINCT battery_tech FROM ev_market ORDER BY battery_tech;").fetchall()]
            countries = [r[0] for r in cursor.execute("SELECT DISTINCT manufacturing_country FROM ev_market ORDER BY manufacturing_country;").fetchall()]
            manufacturers = [r[0] for r in cursor.execute("SELECT DISTINCT manufacturer FROM ev_market ORDER BY manufacturer;").fetchall()]
            
            min_max = cursor.execute("SELECT MIN(price), MAX(price), MIN(driving_range), MAX(driving_range) FROM ev_market;").fetchone()

        return {
            "categories": categories,
            "battery_techs": battery_techs,
            "countries": countries,
            "manufacturers": manufacturers,
            "min_price": min_max[0] or 0,
            "max_price": min_max[1] or 150000,
            "min_range": min_max[2] or 0,
            "max_range": min_max[3] or 1200
        }

    def _build_where_clause(self, filters: Optional[Dict[str, Any]]) -> tuple:
        """Constructs parameterized WHERE condition from filter dictionary."""
        if not filters:
            return [], []

        clauses = []
        params = []

        if filters.get("battery_tech"):
            techs = filters["battery_tech"]
            if isinstance(techs, str):
                techs = [t.strip() for t in techs.split(",") if t.strip()]
            if techs:
                placeholders = ",".join("?" for _ in techs)
                clauses.append(f"battery_tech IN ({placeholders})")
                params.extend(techs)

        if filters.get("vehicle_category"):
            cats = filters["vehicle_category"]
            if isinstance(cats, str):
                cats = [c.strip() for c in cats.split(",") if c.strip()]
            if cats:
                placeholders = ",".join("?" for _ in cats)
                clauses.append(f"vehicle_category IN ({placeholders})")
                params.extend(cats)

        if filters.get("manufacturing_country"):
            country = filters["manufacturing_country"]
            if country and country != "All":
                clauses.append("manufacturing_country = ?")
                params.append(country)

        if filters.get("manufacturer"):
            mfr = filters["manufacturer"]
            if mfr and mfr != "All":
                clauses.append("manufacturer = ?")
                params.append(mfr)

        if filters.get("min_price") is not None and str(filters["min_price"]).isdigit():
            clauses.append("price >= ?")
            params.append(int(filters["min_price"]))

        if filters.get("max_price") is not None and str(filters["max_price"]).isdigit():
            clauses.append("price <= ?")
            params.append(int(filters["max_price"]))

        if filters.get("search"):
            search_str = f"%{filters['search'].strip()}%"
            clauses.append("(manufacturer LIKE ? OR model LIKE ?)")
            params.extend([search_str, search_str])

        return clauses, params


# CLI execution for testing SQL queries directly
if __name__ == "__main__":
    analytics = EVMarketAnalytics()
    print("=" * 70)
    print("GLOBAL EV MARKET KPI SUMMARY")
    print("=" * 70)
    kpis = analytics.get_global_kpis()
    for k, v in kpis.items():
        print(f"  {k:22}: {v}")

    print("\n" + "=" * 70)
    print("EMILY JOHNSON: BATTERY TECH STRATEGY")
    print("=" * 70)
    emily = analytics.get_emily_battery_analysis()
    for row in emily["tech_summary"]:
        print(f"  {row['battery_tech']:12} | Models: {row['model_count']:3} | Total Sales: {row['total_sales']:,} | Avg Range: {row['avg_range']} km | Cost/kWh: ${row['avg_cost_per_kwh']}")

    print("\n" + "=" * 70)
    print("DAVID CHEN: GLOBAL MANUFACTURING DISTRIBUTION")
    print("=" * 70)
    david = analytics.get_david_manufacturing_analysis()
    print("Top Manufacturing Countries:")
    for row in david["country_summary"][:5]:
        print(f"  {row['manufacturing_country']:14} | Sales: {row['total_sales']:,} | Avg Price: ${row['avg_price']:,}")

    print("\n" + "=" * 70)
    print("DR. SARAH WILLIAMS: SUSTAINABLE MOBILITY & SATISFACTION")
    print("=" * 70)
    sarah = analytics.get_sarah_mobility_analysis()
    print("Category Benchmarks:")
    for row in sarah["category_benchmarks"]:
        print(f"  {row['vehicle_category']:14} | Avg Range: {row['avg_range']} km | Avg Rating: {row['avg_rating']}/5.0 | Avg Speed: {row['avg_charging_speed']} kW")
