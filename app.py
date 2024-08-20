from flask import *
from flask_login import *
import os
from flask_sqlalchemy import *
from datetime import datetime 
import base64
import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import validates

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
    user_type = db.Column(db.String(50), default="Client")

    product_movements = db.relationship('ProductMovements', back_populates='user', lazy=True)

    def __init__(self, username, password, nif, email, name, cellphone, last_login=None, status="Active", user_type="Client"):
        self.username = username
        self.password = password
        self.nif = nif
        self.email = email
        self.name = name.title()
        self.cellphone = cellphone
        self.create_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.last_login = last_login
        self.status = status.capitalize()
        self.user_type = user_type.capitalize()

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
# @login_required
def user_manager():
    if request.method == "POST":
        pass
    else:
        user = current_user if current_user.is_authenticated else None
        return render_template("users_manager.html", user=user)

def create_user():
    user = User(username="admin",
                password="admin",
                user_type="Admin",
                nif = "999999999",
                email = "test@example.com",
                name = "Bruno Coelho",
                cellphone = "111111111"
                )
    db.session.add(user)
    db.session.commit()
    print("Criado Com sucesso")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        #create_user()
    app.run(host="0.0.0.0", port=5000, debug=True)