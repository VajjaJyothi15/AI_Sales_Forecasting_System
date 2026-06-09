CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    order_date TEXT,
    customer_id TEXT,
    customer_name TEXT,
    product_name TEXT,
    category TEXT,
    region TEXT,
    quantity INTEGER,
    unit_price REAL,
    sales REAL,
    profit REAL,
    inventory INTEGER
);

CREATE TABLE IF NOT EXISTS forecast_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    forecast_date TEXT,
    predicted_sales REAL,
    lower_bound REAL,
    upper_bound REAL,
    model_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    safety_stock REAL,
    reorder_point REAL,
    eoq REAL,
    stock_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT,
    mae REAL,
    mse REAL,
    rmse REAL,
    r2 REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT,
    report_type TEXT,
    generated_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);