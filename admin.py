from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import secrets
import MySQLdb, mysql
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


#------------GET STATUS------------------------------------------------------------------------


@app.route('/admin_status.html')
def admin_status2():
    connection, cursor = get_database_connection()
    cursor.execute('SELECT status FROM booking_status')
    status_data = cursor.fetchall()
    connection.close()
    return render_template('admin_status.html', status_data=status_data)


#------------GET PRODUCTS------------------------------------------------------------------------


@app.route('/admin_invoice.html')
def admin_invoice2():
    connection, cursor = get_database_connection()
    cursor.execute('SELECT part_id, part_name, part_cost FROM parts')
    products_data = cursor.fetchall()
    connection.close()
    return render_template('admin_invoice.html', products_data=products_data)

#------------GET parts_used for invoice------------------------------------------------------------------------


@app.route('/get_parts_for_booking')
def get_parts_for_booking():
    booking_id = request.args.get('booking_id')
    if not booking_id:
        return jsonify(error="booking_id is required"), 400

    connection, cursor = get_database_connection()

    query = """
    SELECT u.booking_id, u.part_id, p.part_name, p.part_cost
    FROM parts_used u
    INNER JOIN parts p ON u.part_id = p.part_id
    WHERE u.booking_id = %s
    """ 
    cursor.execute(query, (booking_id,))
    parts = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(parts=parts)




#------------GET MECHANICS------------------------------------------------------------------------


@app.route('/admin_schedule.html')
def admin_schedule():
    connection, cursor = get_database_connection()
    cursor.execute('SELECT mechanic_id, name, surname FROM mechanics')
    mechanics_data = cursor.fetchall()
    connection.close()
    return render_template('admin_schedule.html', mechanics_data=mechanics_data)



#------------ASSIGN MECHANIC------------------------------------------------------------------------

    
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


#------------GET PARTS-------------------------------------------------------------------------


@app.route('/admin_products.html')
def admin_products():
    # Veritabanı bağlantısı ve imlecini alın
    connection, cursor = get_database_connection()

    # 'parts' tablosundan verileri çekin
    cursor.execute("SELECT part_id, part_name, part_cost FROM parts")
    parts_data = cursor.fetchall()

    cursor.close()
    connection.close()

    # Verileri HTML şablonu ile gösterin
    return render_template('admin_products.html', parts_data=parts_data)


#------------ASSIGN STATUS PAGE------------------------------------------------------------------------

@app.route('/admin_status', methods=['POST'])
def admin_status():
    data = request.get_json()
    date = data.get('date')

    if date:
        # Get database connection and cursor
        connection, cursor = get_database_connection()

        # Retrieve bookings for the selected date with customer, vehicle, service, and booking status details
        query = """
            SELECT b.booking_id, c.name, c.surname, v.vehicle_type, v.make, s.service_type, m.name, m.surname, f.status
            FROM bookings b
            INNER JOIN customers c ON b.customer_id = c.customer_id
            INNER JOIN vehicles v ON b.vehicle_id = v.vehicle_id
            INNER JOIN services s ON b.service_id = s.service_id
            INNER JOIN mechanics m ON b.mechanic_id = m.mechanic_id
            INNER JOIN booking_status f ON b.booking_status_id = f.booking_status_id
            WHERE b.booking_date = %s
        """
        
        cursor.execute(query, (date,))
        booking_details = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({'date': date, 'booking_details': booking_details})
    
    return jsonify({'date': None, 'booking_details': None})

#----------------------get the information for invoice---------------------------------------------------------------

    
@app.route('/admin_invoice', methods=['POST'])
def admin_invoice():
    data = request.get_json()
    date = data.get('date')

    if date:
        # Get database connection and cursor
        connection, cursor = get_database_connection()

        # Retrieve bookings for the selected date with customer, vehicle, and service details
        query = """
    SELECT b.booking_id, c.name, c.surname, c.mobile_phone, v.make, v.engine_type, s.service_type ,s.service_cost
    FROM bookings b
    INNER JOIN customers c ON b.customer_id = c.customer_id
    INNER JOIN vehicles v ON b.vehicle_id = v.vehicle_id
    INNER JOIN services s ON b.service_id = s.service_id
    WHERE b.booking_date = %s
      """
        
        cursor.execute(query, (date,))
        booking_details = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({'date': date, 'booking_details': booking_details})
    
    return jsonify({'date': None, 'booking_details': None})
#-------------------------assign parts on parts_used------------------------------------------------------------
@app.route('/process_invoice', methods=['POST'])
def process_invoice():
    # Retrieve data from the form
    booking_id = request.form.get('booking_id') 
    products = request.form.getlist('product')
   
    if products:
        connection, cursor = get_database_connection()
        for product in products:
            # Update the chosen part of the user with booking_id
            cursor.execute("INSERT INTO parts_used (booking_id, part_id) VALUES (%s, %s)", (booking_id, product))
            connection.commit()

            # Set the message with Flash
            flash("Part for booking ID {} added successfully to {}".format(booking_id, product), 'success')
            
        cursor.close()
        connection.close()
    else:
        # No product selected, set the error message with Flash
        flash("No product selected!", 'error')

    # Stay on the same page
    return redirect(request.referrer)




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

@app.route('/admin_status.html')
def admin_status1():
    return render_template('admin_status.html')


@app.route('/admin_products.html')
def admin_products1():
    return render_template('admin_products.html')



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

""" ---------------------update mechanic for booking------------------- """

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


""" ---------------------update status----------- """





@app.route('/update_status', methods=["POST"])
def update_status():
    # Formdan verileri al
    booking_id = request.form.get('booking_id')  # Eksiksiz veri almak için get() kullanılabilir
    status = request.form.get('status')

    # Kullanıcı adının önceden kaydedilip kaydedilmediğini kontrol et
    connection, cursor = get_database_connection()
    cursor.execute("SELECT booking_status_id FROM booking_status WHERE status = %s", (status,))
    booking_status_id = cursor.fetchone()
    cursor.close()

    if booking_status_id:
        # Kullanıcının seçtiği durumu booking_status_id ile güncelle
        connection, cursor = get_database_connection()
        cursor.execute("UPDATE bookings SET booking_status_id = %s WHERE booking_id = %s", (booking_status_id[0], booking_id))
        connection.commit()
        cursor.close()
        connection.close()

        
        # Mesajı Flash ile ayarla
        flash("Status for booking ID {} updated successfully to {}".format(booking_id, booking_status_id[0]), 'success')
    else:
        # booking_status_id veritabanında yok, hata mesajını Flash ile ayarla
        flash("Status not found!", 'error')

    # Aynı sayfada kal
    return redirect(request.referrer)



""" ---------------------parca eklemeeee ----------- """

# app.py

# ... (Önceki kodlar)

@app.route('/add_part', methods=['POST'])
def add_part():
    part_name = request.form.get('part_name')
    part_cost = request.form.get('part_cost')

    if part_name and part_cost:
        # Veritabanı bağlantısı ve imlecini alın
        connection, cursor = get_database_connection()

        # 'parts' tablosuna yeni parçayı ekleyin
        query = "INSERT INTO parts (part_name, part_cost) VALUES (%s, %s)"
        cursor.execute(query, (part_name, part_cost))
        connection.commit()

        cursor.close()
        connection.close()

        # Parçanın başarıyla eklenip eklenmediğini göstermek için mesajı Flash ile ayarlayın
        flash("Part '{}' added successfully with cost '{}'".format(part_name, part_cost), 'success')
    else:
        # Eksik veri varsa hata mesajını Flash ile ayarlayın
        flash("Missing part name or part cost!", 'error')

    # Aynı sayfada kal
    return redirect(request.referrer)


""" ---------------------parca çıkarmaaaaaaa ----------- """
#------------DELETE PART FORM-------------------------------------------------------------------------

@app.route('/delete_part_form', methods=['POST'])
def delete_part_form():
    part_id = request.form.get('part_id')  # Formdan girilen parça ID'sini al

    if part_id:
        try:
            part_id = int(part_id)  # Girilen değeri bir tamsayıya çevir
        except ValueError:
            flash("Invalid part ID. Please enter a valid number.", 'error')
            return redirect(url_for('admin_products1'))  # Yanlış ID girildiyse ürünler sayfasına geri dön

        # Veritabanı bağlantısı ve imlecini alın
        connection, cursor = get_database_connection()

        # Girilen parça ID'siyle parçayı veritabanından sil
        query = "DELETE FROM parts WHERE part_id = %s"
        cursor.execute(query, (part_id,))
        connection.commit()

        cursor.close()
        connection.close()

        # Silme işlemi başarılıysa başarılı mesajı Flash ile ayarlanır
        flash("Part with ID {} deleted successfully.".format(part_id), 'success')

    # Ürünler sayfasına geri dön
    return redirect(url_for('admin_products1'))

#------------UPDATE PART FORM eklemeee-------------------------------------------------------------------------

@app.route('/update_part_form', methods=['POST'])
def update_part_form():
    part_id = request.form.get('part_id')  # Formdan girilen parça ID'sini al
    new_part_name = request.form.get('new_part_name')  # Formdan girilen yeni parça adını al
    part_cost = request.form.get('part_cost')  # Formdan girilen parça fiyatını al

    if part_id and part_cost:
        try:
            part_id = int(part_id)  # Girilen parça ID'sini tamsayıya çevir
            part_cost = float(part_cost)  # Girilen parça fiyatını ondalıklı sayıya çevir
        except ValueError:
            flash("Invalid input. Please enter valid data.", 'error')
            return redirect(url_for('admin_products1'))  # Yanlış veri girildiyse ürünler sayfasına geri dön

        # Eğer yeni parça adı girilmemişse, mevcut parça adını veritabanından alın
        if not new_part_name:
            connection, cursor = get_database_connection()
            cursor.execute("SELECT part_name FROM parts WHERE part_id = %s", (part_id,))
            row = cursor.fetchone()
            if row:
                new_part_name = row[0]
            cursor.close()
            connection.close()

        # Veritabanı bağlantısı ve imlecini alın
        connection, cursor = get_database_connection()

        # Girilen parça ID'siyle veritabanında parçayı güncelle
        query = "UPDATE parts SET part_name = %s, part_cost = %s WHERE part_id = %s"
        cursor.execute(query, (new_part_name, part_cost, part_id))

        connection.commit()
        cursor.close()
        connection.close()

        # Güncelleme işlemi başarılıysa başarılı mesajı Flash ile ayarlanır
        flash("Part with ID {} updated successfully.".format(part_id), 'success')

    # Ürünler sayfasına geri dön
    return redirect(url_for('admin_products1'))


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
