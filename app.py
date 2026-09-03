from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sales.db')
SCHEMA_FILE = os.path.join(BASE_DIR, 'schema.sql')

app = Flask(__name__)
app.config['DATABASE'] = DB_PATH


def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not os.path.exists(app.config['DATABASE']):
        conn = get_db()
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print('Initialized database from schema.sql')
    else:
        print('Database already exists at', app.config['DATABASE'])


@app.route('/')
def home():
    return redirect(url_for('dashboard'))


@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        date = request.form.get('date') or datetime.utcnow().strftime('%Y-%m-%d')
        product = request.form.get('product')
        quantity = int(request.form.get('quantity') or 0)
        unit_price = float(request.form.get('unit_price') or 0)
        sales_rep = request.form.get('sales_rep')
        region = request.form.get('region')
        notes = request.form.get('notes')

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO sales(date, product, quantity, unit_price, sales_rep, region, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (date, product, quantity, unit_price, sales_rep, region, notes)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('input_page'))

    return render_template('input.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# API endpoints for charts and data
@app.route('/api/sales/summary')
def api_summary():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT
                       COALESCE(SUM(quantity * unit_price), 0) AS total_sales,
                       COUNT(*) AS total_orders,
                       COALESCE(AVG(quantity * unit_price), 0) AS avg_order_value,
                       COALESCE(SUM(quantity), 0) AS total_quantity
                   FROM sales''')
    row = cur.fetchone()
    conn.close()
    return jsonify(dict(row))


@app.route('/api/sales/time_series')
def api_time_series():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT date(date) AS date, SUM(quantity * unit_price) AS total
        FROM sales
        GROUP BY date(date)
        ORDER BY date(date)
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/sales/by_product')
def api_by_product():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT product, SUM(quantity * unit_price) AS total
        FROM sales
        GROUP BY product
        ORDER BY total DESC
        LIMIT 10
    ''')
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/sales/top_reps')
def api_top_reps():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT sales_rep, SUM(quantity * unit_price) AS total
        FROM sales
        GROUP BY sales_rep
        ORDER BY total DESC
        LIMIT 5
    ''')
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/sales/recent')
def api_recent():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, date, product, quantity, unit_price, sales_rep, region, notes
        FROM sales
        ORDER BY date(date) DESC
        LIMIT 10
    ''')
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
