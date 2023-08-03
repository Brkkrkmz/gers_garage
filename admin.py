from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import secrets
import MySQLdb
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# MySQL yapılandırması
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gersgarage'


# Function to create and return a database connection and cursor
def get_database_connection():
    connection = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )
    cursor = connection.cursor()
    return connection, cursor

@app.route('/')
def index():
    connection, cursor = get_database_connection()
    cursor.execute('SELECT mechanic_id, name, surname FROM mechanics')
    mechanics_data = cursor.fetchall()
    connection.close()
    return render_template('admin_schedule.html', mechanics_data=mechanics_data)




    
@app.route('/view_schedule', methods=['POST'])
def view_schedule():
    data = request.get_json()
    date = data.get('date')

    if date:
        # Get database connection and cursor
        connection, cursor = get_database_connection()

        # Retrieve bookings for the selected date with customer, vehicle, and service details
        query = """
    SELECT b.booking_id, c.name, c.surname, v.vehicle_type, v.make, s.service_type, m.name, m.surname
    FROM bookings b
    INNER JOIN customers c ON b.customer_id = c.customer_id
    INNER JOIN vehicles v ON b.vehicle_id = v.vehicle_id
    INNER JOIN services s ON b.service_id = s.service_id
    INNER JOIN mechanics m ON b.mechanic_id = m.mechanic_id
    WHERE b.booking_date = %s
      """
        
        cursor.execute(query, (date,))
        booking_details = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({'date': date, 'booking_details': booking_details})
    
    return jsonify({'date': None, 'booking_details': None})

#------------STAFF ROSTER-------------------------------------------------------------------------
@app.route('/admin_view_roster', methods=['GET', 'POST'])
def admin_view_roster():
    mechanics_list = []
    if request.method == 'POST':
        date_str = request.form['date']
        selected_date = datetime.strptime(date_str, '%Y-%m-%d')

        for i in range(6): # Seçilen Pazartesi gününden sonraki 5 gün içerisinde
            booking_date = selected_date + timedelta(days=i)
            connection, cursor = get_database_connection()
            query = """
                SELECT m.name, m.surname
                FROM bookings b
                JOIN mechanics m ON b.mechanic_id = m.mechanic_id
                WHERE b.booking_date = %s
            """
            cursor.execute(query, [booking_date])
            mechanics = cursor.fetchall()
            connection.close()
            mechanics_list.append((booking_date.strftime('%Y-%m-%d'), mechanics))

    return render_template('admin_view_roster.html', mechanics_list=mechanics_list)



#-------------------------------------------------------------------------------------

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to the login page when first accessing the website

@app.route('/admin_index.html')
def admin_index1():
    return render_template('admin_index.html')

@app.route('/admin_invoice.html')
def admin_invoice1():
    return render_template('admin_invoice.html')

@app.route('/admin_schedule.html')
def admin_schedule1():
    return render_template('admin_schedule.html')

@app.route('/admin_view_roster.html')
def admin_view_roster1():
    return render_template('admin_view_roster.html')

@app.route('/admin_index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = validate_user(username, password)
        if user:
            # Kullanıcı adı ve şifre doğru, giriş başarılı, ana sayfaya yönlendir
            session['user_id'] = user[0]  # User ID'yi session'a kaydet
            return redirect('/admin_index.html')  # Redirect to admin_index.html after successful login
        else:
            # Kullanıcı adı veya şifre yanlış, hata mesajıyla tekrar login sayfasına dön
            error_message = "Invalid username or password"
            return render_template('admin_login.html', error_message=error_message)

    # For GET requests, render the login page
    return render_template('admin_login.html')

# Kullanıcı adı ve şifreyi doğrula
def validate_user(username, password):
    connection, cursor = get_database_connection()
    cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user


# app.py
# app.py


@app.route('/update_mechanic', methods=['POST'])
def update_mechanic():
    data = request.get_json()
    booking_id = data.get('booking_id')
    mechanic_id = data.get('mechanic_id')

    if booking_id and mechanic_id:
        # Get database connection and cursor (You'll need to define get_database_connection function)
        connection, cursor = get_database_connection()

        # Update the mechanic_id for the booking in the database
        query = "UPDATE bookings SET mechanic_id = %s WHERE booking_id = %s"
        cursor.execute(query, (mechanic_id, booking_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Mechanic updated successfully.'})
    
    return jsonify({'success': False, 'message': 'Booking ID or Mechanic ID is missing.'})







@app.route('/logout')
def logout():
    # Kullanıcıyı çıkış yaparken session'dan sil
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/admin_index')
def admin_index():
    # Check if the user is logged in
    if 'user_id' in session:
        return render_template('admin_index.html')
    else:
        # User is not logged in, redirect to the login page
        return redirect('/admin_login.html') 

if __name__ == "__main__":
    app.run(debug=True)
