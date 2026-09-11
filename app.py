import os
import sqlite3
from flask import Flask, render_template_string, redirect, url_for, request, send_from_directory

app = Flask(__name__)

# تهيئة مجلد التحميلات على السيرفر
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# محفظة باينانس الخاصة بك
MY_BINANCE_USDT_WALLET = "TBv3y23NRT7erMsF7GMeuu6FnCyTDybZ1k"

def init_db():
    # استخدام مسار مؤقت آمن وقابل للكتابة على خوادم ريندر
    db_path = os.path.join(os.getcwd(), 'store.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            file_name TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone() == 0:
        cursor.execute("""
            INSERT INTO products (name, type, price, description, file_name) VALUES 
            ('أداة سحب وتحليل المنتجات من منصة سلة', 'Python Script', 5.0, 'سكربت مخصص للاتصال بالمتاجر المبنية على منصة Salla وسحب الحقول والبيانات مثل المنتجات وحالاتها بنجاح وبشكل تلقائي وسريع.', 'salla_scraper.zip'),
            ('نظام الأتمتة الذكي والترحيب بالعملاء', 'Python Script', 5.0, 'سكربت ذكي يقوم بتهيئة نظام الأتمتة والترحيب بالعملاء بشكل تلقائي وتجهيز بيئة العمل لمهام الكشط البرمجي والذكاء الاصطناعي.', 'smart_client.zip'),
            ('صفحة هبوط احترافية متكاملة ومتجاوبة', 'Template HTML/CSS', 5.0, 'قالب موقع ويب عصري وجذاب ومصمم ليعمل على كافة الشاشات بشكل ممتاز، جاهز ليكون واجهة لمشروعك البرمجي القادم.', 'landing_page.zip')
        """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    db_path = os.path.join(os.getcwd(), 'store.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    all_products = cursor.fetchall()
    conn.close()
    
    # دمج كود الـ HTML الأنيق الخاص بك مباشرة لمنع أخطاء مسارات المجلدات
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>متجر إبراهيم Masoudi للأكواد</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; color: #333; }
            header { background-color: #1e3a8a; color: white; padding: 30px 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            header h1 { margin: 0; font-size: 26px; }
            header p { margin: 8px 0 0; font-size: 15px; opacity: 0.9; }
            .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
            .card { background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); padding: 20px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid #e5e7eb; }
            .badge { color: white; padding: 4px 8px; font-size: 12px; border-radius: 5px; align-self: flex-start; margin-bottom: 10px; font-weight: bold; }
            .badge.python { background-color: #3776ab; }
            .badge.web { background-color: #e34c26; }
            .card h3 { margin: 0 0 10px 0; font-size: 18px; color: #111827; }
            .card p { font-size: 14px; color: #4b5563; line-height: 1.6; margin: 0 0 20px 0; }
            .card-footer { display: flex; align-items: center; justify-content: space-between; border-top: 1px solid #f3f4f6; padding-top: 15px; }
            .price { font-size: 18px; font-weight: bold; color: #10b981; }
            .btn-buy { background-color: #ff9900; color: white; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold; }
            footer { text-align: center; padding: 20px; background-color: #1f2937; color: #9ca3af; font-size: 13px; margin-top: 50px; }
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
                <div>
                    {% if prod[2] == 'Python Script' %}
                    <span class="badge python">{{ prod[2] }}</span>
                    {% else %}
                    <span class="badge web">{{ prod[2] }}</span>
                    {% endif %}
                    <h3>{{ prod[1] }}</h3>
                    <p>{{ prod[4] }}</p>
                </div>
                <div class="card-footer">
                    <span class="price">{{ prod[3] }}$</span>
                    <a href="/pay/{{ prod[0] }}" class="btn-buy">شراء وتحميل تلقائي ⚡</a>
                </div>
            </div>
            {% endfor %}
        </div>
        <footer>
            <p>جميع الحقوق محفوظة © إبراهيم مسعودي 2026</p>
            <p>تم التطوير والبرمجة بالكامل عبر تطبيقات Pydroid 3 & TrebEdit</p>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html, products=all_products)

@app.route('/pay/<int:product_id>')
def pay(product_id):
    db_path = os.path.join(os.getcwd(), 'store.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        return "المنتج غير موجود"

    html_pay = f'''
    <html dir="rtl">
    <body style="font-family:sans-serif; text-align:center; padding:50px; background:#fafafa; color:#333;">
        <h2 style="color:#1e3a8a;">🔐 بوابة الدفع الرقمية الآمنة لمتجر إبراهيم</h2>
        <p>أنت تقوم بشراء: <b>{product[0]}</b></p>
        <p>الرجاء تحويل <b>{product[1]} USDT</b> إلى عنوان محفظة Binance التالي لشبكة <b>(TRC20)</b>:</p>
        <div style="background:#fff; border:2px dashed #ff9900; padding:15px; display:inline-block; font-family:monospace; font-size:18px; margin:20px 0; word-break:break-all; max-width:90%;">
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
    db_path = os.path.join(os.getcwd(), 'store.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, name FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if product:
        file_name = product[0]
        test_file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        if not os.path.exists(test_file_path):
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(f"مرحباً بك! هذا هو ملف السورس كود الخاص بـ: {product[1]} \\nبرمجة وتطوير المطور المتميز إبراهيم مسعودي 2026.")
        return send_from_directory(DOWNLOAD_FOLDER, file_name, as_attachment=True)
    return "خطأ في معالجة المنتج."

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
