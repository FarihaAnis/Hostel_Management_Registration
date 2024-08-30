from flask import Flask, render_template, request, redirect, url_for
from models import Base, login_details, account_reg, employee_reg_acc, admin_page
from sqlalchemy import create_engine, select, Column, ForeignKey
from sqlalchemy.orm import sessionmaker
from userinput import keyboardInput
from validate_password import validate_password
from datetime import datetime

app = Flask(__name__)

def getDbConnection(host, username, password, database):
    url = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}"
    engine = create_engine(url)
    return engine
engine = getDbConnection("localhost", "root", "root", "loginpage")

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    Session = sessionmaker(bind=engine)
    session = Session()
    email_address = request.form.get('email')
    password = request.form.get('password')
    
    if not email_address or not password:
        return render_template('login.html', error="Please provide both email and password.")
    
    try:
        # Querying the account_reg table for the provided email
        account = session.query(account_reg).filter_by(email=email_address).first()
        if account:
            # Check if the password matches the one stored in the database
            if account.password == password:
                login = login_details(email=email_address, password=password, account_type="employee")
                session.add(login)
                session.commit()
                return render_template('admin.html')
            else:
                return render_template('login.html', error="Incorrect password.")
        else:
            return render_template('login.html', error="Email address not found.")

    except Exception as e:
        session.rollback()  
        return render_template('login.html', error=str(e))
    finally:
        session.close() 
  
   
@app.route('/account_registration', methods=['GET', 'POST'])
def account_registration():
    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        session = Session()

        # Get form data
        email_address = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        is_valid, message = validate_password(password)
        if not is_valid:
            return render_template('account_reg.html', error=message)

        if password != confirm_password:
            return render_template('account_reg.html', error="Passwords do not match.")

        try:
            new_account = account_reg(email=email_address, password=password)
            session.add(new_account)
            session.commit()
            return redirect(url_for('employee_registration'))
        except Exception as e:
            session.rollback()
            return render_template('account_reg.html', error=str(e))
        finally:
            session.close()

    return render_template('account_reg.html')


@app.route('/employee_registration', methods=['GET', 'POST'])
def employee_registration():
    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        session = Session()

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        job_title = request.form.get('job_title')
        department = request.form.get('department')
        gender = request.form.get('gender')
        date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date()
        marital_status = request.form.get('marital_status')
        email = request.form.get('email')
        contact_number = request.form.get('contact_number')
        street_address = request.form.get('street_address')
        city = request.form.get('city')
        state = request.form.get('state')
        postcode = request.form.get('postcode')
        country = request.form.get('country')
        

        try:
            latest_account = session.query(account_reg).filter_by(email=email).first()
            if latest_account is None:
                raise Exception("No account registration found for this email. Please create an account first.")
            
            new_employee = employee_reg_acc(
                first_name=first_name,
                last_name=last_name,
                job_title=job_title,
                department=department,
                gender=gender,
                date_of_birth=date_of_birth,
                marital_status=marital_status,
                email=email,
                contact_number=contact_number,
                street_address=street_address,
                city=city,
                state=state,
                postcode=postcode,
                country=country,
                employee_id=latest_account.id
            )
            session.add(new_employee)
            session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            session.rollback()
            return render_template('employee_reg.html', error=str(e))
        finally:
            session.close()
    return render_template('employee_reg.html')

@app.route('/admin')
def admin():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        organizations = session.query(admin_page).all()
        return render_template('admin.html', organizations=organizations)
    finally:
        session.close()

@app.route('/delete', methods=['POST'])
def delete_registration():
    Session = sessionmaker(bind=engine)
    session = Session()
    approval_id = request.form.get('id')  # Correctly retrieve the ID from the form
    try:
        # Query the admin_page table to find the record by ID
        registration = session.query(admin_page).filter_by(id=approval_id).first()
        if registration:
            session.delete(registration)
            session.commit()

        # After deletion, re-query the database to get the updated list of organizations
        organizations = session.query(admin_page).all()
        return render_template('admin.html', organizations=organizations)
    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
