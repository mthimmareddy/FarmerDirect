#hello
from datetime import datetime
from __init__ import db
db.Model.metadata.reflect(db.engine)

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin




class User(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address1 = db.Column(db.String(30), unique=False, nullable=False)
    address2 = db.Column(db.String(20), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(20), unique=False, nullable=False)
    country = db.Column(db.String(20), unique=False, nullable=False)
    zipcode = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    isadmin = db.Column(db.Integer, nullable=False, default=0)
    image_file = db.Column(db.String(200), nullable=False, default='default.jpg')
    farm_image = db.Column(db.String(200), nullable=False, default='farm.jpg')
    farmdescription = db.Column(db.String(500), nullable=False, default="Oraganic farm")
    user_rating = db.Column(db.DECIMAL,nullable=True)
    user_review = db.Column(db.String(100), nullable=True)


    def __repr__(self):
        return "User('{self.fname}', '{self.lname}'), '{self.password}', " \
               "'{self.address1}', '{self.address2}', '{self.city}', '{self.state}', '{self.country}'," \
               "'{self.zipcode}','{self.email}','{self.phone}')"


class Category(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_image = db.Column(db.String(200), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Category('{self.categoryid}', '{self.category_name}','{self.image_file}')"


class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    sku = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(100), nullable=True)
    image2 = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    regular_price = db.Column(db.DECIMAL)
    product_scale = db.Column(db.String(20), nullable=True)
    product_rating = db.Column(db.DECIMAL)
    product_review = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "Product('{self.productid}','{self.product_name}','{self.description}', '{self.image}',  '{self.quantity}', '{self.regular_price}',{self.producerid}')"


class ProducerProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    producerid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Product('{self.producerid}', '{self.productid}')"


class ProductCategory(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Product('{self.categoryid}', '{self.productid}')"


class Cart(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Cart('{self.userid}', '{self.productid}, '{self.quantity}')"




class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    orderid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)

    def __repr__(self):
        return "Order('{self.orderid}', '{self.order_date}','{self.total_price}','{self.userid}'')"


class OrderedProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    ordproductid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey('order.orderid'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Order('{self.ordproductid}', '{self.orderid}','{self.productid}','{self.quantity}')"


####################################################################################################
###############RENTAL PRODUCT TABLES###############################################################
###################################################################################################
class RentalCategory(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_image = db.Column(db.String(200), nullable=False, default='default.jpg')

    def __repr__(self):
        return "RentalCategory('{self.categoryid}', '{self.category_name}','{self.image_file}')"


class RentalProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(100), nullable=True)
    image2 = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_scale=db.Column(db.String(100), nullable=True)
    regular_price = db.Column(db.DECIMAL)
    product_rating = db.Column(db.DECIMAL)
    product_review = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "RentalProduct('{self.productid}','{self.product_name}','{self.description}', '{self.image}',  '{self.quantity}', '{self.regular_price}', '{self.city}')"


class RentalProducerProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    producerid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('rental_product.productid'), nullable=False, primary_key=True)


    def __repr__(self):
        return "RentalProducerProduct('{self.producerid}', '{self.productid}')"


class RentalProductCategory(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryid = db.Column(db.Integer, db.ForeignKey('rental_category.categoryid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('rental_product.productid'), nullable=False, primary_key=True)

    def __repr__(self):
        return "RentalProductCategory('{self.categoryid}', '{self.productid}')"


class RentalCart(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('rental_product.productid'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "RentalCart('{self.userid}', '{self.productid}, '{self.quantity}','{self.days}')"




class RentalOrder(db.Model):
    __table_args__ = {'extend_existing': True}
    orderid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    rentalproductid = db.Column(db.Integer, db.ForeignKey('rental_product.productid'), nullable=False, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)
    rentalorder_date = db.Column(db.DateTime, nullable=False)
    rentalreturn_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    rental_status = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return "RentalOrder('{self.orderid}', '{self.rentalproductid}','{self.userid}','{self.rentalorder_date}','{self.rentalreturn_date}','{self.total_price}','{self.rental_status}')"




class RentalOrderedProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    ordproductid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey('rental_order.orderid'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('rental_product.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "RentalOrderedProduct('{self.ordproductid}', '{self.orderid}','{self.productid}','{self.quantity}')"



class SaleTransaction(db.Model):
    __table_args__ = {'extend_existing': True}
    transactionid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey('order.orderid'), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.DECIMAL, nullable=False)
    cc_number = db.Column(db.String(50), nullable=False)
    cc_type = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "Order('{self.transactionid}', '{self.orderid}','{self.transactiondate}','{self.amount}', '{self.cc_number}','{self.cc_type}','{self.response}')"









class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)

    def __repr__(self):
        return "Post('{self.title}', '{self.date_posted}','{self.content}','{self.author}')"


