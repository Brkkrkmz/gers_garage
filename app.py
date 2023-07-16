from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL yapılandırması
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gersgarage'

mysql = MySQL(app)

# Ana sayfa
@app.route('/')
def home():
    # Veritabanından veri almak için sorgu
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customers")
    users = cursor.fetchall()
    cursor.close()

    return render_template('register.html', users=users)

@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        # Formdan verileri al
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        username = request.form['username']
        phone = request.form['phone']

        # Boş alan kontrolü yap
        if not firstName or not lastName or not email or not password1 or not password2 or not username or not phone:
            message = "Please fill in all fields"
            return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email, username=username, phone=phone)

        # Şifrelerin eşleşip eşleşmediğini kontrol et
        if password1 != password2:
            message = "Passwords do not match. Please try again."
            return render_template('register.html', message=message)

        # E-posta adresinin önceden kaydedilip kaydedilmediğini kontrol et
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        existing_email = cursor.fetchone()
        cursor.close()

        if existing_email:
            message = "This email is already registered. Please use a different email address."
            return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email, username=username, phone=phone)

        # Kullanıcı adının önceden kaydedilip kaydedilmediğini kontrol et
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE username = %s", (username,))
        existing_username = cursor.fetchone()
        cursor.close()

        if existing_username:
            message = "This username is already taken. Please choose a different username."
            return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email, username=username, phone=phone)

        # MySQL cursor oluştur
        cur = mysql.connection.cursor()

        # Veritabanına ekleme sorgusu
        cur.execute("INSERT INTO customers(name, surname, email, password, username, mobile_phone) VALUES (%s, %s, %s, %s, %s, %s)",
                    (firstName, lastName, email, password1, username, phone))

        # Değişiklikleri kaydet ve cursor'u kapat
        mysql.connection.commit()
        cur.close()

        # Başarılı kayıt mesajı
        message = "Registration successful! Please login."
        return redirect('/login?message=' + message)

    return render_template('register.html')

@app.route('/login')
def login():
    # Login sayfasını render etmek için gerekli işlemleri yapabilirsiniz
    message = request.args.get('message')
    return render_template('login.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
