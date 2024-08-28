from flask import *
from flask_login import *
import os
from flask_sqlalchemy import *
from datetime import *
import base64
import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import validates
import random

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
    status = db.Column(db.String(20), default="Active")
    role = db.Column(db.String(40))
    user_type = db.Column(db.String(50), default="Client")
    pin = db.Column(db.Integer, unique=True)

    product_movements = db.relationship('ProductMovements', back_populates='user', lazy=True)
    permissions = db.relationship("UserPermissions", uselist=False, back_populates="user")

    def __init__(self, username, password, nif, email, name, cellphone, role=None, last_login=None, status="Active", user_type="Client"):
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
    warehouse_section = db.Column(db.Integer)
    warehouse_shelf = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Active")
    update_info = db.Column(db.String(20))

    product_movements = db.relationship('ProductMovements', back_populates='product', lazy=True)
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True)

    def __init__(self, ref, qr_code_path, name, product_type, brand, model, buy_price, sell_price, margin, stock, min_recommended_stock, last_update, update_info, status="Active"):
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
        if user and user.password == password:
            login_user(user)
            user.last_login = datetime.now().strftime('%d/%m/%Y %H:%M')
            db.session.commit()
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
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

            if u.status == 'Deactive':
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
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

        new_user = User (
            username = username,
            password = password,
            name = name,
            nif = nif,
            cellphone = cellphone,
            email = email,
            role = role,
            user_type = user_type,
        )

        db.session.add(new_user)
        db.session.commit()
        print("The user has been successfully created.")

        new_user_permissions = UserPermissions(
            user_id=new_user.id,
            can_create_new_users = can_create_new_users,
            can_active_users = can_active_users,
            can_adjust_inventory_differences = can_adjust_inventory_differences,
            can_manage_suppliers = can_manage_suppliers,
            can_view_temperature_logs = can_view_temperature_logs,
            can_adjust_temperature_discrepancies = can_adjust_temperature_discrepancies,
            can_access_high_security_areas = can_access_high_security_areas,
            can_generate_financial_reports = can_generate_financial_reports,
            can_manage_user_permissions = can_manage_user_permissions,
            can_view_audit_logs = can_view_audit_logs,
            can_override_automatic_system_flags = can_override_automatic_system_flags,
            can_manage_orders = can_manage_orders
        )

        db.session.add(new_user_permissions)
        print("Permissions have been successfully added.")
        db.session.commit()

        return redirect(url_for("user_manager"))

    else:
        user = current_user if current_user.is_authenticated else None
        return render_template("manager_new_user_register.html",  user=user)
    
@app.route("/reactivate-users", methods = ["POST", "GET"])
#@login_required
def reactivate_users():
    if request.method == "POST":
        pass
    else:
        all_users = User.query.all()

        user = current_user if current_user.is_authenticated else None
        return render_template("reactivate.html", user=user, all_users=all_users)


def create_user():
    user = User(username="test",
                password="teste",
                user_type="Employee",
                nif = "784512547",
                email = "employee@example.com",
                name = "Darlin Vieira",
                cellphone = "941124478"
                )
    db.session.add(user)
    db.session.commit()
    print("Criado Com sucesso")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        #create_user()
    app.run(host="0.0.0.0", port=5000, debug=True)