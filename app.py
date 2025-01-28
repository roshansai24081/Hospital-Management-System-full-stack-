from flask import Flask,render_template,request,flash,url_for,session,redirect,send_file
from fpdf import FPDF
import random
from io import BytesIO
import mysql.connector
mydb=mysql.connector.connect(host='localhost',
user='root',
password='root',
db='project_hm')

app=Flask(__name__)
app.secret_key='abkqkcsaiwhfdq'


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Adjust the host if required
        user="root",  # Provide your MySQL username
        password="root",  # Provide your MySQL password
        database="project_hm"  # Provide your database name
    )

@app.route('/')
def home():
    return render_template('hospital_main_dashboard.html')

from flask import render_template, request, redirect, url_for, flash
import mysql.connector

@app.route('/signup/admin', methods=['GET', 'POST'])
def signup_admin():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if all fields are filled
        if not (name and email and password):
            flash("Please fill in all fields", "error")
            return redirect(url_for('signup_admin'))  # Redirect back to sign-up page if any field is missing

        try:
            # Establishing the connection
            mydb = mysql.connector.connect(host='localhost',user='root',password='root',db='project_hm')
            # Ensuring the cursor is created only after the connection is successful
            cursor = mydb.cursor()

            # Check if the email already exists in the database
            cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
            existing_admin = cursor.fetchone()

            if existing_admin:
                flash("Email already registered", "error")
                return redirect(url_for('signup_admin'))  # Redirect back if email exists

            # Insert the new admin into the database
            cursor.execute(
                "INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            mydb.commit()  # Commit the transaction to save data

            flash("Sign-up successful! Please log in.", "success")
            return redirect(url_for('signin_admin'))  # Redirect to sign-in page after successful sign-up

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for('signup_admin'))  # Redirect back to sign-up on error

        finally:
            # Ensure that cursor and connection are closed properly
            if cursor:
                cursor.close()
            if mydb:
                mydb.close()

    # For GET request, simply render the signup page
    return render_template('signup_admin.html')
@app.route('/signin/admin', methods=['GET', 'POST'])
def signin_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please fill in both fields", "error")
            return redirect(url_for('signin_admin'))  # Redirect back to the sign-in page

        cursor = None  # Initialize the cursor variable before the try block

        try:
            mydb = mysql.connector.connect(host='localhost',user='root',password='root',db='project_hm')
            cursor = mydb.cursor()  # Now initialize the cursor inside the try block

            # Query to check if the admin exists with the given email
            cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
            admin = cursor.fetchone()

            if admin:
                # Verify if the password matches
                stored_password = admin[3]  # Assuming the password is the 4th column in the 'admins' table
                if stored_password == password:
                    flash("Login successful", "success")
                    return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard
                else:
                    flash("Incorrect password", "error")
            else:
                flash("No admin found with that email", "error")

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
        finally:
            if cursor:
                cursor.close()  # Close the cursor only if it was successfully initialized
            if mydb:
                mydb.close()  # Close the database connection

    return render_template('signin_admin.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/signup/doctor', methods=['GET', 'POST'])
def signup_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        specialty = request.form.get('specialty')  # Specialty for the doctor

        # Validate form data
        if not (name and email and password and specialty):
            flash("All fields are required.", "error")
            return redirect(url_for('signup_doctor'))  # Redirect back if any field is missing

        try:
            cursor = mydb.cursor()

            # Check if the email already exists
            cursor.execute("SELECT * FROM doctors WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("An account with this email already exists.", "error")
                return redirect(url_for('signup_doctor'))

            # Insert doctor data into the doctors table
            cursor.execute("""
                INSERT INTO doctors (name, email, password, specialty)
                VALUES (%s, %s, %s, %s)
            """, (name, email, password, specialty))
            mydb.commit()  # Commit the transaction to save data

            flash("Doctor signup successful. Please log in.", "success")
            return redirect(url_for('signin_doctor'))  # Redirect to the login page after successful signup

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")

        finally:
            if cursor:
                cursor.close()

    return render_template('signup_doctor.html') 


@app.route('/signin/doctor', methods=['GET', 'POST'])
def signin_doctor():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please fill in both fields", "error")
            return redirect(url_for('signin_doctor'))

        cursor = None
        try:
            # Ensure the database connection exists
            if not mydb.is_connected():
                mydb.reconnect()

            # Create a cursor object
            cursor = mydb.cursor()

            # Query to check if the doctor exists with the given email
            cursor.execute("SELECT * FROM doctors WHERE email = %s", (email,))
            doctor = cursor.fetchone()

            if doctor:
                # Verify if the password matches
                stored_password = doctor[3]  # Assuming the password is the 4th column in the 'doctors' table
                if stored_password == password:
                    flash("Login successful", "success")
                    return redirect(url_for('doctor_dashboard'))  # Redirect to doctor dashboard
                else:
                    flash("Incorrect password", "error")
            else:
                flash("No doctor found with that email", "error")

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
        finally:
            # Ensure cursor is closed if it was initialized
            if cursor:
                cursor.close()

    # For GET requests, render the sign-in page
    return render_template('signin_doctor.html')



@app.route('/doctor/dashboard')
def doctor_dashboard():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            appointment_id AS patient_id, 
            CONCAT(first_name, ' ', last_name) AS name, 
            timeslot 
        FROM 
            approved_appointments 
        WHERE 
            status = 'approved'
    """
    cursor.execute(query)
    patients = cursor.fetchall()
    print("Patients Data:", patients)  # Debugging line
    cursor.close()
    connection.close()
    return render_template('doctor_dashboard.html', patients=patients)


@app.route('/patient/<int:patient_id>')
def patient_details(patient_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                appointment_id, 
                first_name, 
                last_name, 
                email, 
                phone, 
                medical_condition, 
                medications, 
                allergies, 
                doctor_name, 
                appointment_date, 
                timeslot 
            FROM 
                approved_appointments 
            WHERE 
                appointment_id = %s
        """
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()
    except Exception as e:
        print("Database error:", e)
        return "An error occurred while fetching the patient details.", 500
    finally:
        cursor.close()
        connection.close()

    if patient:
        return render_template('doctor_patient_details.html', patient=patient)
    else:
        return "Patient not found", 404





@app.route('/signup/patient', methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone_number = request.form.get('phone_number')

        # Check for missing fields
        if not (name and email and password and confirm_password and phone_number):
            flash("All fields are required.", "error")
            return redirect(url_for('signup_patient'))

        # Check password confirmation
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('signup_patient'))

        try:
            cursor = mydb.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM patients WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("An account with this email already exists.", "error")
                return redirect(url_for('signup_patient'))

            # Insert the new patient into the database
            cursor.execute(
                """
                INSERT INTO patients (name, email, password, phone_number)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, password, phone_number)
            )
            mydb.commit()

            flash("Signup successful. Please sign in.", "success")
            return redirect(url_for('signin_patient'))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for('signup_patient'))

        finally:
            if 'cursor' in locals():
                cursor.close()

    return render_template('signup_patient.html')

@app.route('/signin/patient', methods=['GET', 'POST'])
def signin_patient():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        if not (email and password):
            flash("Please fill in both fields.", "error")
            return redirect(url_for('signin_patient'))

        try:
            cursor = mydb.cursor()

            # Query to check if the patient exists with the given email
            cursor.execute("SELECT patient_id, email, password FROM patients WHERE email = %s", (email,))
            patient = cursor.fetchone()

            if patient:
                stored_password = patient[2]  # Assuming password is the 3rd column (index 2)
                if stored_password == password:
                    flash("Login successful.", "success")
                    # Using patient_id to pass to the portal
                    return redirect(url_for('patient_portal', patient_id=patient[0]))  # patient[0] should be the patient_id
                else:
                    flash("Incorrect password.", "error")
            else:
                flash("No account found with that email.", "error")

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")

        finally:
            if 'cursor' in locals():
                cursor.close()

    return render_template('signin_patient.html')


@app.route('/patient_portal/<int:patient_id>', methods=['GET'])
def patient_portal(patient_id):
    # Establish a database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch patient details based on patient_id
        cursor.execute("""
            SELECT 
                name, 
                phone_number AS contact, 
                email 
            FROM patients 
            WHERE patient_id = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        # Check if patient exists
        if not patient:
            return "Patient not found", 404

        # Fetch approved appointments for the patient using the email
        cursor.execute("""
            SELECT 
                appointment_id, 
                appointment_date, 
                timeslot, 
                doctor_name, 
                status 
            FROM approved_appointments 
            WHERE email = %s
        """, (patient['email'],))
        appointments = cursor.fetchall()

        # Render the patient portal template with fetched data
        return render_template(
            'patient_dashboard.html',
            patient=patient,
            appointments=appointments
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Error retrieving data", 500

    finally:
        cursor.close()
        connection.close()

          
@app.route('/appointment', methods=['GET', 'POST'])
def appointment_form():
    try:
        cursor = mydb.cursor(dictionary=True)

        # Fetch doctor names for the dropdown
        cursor.execute("SELECT doctor_id, name FROM doctors")
        doctors = cursor.fetchall()

        if request.method == 'POST':
            # Retrieve form data
            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            medical_condition = request.form.get('medical-condition')
            medications = request.form.get('medications')
            allergies = request.form.get('allergies')
            doctor_id = request.form.get('doctor')
            appointment_date = request.form.get('appointment-date')
            timeslot = request.form.get('timeslot')

            # Insert data into the appointments table with status set to 'Pending'
            cursor.execute(
                """
                INSERT INTO appointments 
                (first_name, last_name, email, phone, medical_condition, medications, allergies, doctor_id, appointment_date, timeslot, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (first_name, last_name, email, phone, medical_condition, medications, allergies, doctor_id, appointment_date, timeslot, 'Pending')
            )
            mydb.commit()

            # Pass the success message to the frontend
            success_message = "Appointment booked successfully! The status is set to 'Pending'."
            return render_template('appointment_form.html', doctors=doctors, success_message=success_message)

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "error")
    finally:
        cursor.close()

    # Render the form with the doctors' data
    return render_template('appointment_form.html', doctors=doctors)

@app.route('/active_patients')
def active_patients():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Query to fetch active patients
        cursor.execute("""
            SELECT appointment_id AS patient_id,
       CONCAT(first_name, ' ', last_name) AS name,
       CONCAT(appointment_date, ' ', timeslot) AS Timeslot,
       `Medical_condition` AS "condition"
        FROM approved_appointments;

        """)

        active_patients = cursor.fetchall()
        
        # Render the active patients template with the data
        return render_template('admin_patients_list.html', patients=active_patients)
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error fetching active patients", 500
    
    finally:
        cursor.close()
        connection.close()


@app.route('/view_patient/<int:patient_id>')
def view_patient(patient_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch the full details of the patient by their ID
        cursor.execute("""
            SELECT * 
            FROM approved_appointments
            WHERE appointment_id = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        if patient:
            # Render the details page for the patient
            return render_template('view_patient.html', patient=patient)
        else:
            return "Patient not found", 404

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error fetching patient details", 500

    finally:
        cursor.close()
        connection.close()

@app.route('/to_discharge_patient1', methods=['POST'])
def to_discharge_patient1():
    patient_id = request.form.get('patient_id')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Fetch results as a dictionary

    try:
        # Fetch the patient's details explicitly selecting the necessary columns
        cursor.execute("""
            SELECT appointment_id, first_name, last_name, appointment_date, timeslot, medical_condition,doctor_name
            FROM approved_appointments
            WHERE appointment_id = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        if patient:
            # Insert the patient into the ready_to_discharge table
            cursor.execute("""
                INSERT INTO ready_to_discharge (appointment_id, first_name, last_name, appointment_date, timeslot, medical_condition,doctor_name)
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            """, (patient['appointment_id'], patient['first_name'], patient['last_name'],
                  patient['appointment_date'], patient['timeslot'], patient['medical_condition'], patient['doctor_name']))

            # Delete the patient from the approved_appointments table
            cursor.execute("""
                DELETE FROM approved_appointments WHERE appointment_id = %s
            """, (patient_id,))

            connection.commit()

            # Redirect back to the active patients page
            return redirect(url_for('active_patients'))

        else:
            return "Patient not found", 404

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error discharging patient", 500

    finally:
        cursor.close()
        connection.close()
@app.route('/to_discharge_patient2', methods=['POST'])
def to_discharge_patient2():
    patient_id = request.form.get('patient_id')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Fetch results as a dictionary

    try:
        # Fetch the patient's details explicitly selecting the necessary columns
        cursor.execute("""
            SELECT appointment_id, first_name, last_name, appointment_date, timeslot, medical_condition,doctor_name
            FROM approved_appointments
            WHERE appointment_id = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        if patient:
            # Insert the patient into the ready_to_discharge table
            cursor.execute("""
                INSERT INTO ready_to_discharge (appointment_id, first_name, last_name, appointment_date, timeslot, medical_condition,doctor_name)
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            """, (patient['appointment_id'], patient['first_name'], patient['last_name'],
                  patient['appointment_date'], patient['timeslot'], patient['medical_condition'], patient['doctor_name']))

            # Delete the patient from the approved_appointments table
            cursor.execute("""
                DELETE FROM approved_appointments WHERE appointment_id = %s
            """, (patient_id,))

            connection.commit()

            # Redirect back to the active patients page
            return redirect(url_for('doctor_dashboard'))

        else:
            return "Patient not found", 404

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error discharging patient", 500

    finally:
        cursor.close()
        connection.close()
@app.route('/pending_appointments')
def pending_appointments():
    cursor = mydb.cursor(dictionary=True)
    
    try:
        # Fetch pending appointments, including the doctor's name
        cursor.execute("""
            SELECT 
                appointment_id AS id,
                CONCAT(first_name, ' ', last_name) AS name,
                appointment_date AS date,
                timeslot AS time,
                (SELECT name FROM doctors WHERE doctors.doctor_id = appointments.doctor_id) AS requested_doctor_name
            FROM 
                appointments
            WHERE 
                status = 'pending';
        """)

        # Fetch all the results
        appointments = cursor.fetchall()

        # Fetch all doctors for the dropdown list
        cursor.execute("SELECT doctor_id, name FROM doctors")
        doctors = cursor.fetchall()

        # Render the template with the fetched data
        return render_template('admin_pending_patient_appointments.html', appointments=appointments, doctors=doctors)

    except mysql.connector.Error as err:
        # Handle database error
        print(f"Database error: {err}")
        return "An error occurred with the database."

    finally:
        # Close the cursor and the database connection
        cursor.close()

@app.route('/approve_appointment', methods=['POST'])
def approve_appointment():
    appointment_id = request.form.get('appointment_id')
    doctor_name=request.form.get('doctor_name')
    doctor_id = request.form.get('doctor')  # Selected doctor by the admin
    timeslot = request.form.get('timeslot')  # Selected timeslot by the admin

    cursor = mydb.cursor(dictionary=True)  # Using dictionary cursor to get the result in dictionary form

    try:
        # Retrieve the appointment details
        cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if appointment:
            # Move the appointment to the approved appointments table with updated doctor and timeslot
            cursor.execute("""
                INSERT INTO approved_appointments 
                (appointment_id, first_name, last_name, email, phone, 
                 medical_condition, medications, allergies, doctor_id, doctor_name,
                 appointment_date, timeslot, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (appointment['appointment_id'], appointment['first_name'], appointment['last_name'], 
                  appointment['email'], appointment['phone'], appointment['medical_condition'], 
                  appointment['medications'], appointment['allergies'], doctor_id, doctor_name,
                  appointment['appointment_date'], timeslot, 'approved'))  # 'approved' as the status

            # Now, delete the approved appointment from the appointments table
            cursor.execute("""
                DELETE FROM appointments
                WHERE appointment_id = %s
            """, (appointment_id,))

            mydb.commit()

        return redirect('/pending_appointments')  # Redirect to the pending appointments page

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error approving appointment", 500
    finally:
        cursor.close()
        
@app.route('/ready_to_discharge')
def ready_to_discharge():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch all patients from the ready_to_discharge table
        cursor.execute("""
            select appointment_id as patient_id, CONCAT(first_name, ' ', last_name) AS patient_name, doctor_name from ready_to_discharge;
        """)
        patients = cursor.fetchall()

        return render_template('ready_to_discharge.html', patients=patients)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error fetching data", 500

    finally:
        cursor.close()
        connection.close()

@app.route('/generate_invoice/<int:appointment_id>', methods=['POST'])
def generate_invoice(appointment_id):
    # Establish a database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch the appointment details using appointment_id
        cursor.execute("""
            SELECT 
                a.appointment_id, 
                a.email AS patient_email, 
                p.name AS patient_name, 
                p.patient_id 
            FROM approved_appointments a
            JOIN patients p ON a.email = p.email
            WHERE a.appointment_id = %s
        """, (appointment_id,))
        appointment_data = cursor.fetchone()

        # Check if the appointment and patient exist
        if appointment_data is None:
            return "Patient not found", 404

        # Extract patient info from the query result
        patient_name = appointment_data['patient_name']
        patient_id = appointment_data['patient_id']

        # Generate random room number and charges as before
        room_number = random.randint(101, 200)
        consultation_fee = 150  # Example consultation fee in dollars
        room_charge = random.randint(100, 500)  # Random room charge
        additional_charges = random.randint(50, 100)  # Additional charges

        total_amount = consultation_fee + room_charge + additional_charges

        # Create PDF for the invoice
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Invoice for Patient: {patient_name}", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Patient ID: {patient_id}", ln=True)
        pdf.cell(200, 10, txt=f"Room Number: {room_number}", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Consultation Fee: ${consultation_fee}", ln=True)
        pdf.cell(200, 10, txt=f"Room Charge: ${room_charge}", ln=True)
        pdf.cell(200, 10, txt=f"Additional Charges: ${additional_charges}", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Total Amount Due: ${total_amount}", ln=True)

        # Output the PDF file
        invoice_filename = f"invoice_{patient_id}.pdf"
        pdf.output(invoice_filename)

        # Return the generated invoice as a downloadable PDF
        return send_file(invoice_filename, as_attachment=True)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Error generating invoice", 500

    finally:
        cursor.close()
        connection.close()



@app.route('/discharge_patient', methods=['POST'])
def discharge_patient():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get the patient ID from the form
        patient_id = request.form['patient_id']

        # Fetch the patient record from ready_to_discharge
        cursor.execute("""
            SELECT * FROM ready_to_discharge
            WHERE appointment_id = %s;
        """, (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            return "Patient not found", 404

        # Insert the patient record into discharged_patients table
        cursor.execute("""
            INSERT INTO discharged_patients (appointment_id, first_name, last_name, doctor_name, discharge_date)
            VALUES (%s, %s, %s, %s, NOW());
        """, (patient['appointment_id'], patient['first_name'], patient['last_name'], patient['doctor_name']))

        # Remove the patient record from ready_to_discharge
        cursor.execute("""
            DELETE FROM ready_to_discharge
            WHERE appointment_id = %s;
        """, (patient_id,))

        # Commit the changes to the database
        connection.commit()

        # Redirect back to the "Ready to Discharge" page
        return redirect('/ready_to_discharge')

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error discharging patient", 500

    finally:
        cursor.close()
        connection.close()

@app.route('/discharged_patients')
def discharged_patients():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch all discharged patients
        cursor.execute("""
            SELECT appointment_id AS id, CONCAT(first_name, ' ', last_name) AS name, doctor_name
            FROM discharged_patients;
        """)
        patients = cursor.fetchall()

        return render_template('discharged_patients.html', patients=patients)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error fetching discharged patients", 500

    finally:
        cursor.close()
        connection.close()
@app.route('/doctors')
def doctors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Fetch the list of doctors from the database (assuming there's a 'name' column)
        cursor.execute("SELECT doctor_id, name FROM doctors")
        doctors = cursor.fetchall()

        # Check if doctors data is empty, print to debug
        print(doctors)

        # Render the template with the list of doctors
        return render_template('doctor_management.html', doctors=doctors)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error fetching data", 500

    finally:
        cursor.close()
        connection.close()

@app.route('/careers')
def careers():
    # Sample job listings, you would typically fetch these from a database
    job_listings = [
        {"title": "Registered Nurse", "description": "We are looking for a compassionate and skilled registered nurse to join our team in the Emergency Department.", "apply_link": "/apply/registered_nurse"},
        {"title": "Medical Laboratory Technician", "description": "We need a detail-oriented Medical Laboratory Technician to support our diagnostic testing team.", "apply_link": "/apply/medical_laboratory_technician"},
        {"title": "Hospital Administrator", "description": "We are seeking a Hospital Administrator with experience in healthcare management.", "apply_link": "/apply/hospital_administrator"},
    ]
    return render_template('careers.html', job_listings=job_listings)


@app.route('/apply/<job_title>')
def apply(job_title):
    return render_template('application_form.html', job_title=job_title)

@app.route('/submit-application', methods=['POST'])
def submit_application():
    job_title = request.form['job_title']
    full_name = request.form['full_name']
    email = request.form['email']
    phone = request.form['phone']
    cover_letter = request.form['cover_letter']

    # Establish database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the form data into the JobApplications table
    insert_query = '''
        INSERT INTO JobApplications (job_title, full_name, email, phone, cover_letter)
        VALUES (%s, %s, %s, %s, %s);
    '''
    cursor.execute(insert_query, (job_title, full_name, email, phone, cover_letter))
    conn.commit()  # Commit the transaction

    # Close the connection
    cursor.close()
    conn.close()

    # Redirect to a confirmation page (or the job listings page)
    return redirect(url_for('careers'))


@app.route('/admin/job-approvals')
def job_approvals():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Select all job applications with pending status
    cursor.execute('SELECT id, job_title, full_name, email, phone, cover_letter, status FROM JobApplications')
    applications = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return render_template('pending_applications.html', applications=applications)

# Route to approve or reject a job application
@app.route('/admin/approve-reject/<int:application_id>/<status>', methods=['POST'])
def approve_reject(application_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the status of the job application (approved or rejected)
    cursor.execute('UPDATE JobApplications SET status = %s WHERE id = %s', (status, application_id))
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    # Redirect back to the job approvals page
    return redirect(url_for('job_approvals'))



if __name__=='__main__':
    app.run(debug=True)