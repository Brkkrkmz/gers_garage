from flask import Flask, render_template, request
import secrets
import MySQLdb  # Bu kısmı düzelttik, Flask-MySQL yerine MySQLdb kullanacağız

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# MySQL yapılandırması
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gersgarage'

# MySQL bağlantısını oluştur
mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

# Admin uygulamasının route ve view fonksiyonları
@app.route('/admin_index')
def admin_index():
    return render_template('admin_index.html')

@app.route('/admin/schedule', methods=['GET', 'POST'])
def admin_schedule():
    if request.method == 'POST':
        selected_date = request.form['selected_date']
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM booking WHERE booking_date = %s", (selected_date,))
        bookings_data = cursor.fetchall()
        cursor.close()

        # Booking nesneleri oluşturma
        bookings = []
        for booking_data in bookings_data:
            booking =Booking(**booking_data)
            bookings.append(booking)

    else:
        # Varsayılan olarak bugünkü rezervasyonları getir
        import datetime
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM booking WHERE booking_date = %s", (today_date,))
        bookings_data = cursor.fetchall()
        cursor.close()

        # Booking nesneleri oluşturma
        bookings = []
        for booking_data in bookings_data:
            booking = Booking(**booking_data)
            bookings.append(booking)

    return render_template('admin_schedule.html', bookings=bookings)


if __name__ == "__main__":
    app.run(debug=True)
