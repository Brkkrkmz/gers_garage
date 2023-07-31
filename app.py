from flask import Flask, render_template, request, redirect, session, flash,jsonify
from flask_mysqldb import MySQL
import secrets
from admin import admin_app


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# MySQL yapılandırması
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gersgarage'

mysql = MySQL(app)



# Araç ekleme işlemi
@app.route('/add_vehicle', methods=["POST"])
def add_vehicle():
    # Formdan verileri al
    customer_id = session.get('user_id')  # Bu, oturum açmış kullanıcının ID'sini alıyoruz
    vehicle_type = request.form['vehicle_type']
    make = request.form['make']
    licence_details = request.form['licence_details']  # Sütun adı "licence_details" olduğu için düzgün yazdığınızdan emin olun
    engine_type = request.form['engine_type']

    # Veritabanına veri eklemek için işlevi çağır
    add_vehicle_to_db(customer_id, vehicle_type, make, licence_details, engine_type)

    flash("Vehicle added successfully.", "success")
    return redirect('/add_vehicle.html')


# Veritabanına veri eklemek için işlev
def add_vehicle_to_db(customer_id, vehicle_type, make, licence_details, engine_type):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO vehicles (customer_id, vehicle_type, make, licence_details, engine_type) VALUES (%s, %s, %s, %s, %s)",
                (customer_id, vehicle_type, make, licence_details, engine_type))
    mysql.connection.commit()
    cur.close()



@app.route('/login.html')
def login1():
    return render_template('login.html')


@app.route('/index.html')
def index():
    return render_template('index.html')




@app.route('/add_vehicle.html')
def vehicle():
    return render_template('add_vehicle.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/prices.html')
def price():
    return render_template('prices.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/service.html')
def service():
    return render_template('service.html')


@app.route('/register.html')
def register():
    return render_template('register.html')


@app.route('/')
def home():
    # Kullanıcı oturumunu kontrol et
    if 'user_id' in session:
        return redirect('/myprofile.html')

    return redirect('/login.html')


@app.route('/add_user', methods=["POST"])
def add_user():
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
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

    # Şifrelerin eşleşip eşleşmediğini kontrol et
    if password1 != password2:
        message = "Passwords do not match. Please try again."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

    # E-posta adresinin önceden kaydedilip kaydedilmediğini kontrol et
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
    existing_email = cursor.fetchone()
    cursor.close()

    if existing_email:
        message = "This email is already registered. Please use a different email address."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

    # Kullanıcı adının önceden kaydedilip kaydedilmediğini kontrol et
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customers WHERE username = %s", (username,))
    existing_username = cursor.fetchone()
    cursor.close()

    if existing_username:
        message = "This username is already taken. Please choose a different username."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

    # MySQL cursor oluştur
    cur = mysql.connection.cursor()

    # Veritabanına ekleme sorgusu
    cur.execute("INSERT INTO customers(customer_id, name, surname, email, password, username, mobile_phone) VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                (firstName, lastName, email, password1, username, phone))

    # Değişiklikleri kaydet ve cursor'u kapat
    mysql.connection.commit()
    cur.close()

    # Başarılı kayıt mesajı
    message = "Registration successful! Please login."
    return redirect('/login?message=' + message)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # E-posta adresine ait kullanıcıyı veritabanından getir
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[4] == password:

            session['user_id'] = user[0]
            session.permanent = True
            return redirect('/myprofile.html')
        else:
            message = "Incorrect email or password. Please try again."
            return render_template('login.html', message=message)

    message = request.args.get('message')
    return render_template('login.html', message=message)


@app.route('/myprofile.html')
def myprofile():
    # Kullanıcı oturumunu kontrol et
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        # Kullanıcının araç bilgilerini al
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE customer_id = %s", (user_id,))
        vehicles = cursor.fetchall()
        cursor.close()
        if user:
            email = user[3]
            mobile_phone = user[2]
            name = user[1]
            surname = user[5]
            # Oturum açmış kullanıcılar için myprofile tuşunu göster
            show_myprofile_button = True
            return render_template('myprofile.html', email=email, mobile_phone=mobile_phone, name=name, surname=surname, show_myprofile_button=show_myprofile_button,vehicles=vehicles)

    # Kullanıcı oturumu yoksa veya çıkış yapılmışsa, login sayfasına yönlendir
    return redirect('/login.html')

@app.route('/booking.html')
def booking():
    # Kullanıcı oturumunu kontrol et
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        # Kullanıcının araç bilgilerini al
        cursor.execute("SELECT * FROM vehicles WHERE customer_id = %s", (user_id,))
        vehicles = cursor.fetchall()
        cursor.close()
        # Kullanıcı oturum açmışsa, booking sayfasını render et ve araç plakalarını da gönder
        return render_template('booking.html', vehicles=vehicles)
    else:
        # Kullanıcı oturum açmamışsa, login sayfasına yönlendir
        return redirect('/login.html')
  # Ekleme yapılan fonksiyonu güncelleyin
@app.route('/add_booking', methods=["POST"])
def add_booking():
    if 'user_id' in session:
        customer_id = session['user_id']
        licence_details = request.form['licence_details']
        booking_status = "Booked"
        booking_type = request.form['booking_type']
        booking_date = request.form['booking_date']
        user_comments = request.form['user_comments']
        # Determine service_id based on booking_status

         # Veritabanında service_type ile booking_type'ı karşılaştırarak service_id'yi alın
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT service_id FROM services WHERE service_type = %s", (booking_type,))
        result = cursor.fetchone()
        if result:
            service_id = result[0]
        else:
            # Eğer eşleşme yoksa, varsayılan olarak service_id'yi 4 olarak ayarlayın
            service_id = 3
        service_id=result
        cursor.close()


        # licence_details ile eşleşen vehicle_id'yi almak için sorgu yapın
        vehicle_id = get_vehicle_id_by_licence_details(licence_details)
        
        if vehicle_id is None:
            flash("Vehicle with licence details {} not found.".format(licence_details), "error")
            return redirect('/booking.html')
        
        # Veritabanına rezervasyon bilgilerini eklemek için işlevi çağır
        add_booking_to_db(customer_id, vehicle_id, service_id, booking_date, booking_status, user_comments, licence_details)
        flash("Booking added successfully.", "success")
        return redirect('/booking.html')
    else:
        return redirect('/login.html')


# Veritabanından licence_details ile eşleşen vehicle_id'yi getiren işlev
def get_vehicle_id_by_licence_details(licence_details):
    cur = mysql.connection.cursor()
    cur.execute("SELECT vehicle_id FROM vehicles WHERE licence_details = %s", (licence_details,))
    result = cur.fetchone()
    cur.close()
    if result:
        return result[0]
    return None



# Veritabanına rezervasyon bilgilerini eklemek için işlev
def add_booking_to_db(customer_id, vehicle_id, service_id, booking_date, booking_status, user_comments, licence_details):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO bookings (customer_id, vehicle_id, service_id, booking_date, booking_status, user_comments, licence_details) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (customer_id, vehicle_id, service_id, booking_date, booking_status, user_comments, licence_details))
    mysql.connection.commit()
    cur.close()



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")

    return redirect('/login.html')

if __name__ == "__main__":
    app.run(debug=True)
    