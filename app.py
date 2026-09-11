import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, request, send_from_directory

app = Flask(__name__, template_folder='templates')

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# محفظة باينانس الخاصة بك لاستلام الأرباح مباشرة
MY_BINANCE_USDT_WALLET = "TBv3y23NRT7erMsF7GMeuu6FnCyTDybZ1k"

def init_db():
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
    cursor.execute("SELECT name, type, price, description FROM products")
    all_products = cursor.fetchall()
    conn.close()
    
    # جلب ملف index.html من مجلد templates بشكل رسمي ونظيف
    return render_template('index.html', products=all_products)

@app.route('/pay/<string:product_name>')
def pay(product_name):
    # عرض صفحة الدفع الرقمية الآمنة مع محفظة باينانس الخاصة بك
    html_pay = f'''
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>بوابة الدفع - متجر إبراهيم</title>
    </head>
    <body style="font-family:sans-serif; text-align:center; padding:50px; background:#fafafa; color:#333;">
        <h2 style="color:#1e3a8a;">🔐 بوابة الدفع الرقمية الآمنة لمتجر إبراهيم</h2>
        <p>أنت تقوم بشراء: <b>{product_name}</b></p>
        <p>الرجاء تحويل <b>5 USDT</b> إلى عنوان محفظة Binance التالي لشبكة <b>(TRC20)</b>:</p>
        <div style="background:#fff; border:2px dashed #ff9900; padding:15px; display:inline-block; font-family:monospace; font-size:18px; margin:20px 0; word-break:break-all; max-width:90%;">
            {MY_BINANCE_USDT_WALLET}
        </div>
        <br><br>
        <a href="/verify_payment" style="background:#10b981; color:white; padding:12px 24px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">محاكاة نجاح الدفع (التسليم الآلي الفوري) ✅</a>
    </body>
    </html>
    '''
    return html_pay

@app.route('/verify_payment')
def verify_payment():
    file_name = "Ibrahim_Codes.zip"
    test_file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    if not os.path.exists(test_file_path):
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("مرحباً بك! هذا هو ملف السورس كود الخاص بك من متجر إبراهيم مسعودي 2026.")
    return send_from_directory(DOWNLOAD_FOLDER, file_name, as_attachment=True)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
