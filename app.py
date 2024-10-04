<<<<<<< HEAD
from flask import *
from flask_login import *
import os
from flask_sqlalchemy import *
from sqlalchemy import *
from datetime import *
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from sqlalchemy.orm import validates
import random
from werkzeug.security import *
import secrets
from colorama import *
from random import *
import random
import qrcode
from io import *

# App config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    nif = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    cellphone = db.Column(db.String(20))
    create_date = db.Column(db.String(20))
    last_login = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Operational")
    role = db.Column(db.String(40))
    user_type = db.Column(db.String(50), default="Client")
    pin = db.Column(db.Integer, unique=True)

    product_movements = db.relationship('ProductMovements', back_populates='user', lazy=True)
    permissions = db.relationship("UserPermissions", uselist=False, back_populates="user")
    logs = db.relationship('WorkSchedulesLogs', backref='user', lazy=True)
    assigned_schedules = db.relationship('AssignedSchedules', backref='user_assigned_schedules', lazy=True)
    sales = db.relationship('Sales', back_populates='user', lazy=True)

    def __init__(self, username, password, nif, email, name, cellphone, role=None, last_login=None, status="Operational", user_type="Client"):
        self.username = username
        self.password = password
        self.nif = nif
        self.email = email
        self.name = name.title()
        self.cellphone = cellphone
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_login = last_login
        self.status = status.capitalize()
        self.role = role
        self.user_type = user_type.capitalize()
        self.pin = random.randint(10000, 99999)

class UserPermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    can_adjust_inventory_differences = db.Column(db.Boolean, default=False)
    can_manage_suppliers = db.Column(db.Boolean, default=False)
    can_view_temperature_logs = db.Column(db.Boolean, default=False)
    can_adjust_temperature_discrepancies = db.Column(db.Boolean, default=False)
    can_access_high_security_areas = db.Column(db.Boolean, default=False)
    can_generate_financial_reports = db.Column(db.Boolean, default=False)
    can_manage_user_permissions = db.Column(db.Boolean, default=False)
    can_view_audit_logs = db.Column(db.Boolean, default=False)
    can_override_automatic_system_flags = db.Column(db.Boolean, default=False)
    can_manage_orders = db.Column(db.Boolean, default=False)
    can_create_new_users = db.Column(db.Boolean, default=False)
    can_active_users = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='permissions')

    def __init__(self, user_id, can_adjust_inventory_differences=False, can_manage_suppliers=False, can_view_temperature_logs=False, can_adjust_temperature_discrepancies=False,can_access_high_security_areas=False, can_generate_financial_reports=False, can_manage_user_permissions=False, can_view_audit_logs=False, can_override_automatic_system_flags=False, can_manage_orders=False, can_create_new_users=False, can_active_users=False):
        self.user_id = user_id
        self.can_adjust_inventory_differences = can_adjust_inventory_differences
        self.can_manage_suppliers = can_manage_suppliers
        self.can_view_temperature_logs = can_view_temperature_logs
        self.can_adjust_temperature_discrepancies = can_adjust_temperature_discrepancies
        self.can_access_high_security_areas = can_access_high_security_areas
        self.can_generate_financial_reports = can_generate_financial_reports
        self.can_manage_user_permissions = can_manage_user_permissions
        self.can_view_audit_logs = can_view_audit_logs
        self.can_override_automatic_system_flags = can_override_automatic_system_flags
        self.can_manage_orders = can_manage_orders
        self.can_create_new_users = can_create_new_users
        self.can_active_users = can_active_users

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(20))
    qr_code_path = db.Column(db.String(100))
    name = db.Column(db.String(50))
    product_type = db.Column(db.String(25))
    brand = db.Column(db.String(30))
    model = db.Column(db.String(30))
    buy_price = db.Column(db.Float)
    sell_price = db.Column(db.Float)
    margin = db.Column(db.Float)
    stock = db.Column(db.Integer)
    min_recommended_stock = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    last_update = db.Column(db.String(14))
    warehouse_section = db.Column(db.String)
    warehouse_shelf = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Active")
    update_info = db.Column(db.String(20))

    product_movements = db.relationship('ProductMovements', back_populates='product', lazy=True)
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True)
    sales = db.relationship('Sales', back_populates='product', lazy=True)

    def __init__(self, ref, qr_code_path, name, product_type, brand, model, buy_price, sell_price, margin, stock, min_recommended_stock, last_update, update_info, warehouse_section, warehouse_shelf, status="Active"):
        self.ref = ref
        self.qr_code_path = qr_code_path
        self.name = name.upper()
        self.product_type = product_type
        self.brand = brand.title()
        self.model = model.title()
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.margin = margin
        self.stock = stock
        self.min_recommended_stock = min_recommended_stock
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_update = last_update
        self.status = status.capitalize()
        self.update_info = update_info
        self.warehouse_section = warehouse_section
        self.warehouse_shelf = warehouse_shelf

class ProductMovements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    movement_type = db.Column(db.String(50), default="Stock Entry")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    invoice_number = db.Column(db.String(30))
    justification = db.Column(db.String(100), default="Customer Purchase")

    product = db.relationship('Product', back_populates='product_movements')
    supplier = db.relationship('Suppliers', back_populates='product_movements')
    user = db.relationship('User', back_populates='product_movements')

    def __init__(self, product_id, supplier_id=None, movement_type="Stock Entry", user_id=None, quantity=0, invoice_number=None, justification="Customer Purchase"):
        self.product_id = product_id
        self.supplier_id = supplier_id
        self.movement_type = movement_type
        self.user_id = user_id
        self.quantity = quantity
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.invoice_number = invoice_number
        self.justification = justification

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(20))
    contact_name = db.Column(db.String(30))
    contact_email = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    type = db.Column(db.String(30))
    country = db.Column(db.String(30))
    adress = db.Column(db.String(50))
    payment_terms = db.Column(db.String(15))
    credit_limit = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    last_order_date = db.Column(db.String(14))
    rating = db.Column(db.Integer)

    product_movements = db.relationship('ProductMovements', back_populates='supplier', lazy=True)

    def __init__(self, supplier_name, contact_name, contact_email, contact_phone, type, country, adress, payment_terms, credit_limit, last_order_date, rating):
        self.supplier_name = supplier_name
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.type = type
        self.country = country
        self.adress = adress
        self.payment_terms = payment_terms
        self.credit_limit = credit_limit
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_order_date = last_order_date
        self.rating = rating

class LogTemperatures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature_id = db.Column(db.Integer, db.ForeignKey('temperatures.id'))
    current_temperature = db.Column(db.Float)
    justification = db.Column(db.String(100))
    create_date = db.Column(db.String(20))

    temperature = db.relationship('Temperatures', back_populates='logs')

    def __init__(self, temperature_id, current_temperature, justification=None):
        self.temperature_id = temperature_id
        self.current_temperature = current_temperature
        self.justification = justification
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')

class Temperatures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_section = db.Column(db.Integer)
    warehouse_deep_freezer = db.Column(db.Integer)
    recommended_temperature = db.Column(db.Float)

    logs = db.relationship('LogTemperatures', back_populates='temperature', lazy=True)

    def __init__(self, warehouse_section, warehouse_deep_freezer, recommended_temperature):
        self.warehouse_section = warehouse_section
        self.warehouse_deep_freezer = warehouse_deep_freezer
        self.recommended_temperature = recommended_temperature

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.String(20))
    
    items = db.relationship('OrderItem', back_populates='order', lazy=True)

    def __init__(self, user_id, order_date=None):
        self.user_id = user_id
        self.order_date = order_date if order_date else datetime.now().strftime('%d/%m/%Y %H:%M')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    
    product = db.relationship('Product', back_populates='order_items')
    order = db.relationship('Order', back_populates='items')

    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    type = db.Column(db.String, default = "In")
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    is_viewed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='notifications')
    message = db.relationship('Message', backref='notifications')

class WorkSchedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule  = db.Column(db.String(5), unique = True)
    time_in = db.Column(db.String(15))
    time_out = db.Column(db.String(15))
    lunch_start = db.Column(db.String(15))
    lunch_end = db.Column(db.String(15))

    logs = db.relationship('WorkSchedulesLogs', backref='work_schedule', lazy=True)

    def __init__(self, schedule, time_in, time_out, lunch_start, lunch_end):
        self.schedule = schedule
        self.time_in = time_in
        self.time_out = time_out
        self.lunch_start = lunch_start
        self.lunch_end = lunch_end

class WorkSchedulesLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('work_schedules.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date_in = db.Column(db.String(30))
    log_type = db.Column(db.String(10), default="Manual")
    record_type = db.Column(db.String(10))
    justification = db.Column(db.String)
    status = db.Column(db.String(20), default="Approved")
    notes = db.Column(db.String)

    def __init__(self, schedule_id, user_id, create_date_in, notes, record_type, log_type="Manual", justification="", status="Approved"):
        self.schedule_id = schedule_id
        self.user_id = user_id
        self.create_date_in = create_date_in
        #datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.log_type = log_type
        self.justification = justification
        self.status = status
        self.record_type = record_type
        self.notes = notes

class AssignedSchedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('work_schedules.id'))
    date = db.Column(db.String)
    status = db.Column(db.String(20), default="Pending")
    is_active = db.Column(db.Boolean, default=False)
    previous_schedule_id = db.Column(db.Integer, db.ForeignKey('assigned_schedules.id'))

    user = db.relationship('User', lazy=True, overlaps="assigned_schedules,user_assigned_schedules")
    schedule = db.relationship('WorkSchedules', backref='assigned_schedules', lazy=True)
    previous_schedule = db.relationship('AssignedSchedules', remote_side=[id], backref='replaced_by')

    def __init__(self, user_id, schedule_id, date, status, is_active, previous_schedule_id):
        self.user_id = user_id
        self.schedule_id = schedule_id
        self.date = date
        self.status = status
        self.is_active = is_active
        self.previous_schedule_id = previous_schedule_id

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_name = db.Column(db.String(100))
    quantity_sold = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Completed")
    
    product = db.relationship('Product', back_populates='sales')
    user = db.relationship('User', back_populates='sales') 
    
    def __init__(self, product_id, quantity_sold, user_id=None, customer_name=None, status="Completed"):
        self.product_id = product_id
        self.quantity_sold = quantity_sold
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M') 
        self.user_id = user_id
        self.customer_name = customer_name
        self.status = status

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String, unique=True)

    def __init__(self, brand_name):
        self.brand_name = brand_name

class ProductTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String, unique=True)

    def __init__(self, product_type):
        self.product_type = product_type

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = "cubix.w.noreply@gmail.com"
SMTP_PASSWORD = "pcyt epef eezt nofr"  

# Default Email Configuration
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        # Enviar o email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        print(f"{Fore.GREEN}Email enviado com sucesso para {to_email}.")
    
    except Exception as e:
        print(f"{Fore.RED}Falha ao enviar email para {to_email}. Erro: {e}")

# Registration Email
def send_registration_email(user, plain_password):
    subject = "Welcome to Our Service!"
    body = f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Email | Cubix</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: Arial, sans-serif;">

    <!-- Main Container  -->
    <div style="max-width: 600px; margin: 0 auto; background-color: #181a1e; padding: 20px; border-radius: 8px;">

        <!-- Header -->
        <div style="text-align: center; padding: 10px 0;">
            <img src="https://i.postimg.cc/Hkfrz86R/Cubix-White.png" alt="Cubix Logo" style="width: 100px; margin-bottom: 20px;">
        </div>

        <!-- Main content -->
        <div style="background-color: #181a1e; color: #ffffff; padding: 20px; border-radius: 8px;">
            <h1 style="color: #ffffff; text-align: center;">Welcome to <span style="color: #ff0060;">Cubix!</span></h1>
            <p style="color: #ffffff;">Hi <span style="color: #ff0060;">{user.name}</span>,</p>
            <p style="color: #ffffff;">Thank you for registering on our platform.</p>
            <p style="color: #ffffff;">We are providing you with the login credentials for your account as requested. Below are your username and <span style="color: #f7d060; text-decoration: underline; font-size: 1.05rem;">temporary password</span> to access the platform. <span style="color: #1b9c85; font-size: 1.05rem;">We recommend changing the password upon your first login to ensure your account's security.</span></p>
            <p style="color: #ffffff; margin-top: 3rem;">Username: <span style="color: #1b9c85; font-size: 1.2rem;">{user.username}</span></p>
            <p style="color: #ffffff; margin-bottom: 3rem;">Temporary Password: <span style="color: #1b9c85; margin-top: 1rem; font-size: 1.2rem;">{plain_password}</span></p>
            <p style="color: #ffffff;">Best regards,</p>
            <p style="color: #ffffff;">Your Company Team</p>
        </div>

        <!-- Footer -->
        <div style="text-align: center; color: #ffffff; background-color: #181a1e; padding: 10px; border-radius: 8px; margin-top: 20px;">
            <p style="margin: 0;">Please be advised that this email was generated automatically from a non-monitored account. We kindly ask that you <span style="color: #ff0060;">do not reply directly to this message.</span></p>
            <p style="margin: 0;">For any assistance or inquiries, please contact our support team through the designated channels.</p>
            <p style="margin: 0;">For any authentication-related inquiries, please send an email to <span style="color: #1b9c85; font-size: 1.05rem;">brunovcoelho.dev@gmail.com</span> or <a href="https://wa.me/351965576916?text=Hello,%0A%0AI%20require%20assistance%20regarding%20authentication%20issues%20with%20my%20account.%0A%0AThank%20you%20for%20your%20attention.%0A%0ABest%20regards." target="_blank" style="text-decoration: none; color: #f7d060;">click here</a> to reach our support team.</p>
        </div>
    </div>

</body>
</html>
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_EMAIL
    msg['To'] = user.email

    # Adicionar o conteúdo HTML ao email
    msg.add_alternative(body, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  # Ativa a criptografia
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
            print(f"Email successfully sent to {user.email}")
    except Exception as e:
        print(f"Failed to send email to {user.email}. Error: {e}")

# Forgot Password Email
def send_password_reset_email(user, new_password):
    subject = "Your Password Has Been Reset"
    body = f"""
    Hi {user.name},

    Your password has been reset. Your new password is: {new_password}

    Please log in and change your password as soon as possible.

    Best regards,
    Your Company Team
    """
    send_email(user.email, subject, body)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Validates user type
@validates("user_type")
def validate_user_type(self, key, user_type):
    allowed_types = ["Admin", "Manager", "Employee", "Client"]
    assert user_type in allowed_types, f"Invalid user type. Allowed types are {allowed_types}"
    return user_type

@app.route("/")
def normal():
    return redirect(url_for("login"))

# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            user.last_login = datetime.now().strftime('%d/%m/%Y %H:%M')
            db.session.commit()
            print(f"{Fore.GREEN}Login successful.")
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
            print(f"{Fore.RED}Invalid username or password")
            return render_template("login.html", error=error)
        
    user = current_user if current_user.is_authenticated else None
    return render_template("login.html", error="", user=user)

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user = current_user if current_user.is_authenticated else None
    return render_template("dashboard.html",  user=user)

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    print(f"{Fore.GREEN}Logout successful.")
    return redirect(url_for('login'))

@app.route("/users-manager", methods=["GET", "POST"])
@login_required
def user_manager():
    if request.method == "POST":
        pass
    else:
        user = current_user if current_user.is_authenticated else None

        last_user = User.query.order_by(User.id.desc()).first()
        last_user_id = last_user.id if last_user else 0

        thirty_days_ago = datetime.now() - timedelta(days=30)
        ninety_days_ago = datetime.now() - timedelta(days=90)

        new_users_count = 0
        deactivated_users_count = 0
        deactivated_users_recent_count = 0
        
        all_users = User.query.all()
        for u in all_users:
            user_create_date = datetime.strptime(u.create_date, '%d/%m/%Y %H:%M')
            if user_create_date >= thirty_days_ago:
                new_users_count += 1

            if u.status == 'Inactive':
                deactivated_users_count += 1
                if user_create_date >= ninety_days_ago:
                    deactivated_users_recent_count += 1
        
        total_permissions = 0
        if user and user.permissions:
            permissions = user.permissions
            total_permissions = sum([
                permissions.can_adjust_inventory_differences,
                permissions.can_manage_suppliers,
                permissions.can_view_temperature_logs,
                permissions.can_adjust_temperature_discrepancies,
                permissions.can_access_high_security_areas,
                permissions.can_generate_financial_reports,
                permissions.can_manage_user_permissions,
                permissions.can_view_audit_logs,
                permissions.can_override_automatic_system_flags,
                permissions.can_manage_orders,
                permissions.can_create_new_users,
                permissions.can_active_users
            ])

        return render_template("users_manager.html", user=user, last_user_id=last_user_id, new_users_count=new_users_count, deactivated_users_count=deactivated_users_count, deactivated_users_recent_count=deactivated_users_recent_count, total_permissions=total_permissions, all_users=all_users)
    
@app.route("/manager-new-user", methods=["GET", "POST"]) 
@login_required
def manager_new_user():
    user = current_user if current_user.is_authenticated else None

    if not user.permissions.can_create_new_users:
        return render_template("no_permission_page.html", user=user)
    
    if request.method == "POST":
        username = request.form["username"]

        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        name = request.form["name"]
        nif = request.form["nif"]
        cellphone = request.form["cellphone"]
        email = request.form["email"]
        role = request.form["role"]
        user_type = request.form["user_type"]

        can_create_new_users = 'can_create_new_users' in request.form
        can_active_users = 'can_active_users' in request.form
        can_adjust_inventory_differences = 'can_adjust_inventory_differences' in request.form
        can_manage_suppliers = 'can_manage_suppliers' in request.form
        can_view_temperature_logs = 'can_view_temperature_logs' in request.form
        can_adjust_temperature_discrepancies = 'can_adjust_temperature_discrepancies' in request.form
        can_access_high_security_areas = 'can_access_high_security_areas' in request.form
        can_generate_financial_reports = 'can_generate_financial_reports' in request.form
        can_manage_user_permissions = 'can_manage_user_permissions' in request.form
        can_view_audit_logs = 'can_view_audit_logs' in request.form
        can_override_automatic_system_flags = 'can_override_automatic_system_flags' in request.form
        can_manage_orders = 'can_manage_orders' in request.form

        new_user = User(
            username=username,
            password=hashed_password, 
            name=name,
            nif=nif,
            cellphone=cellphone,
            email=email,
            role=role,
            user_type=user_type,
        )

        db.session.add(new_user)
        db.session.commit()
        print(f"{Fore.GREEN}The user has been successfully created.") 

        new_user_permissions = UserPermissions(
            user_id=new_user.id,
            can_create_new_users=can_create_new_users,
            can_active_users=can_active_users,
            can_adjust_inventory_differences=can_adjust_inventory_differences,
            can_manage_suppliers=can_manage_suppliers,
            can_view_temperature_logs=can_view_temperature_logs,
            can_adjust_temperature_discrepancies=can_adjust_temperature_discrepancies,
            can_access_high_security_areas=can_access_high_security_areas,
            can_generate_financial_reports=can_generate_financial_reports,
            can_manage_user_permissions=can_manage_user_permissions,
            can_view_audit_logs=can_view_audit_logs,
            can_override_automatic_system_flags=can_override_automatic_system_flags,
            can_manage_orders=can_manage_orders
        )

        db.session.add(new_user_permissions)
        print(f"{Fore.GREEN}Permissions have been successfully added.") 
        db.session.commit()

        send_registration_email(new_user, password)
        print(f"{Fore.GREEN}Registration Email has been successfully sent")

        return redirect(url_for("user_manager"))

    else:
        return render_template("manager_new_user_register.html", user=user)

@app.route("/reactivate-users", methods = ["POST", "GET"])
@login_required
def reactivate_users():
    user = current_user if current_user.is_authenticated else None

    if not user.permissions.can_manage_user_permissions:
        return render_template("no_permission_page.html", user=user)
    
    if request.method == "POST":
        user_name = request.form.get("user_name")
        all_users = User.query.filter(User.name.ilike(f"%{user_name}%")).all()
        return render_template("reactivate.html", user=user, all_users=all_users)
    else:
        all_users = User.query.all()

        return render_template("reactivate.html", user=user, all_users=all_users)
    
@app.route('/change-user-status/<int:user_id>/<new_status>', methods=['POST'])
@login_required
def change_user_status(user_id, new_status):
    user = User.query.get(user_id) 
    if user:
        if new_status in ['Operational', 'Inactive']: 
            user.status = new_status  
            db.session.commit() 
            flash(f'User {user.name} status changed to {new_status}.', 'success')
            print(f"{Fore.GREEN} Status changed to {new_status}")
        else:
            flash('Invalid status value.', 'danger')
            print(f"{Fore.RED} Invalid status value.")
    else:
        flash('User not found.', 'danger')
        print(f"{Fore.RED} User not found.")

    return redirect(url_for('reactivate_users'))

@app.route("/edit-user/<int:user_id>", methods=["POST", "GET"])
@login_required
def edit_user(user_id):
    user_to_edit = User.query.get(user_id) 
    if not user_to_edit:
        flash("User not found.", "danger")
        print(f"{Fore.RED} User not found.")
        return redirect(url_for("user_manager")) 
    
    if request.method == "POST":

        if request.form["username"] != user_to_edit.username:
            user_to_edit.username = request.form["username"]
        
        if request.form["name"] != user_to_edit.name:
            user_to_edit.name = request.form["name"]

        if request.form["nif"] != user_to_edit.nif:
            user_to_edit.nif = request.form["nif"]

        if request.form["cellphone"] != user_to_edit.cellphone:
            user_to_edit.cellphone = request.form["cellphone"]

        if request.form["email"] != user_to_edit.email:
            user_to_edit.email = request.form["email"]

        if request.form["role"] != user_to_edit.role:
            user_to_edit.role = request.form["role"]

        if request.form["user_type"] != user_to_edit.user_type:
            user_to_edit.user_type = request.form["user_type"]

        db.session.commit()
        flash("User details updated successfully.", "success")
        print(f"{Fore.GREEN} User details updated successfully.")
        return redirect(url_for("user_manager"))
        

    else:
        user = current_user if current_user.is_authenticated else None
        return render_template("edit_user.html", user=user, user_to_edit=user_to_edit)
    
@app.route("/reset-password/<int:user_id>", methods=["POST"])
@login_required
def reset_password(user_id):
    user = User.query.get(user_id)

    if user:
        new_password = secrets.token_hex(4)  
        user.password = generate_password_hash(new_password) 
        db.session.commit()
        flash("Password reset successfully. The new password has been sent to the user's email.", "success")
        
        send_password_reset_email(user, new_password)
        print(f"{Fore.GREEN}Password reset successfully. . New password: {new_password} and email sent.")
    else:
        flash("User not found.", "danger")

    return redirect(url_for("user_manager"))

@app.route("/all_users_page", methods=["GET", "POST"])
@login_required
def all_users_page():
    all_users = User.query.all()

    if request.method == "POST":
        pass
    else:
        user = current_user if current_user.is_authenticated else None
        return render_template("all_users_page.html", user=user , all_users=all_users)
    
@app.route("/change-permissions", methods=["GET", "POST"])
@login_required
def change_user_permissions():
    user = current_user if current_user.is_authenticated else None

    if not user.permissions.can_manage_user_permissions:
        return render_template("no_permission_page.html", user=user)
    
    if request.method == "POST":
            search_term = request.form.get("search_term", "").strip()
            search_results = User.query.filter(User.nif.contains(search_term)).all()
            if search_results:
                user_permissions = UserPermissions.query.filter_by(user_id=search_results[0].id).first()
            else:
                user_permissions = None
            return render_template("change_permissions.html", user=user, search_results=search_results, user_permissions=user_permissions)
    else:
        return render_template("change_permissions.html", user=user)

@app.route('/update-permissions/<int:user_id>', methods=['POST'])
@login_required
def update_user_permissions(user_id):
    user = User.query.get_or_404(user_id)

    permissions = {
        'can_create_new_users': request.form.get('can_create_new_users') == 'on',
        'can_active_users': request.form.get('can_active_users') == 'on',
        'can_adjust_inventory_differences': request.form.get('can_adjust_inventory_differences') == 'on',
        'can_manage_suppliers': request.form.get('can_manage_suppliers') == 'on',
        'can_view_temperature_logs': request.form.get('can_view_temperature_logs') == 'on',
        'can_adjust_temperature_discrepancies': request.form.get('can_adjust_temperature_discrepancies') == 'on',
        'can_access_high_security_areas': request.form.get('can_access_high_security_areas') == 'on',
        'can_generate_financial_reports': request.form.get('can_generate_financial_reports') == 'on',
        'can_manage_user_permissions': request.form.get('can_manage_user_permissions') == 'on',
        'can_view_audit_logs': request.form.get('can_view_audit_logs') == 'on',
        'can_override_automatic_system_flags': request.form.get('can_override_automatic_system_flags') == 'on',
        'can_manage_orders': request.form.get('can_manage_orders') == 'on'
    }

    user_permissions = UserPermissions.query.filter_by(user_id=user_id).first()

    if user_permissions:
        for key, value in permissions.items():
            setattr(user_permissions, key, value)
    else:
        user_permissions = UserPermissions(user_id=user_id, **permissions)
        db.session.add(user_permissions)

    print("Permissions changed successfully")
    db.session.commit()

    flash(f"{Fore.GREEN}User permissions updated successfully.", "success")
    return redirect(url_for('change_user_permissions'))

@app.route("/user-settings/<int:user_id>", methods=["GET","POST"])
@login_required
def user_settings(user_id):
     user = current_user if current_user.is_authenticated else None
     user_to_edit = User.query.get(user_id)

     if request.method == "POST":
        if "name" in request.form and request.form["name"].strip() and request.form["name"] != user_to_edit.name:
            user_to_edit.name = request.form["name"]

        if "password" in request.form and request.form["password"].strip():
            hashed_password = generate_password_hash(request.form["password"])
            if not check_password_hash(user_to_edit.password, request.form["password"]):
                user_to_edit.password = hashed_password

        if "cellphone" in request.form and request.form["cellphone"].strip() and request.form["cellphone"] != user_to_edit.cellphone:
            user_to_edit.cellphone = request.form["cellphone"]

        if "email" in request.form and request.form["email"].strip() and request.form["email"] != user_to_edit.email:
            user_to_edit.email = request.form["email"]
        
        db.session.commit()
        flash("User details updated successfully.", "success")
        print(f"{Fore.GREEN} User details updated successfully.")
        return redirect(url_for("user_settings", user_id=user_id))

     else:
         return render_template("user_settings.html", user=user)
     
@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    user = current_user if current_user.is_authenticated else None

    try:
        today = datetime.now().strftime('%d/%m/%Y')

        assigned_schedule = None
        work_schedule = None
        total_work_hours = None
        last_record_type = "Entry"  

        assigned_schedule = AssignedSchedules.query.filter_by(user_id=user.id, date=today).first()

        if assigned_schedule:
            schedule_id = assigned_schedule.schedule_id
            
            work_schedule = WorkSchedules.query.filter_by(id=schedule_id).first()

            if work_schedule:
                if work_schedule.time_in != "OFF" and work_schedule.time_out != "OFF":
                    time_in = datetime.strptime(work_schedule.time_in, "%H:%M")
                    time_out = datetime.strptime(work_schedule.time_out, "%H:%M")
                    lunch_start = datetime.strptime(work_schedule.lunch_start, "%H:%M") if work_schedule.lunch_start else None
                    lunch_end = datetime.strptime(work_schedule.lunch_end, "%H:%M") if work_schedule.lunch_end else None

                    total_work_time = time_out - time_in
                    
                    if lunch_start and lunch_end:
                        lunch_break_duration = lunch_end - lunch_start
                        total_work_time -= lunch_break_duration

                    total_work_hours = total_work_time.total_seconds() / 3600
                else:
                    total_work_hours = 0

                last_log = WorkSchedulesLogs.query.filter_by(user_id=user.id).order_by(WorkSchedulesLogs.create_date_in.desc()).first()
                last_record_type = last_log.record_type if last_log else "Out"

                logs = WorkSchedulesLogs.query.filter_by(user_id=user.id).all()

                def convert_to_datetime(log):
                    return datetime.strptime(log.create_date_in, '%d/%m/%Y %H:%M:%S')

                logs = sorted(logs, key=convert_to_datetime, reverse=True)  
            else:
                flash("Work schedule not found.", "danger")
                logs = []
        else:
            flash("No assigned schedule for today.", "warning")
            logs = []

    except AttributeError as e:
        flash(f"An error occurred: {str(e)}", "danger")
        logs = []
        work_schedule = None

    except Exception as ex:
        flash(f"An unexpected error occurred: {str(ex)}", "danger")
        logs = []
        work_schedule = None

    if request.method == "POST":
        try:
            log_type = request.form.get("log_type") 
            date_input = request.form.get("date")    
            time_input = request.form.get("time")    
            record_type = request.form.get("record_type")  
            justification = request.form.get("justification")

            if not record_type:
                last_log = WorkSchedulesLogs.query.filter_by(user_id=user.id).order_by(WorkSchedulesLogs.create_date_in.desc()).first()
                if last_log and last_log.record_type == "Entry":
                    record_type = "Out"
                else:
                    record_type = "Entry"

            if log_type == "on":  
                create_date_in = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

                new_log = WorkSchedulesLogs(
                    schedule_id=assigned_schedule.schedule_id,
                    user_id=user.id,
                    create_date_in=create_date_in,
                    record_type=record_type,
                    log_type="Automatic",  
                    status="Approved",  
                    justification="",  
                    notes=""
                )
                db.session.add(new_log)
                db.session.commit()
                flash("Automatic time stamp added successfully!", "success")
                print(f"{Fore.GREEN}Automatic time stamp added successfully!")
            else:  
                if date_input and time_input:  
                    datetime_input = datetime.strptime(f"{date_input} {time_input}", '%Y-%m-%d %H:%M')  
                    create_date_in = datetime_input.strftime('%d/%m/%Y %H:%M:%S')  

                    new_log = WorkSchedulesLogs(
                        schedule_id=assigned_schedule.schedule_id,
                        user_id=user.id,
                        create_date_in=create_date_in,
                        record_type=record_type,
                        log_type="Manual",  
                        status="Pending",  
                        justification=justification, 
                        notes=""
                    )
                    db.session.add(new_log)
                    db.session.commit()
                    flash("Manual time stamp added successfully!", "success")
                    print(f"{Fore.GREEN}Manual time stamp added successfully!")
                else:
                    flash("Error: Date and time not provided for manual recording.", "danger")
                    print(f"{Fore.RED}Error: Date and time not provided for manual recording.")
                    
        except Exception as e:
            flash(f"An error occurred while adding the log: {str(e)}", "danger")
            print(f"{Fore.RED}Error: {str(e)}")

        return redirect(url_for("schedule"))
    
    return render_template("schedule_home.html", user=user, work_schedule=work_schedule, total_work_hours=total_work_hours, logs=logs, last_record_type=last_record_type)   
@app.route("/schedule-manager", methods=["GET", "POST"])
@login_required
def schedule_manager():
    user = current_user if current_user.is_authenticated else None

    if user.user_type in ["Admin", "Manager"]:
        schedules_log_query = db.session.query(WorkSchedulesLogs, User.name).join(User, WorkSchedulesLogs.user_id == User.id).filter(
            and_(
                WorkSchedulesLogs.log_type == "Manual", 
                WorkSchedulesLogs.status != "Approved", 
                WorkSchedulesLogs.status != "Rejected"
            )
        )

        if request.method == "POST":
            name = request.form.get("name")
            record_type = request.form.get("record_type")

            if name:
                schedules_log_query = schedules_log_query.filter(User.name.ilike(f"%{name}%"))

            if record_type and record_type != 'all':
                schedules_log_query = schedules_log_query.filter(WorkSchedulesLogs.record_type == record_type)

        schedules_log = schedules_log_query.all()

        return render_template("schedule_manager.html", user=user, schedules_log=schedules_log)
    else:
        return render_template("no_permission_page.html", user=user)

@app.route("/approve-log/<int:log_id>", methods=["POST"])
@login_required
def approve_log(log_id):
    user = current_user if current_user.is_authenticated else None

    if user.user_type in ["Admin", "Manager"]:
        log_entry = WorkSchedulesLogs.query.get(log_id)
        
        if log_entry:
            log_entry.status = "Approved"
            db.session.commit()
            print(f"{Fore.GREEN}Log approved successfully!")
            flash("Log approved successfully!", "success")
        else:
            print(f"{Fore.RED}Log approved successfully!")
            flash("Log not found.", "danger")

        return redirect(url_for("schedule_manager"))
    else:
        return render_template("no_permission_page.html", user=user)

@app.route("/reject-log/<int:log_id>", methods=["POST"])
@login_required
def reject_log(log_id):
    user = current_user if current_user.is_authenticated else None

    if user.user_type in ["Admin", "Manager"]:
        log_entry = WorkSchedulesLogs.query.get(log_id)
        
        if log_entry:
            notes = request.form.get("notes")
            log_entry.status = "Rejected"
            log_entry.notes = notes
            db.session.commit()
            print(f"{Fore.GREEN}Log rejected successfully!")
            flash("Log rejected successfully!", "success")
        else:
            print(f"{Fore.RED}Log not found.")
            flash("Log not found.", "danger")

        return redirect(url_for("schedule_manager"))
    else:
        return render_template("no_permission_page.html", user=user)


@app.route("/approve-all-logs", methods=["POST"])
@login_required
def approve_all_logs():
    logs_to_approve = WorkSchedulesLogs.query.filter(WorkSchedulesLogs.status == 'Pending').all()

    for log in logs_to_approve:
        log.status = 'Approved'
    
    db.session.commit()
    print(f"{Fore.GREEN}All pending logs have been approved!")
    flash("All pending logs have been approved!", "success")

    return redirect(url_for('schedule_manager'))

@app.route("/reject-all-logs", methods=["POST"])
@login_required
def reject_all_logs():
    notes = request.form.get('notes')

    logs_to_reject = WorkSchedulesLogs.query.filter(WorkSchedulesLogs.status == 'Pending').all()

    for log in logs_to_reject:
        log.status = 'Rejected'
        log.notes = notes  
    
    db.session.commit()
    print(f"{Fore.GREEN}All pending logs have been rejected!")
    flash("All pending logs have been rejected!", "danger")

    return redirect(url_for('schedule_manager'))

@app.route("/schedules-all-records", methods=["GET"])
@login_required
def all_schedules_records():
    user = current_user  

    logs = WorkSchedulesLogs.query.filter_by(user_id=user.id).order_by(desc(WorkSchedulesLogs.create_date_in)).all()
    
    return render_template("schedules_all_records.html", user=user, logs=logs)

@app.route("/products-manager", methods = ["GET", "POST"])
@login_required
def products_manager():
    user = current_user if current_user.is_authenticated else None

    last_product = Product.query.order_by(Product.id.desc()).first()
    last_product_id = last_product.id if last_product else 0
    deactivated_products_count = 0
    all_products = Product.query.all()
    last_supplier = Suppliers.query.order_by(Suppliers.id.desc()).first()
    last_supplier_id = last_supplier.id if last_supplier else 0
    out_of_stock_products_count = Product.query.filter(Product.stock == 0).count()

    for p in all_products:
            if p.status == 'Inactive':
                deactivated_products_count += 1

    best_selling_products = db.session.query(Product.name, db.func.sum(Sales.quantity_sold).label('total_sales'),db.func.sum((Product.sell_price - Product.buy_price) * Sales.quantity_sold).label('total_profit')).join(Sales, Product.id == Sales.product_id).group_by(Product.id).order_by(db.func.sum(Sales.quantity_sold).desc()).limit(10).all()

    return render_template("products_manager.html", user=user, last_product_id=last_product_id, deactivated_products_count=deactivated_products_count, last_supplier_id=last_supplier_id, best_selling_products=best_selling_products, out_of_stock_products_count=out_of_stock_products_count)

@app.route("/create-new-product", methods=["POST", "GET"])
@login_required
def create_new_product():
    user = current_user if current_user.is_authenticated else None
    if user.user_type == "Admin" or user.user_type == "Manager":
        brand = request.form.get("brand")
        name = request.form.get("name")
        product_type = request.form.get("product_type")
        buy_price = request.form.get("buy_price")
        margin = request.form.get("margin")
        min_recommended_stock = request.form.get("min_recommended_stock")
        warehouse_section = request.form.get("warehouse_section")
        warehouse_shelf = request.form.get("warehouse_shelf")

        if request.method == "POST":
            sell_price = buy_price + (buy_price * margin / 100)
            
            new_product = Product(
                brand = brand,
                # Continuar a criar a criação dos dados para inserir na base de dados
            )
        else:
            return render_template("create_new_product.html", user=user)
    else:
        return render_template("no_permission_page.html", user=user)
    
@app.route("/get_brands", methods=["GET"])
def get_brands():
    brands = Brands.query.all() 
    brands_list = [{"id": brand.id, "name": brand.brand_name} for brand in brands]
    return jsonify(brands_list)

@app.route("/get-product-type", methods=["GET"])
def get_product_types():
    product_types = ProductTypes.query.all() 
    product_type_list = [{"id": t.id, "name": t.product_type} for t in product_types]
    return jsonify(product_type_list)

@app.route("/product-page/<int:product_id>", methods=["GET"])
def product_page(product_id):
    product = Product.query.filter_by(id=product_id).first()
    
    if not product:
        flash("Product not found.", "danger")
        print(f"{Fore.RED} Product not found.")
        return render_template("no_product_page.html")

    return render_template("product_page.html", product=product)

@app.route("/all-products", methods=["GET", "POST"])
@login_required
def all_products():
    user = current_user if current_user.is_authenticated else None
    all_products = Product.query.all()
    
    if request.method == "POST":
        pass
    else:
        return render_template("all_products_page.html", user=user, all_products=all_products)
    
@app.route("/generate_qr_code/<int:product_id>")
def generate_qr_code(product_id):
    product = db.session.get(Product, product_id)
    
    if not product or not product.qr_code_path:
        return "Product or QR Code path not found", 404
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(product.qr_code_path)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def create_user():
    user = User(username="adhasdasihdaoisasdasdasdasdasdadadadsadd",
                password="test",
                user_type="Employee",
                nif = "784512547a",
                email = "employeeeee@example.com",
                name = "Marcooo Vieira",
                cellphone = "9411244615678"
                )
    db.session.add(user)
    db.session.commit()
    print(f"{Fore.GREEN}Criado Com sucesso")

def create_work_schedules():
    schedules = WorkSchedules(
        schedule = "OFF",
        time_in = "",
        time_out = "",
        lunch_start = "",
        lunch_end = ""
    )
    db.session.add(schedules)
    db.session.commit()
    print(f"{Fore.GREEN}Criado Com sucesso")

def assign_schedules_for_september(user_id=3):
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2024, 10, 31)

    week_schedule_a = 1  
    week_schedule_b = 2  
    weekend_off = 9      

    current_date = start_date
    week_counter = 0

    while current_date <= end_date:
        
        if current_date.weekday() >= 5:  
            schedule_id = weekend_off
        else:
            
            if week_counter % 2 == 0:
                schedule_id = week_schedule_a
            else:
                schedule_id = week_schedule_b

        
        date_str = current_date.strftime('%d/%m/%Y')

        new_schedule = AssignedSchedules(
            user_id=user_id,
            schedule_id=schedule_id,
            date=date_str,
            status = "Approved",
            is_active = True,
            previous_schedule_id = 0
            )
        db.session.add(new_schedule)

        current_date += timedelta(days=1)

        if current_date.weekday() == 0:  
            week_counter += 1

    db.session.commit()
    print("Horários atribuídos para o mês de setembro.")

def creat_product():
    margin = 120  
    buy_price = 745.47

    sell_price = buy_price + (buy_price * margin / 100)

    new_product = Product(
        ref = "SPR54791349",
        qr_code_path = "teste3",
        name = "Brake Clean 200L",
        product_type = "Produtos Químicos",
        brand = "Facon",
        model = "None",
        buy_price = buy_price,
        sell_price = sell_price,
        margin = margin,
        stock = 3,
        min_recommended_stock = 5,
        last_update = "",
        warehouse_section = "D",
        warehouse_shelf = 1,
        status = "Active",
        update_info = datetime.now().strftime('%d/%m/%Y %H:%M')
    )

    db.session.add(new_product)
    db.session.commit()
    print(f"{Fore.GREEN}Criado Com sucesso")

def create_test_supplier():
    new_supplier = Suppliers(
        supplier_name="Teste Supplier",
        contact_name="John Doe",
        contact_email="john.doe@test.com",
        contact_phone="+351912345678",
        type="Alimentar",
        country="Portugal",
        adress="1234 Test Avenue, Lisbon",
        payment_terms="Net 30",
        credit_limit=10000,
        last_order_date=datetime.now().strftime('%d/%m/%Y'),
        rating=5
    )
    
    db.session.add(new_supplier)
    db.session.commit()

    print(f"{Fore.GREEN}Fornecedor {new_supplier.supplier_name} criado com sucesso!")

def create_sales_entries():
    customers = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Davis", "Chris Brown"]
    
    product_ids = [1, 2,3]
    user_ids = [1, 2]  
    
    for _ in range(20):
        product_id = choice(product_ids)
        user_id = choice(user_ids)
        customer_name = choice(customers) 
        quantity_sold = randint(1, 30) 
        
        new_sale = Sales(
            product_id=product_id,
            quantity_sold=quantity_sold,
            user_id=user_id,
            customer_name=customer_name,
            status="Completed"
        )
        
        db.session.add(new_sale)
    db.session.commit()
    print("Vendas criadas com sucesso!")

def create_brands():
    brands = [
        "Falcon", "Facon", "Bosch", "Philips", "Samsung", "Sharp", "Kenmore", "Electrolux", "KitchenAid", "Whirlpool",
        "Sony", "LG", "Panasonic", "GE Appliances", "Frigidaire", "Miele", "Maytag", "Sub-Zero", "Viking", "Thermador",
        "Siemens", "Beko", "Haier", "Hitachi", "Liebherr", "Gorenje", "Smeg", "Zanussi", "Fisher & Paykel", "DeLonghi",
        "Braun", "Rowenta", "Tefal", "Krups", "Russell Hobbs", "Morphy Richards", "Dyson", "Hoover", "Bissell", "Shark",
        "Makita", "DeWalt", "Black & Decker", "Craftsman", "Ryobi", "Milwaukee", "Hitachi Tools", "Hilti", "Bosch Tools",
        "Karcher", "Stanley", "Metabo", "Ridgid", "Skil", "Worx", "Dremel", "Festool", "Porter-Cable", "Husqvarna",
        "Honda", "Yamaha", "Kawasaki", "Suzuki", "Harley-Davidson", "Ducati", "BMW", "Mercedes-Benz", "Audi", "Volkswagen",
        "Porsche", "Ford", "Chevrolet", "Cadillac", "Buick", "Jeep", "Tesla", "Nissan", "Toyota", "Subaru", "Mitsubishi",
        "Hyundai", "Kia", "Mazda", "Volvo", "Land Rover", "Jaguar", "Peugeot", "Renault", "Citroen", "Fiat", "Alfa Romeo",
        "Ferrari", "Lamborghini", "Bugatti", "Maserati", "McLaren", "Aston Martin", "Rolls-Royce", "Bentley", "Pagani",
        "Hugo Boss", "Gucci", "Prada", "Versace", "Armani", "Ralph Lauren", "Calvin Klein", "Tommy Hilfiger", "Nike", "Adidas",
        "Puma", "Reebok", "Under Armour", "New Balance", "Fila", "Converse", "Vans", "Levi's", "Wrangler", "Diesel",
        "Gap", "Zara", "H&M", "Uniqlo", "Benetton", "Burberry", "Givenchy", "Yves Saint Laurent", "Hermes", "Chanel",
        "Louis Vuitton", "Balenciaga", "Fendi", "Valentino", "Dolce & Gabbana", "Alexander McQueen", "Celine", "Christian Dior",
        "Rolex", "Omega", "Tag Heuer", "Breitling", "Patek Philippe", "Audemars Piguet", "Vacheron Constantin", "Seiko",
        "Citizen", "Casio", "Swatch", "Fossil", "Michael Kors", "Tissot", "Longines", "Hublot", "Panerai", "IWC", "Chopard",
        "Cartier", "Montblanc", "Bvlgari", "Tiffany & Co.", "Ray-Ban", "Oakley", "Persol", "Maui Jim", "Tom Ford",
        "Warby Parker", "Bose", "JBL", "Sennheiser", "Beats by Dre", "Sony Audio", "Bang & Olufsen", "Klipsch", "Pioneer",
        "Harman Kardon", "Denon", "Marantz", "Onkyo", "Yamaha Audio", "Focal", "KEF", "Bowers & Wilkins", "Polk Audio",
        "Logitech", "Corsair", "Razer", "SteelSeries", "HyperX", "Alienware", "MSI", "Asus", "Acer", "Dell", "HP",
        "Lenovo", "Toshiba", "Apple", "Microsoft", "Google", "Amazon", "Intel", "AMD", "NVIDIA", "Seagate", "Western Digital",
        "Sandisk", "Kingston", "Crucial", "Corsair Memory", "G.SKILL", "Samsung SSD", "Sony PlayStation", "Microsoft Xbox",
        "Nintendo", "Logitech Gaming", "Thrustmaster", "Roccat", "Cooler Master", "EVGA", "Zotac", "ASRock", "Gigabyte",
        "Biostar", "HP Enterprise", "Synology", "QNAP", "Netgear", "TP-Link", "Cisco", "Ubiquiti", "D-Link", "Linksys",
        "Huawei", "Xiaomi", "OnePlus", "Oppo", "Realme", "Vivo", "Honor", "ZTE", "Sony Mobile", "Nokia", "BlackBerry",
        "Motorola", "HTC", "Palm", "LG Mobile", "Lenovo Mobile", "Alcatel", "Micromax", "Blu", "Infinix", "Tecno",
        "Itel", "Gionee", "Lava", "Coolpad", "Meizu", "Vernee", "LeEco", "Doogee", "Cubot", "UMIDIGI", "Oukitel",
        "CAT", "Kyocera", "Sonim", "Fairphone", "Jolla", "Turing", "Yota", "Kogan", "Google Pixel", "Asus ROG Phone",
        "Nubia", "Redmi", "Honor Magic", "Realme Narzo", "Poco", "iQOO", "Vivo Nex", "Oppo Find", "Xiaomi Mi",
        "Xiaomi Redmi", "Xiaomi Black Shark", "OnePlus Nord", "Sony Xperia", "Sharp Aquos", "TCL", "Hisense", "Panasonic Viera",
        "Philips TV", "Samsung QLED", "LG OLED", "Vizio", "Roku TV", "Insignia", "Toshiba TV", "Hitachi TV", "Westinghouse",
        "Element Electronics", "Sceptre", "Skyworth", "Changhong", "Vu Televisions", "Thomson TV", "iFFALCON", "Blaupunkt",
        "Haier TV", "BPL", "Kodak", "Micromax TV", "Lloyd", "Aisen", "Shinco", "Noble Skiodo", "Activa", "Murphy",
        "Intex", "Salora", "Daewoo", "Akai", "AOC", "Polaroid", "Toshiba Laptops", "Sony Vaio", "Acer Predator",
        "Asus TUF", "HP Omen", "Dell XPS", "Microsoft Surface", "Lenovo ThinkPad", "Razer Blade", "Alienware Gaming",
        "MSI Gaming", "Gigabyte Aero", "Huawei MateBook", "Apple MacBook", "Google Chromebook", "Samsung Galaxy Book",
        "LG Gram", "Fujitsu Laptops", "Panasonic Toughbook", "NEC Computers", "Toshiba Portege", "Sony Walkman",
        "Bowers & Wilkins Headphones", "Shure", "Jabra", "Plantronics", "Audio-Technica", "Beyerdynamic", "AKG", "Grado",
        "Focal Headphones", "Audeze", "Sennheiser HD", "V-Moda", "FiiO", "Klipsch Headphones", "Ultimate Ears", "Anker",
        "Belkin", "Mophie", "OtterBox", "Spigen", "LifeProof", "Incase", "Speck", "Targus", "Kensington", "Case Logic"
    ]
    
    try:
        for brand in brands:
            new_brand = Brands(brand_name=brand)  
            db.session.add(new_brand)
        
        db.session.commit()
        print("Marcas criadas com sucesso!")
    except Exception as e:
        db.session.rollback()  
        print(f"Erro ao criar marcas: {e}")

def create_product_types():
    types = [
        "Electronics", "Furniture", "Clothing", "Food", "Appliances", 
        "Automotive", "Beauty Products", "Books", "Building Materials", 
        "Cameras", "Cell Phones", "Computers", "Drones", "Fitness Equipment", 
        "Gaming Consoles", "Garden Supplies", "Groceries", "Hand Tools", 
        "Health Products", "Home Decor", "Industrial Equipment", "Jewelry", 
        "Kitchenware", "Laptops", "Lighting", "Luggage", "Musical Instruments", 
        "Office Supplies", "Outdoor Gear", "Pet Supplies", "Pharmaceuticals", 
        "Power Tools", "Printers", "Security Systems", "Shoes", "Smart Devices", 
        "Sporting Goods", "Stationery", "Toys", "TVs", "Vacuum Cleaners", 
        "Watches", "Wine & Spirits", "Cleaning Supplies", "Medical Equipment", 
        "Bicycles", "Camping Equipment", "Travel Accessories", "Luxury Goods", 
        "Art Supplies", "Audio Equipment", "Baby Products", "Bedding", 
        "Craft Supplies", "Gift Items", "Outdoor Furniture", "Party Supplies", 
        "Plumbing Supplies", "Seasonal Decor", "Storage Solutions", 
        "Sunglasses", "Tableware", "Textiles", "Tools", "Toys & Games", 
        "Vehicles", "Welding Equipment", "Window Coverings", "Workout Gear", 
        "Bakery Products", "Batteries", "Beverages", "Candles", "Car Care Products",
        "Cookware", "Cosmetics", "Detergents", "Diapers", "Fabrics", 
        "Fishing Gear", "Footwear", "Fragrances", "Gardening Tools", 
        "Gift Cards", "Grills", "Headphones", "Hiking Gear", "Home Improvement", 
        "Hunting Gear", "Ink & Toner", "Interior Decor", "Janitorial Supplies", 
        "Laundry Supplies", "Mattresses", "Motorcycle Parts", "Nutritional Supplements", 
        "Office Furniture", "Painting Supplies", "Party Favors", "Personal Care", 
        "Pet Food", "Photography Equipment", "Pool Supplies", "Refrigerators", 
        "Scooters", "Smart Home Devices", "Solar Panels", "Sportswear", 
        "Stationery Supplies", "Surgical Supplies", "Table Lamps", "Tents", 
        "Tires", "Travel Bags", "Vitamins & Supplements", "Washing Machines", 
        "Welding Supplies", "Wind Turbines", "Work Boots", "Yoga Equipment"
    ]

    try:
        for t in types:
            new_type = ProductTypes(product_type=t)  
            db.session.add(new_type)
        
        db.session.commit()
        print("Tipos criados com sucesso!")
    except Exception as e:
        db.session.rollback()  
        print(f"Erro ao criar marcas: {e}")

if __name__ == "__main__":
    init(autoreset=True)
    with app.app_context():
        db.create_all()
        #create_user()
        #create_work_schedules()
        #assign_schedules_for_september()
        #creat_product()
        #create_test_supplier()
        #create_sales_entries()
        #create_brands()
        #create_product_types()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

=======
from flask import *
from flask_login import *
import os
from flask_sqlalchemy import *
from sqlalchemy import *
from datetime import *
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from sqlalchemy.orm import validates
import random
from werkzeug.security import *
import secrets
from colorama import *
from random import *
import random
import qrcode
from io import *

# cubix-no-reply@hotmail.com

# App config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    nif = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    cellphone = db.Column(db.String(20))
    create_date = db.Column(db.String(20))
    last_login = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Operational")
    role = db.Column(db.String(40))
    user_type = db.Column(db.String(50), default="Client")
    pin = db.Column(db.Integer, unique=True)

    product_movements = db.relationship('ProductMovements', back_populates='user', lazy=True)
    permissions = db.relationship("UserPermissions", uselist=False, back_populates="user")
    logs = db.relationship('WorkSchedulesLogs', backref='user', lazy=True)
    assigned_schedules = db.relationship('AssignedSchedules', backref='user_assigned_schedules', lazy=True)
    sales = db.relationship('Sales', back_populates='user', lazy=True)

    def __init__(self, username, password, nif, email, name, cellphone, role=None, last_login=None, status="Operational", user_type="Client"):
        self.username = username
        self.password = password
        self.nif = nif
        self.email = email
        self.name = name.title()
        self.cellphone = cellphone
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_login = last_login
        self.status = status.capitalize()
        self.role = role
        self.user_type = user_type.capitalize()
        self.pin = random.randint(10000, 99999)

class UserPermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    can_adjust_inventory_differences = db.Column(db.Boolean, default=False)
    can_manage_suppliers = db.Column(db.Boolean, default=False)
    can_view_temperature_logs = db.Column(db.Boolean, default=False)
    can_adjust_temperature_discrepancies = db.Column(db.Boolean, default=False)
    can_access_high_security_areas = db.Column(db.Boolean, default=False)
    can_generate_financial_reports = db.Column(db.Boolean, default=False)
    can_manage_user_permissions = db.Column(db.Boolean, default=False)
    can_view_audit_logs = db.Column(db.Boolean, default=False)
    can_override_automatic_system_flags = db.Column(db.Boolean, default=False)
    can_manage_orders = db.Column(db.Boolean, default=False)
    can_create_new_users = db.Column(db.Boolean, default=False)
    can_active_users = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='permissions')

    def __init__(self, user_id, can_adjust_inventory_differences=False, can_manage_suppliers=False, can_view_temperature_logs=False, can_adjust_temperature_discrepancies=False,can_access_high_security_areas=False, can_generate_financial_reports=False, can_manage_user_permissions=False, can_view_audit_logs=False, can_override_automatic_system_flags=False, can_manage_orders=False, can_create_new_users=False, can_active_users=False):
        self.user_id = user_id
        self.can_adjust_inventory_differences = can_adjust_inventory_differences
        self.can_manage_suppliers = can_manage_suppliers
        self.can_view_temperature_logs = can_view_temperature_logs
        self.can_adjust_temperature_discrepancies = can_adjust_temperature_discrepancies
        self.can_access_high_security_areas = can_access_high_security_areas
        self.can_generate_financial_reports = can_generate_financial_reports
        self.can_manage_user_permissions = can_manage_user_permissions
        self.can_view_audit_logs = can_view_audit_logs
        self.can_override_automatic_system_flags = can_override_automatic_system_flags
        self.can_manage_orders = can_manage_orders
        self.can_create_new_users = can_create_new_users
        self.can_active_users = can_active_users

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(20))
    qr_code_path = db.Column(db.String(100))
    name = db.Column(db.String(50))
    product_type = db.Column(db.String(25))
    brand = db.Column(db.String(30))
    model = db.Column(db.String(30))
    buy_price = db.Column(db.Float)
    sell_price = db.Column(db.Float)
    margin = db.Column(db.Float)
    stock = db.Column(db.Integer)
    min_recommended_stock = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    last_update = db.Column(db.String(14))
    warehouse_section = db.Column(db.String)
    warehouse_shelf = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Active")
    update_info = db.Column(db.String(20))

    product_movements = db.relationship('ProductMovements', back_populates='product', lazy=True)
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True)
    sales = db.relationship('Sales', back_populates='product', lazy=True)

    def __init__(self, ref, qr_code_path, name, product_type, brand, model, buy_price, sell_price, margin, stock, min_recommended_stock, last_update, update_info, warehouse_section, warehouse_shelf, status="Active"):
        self.ref = ref
        self.qr_code_path = qr_code_path
        self.name = name.upper()
        self.product_type = product_type
        self.brand = brand.title()
        self.model = model.title()
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.margin = margin
        self.stock = stock
        self.min_recommended_stock = min_recommended_stock
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_update = last_update
        self.status = status.capitalize()
        self.update_info = update_info
        self.warehouse_section = warehouse_section
        self.warehouse_shelf = warehouse_shelf

class ProductMovements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    movement_type = db.Column(db.String(50), default="Stock Entry")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    invoice_number = db.Column(db.String(30))
    justification = db.Column(db.String(100), default="Customer Purchase")

    product = db.relationship('Product', back_populates='product_movements')
    supplier = db.relationship('Suppliers', back_populates='product_movements')
    user = db.relationship('User', back_populates='product_movements')

    def __init__(self, product_id, supplier_id=None, movement_type="Stock Entry", user_id=None, quantity=0, invoice_number=None, justification="Customer Purchase"):
        self.product_id = product_id
        self.supplier_id = supplier_id
        self.movement_type = movement_type
        self.user_id = user_id
        self.quantity = quantity
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.invoice_number = invoice_number
        self.justification = justification

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(20))
    contact_name = db.Column(db.String(30))
    contact_email = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    type = db.Column(db.String(30))
    country = db.Column(db.String(30))
    adress = db.Column(db.String(50))
    payment_terms = db.Column(db.String(15))
    credit_limit = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    last_order_date = db.Column(db.String(14))
    rating = db.Column(db.Integer)

    product_movements = db.relationship('ProductMovements', back_populates='supplier', lazy=True)

    def __init__(self, supplier_name, contact_name, contact_email, contact_phone, type, country, adress, payment_terms, credit_limit, last_order_date, rating):
        self.supplier_name = supplier_name
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.type = type
        self.country = country
        self.adress = adress
        self.payment_terms = payment_terms
        self.credit_limit = credit_limit
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_order_date = last_order_date
        self.rating = rating

class LogTemperatures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature_id = db.Column(db.Integer, db.ForeignKey('temperatures.id'))
    current_temperature = db.Column(db.Float)
    justification = db.Column(db.String(100))
    create_date = db.Column(db.String(20))

    temperature = db.relationship('Temperatures', back_populates='logs')

    def __init__(self, temperature_id, current_temperature, justification=None):
        self.temperature_id = temperature_id
        self.current_temperature = current_temperature
        self.justification = justification
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')

class Temperatures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_section = db.Column(db.Integer)
    warehouse_deep_freezer = db.Column(db.Integer)
    recommended_temperature = db.Column(db.Float)

    logs = db.relationship('LogTemperatures', back_populates='temperature', lazy=True)

    def __init__(self, warehouse_section, warehouse_deep_freezer, recommended_temperature):
        self.warehouse_section = warehouse_section
        self.warehouse_deep_freezer = warehouse_deep_freezer
        self.recommended_temperature = recommended_temperature

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.String(20))
    
    items = db.relationship('OrderItem', back_populates='order', lazy=True)

    def __init__(self, user_id, order_date=None):
        self.user_id = user_id
        self.order_date = order_date if order_date else datetime.now().strftime('%d/%m/%Y %H:%M')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    
    product = db.relationship('Product', back_populates='order_items')
    order = db.relationship('Order', back_populates='items')

    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    type = db.Column(db.String, default = "In")
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    is_viewed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='notifications')
    message = db.relationship('Message', backref='notifications')

class WorkSchedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule  = db.Column(db.String(5), unique = True)
    time_in = db.Column(db.String(15))
    time_out = db.Column(db.String(15))
    lunch_start = db.Column(db.String(15))
    lunch_end = db.Column(db.String(15))

    logs = db.relationship('WorkSchedulesLogs', backref='work_schedule', lazy=True)

    def __init__(self, schedule, time_in, time_out, lunch_start, lunch_end):
        self.schedule = schedule
        self.time_in = time_in
        self.time_out = time_out
        self.lunch_start = lunch_start
        self.lunch_end = lunch_end

class WorkSchedulesLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('work_schedules.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date_in = db.Column(db.String(30))
    log_type = db.Column(db.String(10), default="Manual")
    record_type = db.Column(db.String(10))
    justification = db.Column(db.String)
    status = db.Column(db.String(20), default="Approved")
    notes = db.Column(db.String)

    def __init__(self, schedule_id, user_id, create_date_in, notes, record_type, log_type="Manual", justification="", status="Approved"):
        self.schedule_id = schedule_id
        self.user_id = user_id
        self.create_date_in = create_date_in
        #datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.log_type = log_type
        self.justification = justification
        self.status = status
        self.record_type = record_type
        self.notes = notes

class AssignedSchedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('work_schedules.id'))
    date = db.Column(db.String)
    status = db.Column(db.String(20), default="Pending")
    is_active = db.Column(db.Boolean, default=False)
    previous_schedule_id = db.Column(db.Integer, db.ForeignKey('assigned_schedules.id'))

    user = db.relationship('User', lazy=True, overlaps="assigned_schedules,user_assigned_schedules")
    schedule = db.relationship('WorkSchedules', backref='assigned_schedules', lazy=True)
    previous_schedule = db.relationship('AssignedSchedules', remote_side=[id], backref='replaced_by')

    def __init__(self, user_id, schedule_id, date, status, is_active, previous_schedule_id):
        self.user_id = user_id
        self.schedule_id = schedule_id
        self.date = date
        self.status = status
        self.is_active = is_active
        self.previous_schedule_id = previous_schedule_id

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_name = db.Column(db.String(100))
    quantity_sold = db.Column(db.Integer)
    create_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Completed")
    
    product = db.relationship('Product', back_populates='sales')
    user = db.relationship('User', back_populates='sales') 
    
    def __init__(self, product_id, quantity_sold, user_id=None, customer_name=None, status="Completed"):
        self.product_id = product_id
        self.quantity_sold = quantity_sold
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M') 
        self.user_id = user_id
        self.customer_name = customer_name
        self.status = status

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String, unique=True)

    def __init__(self, brand_name):
        self.brand_name = brand_name

class ProductTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String, unique=True)

    def __init__(self, product_type):
        self.product_type = product_type

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = "cubix.w.noreply@gmail.com"
SMTP_PASSWORD = "pcyt epef eezt nofr"  

# Default Email Configuration
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        # Enviar o email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        print(f"{Fore.GREEN}Email enviado com sucesso para {to_email}.")
    
    except Exception as e:
        print(f"{Fore.RED}Falha ao enviar email para {to_email}. Erro: {e}")

# Registration Email
def send_registration_email(user, plain_password):
    subject = "Welcome to Our Service!"
    body = f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Email | Cubix</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: Arial, sans-serif;">

    <!-- Main Container  -->
    <div style="max-width: 600px; margin: 0 auto; background-color: #181a1e; padding: 20px; border-radius: 8px;">

        <!-- Header -->
        <div style="text-align: center; padding: 10px 0;">
            <img src="https://i.postimg.cc/Hkfrz86R/Cubix-White.png" alt="Cubix Logo" style="width: 100px; margin-bottom: 20px;">
        </div>

        <!-- Main content -->
        <div style="background-color: #181a1e; color: #ffffff; padding: 20px; border-radius: 8px;">
            <h1 style="color: #ffffff; text-align: center;">Welcome to <span style="color: #ff0060;">Cubix!</span></h1>
            <p style="color: #ffffff;">Hi <span style="color: #ff0060;">{user.name}</span>,</p>
            <p style="color: #ffffff;">Thank you for registering on our platform.</p>
            <p style="color: #ffffff;">We are providing you with the login credentials for your account as requested. Below are your username and <span style="color: #f7d060; text-decoration: underline; font-size: 1.05rem;">temporary password</span> to access the platform. <span style="color: #1b9c85; font-size: 1.05rem;">We recommend changing the password upon your first login to ensure your account's security.</span></p>
            <p style="color: #ffffff; margin-top: 3rem;">Username: <span style="color: #1b9c85; font-size: 1.2rem;">{user.username}</span></p>
            <p style="color: #ffffff; margin-bottom: 3rem;">Temporary Password: <span style="color: #1b9c85; margin-top: 1rem; font-size: 1.2rem;">{plain_password}</span></p>
            <p style="color: #ffffff;">Best regards,</p>
            <p style="color: #ffffff;">Your Company Team</p>
        </div>

        <!-- Footer -->
        <div style="text-align: center; color: #ffffff; background-color: #181a1e; padding: 10px; border-radius: 8px; margin-top: 20px;">
            <p style="margin: 0;">Please be advised that this email was generated automatically from a non-monitored account. We kindly ask that you <span style="color: #ff0060;">do not reply directly to this message.</span></p>
            <p style="margin: 0;">For any assistance or inquiries, please contact our support team through the designated channels.</p>
            <p style="margin: 0;">For any authentication-related inquiries, please send an email to <span style="color: #1b9c85; font-size: 1.05rem;">brunovcoelho.dev@gmail.com</span> or <a href="https://wa.me/351965576916?text=Hello,%0A%0AI%20require%20assistance%20regarding%20authentication%20issues%20with%20my%20account.%0A%0AThank%20you%20for%20your%20attention.%0A%0ABest%20regards." target="_blank" style="text-decoration: none; color: #f7d060;">click here</a> to reach our support team.</p>
        </div>
    </div>

</body>
</html>
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_EMAIL
    msg['To'] = user.email

    # Adicionar o conteúdo HTML ao email
    msg.add_alternative(body, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  # Ativa a criptografia
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
            print(f"Email successfully sent to {user.email}")
    except Exception as e:
        print(f"Failed to send email to {user.email}. Error: {e}")

# Forgot Password Email
def send_password_reset_email(user, new_password):
    subject = "Your Password Has Been Reset"
    body = f"""
    Hi {user.name},

    Your password has been reset. Your new password is: {new_password}

    Please log in and change your password as soon as possible.

    Best regards,
    Your Company Team
    """
    send_email(user.email, subject, body)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Validates user type
@validates("user_type")
def validate_user_type(self, key, user_type):
    allowed_types = ["Admin", "Manager", "Employee", "Client"]
    assert user_type in allowed_types, f"Invalid user type. Allowed types are {allowed_types}"
    return user_type

@app.route("/")
def normal():
    return redirect(url_for("login"))

# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            user.last_login = datetime.now().strftime('%d/%m/%Y %H:%M')
            db.session.commit()
            print(f"{Fore.GREEN}Login successful.")
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
            print(f"{Fore.RED}Invalid username or password")
            return render_template("login.html", error=error)
        
    user = current_user if current_user.is_authenticated else None
    return render_template("login.html", error="", user=user)

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user = current_user if current_user.is_authenticated else None
    return render_template("dashboard.html",  user=user)

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    print(f"{Fore.GREEN}Logout successful.")
    return redirect(url_for('login'))

@app.route("/users-manager", methods=["GET", "POST"])
@login_required
def user_manager():
    if request.method == "POST":
        pass
    else:
        user = current_user if current_user.is_authenticated else None

        last_user = User.query.order_by(User.id.desc()).first()
        last_user_id = last_user.id if last_user else 0

        thirty_days_ago = datetime.now() - timedelta(days=30)
        ninety_days_ago = datetime.now() - timedelta(days=90)

        new_users_count = 0
        deactivated_users_count = 0
        deactivated_users_recent_count = 0
        
        all_users = User.query.all()
        for u in all_users:
            user_create_date = datetime.strptime(u.create_date, '%d/%m/%Y %H:%M')
            if user_create_date >= thirty_days_ago:
                new_users_count += 1

            if u.status == 'Inactive':
                deactivated_users_count += 1
                if user_create_date >= ninety_days_ago:
                    deactivated_users_recent_count += 1
        
        total_permissions = 0
        if user and user.permissions:
            permissions = user.permissions
            total_permissions = sum([
                permissions.can_adjust_inventory_differences,
                permissions.can_manage_suppliers,
                permissions.can_view_temperature_logs,
                permissions.can_adjust_temperature_discrepancies,
                permissions.can_access_high_security_areas,
                permissions.can_generate_financial_reports,
                permissions.can_manage_user_permissions,
                permissions.can_view_audit_logs,
                permissions.can_override_automatic_system_flags,
                permissions.can_manage_orders,
                permissions.can_create_new_users,
                permissions.can_active_users
            ])

        return render_template("users_manager.html", user=user, last_user_id=last_user_id, new_users_count=new_users_count, deactivated_users_count=deactivated_users_count, deactivated_users_recent_count=deactivated_users_recent_count, total_permissions=total_permissions, all_users=all_users)
    
@app.route("/manager-new-user", methods=["GET", "POST"]) 
@login_required
def manager_new_user():
    user = current_user if current_user.is_authenticated else None

    if not user.permissions.can_create_new_users:
        return render_template("no_permission_page.html", user=user)
    
    if request.method == "POST":
        username = request.form["username"]

        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        name = request.form["name"]
        nif = request.form["nif"]
        cellphone = request.form["cellphone"]
        email = request.form["email"]
        role = request.form["role"]
        user_type = request.form["user_type"]

        can_create_new_users = 'can_create_new_users' in request.form
        can_active_users = 'can_active_users' in request.form
        can_adjust_inventory_differences = 'can_adjust_inventory_differences' in request.form
        can_manage_suppliers = 'can_manage_suppliers' in request.form
        can_view_temperature_logs = 'can_view_temperature_logs' in request.form
        can_adjust_temperature_discrepancies = 'can_adjust_temperature_discrepancies' in request.form
        can_access_high_security_areas = 'can_access_high_security_areas' in request.form
        can_generate_financial_reports = 'can_generate_financial_reports' in request.form
        can_manage_user_permissions = 'can_manage_user_permissions' in request.form
        can_view_audit_logs = 'can_view_audit_logs' in request.form
        can_override_automatic_system_flags = 'can_override_automatic_system_flags' in request.form
        can_manage_orders = 'can_manage_orders' in request.form

        new_user = User(
            username=username,
            password=hashed_password, 
            name=name,
            nif=nif,
            cellphone=cellphone,
            email=email,
            role=role,
            user_type=user_type,
        )

        db.session.add(new_user)
        db.session.commit()
        print(f"{Fore.GREEN}The user has been successfully created.") 

        new_user_permissions = UserPermissions(
            user_id=new_user.id,
            can_create_new_users=can_create_new_users,
            can_active_users=can_active_users,
            can_adjust_inventory_differences=can_adjust_inventory_differences,
            can_manage_suppliers=can_manage_suppliers,
            can_view_temperature_logs=can_view_temperature_logs,
            can_adjust_temperature_discrepancies=can_adjust_temperature_discrepancies,
            can_access_high_security_areas=can_access_high_security_areas,
            can_generate_financial_reports=can_generate_financial_reports,
            can_manage_user_permissions=can_manage_user_permissions,
            can_view_audit_logs=can_view_audit_logs,
            can_override_automatic_system_flags=can_override_automatic_system_flags,
            can_manage_orders=can_manage_orders
        )

        db.session.add(new_user_permissions)
        print(f"{Fore.GREEN}Permissions have been successfully added.") 
        db.session.commit()

        send_registration_email(new_user, password)
        print(f"{Fore.GREEN}Registration Email has been successfully sent")

        return redirect(url_for("user_manager"))

    else:
        return render_template("manager_new_user_register.html", user=user)

@app.route("/reactivate-users", methods = ["POST", "GET"])
@login_required
def reactivate_users():
    user = current_user if current_user.is_authenticated else None

    if not user.permissions.can_manage_user_permissions:
        return render_template("no_permission_page.html", user=user)
    
    if request.method == "POST":
        user_name = request.form.get("user_name")
        all_users = User.query.filter(User.name.ilike(f"%{user_name}%")).all()
        return render_template("reactivate.html", user=user, all_users=all_users)
    else:
        all_users = User.query.all()

        return render_template("reactivate.html", user=user, all_users=all_users)
    
@app.route('/change-user-status/<int:user_id>/<new_status>', methods=['POST'])
@login_required
def change_user_status(user_id, new_status):
    user = User.query.get(user_id) 
    if user:
        if new_status in ['Operational', 'Inactive']: 
            user.status = new_status  
            db.session.commit() 
            flash(f'User {user.name} status changed to {new_status}.', 'success')
            print(f"{Fore.GREEN} Status changed to {new_status}")
        else:
            flash('Invalid status value.', 'danger')
            print(f"{Fore.RED} Invalid status value.")
    else:
        flash('User not found.', 'danger')
        print(f"{Fore.RED} User not found.")

    return redirect(url_for('reactivate_users'))

@app.route("/edit-user/<int:user_id>", methods=["POST", "GET"])
@login_required
def edit_user(user_id):
    user_to_edit = User.query.get(user_id) 
    if not user_to_edit:
        flash("User not found.", "danger")
        print(f"{Fore.RED} User not found.")
        return redirect(url_for("user_manager")) 
    
    if request.method == "POST":

        if request.form["username"] != user_to_edit.username:
            user_to_edit.username = request.form["username"]
        
        if request.form["name"] != user_to_edit.name:
            user_to_edit.name = request.form["name"]

        if request.form["nif"] != user_to_edit.nif:
            user_to_edit.nif = request.form["nif"]

        if request.form["cellphone"] != user_to_edit.cellphone:
            user_to_edit.cellphone = request.form["cellphone"]

        if request.form["email"] != user_to_edit.email:
            user_to_edit.email = request.form["email"]

        if request.form["role"] != user_to_edit.role:
            user_to_edit.role = request.form["role"]

        if request.form["user_type"] != user_to_edit.user_type:
            user_to_edit.user_type = request.form["user_type"]

        db.session.commit()
        flash("User details updated successfully.", "success")
        print(f"{Fore.GREEN} User details updated successfully.")
        return redirect(url_for("user_manager"))
        

    else:
        user = current_user if current_user.is_authenticated else None
        return render_template("edit_user.html", user=user, user_to_edit=user_to_edit)
    
@app.route("/reset-password/<int:user_id>", methods=["POST"])
@login_required
def reset_password(user_id):
    user = User.query.get(user_id)

    if user:
        new_password = secrets.token_hex(4)  
        user.password = generate_password_hash(new_password) 
        db.session.commit()
        flash("Password reset successfully. The new password has been sent to the user's email.", "success")
        
        send_password_reset_email(user, new_password)
        print(f"{Fore.GREEN}Password reset successfully. . New password: {new_password} and email sent.")
    else:
        flash("User not found.", "danger")

    return redirect(url_for("user_manager"))

@app.route("/all_users_page", methods=["GET", "POST"])
@login_required
def all_users_page():
    all_users = User.query.all()

    if request.method == "POST":
        pass
    else:
        user = current_user if current_user.is_authenticated else None
        return render_template("all_users_page.html", user=user , all_users=all_users)
    
@app.route("/change-permissions", methods=["GET", "POST"])
@login_required
def change_user_permissions():
    user = current_user if current_user.is_authenticated else None

    if not user.permissions.can_manage_user_permissions:
        return render_template("no_permission_page.html", user=user)
    
    if request.method == "POST":
            search_term = request.form.get("search_term", "").strip()
            search_results = User.query.filter(User.nif.contains(search_term)).all()
            if search_results:
                user_permissions = UserPermissions.query.filter_by(user_id=search_results[0].id).first()
            else:
                user_permissions = None
            return render_template("change_permissions.html", user=user, search_results=search_results, user_permissions=user_permissions)
    else:
        return render_template("change_permissions.html", user=user)

@app.route('/update-permissions/<int:user_id>', methods=['POST'])
@login_required
def update_user_permissions(user_id):
    user = User.query.get_or_404(user_id)

    permissions = {
        'can_create_new_users': request.form.get('can_create_new_users') == 'on',
        'can_active_users': request.form.get('can_active_users') == 'on',
        'can_adjust_inventory_differences': request.form.get('can_adjust_inventory_differences') == 'on',
        'can_manage_suppliers': request.form.get('can_manage_suppliers') == 'on',
        'can_view_temperature_logs': request.form.get('can_view_temperature_logs') == 'on',
        'can_adjust_temperature_discrepancies': request.form.get('can_adjust_temperature_discrepancies') == 'on',
        'can_access_high_security_areas': request.form.get('can_access_high_security_areas') == 'on',
        'can_generate_financial_reports': request.form.get('can_generate_financial_reports') == 'on',
        'can_manage_user_permissions': request.form.get('can_manage_user_permissions') == 'on',
        'can_view_audit_logs': request.form.get('can_view_audit_logs') == 'on',
        'can_override_automatic_system_flags': request.form.get('can_override_automatic_system_flags') == 'on',
        'can_manage_orders': request.form.get('can_manage_orders') == 'on'
    }

    user_permissions = UserPermissions.query.filter_by(user_id=user_id).first()

    if user_permissions:
        for key, value in permissions.items():
            setattr(user_permissions, key, value)
    else:
        user_permissions = UserPermissions(user_id=user_id, **permissions)
        db.session.add(user_permissions)

    print("Permissions changed successfully")
    db.session.commit()

    flash(f"{Fore.GREEN}User permissions updated successfully.", "success")
    return redirect(url_for('change_user_permissions'))

@app.route("/user-settings/<int:user_id>", methods=["GET","POST"])
@login_required
def user_settings(user_id):
     user = current_user if current_user.is_authenticated else None
     user_to_edit = User.query.get(user_id)

     if request.method == "POST":
        if "name" in request.form and request.form["name"].strip() and request.form["name"] != user_to_edit.name:
            user_to_edit.name = request.form["name"]

        if "password" in request.form and request.form["password"].strip():
            hashed_password = generate_password_hash(request.form["password"])
            if not check_password_hash(user_to_edit.password, request.form["password"]):
                user_to_edit.password = hashed_password

        if "cellphone" in request.form and request.form["cellphone"].strip() and request.form["cellphone"] != user_to_edit.cellphone:
            user_to_edit.cellphone = request.form["cellphone"]

        if "email" in request.form and request.form["email"].strip() and request.form["email"] != user_to_edit.email:
            user_to_edit.email = request.form["email"]
        
        db.session.commit()
        flash("User details updated successfully.", "success")
        print(f"{Fore.GREEN} User details updated successfully.")
        return redirect(url_for("user_settings", user_id=user_id))

     else:
         return render_template("user_settings.html", user=user)
     
@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    user = current_user if current_user.is_authenticated else None

    try:
        today = datetime.now().strftime('%d/%m/%Y')

        assigned_schedule = None
        work_schedule = None
        total_work_hours = None
        last_record_type = "Entry"  

        assigned_schedule = AssignedSchedules.query.filter_by(user_id=user.id, date=today).first()

        if assigned_schedule:
            schedule_id = assigned_schedule.schedule_id
            
            work_schedule = WorkSchedules.query.filter_by(id=schedule_id).first()

            if work_schedule:
                if work_schedule.time_in != "OFF" and work_schedule.time_out != "OFF":
                    time_in = datetime.strptime(work_schedule.time_in, "%H:%M")
                    time_out = datetime.strptime(work_schedule.time_out, "%H:%M")
                    lunch_start = datetime.strptime(work_schedule.lunch_start, "%H:%M") if work_schedule.lunch_start else None
                    lunch_end = datetime.strptime(work_schedule.lunch_end, "%H:%M") if work_schedule.lunch_end else None

                    total_work_time = time_out - time_in
                    
                    if lunch_start and lunch_end:
                        lunch_break_duration = lunch_end - lunch_start
                        total_work_time -= lunch_break_duration

                    total_work_hours = total_work_time.total_seconds() / 3600
                else:
                    total_work_hours = 0

                last_log = WorkSchedulesLogs.query.filter_by(user_id=user.id).order_by(WorkSchedulesLogs.create_date_in.desc()).first()
                last_record_type = last_log.record_type if last_log else "Out"

                logs = WorkSchedulesLogs.query.filter_by(user_id=user.id).all()

                def convert_to_datetime(log):
                    return datetime.strptime(log.create_date_in, '%d/%m/%Y %H:%M:%S')

                logs = sorted(logs, key=convert_to_datetime, reverse=True)  
            else:
                flash("Work schedule not found.", "danger")
                logs = []
        else:
            flash("No assigned schedule for today.", "warning")
            logs = []

    except AttributeError as e:
        flash(f"An error occurred: {str(e)}", "danger")
        logs = []
        work_schedule = None

    except Exception as ex:
        flash(f"An unexpected error occurred: {str(ex)}", "danger")
        logs = []
        work_schedule = None

    if request.method == "POST":
        try:
            log_type = request.form.get("log_type") 
            date_input = request.form.get("date")    
            time_input = request.form.get("time")    
            record_type = request.form.get("record_type")  
            justification = request.form.get("justification")

            if not record_type:
                last_log = WorkSchedulesLogs.query.filter_by(user_id=user.id).order_by(WorkSchedulesLogs.create_date_in.desc()).first()
                if last_log and last_log.record_type == "Entry":
                    record_type = "Out"
                else:
                    record_type = "Entry"

            if log_type == "on":  
                create_date_in = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

                new_log = WorkSchedulesLogs(
                    schedule_id=assigned_schedule.schedule_id,
                    user_id=user.id,
                    create_date_in=create_date_in,
                    record_type=record_type,
                    log_type="Automatic",  
                    status="Approved",  
                    justification="",  
                    notes=""
                )
                db.session.add(new_log)
                db.session.commit()
                flash("Automatic time stamp added successfully!", "success")
                print(f"{Fore.GREEN}Automatic time stamp added successfully!")
            else:  
                if date_input and time_input:  
                    datetime_input = datetime.strptime(f"{date_input} {time_input}", '%Y-%m-%d %H:%M')  
                    create_date_in = datetime_input.strftime('%d/%m/%Y %H:%M:%S')  

                    new_log = WorkSchedulesLogs(
                        schedule_id=assigned_schedule.schedule_id,
                        user_id=user.id,
                        create_date_in=create_date_in,
                        record_type=record_type,
                        log_type="Manual",  
                        status="Pending",  
                        justification=justification, 
                        notes=""
                    )
                    db.session.add(new_log)
                    db.session.commit()
                    flash("Manual time stamp added successfully!", "success")
                    print(f"{Fore.GREEN}Manual time stamp added successfully!")
                else:
                    flash("Error: Date and time not provided for manual recording.", "danger")
                    print(f"{Fore.RED}Error: Date and time not provided for manual recording.")
                    
        except Exception as e:
            flash(f"An error occurred while adding the log: {str(e)}", "danger")
            print(f"{Fore.RED}Error: {str(e)}")

        return redirect(url_for("schedule"))
    
    return render_template("schedule_home.html", user=user, work_schedule=work_schedule, total_work_hours=total_work_hours, logs=logs, last_record_type=last_record_type)   
@app.route("/schedule-manager", methods=["GET", "POST"])
@login_required
def schedule_manager():
    user = current_user if current_user.is_authenticated else None

    if user.user_type in ["Admin", "Manager"]:
        schedules_log_query = db.session.query(WorkSchedulesLogs, User.name).join(User, WorkSchedulesLogs.user_id == User.id).filter(
            and_(
                WorkSchedulesLogs.log_type == "Manual", 
                WorkSchedulesLogs.status != "Approved", 
                WorkSchedulesLogs.status != "Rejected"
            )
        )

        if request.method == "POST":
            name = request.form.get("name")
            record_type = request.form.get("record_type")

            if name:
                schedules_log_query = schedules_log_query.filter(User.name.ilike(f"%{name}%"))

            if record_type and record_type != 'all':
                schedules_log_query = schedules_log_query.filter(WorkSchedulesLogs.record_type == record_type)

        schedules_log = schedules_log_query.all()

        return render_template("schedule_manager.html", user=user, schedules_log=schedules_log)
    else:
        return render_template("no_permission_page.html", user=user)

@app.route("/approve-log/<int:log_id>", methods=["POST"])
@login_required
def approve_log(log_id):
    user = current_user if current_user.is_authenticated else None

    if user.user_type in ["Admin", "Manager"]:
        log_entry = WorkSchedulesLogs.query.get(log_id)
        
        if log_entry:
            log_entry.status = "Approved"
            db.session.commit()
            print(f"{Fore.GREEN}Log approved successfully!")
            flash("Log approved successfully!", "success")
        else:
            print(f"{Fore.RED}Log approved successfully!")
            flash("Log not found.", "danger")

        return redirect(url_for("schedule_manager"))
    else:
        return render_template("no_permission_page.html", user=user)

@app.route("/reject-log/<int:log_id>", methods=["POST"])
@login_required
def reject_log(log_id):
    user = current_user if current_user.is_authenticated else None

    if user.user_type in ["Admin", "Manager"]:
        log_entry = WorkSchedulesLogs.query.get(log_id)
        
        if log_entry:
            notes = request.form.get("notes")
            log_entry.status = "Rejected"
            log_entry.notes = notes
            db.session.commit()
            print(f"{Fore.GREEN}Log rejected successfully!")
            flash("Log rejected successfully!", "success")
        else:
            print(f"{Fore.RED}Log not found.")
            flash("Log not found.", "danger")

        return redirect(url_for("schedule_manager"))
    else:
        return render_template("no_permission_page.html", user=user)


@app.route("/approve-all-logs", methods=["POST"])
@login_required
def approve_all_logs():
    logs_to_approve = WorkSchedulesLogs.query.filter(WorkSchedulesLogs.status == 'Pending').all()

    for log in logs_to_approve:
        log.status = 'Approved'
    
    db.session.commit()
    print(f"{Fore.GREEN}All pending logs have been approved!")
    flash("All pending logs have been approved!", "success")

    return redirect(url_for('schedule_manager'))

@app.route("/reject-all-logs", methods=["POST"])
@login_required
def reject_all_logs():
    notes = request.form.get('notes')

    logs_to_reject = WorkSchedulesLogs.query.filter(WorkSchedulesLogs.status == 'Pending').all()

    for log in logs_to_reject:
        log.status = 'Rejected'
        log.notes = notes  
    
    db.session.commit()
    print(f"{Fore.GREEN}All pending logs have been rejected!")
    flash("All pending logs have been rejected!", "danger")

    return redirect(url_for('schedule_manager'))

@app.route("/schedules-all-records", methods=["GET"])
@login_required
def all_schedules_records():
    user = current_user  

    logs = WorkSchedulesLogs.query.filter_by(user_id=user.id).order_by(desc(WorkSchedulesLogs.create_date_in)).all()
    
    return render_template("schedules_all_records.html", user=user, logs=logs)

@app.route("/products-manager", methods = ["GET", "POST"])
@login_required
def products_manager():
    user = current_user if current_user.is_authenticated else None

    last_product = Product.query.order_by(Product.id.desc()).first()
    last_product_id = last_product.id if last_product else 0
    deactivated_products_count = 0
    all_products = Product.query.all()
    last_supplier = Suppliers.query.order_by(Suppliers.id.desc()).first()
    last_supplier_id = last_supplier.id if last_supplier else 0
    out_of_stock_products_count = Product.query.filter(Product.stock == 0).count()

    for p in all_products:
            if p.status == 'Inactive':
                deactivated_products_count += 1

    best_selling_products = db.session.query(Product.name, db.func.sum(Sales.quantity_sold).label('total_sales'),db.func.sum((Product.sell_price - Product.buy_price) * Sales.quantity_sold).label('total_profit')).join(Sales, Product.id == Sales.product_id).group_by(Product.id).order_by(db.func.sum(Sales.quantity_sold).desc()).limit(10).all()

    return render_template("products_manager.html", user=user, last_product_id=last_product_id, deactivated_products_count=deactivated_products_count, last_supplier_id=last_supplier_id, best_selling_products=best_selling_products, out_of_stock_products_count=out_of_stock_products_count)

@app.route("/create-new-product", methods=["POST", "GET"])
@login_required
def create_new_product():
    user = current_user if current_user.is_authenticated else None
    if user.user_type == "Admin" or user.user_type == "Manager":
        brand = request.form.get("brand")
        name = request.form.get("name")
        product_type = request.form.get("product_type")
        buy_price = request.form.get("buy_price")
        margin = request.form.get("margin")
        min_recommended_stock = request.form.get("min_recommended_stock")
        warehouse_section = request.form.get("warehouse_section")
        warehouse_shelf = request.form.get("warehouse_shelf")

        if request.method == "POST":
            sell_price = buy_price + (buy_price * margin / 100)
            
            new_product = Product(
                brand = brand,
                # Continuar a criar a criação dos dados para inserir na base de dados
            )
        else:
            return render_template("create_new_product.html", user=user)
    else:
        return render_template("no_permission_page.html", user=user)
    
@app.route("/get_brands", methods=["GET"])
def get_brands():
    brands = Brands.query.all() 
    brands_list = [{"id": brand.id, "name": brand.brand_name} for brand in brands]
    return jsonify(brands_list)

@app.route("/get-product-type", methods=["GET"])
def get_product_types():
    product_types = ProductTypes.query.all() 
    product_type_list = [{"id": t.id, "name": t.product_type} for t in product_types]
    return jsonify(product_type_list)

@app.route("/product-page/<int:product_id>", methods=["GET"])
def product_page(product_id):
    product = Product.query.filter_by(id=product_id).first()
    
    if not product:
        flash("Product not found.", "danger")
        print(f"{Fore.RED} Product not found.")
        return render_template("no_product_page.html")

    return render_template("product_page.html", product=product)

@app.route("/all-products", methods=["GET", "POST"])
@login_required
def all_products():
    user = current_user if current_user.is_authenticated else None
    all_products = Product.query.all()
    
    if request.method == "POST":
        pass
    else:
        return render_template("all_products_page.html", user=user, all_products=all_products)
    
@app.route("/generate_qr_code/<int:product_id>")
def generate_qr_code(product_id):
    product = db.session.get(Product, product_id)
    
    if not product or not product.qr_code_path:
        return "Product or QR Code path not found", 404
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(product.qr_code_path)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def create_user():
    user = User(username="adhasdasihdaoisasdasdasdasdasdadadadsadd",
                password="test",
                user_type="Employee",
                nif = "784512547a",
                email = "employeeeee@example.com",
                name = "Marcooo Vieira",
                cellphone = "9411244615678"
                )
    db.session.add(user)
    db.session.commit()
    print(f"{Fore.GREEN}Criado Com sucesso")

def create_work_schedules():
    schedules = WorkSchedules(
        schedule = "OFF",
        time_in = "",
        time_out = "",
        lunch_start = "",
        lunch_end = ""
    )
    db.session.add(schedules)
    db.session.commit()
    print(f"{Fore.GREEN}Criado Com sucesso")

def assign_schedules_for_september(user_id=3):
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2024, 10, 31)

    week_schedule_a = 1  
    week_schedule_b = 2  
    weekend_off = 9      

    current_date = start_date
    week_counter = 0

    while current_date <= end_date:
        
        if current_date.weekday() >= 5:  
            schedule_id = weekend_off
        else:
            
            if week_counter % 2 == 0:
                schedule_id = week_schedule_a
            else:
                schedule_id = week_schedule_b

        
        date_str = current_date.strftime('%d/%m/%Y')

        new_schedule = AssignedSchedules(
            user_id=user_id,
            schedule_id=schedule_id,
            date=date_str,
            status = "Approved",
            is_active = True,
            previous_schedule_id = 0
            )
        db.session.add(new_schedule)

        current_date += timedelta(days=1)

        if current_date.weekday() == 0:  
            week_counter += 1

    db.session.commit()
    print("Horários atribuídos para o mês de setembro.")

def creat_product():
    margin = 120  
    buy_price = 745.47

    sell_price = buy_price + (buy_price * margin / 100)

    new_product = Product(
        ref = "SPR54791349",
        qr_code_path = "teste3",
        name = "Brake Clean 200L",
        product_type = "Produtos Químicos",
        brand = "Facon",
        model = "None",
        buy_price = buy_price,
        sell_price = sell_price,
        margin = margin,
        stock = 3,
        min_recommended_stock = 5,
        last_update = "",
        warehouse_section = "D",
        warehouse_shelf = 1,
        status = "Active",
        update_info = datetime.now().strftime('%d/%m/%Y %H:%M')
    )

    db.session.add(new_product)
    db.session.commit()
    print(f"{Fore.GREEN}Criado Com sucesso")

def create_test_supplier():
    new_supplier = Suppliers(
        supplier_name="Teste Supplier",
        contact_name="John Doe",
        contact_email="john.doe@test.com",
        contact_phone="+351912345678",
        type="Alimentar",
        country="Portugal",
        adress="1234 Test Avenue, Lisbon",
        payment_terms="Net 30",
        credit_limit=10000,
        last_order_date=datetime.now().strftime('%d/%m/%Y'),
        rating=5
    )
    
    db.session.add(new_supplier)
    db.session.commit()

    print(f"{Fore.GREEN}Fornecedor {new_supplier.supplier_name} criado com sucesso!")

def create_sales_entries():
    customers = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Davis", "Chris Brown"]
    
    product_ids = [1, 2,3]
    user_ids = [1, 2]  
    
    for _ in range(20):
        product_id = choice(product_ids)
        user_id = choice(user_ids)
        customer_name = choice(customers) 
        quantity_sold = randint(1, 30) 
        
        new_sale = Sales(
            product_id=product_id,
            quantity_sold=quantity_sold,
            user_id=user_id,
            customer_name=customer_name,
            status="Completed"
        )
        
        db.session.add(new_sale)
    db.session.commit()
    print("Vendas criadas com sucesso!")

def create_brands():
    brands = [
        "Falcon", "Facon", "Bosch", "Philips", "Samsung", "Sharp", "Kenmore", "Electrolux", "KitchenAid", "Whirlpool",
        "Sony", "LG", "Panasonic", "GE Appliances", "Frigidaire", "Miele", "Maytag", "Sub-Zero", "Viking", "Thermador",
        "Siemens", "Beko", "Haier", "Hitachi", "Liebherr", "Gorenje", "Smeg", "Zanussi", "Fisher & Paykel", "DeLonghi",
        "Braun", "Rowenta", "Tefal", "Krups", "Russell Hobbs", "Morphy Richards", "Dyson", "Hoover", "Bissell", "Shark",
        "Makita", "DeWalt", "Black & Decker", "Craftsman", "Ryobi", "Milwaukee", "Hitachi Tools", "Hilti", "Bosch Tools",
        "Karcher", "Stanley", "Metabo", "Ridgid", "Skil", "Worx", "Dremel", "Festool", "Porter-Cable", "Husqvarna",
        "Honda", "Yamaha", "Kawasaki", "Suzuki", "Harley-Davidson", "Ducati", "BMW", "Mercedes-Benz", "Audi", "Volkswagen",
        "Porsche", "Ford", "Chevrolet", "Cadillac", "Buick", "Jeep", "Tesla", "Nissan", "Toyota", "Subaru", "Mitsubishi",
        "Hyundai", "Kia", "Mazda", "Volvo", "Land Rover", "Jaguar", "Peugeot", "Renault", "Citroen", "Fiat", "Alfa Romeo",
        "Ferrari", "Lamborghini", "Bugatti", "Maserati", "McLaren", "Aston Martin", "Rolls-Royce", "Bentley", "Pagani",
        "Hugo Boss", "Gucci", "Prada", "Versace", "Armani", "Ralph Lauren", "Calvin Klein", "Tommy Hilfiger", "Nike", "Adidas",
        "Puma", "Reebok", "Under Armour", "New Balance", "Fila", "Converse", "Vans", "Levi's", "Wrangler", "Diesel",
        "Gap", "Zara", "H&M", "Uniqlo", "Benetton", "Burberry", "Givenchy", "Yves Saint Laurent", "Hermes", "Chanel",
        "Louis Vuitton", "Balenciaga", "Fendi", "Valentino", "Dolce & Gabbana", "Alexander McQueen", "Celine", "Christian Dior",
        "Rolex", "Omega", "Tag Heuer", "Breitling", "Patek Philippe", "Audemars Piguet", "Vacheron Constantin", "Seiko",
        "Citizen", "Casio", "Swatch", "Fossil", "Michael Kors", "Tissot", "Longines", "Hublot", "Panerai", "IWC", "Chopard",
        "Cartier", "Montblanc", "Bvlgari", "Tiffany & Co.", "Ray-Ban", "Oakley", "Persol", "Maui Jim", "Tom Ford",
        "Warby Parker", "Bose", "JBL", "Sennheiser", "Beats by Dre", "Sony Audio", "Bang & Olufsen", "Klipsch", "Pioneer",
        "Harman Kardon", "Denon", "Marantz", "Onkyo", "Yamaha Audio", "Focal", "KEF", "Bowers & Wilkins", "Polk Audio",
        "Logitech", "Corsair", "Razer", "SteelSeries", "HyperX", "Alienware", "MSI", "Asus", "Acer", "Dell", "HP",
        "Lenovo", "Toshiba", "Apple", "Microsoft", "Google", "Amazon", "Intel", "AMD", "NVIDIA", "Seagate", "Western Digital",
        "Sandisk", "Kingston", "Crucial", "Corsair Memory", "G.SKILL", "Samsung SSD", "Sony PlayStation", "Microsoft Xbox",
        "Nintendo", "Logitech Gaming", "Thrustmaster", "Roccat", "Cooler Master", "EVGA", "Zotac", "ASRock", "Gigabyte",
        "Biostar", "HP Enterprise", "Synology", "QNAP", "Netgear", "TP-Link", "Cisco", "Ubiquiti", "D-Link", "Linksys",
        "Huawei", "Xiaomi", "OnePlus", "Oppo", "Realme", "Vivo", "Honor", "ZTE", "Sony Mobile", "Nokia", "BlackBerry",
        "Motorola", "HTC", "Palm", "LG Mobile", "Lenovo Mobile", "Alcatel", "Micromax", "Blu", "Infinix", "Tecno",
        "Itel", "Gionee", "Lava", "Coolpad", "Meizu", "Vernee", "LeEco", "Doogee", "Cubot", "UMIDIGI", "Oukitel",
        "CAT", "Kyocera", "Sonim", "Fairphone", "Jolla", "Turing", "Yota", "Kogan", "Google Pixel", "Asus ROG Phone",
        "Nubia", "Redmi", "Honor Magic", "Realme Narzo", "Poco", "iQOO", "Vivo Nex", "Oppo Find", "Xiaomi Mi",
        "Xiaomi Redmi", "Xiaomi Black Shark", "OnePlus Nord", "Sony Xperia", "Sharp Aquos", "TCL", "Hisense", "Panasonic Viera",
        "Philips TV", "Samsung QLED", "LG OLED", "Vizio", "Roku TV", "Insignia", "Toshiba TV", "Hitachi TV", "Westinghouse",
        "Element Electronics", "Sceptre", "Skyworth", "Changhong", "Vu Televisions", "Thomson TV", "iFFALCON", "Blaupunkt",
        "Haier TV", "BPL", "Kodak", "Micromax TV", "Lloyd", "Aisen", "Shinco", "Noble Skiodo", "Activa", "Murphy",
        "Intex", "Salora", "Daewoo", "Akai", "AOC", "Polaroid", "Toshiba Laptops", "Sony Vaio", "Acer Predator",
        "Asus TUF", "HP Omen", "Dell XPS", "Microsoft Surface", "Lenovo ThinkPad", "Razer Blade", "Alienware Gaming",
        "MSI Gaming", "Gigabyte Aero", "Huawei MateBook", "Apple MacBook", "Google Chromebook", "Samsung Galaxy Book",
        "LG Gram", "Fujitsu Laptops", "Panasonic Toughbook", "NEC Computers", "Toshiba Portege", "Sony Walkman",
        "Bowers & Wilkins Headphones", "Shure", "Jabra", "Plantronics", "Audio-Technica", "Beyerdynamic", "AKG", "Grado",
        "Focal Headphones", "Audeze", "Sennheiser HD", "V-Moda", "FiiO", "Klipsch Headphones", "Ultimate Ears", "Anker",
        "Belkin", "Mophie", "OtterBox", "Spigen", "LifeProof", "Incase", "Speck", "Targus", "Kensington", "Case Logic"
    ]
    
    try:
        for brand in brands:
            new_brand = Brands(brand_name=brand)  
            db.session.add(new_brand)
        
        db.session.commit()
        print("Marcas criadas com sucesso!")
    except Exception as e:
        db.session.rollback()  
        print(f"Erro ao criar marcas: {e}")

def create_product_types():
    types = [
        "Electronics", "Furniture", "Clothing", "Food", "Appliances", 
        "Automotive", "Beauty Products", "Books", "Building Materials", 
        "Cameras", "Cell Phones", "Computers", "Drones", "Fitness Equipment", 
        "Gaming Consoles", "Garden Supplies", "Groceries", "Hand Tools", 
        "Health Products", "Home Decor", "Industrial Equipment", "Jewelry", 
        "Kitchenware", "Laptops", "Lighting", "Luggage", "Musical Instruments", 
        "Office Supplies", "Outdoor Gear", "Pet Supplies", "Pharmaceuticals", 
        "Power Tools", "Printers", "Security Systems", "Shoes", "Smart Devices", 
        "Sporting Goods", "Stationery", "Toys", "TVs", "Vacuum Cleaners", 
        "Watches", "Wine & Spirits", "Cleaning Supplies", "Medical Equipment", 
        "Bicycles", "Camping Equipment", "Travel Accessories", "Luxury Goods", 
        "Art Supplies", "Audio Equipment", "Baby Products", "Bedding", 
        "Craft Supplies", "Gift Items", "Outdoor Furniture", "Party Supplies", 
        "Plumbing Supplies", "Seasonal Decor", "Storage Solutions", 
        "Sunglasses", "Tableware", "Textiles", "Tools", "Toys & Games", 
        "Vehicles", "Welding Equipment", "Window Coverings", "Workout Gear", 
        "Bakery Products", "Batteries", "Beverages", "Candles", "Car Care Products",
        "Cookware", "Cosmetics", "Detergents", "Diapers", "Fabrics", 
        "Fishing Gear", "Footwear", "Fragrances", "Gardening Tools", 
        "Gift Cards", "Grills", "Headphones", "Hiking Gear", "Home Improvement", 
        "Hunting Gear", "Ink & Toner", "Interior Decor", "Janitorial Supplies", 
        "Laundry Supplies", "Mattresses", "Motorcycle Parts", "Nutritional Supplements", 
        "Office Furniture", "Painting Supplies", "Party Favors", "Personal Care", 
        "Pet Food", "Photography Equipment", "Pool Supplies", "Refrigerators", 
        "Scooters", "Smart Home Devices", "Solar Panels", "Sportswear", 
        "Stationery Supplies", "Surgical Supplies", "Table Lamps", "Tents", 
        "Tires", "Travel Bags", "Vitamins & Supplements", "Washing Machines", 
        "Welding Supplies", "Wind Turbines", "Work Boots", "Yoga Equipment"
    ]

    try:
        for t in types:
            new_type = ProductTypes(product_type=t)  
            db.session.add(new_type)
        
        db.session.commit()
        print("Tipos criados com sucesso!")
    except Exception as e:
        db.session.rollback()  
        print(f"Erro ao criar marcas: {e}")

if __name__ == "__main__":
    init(autoreset=True)
    with app.app_context():
        db.create_all()
        #create_user()
        #create_work_schedules()
        #assign_schedules_for_september()
        #creat_product()
        #create_test_supplier()
        #create_sales_entries()
        #create_brands()
        #create_product_types()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

>>>>>>> origin/main
    # use_reloader=False