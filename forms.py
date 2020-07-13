import hashlib
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from flask import session
from flask import url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, RadioField, FloatField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email
import random
from __init__ import mysql,db
from models import *
import routes

def update_rentalOrderStatus():
    print(datetime.now())


def knowrentalprices(productid,numdays=1,driver=False,delivery=False):
        regular_price= RentalProduct.query.with_entities(RentalProduct.regular_price).filter(RentalProduct.productid==productid).first()
        print(regular_price[0])
        totalsum = 0
        driver_charges=0
        delivery_charges=0
        rent =int(regular_price[0])*numdays
        if driver:
            driver_charges = 500*numdays
        if delivery:
            delivery_charges = 500
        tax = ("%.2f" % (.06 * float(totalsum)))
        totalsum = rent+driver_charges+delivery_charges
        # print(totalsum,tax,productsincart)
        return (rent,totalsum,delivery_charges,driver_charges,tax)


def searchproducts(search_string):
    products = Product.query.all()
    data = []
    for item in products:
        if search_string in item.product_name:
            data.append(item)
    #print('data:',data)
    final_data = massageItemData(data)
    return final_data

def productsbyproducer(email):
    userid=User.query.with_entities(User.userid).filter(User.email == email).first()
    print(userid)

    productDetailsByuserId = Product.query.join(ProducerProduct, Product.productid == ProducerProduct.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.discounted_price,
                     Product.image) \
        .join(User, User.userid == ProducerProduct.producerid) \
        .filter(User.userid == userid) \
        .add_columns(User.fname) \
        .all()

    print('productDetailsByuserId', productDetailsByuserId)

    # producerName = productDetailsByuserId[0].fname
    data = massageItemData(productDetailsByuserId)
    print(data)
    return data


def getAllProducts():
    itemData = Product.query.join(ProductCategory, Product.productid == ProductCategory.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.description,
                     Product.image, Product.quantity) \
        .join(Category, Category.categoryid == ProductCategory.categoryid) \
        .order_by(Category.categoryid.desc()) \
        .all()
    data = massageItemData(itemData)

    return itemData


def getCategoryDetails():
    itemData = Category.query.join(ProductCategory, Category.categoryid == ProductCategory.categoryid) \
        .join(Product, Product.productid == ProductCategory.productid) \
        .order_by(Category.categoryid.desc()) \
        .distinct(Category.categoryid) \
        .all()


    itemDataByUser = Category.query.join(ProductCategory, Category.categoryid == ProductCategory.categoryid) \
        .join(ProducerProduct, ProductCategory.productid == ProducerProduct.productid).filter(ProducerProduct.producerid == 2)\
        .order_by(Category.categoryid.desc()) \
        .distinct(Category.categoryid) \
        .all()
    print('itemDataByUser',itemDataByUser)

    return itemData

def getProducerCategory(category_name):
    categoryId = Category.query.with_entities(Category.categoryid).filter(
        Category.category_name == category_name).first()
    print('Inside new function',category_name,categoryId)
    itemData=User.query.join(ProducerProduct, User.userid == ProducerProduct.producerid) \
            .add_columns(User.image_file,User.fname, User.city,User.userid, User.email, ProducerProduct.producerid, ProducerProduct.productid)\
            .join(ProductCategory, ProductCategory.productid == ProducerProduct.productid)\
        .add_columns(ProductCategory.categoryid).filter(ProductCategory.categoryid==categoryId).all()


    '''
    productDetailsByCategoryIdperuser = ProductCategory.query.with_entities(ProductCategory.productid).filter(ProductCategory.categoryid == categoryId) \
            .join(Product,Product.productid == ProductCategory.productid)\
            .add_columns(Product.product_name,Product.description,Product.image,Product.quantity,Product.regular_price,
                         Product.discounted_price).all()
    '''
    productDetailsByCategoryIdperuser = Product.query.join(ProductCategory).filter(ProductCategory.categoryid == categoryId) \
        .join(ProducerProduct).filter(ProducerProduct.producerid == 4).all()
    #print('productDetailsByCategoryIdperuser',productDetailsByCategoryIdperuser,len(productDetailsByCategoryIdperuser))

    return itemData,productDetailsByCategoryIdperuser,len(itemData)

def getRentOwnersDetails(loc=None,cat=None):
    if cat and not loc:
        itemData = User.query.join(RentalProducerProduct, User.userid == RentalProducerProduct.producerid) \
            .add_columns(User.fname, User.userid, User.city)\
            .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
            .add_columns(RentalProductCategory.categoryid).filter(RentalProductCategory.categoryid==cat)\
            .join(RentalCategory, RentalCategory.categoryid == cat ) \
            .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()

    elif loc and not cat:
        itemData = User.query.filter(User.city==loc).join(RentalProducerProduct, User.userid == RentalProducerProduct.producerid) \
            .add_columns(User.fname, User.userid, User.city) \
            .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
            .add_columns(RentalProductCategory.categoryid) \
            .join(RentalCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
            .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()

    elif loc and cat:
        itemData = User.query.filter(User.city==loc).join(RentalProducerProduct, User.userid == RentalProducerProduct.producerid) \
            .add_columns(User.fname, User.userid, User.city)\
            .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
            .add_columns(RentalProductCategory.categoryid).filter(RentalProductCategory.categoryid==cat)\
            .join(RentalCategory, RentalCategory.categoryid == cat ) \
            .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()
    else:

        itemData = User.query.join(RentalProducerProduct, User.userid == RentalProducerProduct.producerid) \
            .add_columns(User.fname, User.userid, User.city) \
            .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
            .add_columns(RentalProductCategory.categoryid) \
            .join(RentalCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
            .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()
    return itemData

def getProducerDetails(rent=False):
    '''
    itemData2=User.query.join(ProducerProduct, User.userid == ProducerProduct.producerid) \
        .add_columns(User.fname,User.email,User.userid,User.city,User.image_file).distinct(User.userid)\
        .join(ProductCategory, ProductCategory.productid == ProducerProduct.productid)\
        .add_columns(ProductCategory.categoryid)\
        .join(Category, Category.categoryid == ProductCategory.categoryid)\
        .add_columns(Category.category_name,Category.categoryid).all()
    '''
    itemData2=User.query.filter_by(isadmin=1).all()


    data2 = RentalProducerProduct.query.join(RentalProductCategory,
                                             RentalProducerProduct.productid == RentalProductCategory.productid) \
        .join(User, User.userid == RentalProducerProduct.producerid) \
        .add_columns(User.fname, User.image_file, User.userid, User.address1, User.address2, User.city,
                     User.zipcode,User.phone) \
        .add_columns(RentalProductCategory.categoryid).join(RentalCategory,
                                                            RentalCategory.categoryid == RentalProductCategory.categoryid) \
        .add_columns(RentalCategory.category_name).all()

    farmerrentcategories = {}

    for item in data2:
        farmerrentcategories.setdefault(item.fname, list(set([]))).append(item.category_name)
    for k, v in farmerrentcategories.items():
        farmerrentcategories[k] = list(set(v))
        #farmerrentcategories, Producerdata = modifyProducerdata(data2)
        #return farmerrentcategories, Producerdata

    data1 = ProducerProduct.query.join(ProductCategory, ProducerProduct.productid == ProductCategory.productid) \
        .join(User, User.userid == ProducerProduct.producerid)\
        .add_columns(User.fname,User.image_file,User.userid,User.address1,User.address2,User.city,User.zipcode,User.phone)     \
        .add_columns(ProductCategory.categoryid).join(Category,Category.categoryid == ProductCategory.categoryid)\
        .add_columns(Category.category_name).all()
    farmercategories = {}

    for item in data1:
        farmercategories.setdefault(item.fname, list(set([]))).append(item.category_name)
    for k, v in farmercategories.items():
        farmercategories[k] = list(set(v))
    farmercategories,Producerdata=modifyProducerdata(data1,data2)

    return farmercategories,Producerdata

def getFarmerData(city_name=None,category_name=None):
    data=''
    data1 = ProducerProduct.query.join(ProductCategory, ProducerProduct.productid == ProductCategory.productid) \
        .join(User, User.userid == ProducerProduct.producerid) \
        .add_columns(User.fname, User.image_file, User.userid, User.address1, User.address2, User.city, User.zipcode,
                     User.phone) \
        .add_columns(ProductCategory.categoryid).join(Category, Category.categoryid == ProductCategory.categoryid) \
        .add_columns(Category.category_name).all()
    data2 = RentalProducerProduct.query.join(RentalProductCategory,
                                             RentalProducerProduct.productid == RentalProductCategory.productid) \
        .join(User, User.userid == RentalProducerProduct.producerid) \
        .add_columns(User.fname, User.image_file, User.userid, User.address1, User.address2, User.city,
                     User.zipcode, User.phone) \
        .add_columns(RentalProductCategory.categoryid).join(RentalCategory,
                                                            RentalCategory.categoryid == RentalProductCategory.categoryid) \
        .add_columns(RentalCategory.category_name).all()
    data = modifyProducerdata(data1, data2)


    if city_name and category_name:
        if Category.query.filter_by(category_name=category_name).first():
            data1 = User.query.filter(User.city == city_name).join(ProducerProduct,
                                                                                 User.userid == ProducerProduct.producerid) \
                .add_columns(User.image_file, User.fname, User.phone, User.userid, User.address1, User.address2, User.city,
                             User.zipcode, User.email) \
                .join(ProductCategory, ProductCategory.productid == ProducerProduct.productid) \
                .add_columns(ProductCategory.categoryid).join(Category, Category.categoryid == ProductCategory.categoryid) \
                .add_columns(Category.category_name, Category.categoryid).filter(Category.category_name==category_name).all()
        else:
            data1 = User.query.filter(User.city == city_name).join(ProducerProduct,
                                                                   User.userid == ProducerProduct.producerid) \
                .add_columns(User.image_file, User.fname, User.phone, User.userid, User.address1, User.address2,
                             User.city,
                             User.zipcode, User.email) \
                .join(ProductCategory, ProductCategory.productid == ProducerProduct.productid) \
                .add_columns(ProductCategory.categoryid).join(Category,
                                                              Category.categoryid == ProductCategory.categoryid) \
                .add_columns(Category.category_name, Category.categoryid).all()

        if RentalCategory.query.filter_by(category_name=category_name).first():
            print('inside rental data2')
            data2 = User.query.filter(User.city == city_name).join(RentalProducerProduct,
                                                                   User.userid == RentalProducerProduct.producerid) \
                .add_columns(User.image_file, User.fname, User.phone, User.userid, User.address1, User.address2,
                             User.city, User.zipcode, User.email) \
                .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
                .add_columns(RentalProductCategory.categoryid).join(RentalCategory,
                                                                    RentalCategory.categoryid == RentalProductCategory.categoryid) \
                .add_columns(RentalCategory.category_name, RentalCategory.categoryid).filter(RentalCategory.category_name==category_name).all()
        else:


            data2 = User.query.filter(User.city == city_name).join(RentalProducerProduct,
                                                                              User.userid == RentalProducerProduct.producerid) \
                .add_columns(User.image_file, User.fname, User.phone, User.userid, User.address1, User.address2,
                             User.city, User.zipcode, User.email) \
                .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
                .add_columns(RentalProductCategory.categoryid).join(RentalCategory,
                                                                    RentalCategory.categoryid == RentalProductCategory.categoryid) \
                .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()
        print(data1,data2,type(data1),type(data2))

        if len(data1)!=0 or len(data2)!=0 :
            data = modifyProducerdata(data1, data2)
        else:
            data=[]
            print('no results found')
    return data


def modifyProducerdata(data1,data2):
    farmercategories = {}
    for item in data1:
        farmercategories.setdefault(item.fname, list(set([]))).append(item.category_name)

    for k, v in farmercategories.items():
        farmercategories[k] = list(set(v))


    farmerrentcategories = {}
    for item in data2:
        farmerrentcategories.setdefault(item.fname, list(set([]))).append(item.category_name)

    for k, v in farmercategories.items():
        farmercategories[k] = list(set(v))
    for k, v in farmerrentcategories.items():
        farmerrentcategories[k] = list(set(v))

    data=[]
    for key in farmercategories.keys():
            my_list=[]
            for item in data1:
                 if item.fname==key :
                    #print(key,farmerrentcategories[key])
                    my_list.append(item.fname)
                    my_list.append(item.userid)
                    my_list.append(farmercategories[key])
                    my_list.append(item.image_file)
                    my_list.append((item.address1) + item.address2)
                    my_list.append(item.city)
                    my_list.append(item.zipcode)
                    my_list.append(item.phone)
                    if key in farmerrentcategories.keys():
                     my_list.append(farmerrentcategories[key])
                    break
            data.append(my_list)
    return data

def getLocationDetails():

    data = ProducerProduct.query.with_entities(ProducerProduct.producerid,ProducerProduct.productid,ProducerProduct.productcity).group_by(ProducerProduct.productcity).all()
    print('Location itemdata',data)
    '''
    itemdata=[]
    for i in range(len(data)):
        for j in range(len(data[0])):
            itemdata.append(data[i][j])
    '''
    return data

def massageItemData(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


def is_valid(email, password):
    # Using Flask-SQLAlchmy ORM
    # data = User.query.with_entities(User.email, User.password).all()

    # Using Raw SQL Select Query
    cur = mysql.connection.cursor()
    cur.execute("SELECT email, password FROM user")
    userData = cur.fetchall()
    cur.close()

    for row in userData:
        if row['email'] == email :
                #and row['password'] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


def getLoginUserDetails():
    productCountinCartForGivenUser = 0
    productCountinCart = []
    loggedIn = False
    userid=999
    firstName=""
    email=None

    if 'email' not in session:
        #print('no session hell00',session)

        try:
            userid, firstName = User.query.with_entities(User.userid, User.fname).filter(User.email == "guestuser@gmail.com").first()
        except:
            str1 = random.randint(2,9999)
            password="guest"
            guestemail="guestuser@gmail.com"
            user = User(fname="Guestuser" + str(str1), lname="guest" + str(str1),
                        password=hashlib.md5(password.encode()).hexdigest(),
                        address1="", address2="", city="", state="", country="", zipcode="",
                        email=guestemail, phone="",image_file='default.jpg')
            db.session.add(user)
            db.session.flush()
            db.session.commit()



    else:

        loggedIn = True
        userid, firstName,email = User.query.with_entities(User.userid, User.fname,User.email).filter(User.email == session['email']).first()
        # for Cart in Cart.query.filter(Cart.userId == userId).distinct(Products.productId):

    for cart in Cart.query.filter(Cart.userid == userid).all():
        productCountinCart.append(cart.productid)

    for cart in RentalCart.query.filter(RentalCart.userid == userid).all():
        productCountinCart.append(cart.productid)

    productCountinCartForGivenUser = len(productCountinCart)
    return (loggedIn, firstName, productCountinCartForGivenUser,userid)


def getProductDetails(productId):
    productDetailsById = Product.query.filter(Product.productid == productId).first()
    return productDetailsById

def getrentalProductDetails(productId):
    productDetailsById = RentalProduct.query.filter(RentalProduct.productid == productId).first()
    print('productDetailsById',productDetailsById)
    return productDetailsById


def extractUserselection(request):
    category = request.form['category']
    product = request.form['product']
    location = request.form['location']
    res=[]
    res.append(category)
    print(res)
    return res

def convertdates(date1,date2):
    print('date1:{0},date2:{1}'.format(date1,date2))


    l1 = (date1.split(" "))
    l1=l1[0].split('-')
    l1 = [int(item) for item in l1]
    l2 = (date2.split(" "))
    l2 = l2[0].split('-')
    l2 = [int(item) for item in l2]



    d0 = date(*(l1))
    d1 = date(*(l2))
    delta = d1 - d0
    return delta.days


def extractAndPersistUserDataFromForm(request,isadmin):
    password = request.form['password']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    address1 = request.form['address1']
    address2 = request.form['address2']
    zipcode = request.form['zipcode']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    phone = request.form['phone']

    #print('type',request.files['pimage'])

    #image_file = request.form['pimage']
    image_file=routes.save_picture(request.files['profile_photo'])
    farm_image=routes.save_picture(request.files['farm_photo'])

    user = User(fname=firstName, lname=lastName, password=hashlib.md5(password.encode()).hexdigest(), address1=address1,
                address2=address2,city=city, state=state, country=country, zipcode=zipcode, email=email, phone=phone,isadmin=isadmin,image_file=image_file,farm_image=farm_image)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return "Registered Successfully"


def isUserLoggedIn():
    if 'email' not in session:
        return False
    else:
        return True


# check if user is an admin.html
def isUserAdmin():
    if isUserLoggedIn():

        userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
        #print('userid',userId)
        currentUser = User.query.get_or_404(userId)
        print('current status:',currentUser.isadmin)
        return currentUser.isadmin



# Using Flask-SQL Alchemy SubQuery
def extractAndPersistKartDetailsUsingSubquery(productId,quantity=1,rent=False,num_days=1):
    loggedIn, firstName, productCountinKartForGivenUser, userId = getLoginUserDetails()
    print('userid',userId,firstName)

    subqury = Cart.query.filter(Cart.userid == userId).filter(Cart.productid == productId).subquery()
    qry = db.session.query(Cart.quantity).select_entity_from(subqury).all()
    products=Product.query.all()

    for item in products:
        #print('Product id', item.product_name, item.quantity, quantity)
        if int(item.productid) == int(productId):
            if int(item.quantity) < int(quantity):
                quantity = int(item.quantity)
                break
            else:
                quantity = int(quantity)
                break

    if len(qry) == 0:
        print('quantity',quantity)
        cart = Cart(userid=userId, productid=productId, quantity=quantity)
        #db.session.add(cart)
    else:
        print('else quantity', quantity,qry[0][0])
        cart = Cart(userid=userId, productid=productId, quantity=int(qry[0][0]) + int(quantity))
        #db.session.add(cart)
    if rent:
        subqury = RentalCart.query.filter(RentalCart.userid == userId).filter(RentalCart.productid == productId).subquery()
        qry = db.session.query(RentalCart.quantity).select_entity_from(subqury).all()
        if len(qry) == 0:
            cart = RentalCart(userid=userId, productid=productId, quantity=quantity,days=num_days)
            #db.session.add(cart)
        else:
            cart = RentalCart(userid=userId, productid=productId, quantity=int(qry[0][0]) + int(quantity),days=num_days)
            db.session.add(cart)
    #print(cart)
    db.session.merge(cart)
    print(cart)
    db.session.flush()
    db.session.commit()



# Using Flask-SQL Alchemy query
def extractAndPersistKartDetailsUsingkwargs(productId):
    userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
    userId = userId[0]

    kwargs = {'userid': userId, 'productid': productId}
    quantity = Cart.query.with_entities(Cart.quantity).filter_by(**kwargs).first()

    if quantity is not None:
        cart = Cart(userid=userId, productid=productId, quantity=quantity[0] + 1)
    else:
        cart = Cart(userid=userId, productid=productId, quantity=1)

    db.session.merge(cart)
    db.session.flush()
    db.session.commit()


class addCategoryForm(FlaskForm):
    category_image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png'])])
    category_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class addProductForm(FlaskForm):
    category = SelectField('Category:', coerce=int, id='select_category')
    sku = IntegerField('Product SKU:', validators=[DataRequired()])
    productName = StringField('Product Name:', validators=[DataRequired()])
    productDescription = TextAreaField('Product Description:', validators=[DataRequired()])
    priceingScale= SelectField('priceingScale:', coerce=int, id='select_scale')
    productPrice = FloatField('Product Price:', validators=[DataRequired()])
    productQuantity = IntegerField('Product Quantity:', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

class addUserForm(FlaskForm):
    #image_file = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Update email:', validators=[DataRequired()])
    firstName = StringField('Update Firstname:', validators=[DataRequired()])
    #confirmpassword = StringField('Confirm Password:', validators=[DataRequired()])
    #phone = StringField('Phone:', validators=[DataRequired()])
    #farmdescription = StringField('farmdescription:', validators=[DataRequired()])
    submit = SubmitField('Save')



    # START CART MODULE
# Gets products in the cart
def getusercartdetails(rent=False):
    loggedIn, firstName, productCountinKartForGivenUser, userId = getLoginUserDetails()

    products2 = RentalProduct.query.join(RentalCart, RentalProduct.productid == RentalCart.productid) \
            .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.regular_price,  RentalCart.days,RentalProduct.image) \
            .add_columns(RentalProduct.regular_price * RentalCart.days).filter(RentalCart.userid == userId)

    products1=Product.query.join(Cart, Product.productid == Cart.productid) \
                .add_columns(Product.productid, Product.product_name, Product.regular_price, Cart.quantity, Product.image) \
                .add_columns(Product.regular_price * Cart.quantity).filter(Cart.userid == userId)

    #print(type(products1),products1)


    totalsum1 = 0
    totalsum2 = 0

    for row in products1:
        totalsum1 += float(row[6])

    for row in products2:
        totalsum2 += float(row[6])

    tax1 = ("%.2f" % (.06 * float(totalsum1)))
    tax2 = ("%.2f" % (.06 * float(totalsum1)))

    totalsum1 = float("%.2f" % (1.06 * float(totalsum1)))
    #print(totalsum,tax,productsincart)
    return (products1, totalsum1,tax1,products2, totalsum2,tax2)


# Removes products from cart when user clicks remove
def removeProductFromCart(productId):
    loggedIn, firstName, productCountinKartForGivenUser, userId = getLoginUserDetails()
    kwargs = {'userid': userId, 'productid': productId}
    cart = Cart.query.filter_by(**kwargs).first()
    if productId is not None:
        db.session.delete(cart)
        db.session.commit()
        flash("Product has been removed from cart !!")
    else:
        flash("failed to remove Product cart please try again !!")
    return redirect(url_for('cart'))


# flask form for checkout details
class checkoutForm(FlaskForm):
    fullname = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    address = TextAreaField('address',
                            validators=[DataRequired()])
    city = StringField('city',
                       validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('state',
                        validators=[DataRequired(), Length(min=2, max=20)])
    zip = StringField('zip',
                      validators=[DataRequired(), Length(min=2, max=6)])
    cctype = RadioField('cardtype')
    cardname = StringField('cardnumber',
                           validators=[DataRequired(), Length(min=12, max=12)])
    ccnumber = StringField('Credit card number',
                           validators=[DataRequired()])

    expmonth = StringField('Exp Month',
                           validators=[DataRequired(), Length(min=12, max=12)])
    expyear = StringField('Expiry Year',
                          validators=[DataRequired(), Length(min=4, max=4)])
    cvv = StringField('CVV',
                      validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('MAKE PAYMENT')


# Gets form data for the sales transaction

def extractOrderdetails(request, totalsum):
    try:
        customer = User.query.filter_by(email=session['email']).first()
        if customer:
            fullname = customer.fname+" "+customer.lname
            email = customer.email
            address = customer.address1 + customer.address2 + "\nDistrict: " + customer.state + "\nCity: " + customer.city + \
                      "\nState:" + customer.country + "\nZipCode:" + customer.zipcode
            #address = customer.address1+" "+customer.address1
            phone = customer.phone
            city = customer.city
            state = customer.state
            zipcode = customer.zipcode

    except:
        fullname = request.form['first_name']
        email = request.form['email']
        address = request.form['address_line_1']
        phone = request.form['phone']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['postalcode']
    '''
    cctype = request.form['cardtype']
    ccnumber = request.form['cardnumber']
    cardname = request.form['cardname']
    expmonth = request.form['expmonth']
    expyear = request.form['expyear']
    provider = request.form['provider']
    cvv = request.form['cvv']
    '''
    orderdate = datetime.utcnow()

    loggedIn, firstName, noOfItems, userId = getLoginUserDetails()
    #orderid=random.randint(50,999999)
    order = Order(order_date=orderdate, total_price=totalsum, userid=userId)
    db.session.add(order)
    db.session.flush()
    db.session.commit()

    orderid = Order.query.with_entities(Order.orderid).filter(Order.userid == userId).order_by(
        Order.orderid.desc()).first()

    # add details to ordered;
    #  products table
    addOrderedproducts(userId, orderid)
    # add transaction details to the table
    #updateSalestransaction(totalsum, ccnumber, orderid, cctype)

    # remove ordered products from cart after transaction is successful
    removeordprodfromcart(userId)
    removeordprodfromstock(orderid)
    try:

        guestid=User.query.with_entities(User.userid).filter(User.email=="guestuser@gmail.com").first()
        print('guestId',guestid)
        if guestid==userId:
            removeguestuserfromUser(userId=guestid)
    except:
        pass

    #print('email',email)
    return (email, fullname, orderid, address, fullname, phone)

    #return (email, fullname, orderid, address, fullname, phone, provider)


# adds data to orderdproduct table

def addOrderedproducts(userId, orderid):
    cart = Cart.query.with_entities(Cart.productid, Cart.quantity).filter(Cart.userid == userId)
    rentcart = RentalCart.query.with_entities(RentalCart.productid, RentalCart.quantity).filter(RentalCart.userid == userId)

    for item in cart:
        orderedproduct = OrderedProduct(orderid=orderid, productid=item.productid, quantity=item.quantity)
        db.session.add(orderedproduct)

        db.session.flush()
        db.session.commit()
    '''

    for item in rentcart:
        #orderedproduct = OrderedProduct(orderid=orderid, productid=item.productid, quantity=item.quantity)
        orderedrentproduct = RentalOrderedProduct(orderid=orderid, productid=item.productid, quantity=item.quantity)
        #db.session.add(orderedproduct)
        db.session.add(orderedrentproduct)
        db.session.flush()
        db.session.commit()
    '''


# removes all sold products from cart for the user

def removeordprodfromcart(userId):
    userid = userId
    db.session.query(Cart).filter(Cart.userid == userid).delete()
    db.session.query(RentalCart).filter(RentalCart.userid == userid).delete()
    db.session.commit()

def updateProductStockStatus():
    products=Product.query.all()
    #mydata = db.session.query(Product).filter(Product.quantity == 0).all()
    #print('mydata',mydata)
    for item in products:
        print(item.productid,item.product_name,item.quantity)
        if item.quantity<0:
            item.product_review="Out of stock"
            db.session.commit()

        else:
            item.product_review="available"

        print(item.product_review)



def removeordprodfromstock(orderid):
    orderid = orderid
    data=db.session.query(OrderedProduct).filter(OrderedProduct.orderid == orderid)
    for item in data:
        print(item.productid,item.quantity)
        #prod_quantity=db.session.query(OrderedProduct).filter(OrderedProduct.productid == item.productid)
        mydata=db.session.query(Product).filter(Product.productid == item.productid).first()
        print(mydata)
        mydata.quantity= mydata.quantity-item.quantity
        db.session.commit()

        #cur = mysql.connection.cursor()
        #cur.execute("SELECT email, password FROM user")
        #cur.update(Product).values(Product.stock == Product.stock-item.quantity ).where(Product.productid == item.productid)
        #cur.close()

def removeguestuserfromUser(userId):
    userid = userId
    db.session.query(User).filter(User.userid == userid).delete()
    db.session.commit()


# adds sales transaction

def updateSalestransaction(totalsum, ccnumber, orderid, cctype):
    salesTransaction = SaleTransaction(orderid=orderid, transaction_date=datetime.utcnow(), amount=totalsum,
                                       cc_number=ccnumber, cc_type=cctype, response="success")
    db.session.add(salesTransaction)
    db.session.flush()
    db.session.commit()


# sends email for order confirmation

def sendEmailconfirmation(email,ordernumber,phonenumber):
    print('Trying to send Email',email)
    import smtplib, ssl
    #ordernumber=3

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "manjujnv87@gmail.com"
    receiver_email = email
    password = "Brave@2020"
    # Create the plain-text and HTML version of your message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Order is confirmed, Order Number:{}".format(ordernumber)
    message["From"] = sender_email
    message["To"] = receiver_email
    text = "Your number is:"+str(phonenumber)

    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a>
           has many great tutorials.
        </p>
        <a>How are you?</a>
    <a href="http://mthimmareddy.pythonanywhere.com">See Us</a>

      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def sendForgotEmail(email):
    import smtplib, ssl

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "servinglocalindia@gmail.com"
    receiver_email = email
    password = "Brave@2020"
    # Create the plain-text and HTML version of your message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password reset for {0} on www.servinglocalindia.com".format(email)
    message["From"] = sender_email
    message["To"] = receiver_email
    text = "You're receiving this e-mail because you requested a password reset for your user account at servinglocalindia." \
           "Please go to the following page and choose a new password:http://127.0.0.1:5000/reset_password/confirm/{0}".format(str(email))
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

















    '''
    msg = MIMEMultipart()
    sitemail = "servinglocalindia@gmail.com"
    msg['Subject'] = "Your Order has been placed for " + username
    msg['From'] = sitemail
    msg['To'] = email
    text = "Hello!\nThank you for shopping with us.Your order No is:" +str(ordernumber)
    html = """\
        <html>
          <head></head>
          <body>
            <p><br>
               Please stay tuned for more fabulous offers and gadgets.You can visit your account for more details on this order.<br>
               <br>Please write to us at <u>"servinglocalindia@farmer.com"</u> for any assistance.</br>
               <br></br>
               <br></br>
               Thank you!
               <br></br>
               Servinglocalindia Team
            </p>
          </body>
        </html>
        """
    msg1 = MIMEText(text, 'plain')
    msg2 = MIMEText(html, 'html')
    msg.attach(msg1)
    msg.attach(msg2)
    try:
        server = smtplib.SMTP(host='smtp.gmail.com', port=465)
        server.connect('smtp.mail.com', 465)
        # Extended Simple Mail Transfer Protocol (ESMTP) command sent by an email server to identify itself when connecting to another email.

        server.ehlo()
        # upgrade insecure connection to secure
        server.starttls()
        server.ehlo()
        server.login(sitemail, "Brave@2020")
        server.ehlo()
        server.sendmail(sitemail, email, msg.as_string())
        # hack to send text confirmation using emailsms gateway

        if (provider == "Tmobile"):
            phonenumber = phonenumber + "@tmomail.net"
        if (provider == "ATT"):
            phonenumber = phonenumber + "@txt.att.net"
        server.sendmail(sitemail, phonenumber, msg.as_string())

        server.quit()
    except:
        print('email not sent')
    '''

# except:
#     "no tls please try again later"
#     return False

# def sendTextnotification(phone,fullname,orderid):


# problem 1--TextMagic lots of unknown packages
# username = "akankshanegi"
# token = "di18DWYaXQRT3KqDLn8wfYpr5utQl3"
# client = TextmagicRestClient(username, token)
#
# message = client.messages.create(phones="8478486054", text="Hello TextMagic")

# problem 2--TWILIO not free need to buy a paid number
# # the following line needs your Twilio Account SID and Auth Token
# client = Client("AC488c3b9e98a6bbbf84d5002631f2fd63", "f1b4ca2a3913f5f39ba6a7cf44afb77f")
#
# # change the "from_" number to your Twilio number and the "to" number
# # to the phone number you signed up for Twilio with, or upgrade your
# # account to send SMS to any phone number
# client.messages.create(to="+18478486054",
#                        from_="+15005550006",
#                        body="Hello from Python!")


# END CART MODULE


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')



###############################################
def sendAlertNotification(email):
    import smtplib, ssl

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "manjujnv87@gmail.com"
    receiver_email = email
    password = "Brave@2020"
    # Create the plain-text and HTML version of your message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Product alert notification to Email:{0}".format(email)
    message["From"] = sender_email
    message["To"] = receiver_email
    text = "You're receiving this e-mail because you requested a for the product which is not in stock currently"
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    status=False

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            status=True
    except:
        status=False
    return status