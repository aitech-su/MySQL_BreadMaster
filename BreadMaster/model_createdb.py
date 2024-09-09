from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

# 建立Flask應用程式
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Hsnut%40102260424@localhost:3306/breadmaster'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 建立與MySQL伺服器的連線
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='Hsnut@102260424'
)

# 建立資料庫
try:
    with connection.cursor() as cursor:
        sql = "CREATE DATABASE IF NOT EXISTS breadmaster"
        cursor.execute(sql)
    connection.commit()
    print("資料庫 'breadmaster' 建立成功")
except pymysql.Error as e:
    print("資料庫建立失敗:", str(e))
finally:
    connection.close()

# 建立資料庫連線
db = SQLAlchemy(app)

# 定義模型 table
class Buyer(db.Model):
    __tablename__ = 'buyer'
    phone_number = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    late_record = db.Column(db.Integer, default=0)

class Store(db.Model):
    __tablename__ = 'store'
    branch_name = db.Column(db.String(50), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    business_hours = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    order_number = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), db.ForeignKey('buyer.phone_number'))
    order_status = db.Column(db.String(20), nullable=False)
    order_time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

class Leftover_Product(db.Model):
    __tablename__ = 'leftover_product'
    branch_name = db.Column(db.String(50), db.ForeignKey('store.branch_name'), primary_key=True, index = True)
    product_code = db.Column(db.String(20), primary_key=True, index = True)
    expiration_date = db.Column(db.Date, nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    product_description = db.Column(db.String(200), nullable=False)
    
class Order_Item(db.Model):
    __tablename__ = 'order_item'
    order_number = db.Column(db.Integer, db.ForeignKey('orders.order_number'), primary_key=True)
    branch_name = db.Column(db.String(50), db.ForeignKey('store.branch_name'), primary_key=True)
    product_code = db.Column(db.String(20), db.ForeignKey('leftover_product.product_code'), primary_key=True)
    item_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    quantity_ordered = db.Column(db.Integer, nullable=False)

class Leftover_History(db.Model):
    __tablename__ = 'leftover_history'
    branch_name = db.Column(db.String(50), db.ForeignKey('store.branch_name'), primary_key=True)
    product_code = db.Column(db.String(20), db.ForeignKey('leftover_product.product_code'), primary_key=True)
    removal_time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), primary_key=True)
    quantity_removed = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = 'review'
    phone_number = db.Column(db.String(20), db.ForeignKey('buyer.phone_number'), primary_key=True)
    branch_name = db.Column(db.String(50), db.ForeignKey('store.branch_name'), primary_key=True)
    score = db.Column(db.Integer)
    content = db.Column(db.String(500))

class Frequently_Used_Store(db.Model):
    __tablename__ = 'frequently_used_store'
    phone_number = db.Column(db.String(20), db.ForeignKey('buyer.phone_number'), primary_key=True)
    branch_name = db.Column(db.String(50), db.ForeignKey('store.branch_name'), primary_key=True)


# 建立資料表
with app.app_context():  
    db.create_all()
    db.session.commit()
