from flask import Flask, render_template, request
import MySQLdb
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# MySQL yapılandırması
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gersgarage'

# Booking sınıfı (Örnek, veritabanı şemanıza göre düzenlenmelidir)
class Booking:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.booking_date = kwargs.get('booking_date')

# MySQL bağlantısını oluştur
def connect_db():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# MySQL bağlantısını kapat
def close_db(cursor, connection):
    cursor.close()
    connection.commit()
    connection.close()


@app.route('/admin/invoice')
def admin_invoice():
    # Burada fatura oluşturma işlemleri yapılabilir
    return render_template('admin_invoice.html')


# Admin uygulamasının route ve view fonksiyonları
@app.route('/')
def admin_index():
    return render_template('admin_index.html')


@app.route('/admin/schedule', methods=['GET', 'POST'])
def admin_schedule():
    if request.method == 'POST':
        selected_date = request.form['selected_date']
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM booking WHERE booking_date = %s", (selected_date,))
            bookings_data = cursor.fetchall()

            # Booking nesneleri oluşturma
            bookings = []
            for booking_data in bookings_data:
                booking = Booking(**booking_data)
                bookings.append(booking)

        except Exception as e:
            print(f"Hata: {e}")
            bookings = []

        finally:
            close_db(cursor, connection)

    else:
        try:
            import datetime
            today_date = datetime.date.today().strftime('%Y-%m-%d')
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM booking WHERE booking_date = %s", (today_date,))
            bookings_data = cursor.fetchall()

            # Booking nesneleri oluşturma
            bookings = []
            for booking_data in bookings_data:
                booking = Booking(**booking_data)
                bookings.append(booking)

        except Exception as e:
            print(f"Hata: {e}")
            bookings = []

        finally:
            close_db(cursor, connection)

    return render_template('admin_schedule.html', bookings=bookings)


if __name__ == "__main__":
    app.run(debug=True)
