# app.py
from flask import Flask, render_template, request, redirect, session, flash,jsonify
from flask_mysqldb import MySQL
import secrets



app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gersgarage'

mysql = MySQL(app)

#-------------------------------------------------get status for  car --------------------------------
@app.route('/get_status', methods=['POST'])
def get_status():
    # Get license number
    lisans_numarasi = request.form['lisans_numarasi']

    #   get  booking_status_id from bookings table
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT booking_status_id FROM bookings WHERE licence_details = %s", (lisans_numarasi,))
    booking_status_id = cursor.fetchone()
    cursor.close()

    if booking_status_id:
        #  get value from Booking_status table 
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT status FROM booking_status WHERE booking_status_id = %s", (booking_status_id[0],))
        status = cursor.fetchone()
        cursor.close()

        return jsonify({'status': status[0]})
    else:
        return jsonify({'status': 'Not Found'})











      #   ADD VEHİCLE
@app.route('/add_vehicle', methods=["POST"])
def add_vehicle():
    # get data from form
    customer_id = session.get('user_id')
    vehicle_type = request.form['vehicle_type']
    make = request.form['make']
    licence_details = request.form['licence_details']
    engine_type = request.form['engine_type']


    # Call function to insert data into database
    result = add_vehicle_to_db(customer_id, vehicle_type, make, licence_details, engine_type)

    if result:
        flash("Vehicle added successfully.", "success")
    else:
        flash("A vehicle with the same license number already exists.", "error")

    return redirect('/add_vehicle.html')


# Function to insert data into database

def add_vehicle_to_db(customer_id, vehicle_type, make, licence_details, engine_type):
    cur = mysql.connection.cursor()

    # Query the license number in the database
    cur.execute("SELECT COUNT(*) FROM vehicles WHERE licence_details = %s", (licence_details,))
    count = cur.fetchone()[0]

    if count > 0:
       # If the license number is already in the database, do not add it
        cur.close()
        return False
    else:
        # If the license number is not in the database, add the agent

        cur.execute("INSERT INTO vehicles (customer_id, vehicle_type, make, licence_details, engine_type) VALUES (%s, %s, %s, %s, %s)",
                    (customer_id, vehicle_type, make, licence_details, engine_type))
        mysql.connection.commit()
        cur.close()
        return True



@app.route('/vehicle_status.html')
def vehicle_status():
    return render_template('vehicle_status.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login1():
    return render_template('login.html')


@app.route('/add_vehicle.html')
def vehicle():
    return render_template('add_vehicle.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')

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
# Check user session
    if 'user_id' in session:
        return redirect('/myprofile.html')

    return redirect('/login.html')

def is_valid_password(password):
# Check if the password is at least 9 characters long
    if len(password) < 9:
        return False

# Check if the password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

# Check if the password contains at least one letter
    if not any(char.isalpha() for char in password):
        return False

# Check if the password contains at least one punctuation mark
    if not any(char in r"!@#$%^&*()_+-=[]{}|\;:'\",.<>/?`~" for char in password):
        return False

    return True


@app.route('/add_user', methods=["POST"])
def add_user():
# Get data from form
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password2']
    username = request.form['username']
    phone = request.form['phone']

     # Check for free space
    if not firstName or not lastName or not email or not password1 or not password2 or not username or not phone:
        message = "Please fill in all fields"
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

 # Check if passwords match
    if password1 != password2:
        message = "Passwords do not match. Please try again."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)
    

# Check password requirements
    if not is_valid_password(password1):
        message = "Password must be at least 9 characters long and contain at least one digit, one letter, and one special character."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

# Check if the e-mail address is already registered
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
    existing_email = cursor.fetchone()
    cursor.close()

    if existing_email:
        message = "This email is already registered. Please use a different email address."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

# Check if username is already registered
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customers WHERE username = %s", (username,))
    existing_username = cursor.fetchone()
    cursor.close()

    if existing_username:
        message = "This username is already taken. Please choose a different username."
        return render_template('register.html', message=message, firstName=firstName, lastName=lastName, email=email,
                               username=username, phone=phone)

# Create MySQL cursor
    cur = mysql.connection.cursor()

# Query to insert into database
    cur.execute("INSERT INTO customers(customer_id, name, surname, email, password, username, mobile_phone) VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                (firstName, lastName, email, password1, username, phone))

# Save changes and close cursor
    mysql.connection.commit()
    cur.close()

# Successful registration message
    message = "Registration successful! Please login."
    return redirect('/login?message=' + message)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

# Fetch the user of the e-mail address from the database
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
# Check user session
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
    # Get user's vehicle information
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE customer_id = %s", (user_id,))
        vehicles = cursor.fetchall()
        cursor.close()
        if user:
            email = user[3]
            mobile_phone = user[2]
            name = user[1]
            surname = user[5]
    # Show myprofile key for logged in users
            show_myprofile_button = True
            return render_template('myprofile.html', email=email, mobile_phone=mobile_phone, name=name, surname=surname, show_myprofile_button=show_myprofile_button,vehicles=vehicles)

# Redirect to login page if user is not logged in or logged out
    return redirect('/login.html')

@app.route('/booking.html')
def booking():
# Check user session

    if 'user_id' not in session or not session['user_id']:
      
        return redirect('/login.html')
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
# Get user's vehicle information
        cursor.execute("SELECT * FROM vehicles WHERE customer_id = %s", (user_id,))
        vehicles = cursor.fetchall()
        cursor.close()
# If the user is logged in, render the booking page and also send the license plates
        return render_template('booking.html', vehicles=vehicles)
    else:
# Redirect to login page if user is not logged in
        return redirect('/login.html')
# Update the added function


#booking limit
def get_total_workload_for_date(booking_date):
    cursor = mysql.connection.cursor()
    query = """
    SELECT SUM(s.workload) 
    FROM bookings b 
    JOIN services s ON b.service_id = s.service_id 
    WHERE b.booking_date = %s
    """
    cursor.execute(query, (booking_date,))
    total_workload = cursor.fetchone()[0]
    cursor.close()
    return total_workload if total_workload else 0

@app.route('/add_booking', methods=["POST"])
def add_booking():
    if 'user_id' in session:
        customer_id = session['user_id']
        licence_details = request.form['licence_details']
        booking_type = request.form['booking_type']
        booking_date = request.form['booking_date']
        user_comments = request.form['user_comments']
    
        # Determine service_id based on booking_status
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT service_id, workload FROM services WHERE service_type = %s", (booking_type,))
        result = cursor.fetchone()
        cursor.close()
        
        if not result:
            flash("Invalid service type.", "error")
            return redirect('/booking.html')

        service_id, workload = result

        # Check if total workload will exceed the limit
        current_workload = get_total_workload_for_date(booking_date)
        if current_workload + workload > 20:
            flash("Booking cannot be made as the workload for the day is exceeded.", "error")
            return redirect('/booking.html')

        # Query to get vehicle_id matching license_details
        vehicle_id = get_vehicle_id_by_licence_details(licence_details)
        
        if vehicle_id is None:
            flash("Vehicle with licence details {} not found.".format(licence_details), "error")
            return redirect('/booking.html')
        
        # Call function to add reservation information to database
        add_booking_to_db(customer_id, vehicle_id, service_id, booking_date, user_comments, licence_details)
        flash("Booking added successfully.", "success")
        return redirect('/booking.html')
    else:
        return redirect('/login.html')


# Function to retrieve vehicle_id matching license_details from database
def get_vehicle_id_by_licence_details(licence_details):
    cur = mysql.connection.cursor()
    cur.execute("SELECT vehicle_id FROM vehicles WHERE licence_details = %s", (licence_details,))
    result = cur.fetchone()
    cur.close()
    if result:
        return result[0]
    return None



# Function to add reservation information to the database
def add_booking_to_db(customer_id, vehicle_id, service_id, booking_date, user_comments, licence_details):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO bookings (customer_id, vehicle_id, service_id, booking_date, user_comments, licence_details) VALUES (%s, %s, %s, %s, %s, %s)",
                (customer_id, vehicle_id, service_id, booking_date, user_comments, licence_details))
    mysql.connection.commit()
    cur.close()


@app.route('/prices.html')
def show_parts():

        cursor=mysql.connection.cursor()
        cursor.execute("SELECT part_id, part_name, part_cost FROM parts")
        parts_data = cursor.fetchall()
        print(parts_data)
        cursor.close()

        
        # Sending data to html
        return render_template('prices.html', parts_data=parts_data)
   






@app.route('/logout')
def logout():
    session['user_id'] = ''
    flash("You have been logged out.", "success")

    return redirect('/login.html')



if __name__ == "__main__":
     app.run(debug=True)
    