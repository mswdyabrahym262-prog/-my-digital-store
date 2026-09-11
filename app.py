import os
import sqlite3
from flask import Flask, render_template_string, redirect, url_for, request, send_from_directory

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

MY_BINANCE_USDT_WALLET = "TBv3y23NRT7erMsF7GMeuu6FnCyTDybZ1k"

def init_db():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", 
                       ("أداة سحب وتحليل المنتجات من منصة سلة", 5.0, "سكربت مخصص للاتصال بالمتاجر وسحب البيانات تلقائياً."))
        cursor.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", 
                       ("نظام الأتمتة الذكي والترحيب بالعملاء", 5.0, "سكربت ذكي يقوم بتهيئة نظام الأتمتة والترحيب بالعملاء."))
        cursor.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", 
                       ("صفحة هبوط احترافية متكاملة ومتجاوبة", 5.0, "قالب موقع ويب عصري وجذاب ومصمم ليعمل على كافة الشاشات."))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>متجر إبراهيم Masoudi للأكواد</title>
        <style>
            body { font-family: sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; color: #333; text-align: center; }
            header { background-color: #1e3a8a; color: white; padding: 30px 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
            .card { background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); padding: 20px; width: 300px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid #e5e7eb; }
            .price { font-size: 22px; font-weight: bold; color: #10b981; margin: 15px 0; }
            .btn-buy { background-color: #ff9900; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; display: inline-block; }
        </style>
    </head>
    <body>
        <header>
            <h1>متجر إبراهيم Masoudi الرقمي</h1>
            <p>أكواد Python جاهزة وقوانين ويب احترافية مبرمجة ومجربة بالكامل</p>
        </header>
        <div class="container">
            {% for prod in products %}
            <div class="card">
                <h3>{{ prod[1] }}</h3>
                <p>{{ prod[3] }}</p>
                <div class="price">{{ prod[2] }}$</div>
                <a href="/pay/{{ prod[0] }}" class="btn-buy">شراء وتحميل تلقائي ⚡</a>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, products=products)

@app.route('/pay/<int:product_id>')
def pay(product_id):
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    html_pay = f'''
    <html dir="rtl">
    <body style="font-family:sans-serif; text-align:center; padding:50px; background:#fafafa;">
        <h2>🔐 بوابة الدفع الرقمية الآمنة لمتجر إبراهيم</h2>
        <p>أنت تقوم بشراء: <b>{product[0]}</b></p>
        <p>الرجاء تحويل <b>{product[1]} USDT</b> إلى عنوان محفظة Binance التالي لشبكة <b>(TRC20)</b>:</p>
        <div style="background:#fff; border:2px dashed #ff9900; padding:15px; display:inline-block; font-family:monospace; font-size:16px; word-break:break-all; max-width:90%;">
            {MY_BINANCE_USDT_WALLET}
        </div>
        <br><br>
        <a href="/verify_payment/{product_id}" style="background:#10b981; color:white; padding:12px 24px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">محاكاة نجاح الدفع (التسليم الآلي الفوري) ✅</a>
    </body>
    </html>
    '''
    return html_pay

@app.route('/verify_payment/<int:product_id>')
def verify_payment(product_id):
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    file_name = f"product_{product_id}.zip"
    test_file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    if not os.path.exists(test_file_path):
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(f"مرحباً بك! هذا هو ملف السورس كود الخاص بـ: {product[0]} \\nبرمجة وتطوير المطور المتميز إبراهيم مسعودي 2026.")
            
    return send_from_directory(DOWNLOAD_FOLDER, file_name, as_attachment=True)

if __name__ == '__main__':
    init_db()
        import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
