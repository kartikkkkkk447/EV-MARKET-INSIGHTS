"""
Electric Vehicle Market Performance & Insights
Production-Ready Flask Web Application
"""

import os
import io
import csv
from flask import Flask, render_template, request, jsonify, Response, send_file
from sql_operations import EVMarketAnalytics, get_db_connection

app = Flask(__name__)
analytics = EVMarketAnalytics()

def parse_filters(req_args):
    """Extracts and normalizes filter parameters from GET request."""
    filters = {}
    
    # Battery technology filter (can be multi-selected or comma-separated)
    battery_tech = req_args.get('battery_tech')
    if battery_tech and battery_tech != 'All':
        filters['battery_tech'] = [b.strip() for b in battery_tech.split(',') if b.strip()]

    # Vehicle category filter
    vehicle_category = req_args.get('vehicle_category')
    if vehicle_category and vehicle_category != 'All':
        filters['vehicle_category'] = [c.strip() for c in vehicle_category.split(',') if c.strip()]

    # Manufacturing country
    country = req_args.get('country')
    if country and country != 'All':
        filters['manufacturing_country'] = country

    # Manufacturer
    manufacturer = req_args.get('manufacturer')
    if manufacturer and manufacturer != 'All':
        filters['manufacturer'] = manufacturer

    # Price range
    min_price = req_args.get('min_price')
    if min_price and min_price.isdigit():
        filters['min_price'] = int(min_price)

    max_price = req_args.get('max_price')
    if max_price and max_price.isdigit():
        filters['max_price'] = int(max_price)

    # Search keyword
    search = req_args.get('search')
    if search:
        filters['search'] = search.strip()

    return filters

@app.route('/')
def dashboard():
    """Renders the executive home dashboard."""
    filter_options = analytics.get_filter_options()
    initial_kpis = analytics.get_global_kpis()
    return render_template('index.html', filter_options=filter_options, initial_kpis=initial_kpis)

@app.route('/persona/emily')
def persona_emily():
    """Dedicated deep-dive workspace for Emily Johnson (Battery Tech Strategy)."""
    filter_options = analytics.get_filter_options()
    data = analytics.get_emily_battery_analysis()
    kpis = analytics.get_global_kpis()
    return render_template('emily.html', filter_options=filter_options, data=data, kpis=kpis)

@app.route('/persona/david')
def persona_david():
    """Dedicated deep-dive workspace for David Chen (Manufacturing & Country BI)."""
    filter_options = analytics.get_filter_options()
    data = analytics.get_david_manufacturing_analysis()
    kpis = analytics.get_global_kpis()
    return render_template('david.html', filter_options=filter_options, data=data, kpis=kpis)

@app.route('/persona/sarah')
def persona_sarah():
    """Dedicated deep-dive workspace for Dr. Sarah Williams (Range & Satisfaction)."""
    filter_options = analytics.get_filter_options()
    data = analytics.get_sarah_mobility_analysis()
    kpis = analytics.get_global_kpis()
    return render_template('sarah.html', filter_options=filter_options, data=data, kpis=kpis)

# ==========================================
# REST API Endpoints for Dynamic AJAX Charts
# ==========================================

@app.route('/api/kpis')
def api_kpis():
    """Returns updated KPI summary matching filters."""
    filters = parse_filters(request.args)
    kpis = analytics.get_global_kpis(filters)
    return jsonify(kpis)

@app.route('/api/emily')
def api_emily():
    """Returns Emily's battery analytics datasets."""
    filters = parse_filters(request.args)
    data = analytics.get_emily_battery_analysis(filters)
    return jsonify(data)

@app.route('/api/david')
def api_david():
    """Returns David's manufacturing & country distribution datasets."""
    filters = parse_filters(request.args)
    data = analytics.get_david_manufacturing_analysis(filters)
    return jsonify(data)

@app.route('/api/sarah')
def api_sarah():
    """Returns Sarah's mobility, range, and customer satisfaction datasets."""
    filters = parse_filters(request.args)
    data = analytics.get_sarah_mobility_analysis(filters)
    return jsonify(data)

@app.route('/api/models')
def api_models():
    """Returns paginated and sorted models for data table."""
    filters = parse_filters(request.args)
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    sort_by = request.args.get('sort_by', 'annual_sales')
    sort_order = request.args.get('sort_order', 'DESC')
    
    result = analytics.get_models_table(filters, page=page, page_size=page_size,
                                         sort_by=sort_by, sort_order=sort_order)
    return jsonify(result)

@app.route('/api/model/<int:model_id>')
def api_model_detail(model_id):
    """Returns single model specs for quick modal preview."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ev_market WHERE id = ?;", (model_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(dict(row))

@app.route('/api/export')
def api_export():
    """Exports filtered dataset as CSV."""
    filters = parse_filters(request.args)
    # Fetch all records matching filter
    result = analytics.get_models_table(filters, page=1, page_size=10000, sort_by='annual_sales')
    models = result['models']

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Manufacturer", "Model", "Vehicle Category", "Battery Tech",
        "Battery Capacity (kWh)", "Driving Range (km)", "Price (USD)",
        "Charging Speed (kW)", "Manufacturing Country", "Customer Rating", "Annual Sales"
    ])
    for m in models:
        writer.writerow([
            m['id'], m['manufacturer'], m['model'], m['vehicle_category'], m['battery_tech'],
            m['battery_capacity'], m['driving_range'], m['price'],
            m['charging_speed'], m['manufacturing_country'], m['customer_rating'], m['annual_sales']
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=ev_market_insights.csv"}
    )

if __name__ == '__main__':
    # Initialize DB if not present
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'database.db')):
        from generate_data import init_database
        init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
