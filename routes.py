'''
Added comment
'''
import os
import secrets



from flask import render_template, request,abort
from __init__ import *
#from __init__ import db,mysql
from PIL import Image
#from plotly.offline import plot
#import plotly.graph_objs as go
from flask import Markup,flash
from models import *
from forms import *
from flask import session
import random

from flask import url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, RadioField, FloatField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email

loggedIn=False
firstName="guest"
userid=9999
productCountinKartForGivenUser=0
isadmin=999
admin=True
reset_password=False
confirm=False

current_date = datetime.now()
current_date = str(current_date).split(" ")
current_date = current_date[0]
##logging.warning('current_date', current_date)
###################################################33
   #*************#logging**************
###################################################



#session['email']="manjujnv87@gmail.com"

#session_data={}
def login_details():
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    isadmin=isUserAdmin()
    return isadmin,loggedIn, firstName, productCountinKartForGivenUser, userid

############Error Handling#############################
@app.errorhandler(404)
def not_found(error):
    #logging.warning('inside 404:{0}'.format(error))
    return render_template('errors/404.html',error=error)

@app.errorhandler(500)
def not_found(error):
    #logging.warning('inside 500')
    error="Server Error,Kindly check with Customer care or try to relogin again"
    return render_template('errors/404.html',error=error)

@app.errorhandler(401)
def not_found(error):
    #logging.warning('inside 401')
    error="You are not authorized to access this page"
    return render_template('errors/404.html',error=error)


@app.errorhandler(405)
def not_found(error):
    #logging.warning('inside 405')
    return render_template('errors/404.html')


@app.route('/search',methods=['GET','POST'])
def listfarmers():
    loc=request.args.get('terms')
    ##logging.warning('location',loc)

    itemData = User.query.filter(User.city==loc).join(ProducerProduct, User.userid ==ProducerProduct.producerid) \
        .add_columns(User.fname, User.userid, User.city,User.image_file)\
        .join(ProductCategory,ProductCategory.productid == ProducerProduct.productid) \
        .add_columns(ProductCategory.categoryid).join(Category,Category.categoryid==ProductCategory.categoryid)\
        .add_columns(Category.category_name, Category.categoryid).all()


    return render_template("sellProducts.html", ProducerData=itemData)

@app.route('/account')
def show_account():

    ##logging.warning('inside account',session)
    #session['email']=email

    customer = User.query.filter(User.email == session['email']).one()
    userid,isadmin=User.query.with_entities(User.userid,User.isadmin).filter(User.email == session['email']).first()
    orders=Order.query.with_entities(Order.order_date,Order.total_price,Order.orderid).filter(Order.userid==userid).all()

    ProductsbyUser = ProducerProduct.query.with_entities(ProducerProduct.productid).filter(
        ProducerProduct.producerid == userid) \
        .join(Product).add_columns(Product.productid, Product.product_name, Product.regular_price,
                                    Product.image) \
        .filter(ProducerProduct.productid == Product.productid).all()
    if isadmin:
        return render_template("farmeraccount.html", customer=customer,orders=orders,products=ProductsbyUser)
    else:
        return render_template("account.html", customer=customer,orders=orders,products=ProductsbyUser)
    return render_template("account.html", customer=customer,orders=orders,products=ProductsbyUser)





@app.route("/marketwatch")
def marketwatch():
    msg="KNOW MARKET RATES OF YOUR CROP"
    return render_template('test.html',msg=msg)
    #return render_template('marketwatch.html',msg=msg)


@app.route("/blog")
def blog():


    #page = request.args.get('page', 1, type=int)
    posts = Post.query.all()
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('FDblog.html',posts=posts,blog=True)

@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=userid)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('root'))
    return render_template('create_posts.html', title='New Post',
                           form=form, legend='New Post',firstName=firstName)


@app.route("/post/<int:post_id>")
def post(post_id):
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    post = Post.query.get_or_404(post_id)
    #logging.warning(post)
    return render_template('post.html', title=post.title, post=post,userid=userid,firstName=firstName)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])

def update_post(post_id):
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    post = Post.query.get_or_404(post_id)

    if post.author != userid:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_posts.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    post = Post.query.get_or_404(post_id)
    if post.author != userid:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog'))



@app.route("/sellProducts",methods=['POST','GET'])
def sellProducts():
       city_name=None
       loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
       ##logging.warning(loggedIn,firstName,productCountinKartForGivenUser)
       productsDataall = Product.query.all()
       locationDataall = User.query.with_entities(User.city).filter(User.isadmin == 1).all()
       locationDataall = list(set(locationDataall))
       allProductDetails = getAllProducts()
       allProductsMassagedDetails = massageItemData(allProductDetails)
       categoryData= getCategoryDetails()

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

       data = modifyProducerdata(data1,data2)
       for item in data:
           print('final',item)

       #Producercategory,data= getProducerDetails()
       #Producerrentcategory, data2 = getProducerDetails(rent=True)
       #print(Producerrentcategory,data2)

       categoryDataall = Category.query.all()
       msg = "SHOWING THE FARMERS LISTING ALL CATEGORIES"

       city_name = request.args.get('city_name')
       #print('city type',type(city_name))
       msg_city="SHOWING THE ALL PRODUCTS FROM ALL LOCATIONS"

       if city_name:
           ProducerproductData = User.query.filter(User.city == city_name).join(ProducerProduct,
                                                                   User.userid == ProducerProduct.producerid) \
               .add_columns(User.image_file,User.fname,User.phone,User.userid,User.address1,User.address2,User.city,User.zipcode,User.email) \
               .join(ProductCategory, ProductCategory.productid == ProducerProduct.productid) \
               .add_columns(ProductCategory.categoryid).join(Category,Category.categoryid == ProductCategory.categoryid) \
               .add_columns(Category.category_name, Category.categoryid).all()

           ProducerrentData = User.query.filter(User.city == city_name).join(RentalProducerProduct,
                                                                         User.userid == RentalProducerProduct.producerid) \
               .add_columns(User.image_file, User.fname, User.phone, User.userid, User.address1, User.address2,
                            User.city, User.zipcode, User.email) \
               .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
               .add_columns(RentalProductCategory.categoryid).join(RentalCategory,
                                                                   RentalCategory.categoryid == RentalProductCategory.categoryid) \
               .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()


           #print('ProducerData',ProducerData)
           data = modifyProducerdata(ProducerproductData,ProducerrentData)
           print('len of data',len(data))
           msg_city = "SHOWING THE ALL PRODUCTS FROM {0}".format(city_name)

           productsDataall = User.query.filter(User.city == city_name).join(ProducerProduct,
                                                                            User.userid == ProducerProduct.producerid) \
               .add_columns(User.image_file, User.fname, User.phone, User.userid, User.city, User.email,
                            ProducerProduct.productid) \
               .join(Product, Product.productid == ProducerProduct.productid) \
               .add_columns(Product.productid, Product.product_name, Product.regular_price,
                            Product.image, Product.quantity).all()





       if request.method == 'POST':
           category_name = request.form.get("category")
           ProducerData, productsdata, num = getProducerCategory(category_name)
           data = modifyProducerdata(ProducerData,data2)
           msg = "SHOWING THE FARMERS LISTING CATEGORY:{}".format(category_name).upper()



       return render_template('sellProducts.html', productpage=True,itemData=allProductsMassagedDetails, loggedIn=loggedIn, firstName=firstName,
                              productCountinKartForGivenUser=productCountinKartForGivenUser,ProducerData=data,
                              categoryData=categoryData, categoryDataall=categoryDataall,
                              locationDataall=locationDataall, productsDataall=productsDataall,msg=msg,msg_city=msg_city)


@app.route("/productAlertNotification" , methods=['GET','POST'])
def productAlertNotification():
    if request.method == 'POST':
        email = request.form['email']
        print('email',email)
        status=sendAlertNotification(email=email)
        #print('Status',status)
        if status:
            flash('Alert message sent success')
    return render_template('productAlertNotification.html')






@app.route("/neighbourFarmers",methods=['POST','GET'])
def neighbourFarmers():
    return render_template("neighbourFarmers.html",ProducerData = getProducerDetails())






@app.route("/ForgotForm")
def ForgotForm():
    return render_template('password_reset.html',reset_password=reset_password,confirm=confirm)

@app.route("/reset_password/done" , methods=['GET','POST'])
def resetForm():
    if request.method == 'POST':
        email = request.form['email']
        sendForgotEmail(email=email)
    return render_template('password_reset.html',reset_password=True)

@app.route("/reset_password/confirm/<string:email>" , methods=['GET','POST'])
def ConfirmForm(email):
    if request.method == 'POST':
        password1 = request.form['new_password1']
        password2 = request.form['new_password2']
        if password1 == password2:
            ##logging.warning('password match')
            userid=User.query.with_entities(User.userid).filter(User.email==email).first()
            user = User.query.get_or_404(userid)
            user.password=hashlib.md5(password1.encode()).hexdigest()
            db.session.commit()

    return render_template('password_reset.html',confirm=True,reset_password=False)

@app.route("/signInF")
def loginFormF():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        error = 'Invalid UserId / Password'
        return render_template('login.html',isadmin=1)


@app.route("/signIn")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        error = 'Invalid UserId / Password'
        return render_template('login.html',isadmin=2)

@app.route("/signInC")
def loginFormC():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        error = 'Invalid UserId / Password'
        return render_template('login.html',isadmin=0)


@app.route("/login", methods=['POST', 'GET'])
def login():
    global loggedIn;
    global firstName;
    global userid;
    global productCountinKartForGivenUser;
    global isadmin
    #global email
    #global session

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if is_valid(email, password):
                session['email'] = email
                loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
                session['email'] = email
                session.modified = True
                #logging.warning('INSIDE LOGIN:{0}'.format(session,session['email']))

                #session_data['firstName']=firstName

                if isUserAdmin() == 2:
                    return redirect(url_for('admin'))
                elif isUserAdmin() == 1:
                    ##logging.warning('inside login')
                    return redirect(url_for('farmer', firstName=firstName, userid=userid))
                else:
                    ##logging.warning('inside login session',session)
                    return redirect(url_for('root'))


        else:
            error = 'Invalid UserId / Password'
            ##logging.warning(error)
            return render_template('login.html', error=error)




@app.route("/logout")
def logout():
    session.pop('email', None)
    #flash("You are Logged out")
    return redirect(url_for('root'))


@app.route("/registerationForm")
def registrationForm():
    isadmin=request.args.get("isadmin")
    ##logging.warning('isadmin i',isadmin)
    return render_template("register.html",isadmin=isadmin)


@app.route("/register", methods=['GET', 'POST'])
def register():
    isadmin = request.args.get("isadmin")
    if request.method == 'POST':
        # Parse form data
        msg = extractAndPersistUserDataFromForm(request,isadmin)
        return render_template("login.html", error=msg)


@app.route('/',methods=['GET', 'POST'])
@app.route("/home")
def root():


    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    #logger.info(loggedIn,firstName)
    #updateProductStockStatus()

    return render_template('index.html',firstName=firstName,productCountinKartForGivenUser=productCountinKartForGivenUser)


@app.route('/displayCategory')
@app.route('/displayCategory/<category_name>',methods=['GET', 'POST'])
def displayCategory(category_name=None):
    categoryId = request.args.get("categoryid")
    producerId = request.args.get("producerId")
    if not categoryId:
        categoryId = Category.query.with_entities(Category.categoryid).filter(
             Category.category_name == category_name).first()
        categoryId=categoryId[0]
        ##logging.warning('categoryId',categoryId)
    loggedIn, firstName, noOfItems, userid = getLoginUserDetails()
    if producerId:
        productDetailsByCategoryId = Product.query.join(ProducerProduct)\
            .filter(ProducerProduct.producerid == producerId) \
            .join(ProductCategory, Product.productid == ProductCategory.productid) \
            .add_columns(Product.productid, Product.product_name, Product.regular_price,
                         Product.image, Product.quantity) \
            .join(Category, Category.categoryid == ProductCategory.categoryid) \
            .filter(Category.categoryid == int(categoryId)) \
            .add_columns(Category.category_name) \
            .all()
    else:
        productDetailsByCategoryId = Product.query.join(ProductCategory, Product.productid == ProductCategory.productid) \
             .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.price_scale,
                          Product.image,Product.quantity) \
             .join(Category, Category.categoryid == ProductCategory.categoryid) \
             .filter(Category.categoryid == int(categoryId)) \
             .add_columns(Category.category_name) \
             .all()
    if len(productDetailsByCategoryId)!= 0:
         categoryName = productDetailsByCategoryId[0].category_name
         data = productDetailsByCategoryId
         for item in productDetailsByCategoryId:
             print('Inside category',item)
         return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName,
                                noOfItems=noOfItems)
    else:
         return('<h1>No results found for this category</h1>')


'''
@app.route("/displayProductsByLocation")
def displayProductsByLocation():
     loggedIn, firstName, noOfItems,userid = getLoginUserDetails()
     producerid = request.args.get("producerid")
     productDetailsByLocation = Product.query.join(ProducerProduct, Product.productid == ProducerProduct.productid) \
         .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.price_scale,
                      Product.image) \
         .join(User, User.city == ProducerProduct.productcity).all()

     ##logging.warning('productDetailsByuserId',type(productDetailsByLocation))
'''

@app.route("/displayProducerPage")
def displayProducerPage():
 loggedIn, firstName, noOfItems,userid = getLoginUserDetails()
 ##logging.warning(userid)
 #farmdescription = User.query.with_entities(User.farmdescription).filter(User.userid==producerid)
 try:
     fname = request.args.get("fname")
     producerid = request.args.get("producerid")
     if producerid:
         profile_img,Producername,farmdescription = User.query.with_entities(User.image_file,User.fname,User.farmdescription)\
             .filter(User.userid == producerid).first()
     if fname:
         producerid,profile_img, Producername, farmdescription=User.query.with_entities(User.userid,User.image_file,User.fname, User.farmdescription) \
             .filter(User.fname == fname).first()
 except:
     pass

 ##logging.warning('farmdescription',Producername,farmdescription)
 rentalproducts= RentalProduct.query.all()

 RentalCategoryData = RentalCategory.query.join(RentalProductCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
     .add_columns(RentalCategory.category_name, RentalCategory.categoryid, RentalCategory.category_image) \
     .join(RentalProducerProduct, RentalProductCategory.productid == RentalProducerProduct.productid).filter(
     RentalProducerProduct.producerid == producerid) \
     .add_columns(RentalProducerProduct.producerid).order_by(RentalCategory.categoryid.desc()) \
     .distinct(RentalCategory.categoryid) \
     .all()


 CategoryData = Category.query.join(ProductCategory, Category.categoryid == ProductCategory.categoryid) \
     .add_columns(Category.category_name,Category.categoryid,Category.category_image)\
     .join(ProducerProduct, ProductCategory.productid == ProducerProduct.productid).filter(ProducerProduct.producerid == producerid) \
     .add_columns(ProducerProduct.producerid).order_by(Category.categoryid.desc()) \
     .distinct(Category.categoryid) \
     .all()

 return render_template('displayProducerPage.html', RentalCategoryData=RentalCategoryData,rentalproducts=rentalproducts,CategoryData=CategoryData, loggedIn=loggedIn, firstName=firstName,
                        producerid=producerid,noOfItems=noOfItems,farmdescription=farmdescription,Producername=Producername.upper(),profile=profile_img)



@app.route("/displayProductsByProducer")
def displayProductsByProducer():
 loggedIn, firstName, noOfItems,userid = getLoginUserDetails()
 producerid = request.args.get("producerid")
 categoryid = request.args.get("categoryid")
 rent=False
 print('inside displayProductsByProducer',producerid,categoryid)


 rentalcategoryid = request.args.get("rentcategoryid")

 if rentalcategoryid:
     rent=True
     productDetailsByuserId = RentalProducerProduct.query.with_entities(RentalProducerProduct.productid).filter(
         RentalProducerProduct.producerid == producerid) \
         .join(RentalProduct).add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.regular_price,
                                          RentalProduct.image,RentalProduct.price_scale,RentalProduct.quantity) \
         .filter(RentalProducerProduct.productid == RentalProduct.productid).join(RentalProductCategory).add_columns(
         RentalProductCategory.categoryid) \
         .filter(RentalProductCategory.categoryid == rentalcategoryid).all()
 if categoryid:
     print('inside categoryid',categoryid)

     productDetailsByuserId = ProducerProduct.query.with_entities(ProducerProduct.productid).filter(ProducerProduct.producerid == producerid)\
         .join(Product).add_columns(Product.productid, Product.product_name, Product.regular_price,
                                    Product.price_scale,Product.image,Product.quantity)\
         .filter(ProducerProduct.productid==Product.productid).join(ProductCategory).add_columns(ProductCategory.categoryid)\
         .filter(ProductCategory.categoryid == categoryid).all()
     print(productDetailsByuserId,len(productDetailsByuserId))



 data = productDetailsByuserId
 print(loggedIn,firstName,noOfItems,rent)

 return render_template('displayProducerproducts.html', data=data, loggedIn=loggedIn, firstName=firstName,
                        noOfItems=noOfItems,rent=rent)




@app.route("/productDescription")
def productDescription():
 loggedIn, firstName, noOfItems,userid= getLoginUserDetails()
 productid = request.args.get('productId')
 productDetailsByProductId = getProductDetails(productid)
 return render_template("productDescription.html", data=productDetailsByProductId, loggedIn=loggedIn,
                        firstName=firstName,userid=userid,
                        productCountinKartForGivenUser=noOfItems)


@app.route("/addToCart", methods=['GET', 'POST'])
def addToCart():
 num_products=1
 num_days = 1
 rent=False
 buyNow=False
 productId = request.args.get('productId')
 print('productId',productId)
 rent = request.args.get('rent')
 buyNow = request.args.get('buyNow')
 ##logging.warning('renatl status',rent)
 if rent:
     if request.method=='POST':
         num_days =  request.form.get('num_days')
         ##logging.warning('inside Number of days',num_days)
         extractAndPersistKartDetailsUsingSubquery(productId, num_products, rent=True, num_days=num_days)
 else:
     if request.method == 'POST':
         #logging.warning('inside sell products')
         num_products=request.form.get("numproduct")
         #Quantity=request.form.get("price")
         #logging.warning('Number of products',num_products)
         extractAndPersistKartDetailsUsingSubquery(productId, num_products)
         if buyNow:
             flash('Item successfully added to cart !!', 'success')
             return redirect(url_for('checkoutForm'))


 flash('Item successfully added to cart !!', 'success')
 return redirect(url_for('sellProducts'))


@app.route("/cart")
def cart():

 loggedIn, firstName, productCountinKartForGivenUser,userid = getLoginUserDetails()
 cartdetails1, totalsum1,tax1, cartdetails2, totalsum2,tax2  = getusercartdetails()
 #locdata = User.query.all()
 data={}
 locdata = User.query.filter(User.isadmin==1).all()
 for item in locdata:
     if item.city not in data:
         data[item.city]=["Toll gate","bus stop","near school"]
 #logging.warning(data)

 grand_total=totalsum1+totalsum2

 #logging.warning('grand_total',grand_total)
 return render_template("cart.html", locdata=locdata,cartData1=cartdetails1, cartData2=cartdetails2,productCountinKartForGivenUser=productCountinKartForGivenUser, loggedIn=loggedIn,
                        firstName=firstName, totalsum1=totalsum1,totalsum2=totalsum2, tax1=tax1,tax2=tax2, grand_total=grand_total,userid=userid)

def save_picture(form_picture,email=None):
     random_hex = secrets.token_hex(8)
     #logging.warning('form_picture',form_picture)

     try:
         #logging.warning('form_picture filename:',form_picture.filename)
         _, f_ext = os.path.splitext(form_picture.filename)
     except:

         _, f_ext = os.path.splitext(form_picture)
         #logging.warning('Value,.....',_)
     if email :
         picture_fn = email + f_ext
         #picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
     else:
         picture_fn = random_hex + f_ext
     picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

     output_size = (250, 250)

     image = Image.open(form_picture)
     image.thumbnail(output_size)
     image.save(picture_path)




     #logging.warning('picture_path{0}{1}',picture_path,picture_fn)

     return picture_fn


@app.route("/category/<int:category_id>", methods=['GET'])
def category(category_id):
     if isUserAdmin():
         category = Category.query.get_or_404(category_id)
         ##logging.warning(category.category_name,category.category_image,category_id)
         return render_template('adminCategory.html', category=category,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                            productCountinKartForGivenUser=productCountinKartForGivenUser)
     return redirect(url_for('root'))

@app.route("/categories/new", methods=['GET', 'POST'])
def addCategory():
     if isUserAdmin():
         form = addCategoryForm()
         category_icon=''
         if form.validate_on_submit():
             ##logging.warning(form.category_image.data,form.category_name.data)
             if form.category_image.data:
                 category_icon = save_picture(form.category_image.data)
                 ##logging.warning(category_icon)

             ##logging.warning('Picture saved',category_icon)
             category = Category(category_name=form.category_name.data,category_image=category_icon)
             db.session.add(category)
             db.session.commit()
             flash('Category {form.category_name.data}! added successfully', 'success')
             return redirect(url_for('getCategories'))
         return render_template("addCategory.html", form=form)
     return redirect(url_for('getCategories'))




@app.route("/categories/<int:category_id>/update", methods=['GET', 'POST'])
def update_category(category_id):
 if isUserAdmin():
     category = Category.query.get_or_404(category_id)
     form = addCategoryForm()
     category_icon = ""  # safer way in case the image is not included in the form
     if form.validate_on_submit():
         if form.category_image.data:
             category_icon = save_picture(form.category_image.data)

         category.category_name= form.category_name.data
         category.category_image = category_icon
         db.session.commit()

         ##logging.warning(category)
         flash('This category has been updated!', 'success')
         return redirect(url_for('getCategories'))
     elif request.method == 'GET':
         form.category_name.data = category.category_name
     return render_template('addCategory.html', legend="Update Category", form=form,category=category)
 return redirect(url_for('getCategories'))


@app.route("/category/<int:category_id>/delete", methods=['POST'])
def delete_category(category_id):
 if isUserAdmin()==2:
     ProductCategory.query.filter_by(categoryid=category_id).delete()
     db.session.commit()
     category= Category.query.get_or_404(category_id)
     db.session.delete(category)
     db.session.commit()
     flash('Your category has been deleted!', 'success')
     return redirect(url_for('getCategories'))
 else:
     flash('Access denied to delete category', 'success')
     return redirect(url_for('getCategories'))

@app.route("/getcategories", methods=['GET'])
def getCategories():
 cur = mysql.connection.cursor()
 #Query for number of products on a category:
 cur.execute('SELECT category.categoryid, category.category_name,category.category_image,COUNT(product_category.productid) as noOfProducts FROM category LEFT JOIN product_category ON category.categoryid = product_category.categoryid GROUP BY category.categoryid');
 categories = cur.fetchall()
 return render_template('adminCategories.html', categories = categories,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                        productCountinKartForGivenUser=productCountinKartForGivenUser)
 #return redirect(url_for('root'))


#this method is copied from Schafer's tutorials



@app.route("/admin", methods=['GET'])
def admin():
 global firstName
 global isadmin
 global admin
 loggedIn, firstName, productCountinKartForGivenUser, userId = getLoginUserDetails()
 #logging.warning('inside admin,Userid{0},isadmin{1}'.format(userid,isadmin))
 isadmin = User.query.with_entities(User.isadmin).filter( User.userid == userId).first()
 #logging.warning('isadmin value',isadmin[0])
 isadmin=isadmin[0]
 if isadmin==2:
     admin=True
     return render_template('admin.html',default=True,firstName=firstName,loggedIn=loggedIn,isadmin=isadmin,admin=admin,userid=userid,productCountinKartForGivenUser=productCountinKartForGivenUser)
 else:
     abort(401)



@app.route("/farmer", methods=['GET'])
def farmer():
 loggedIn, firstName, productCountinKartForGivenUser, userId = getLoginUserDetails()
 return render_template('Farmer.html', firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                        productCountinKartForGivenUser=productCountinKartForGivenUser)




@app.route("/getproducts", methods=['GET'])
def getProducts():
 products=Product.query.all()
 #global userid
 loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
 #logging.warning('userid',userid)
 if isUserAdmin() == 2:
     products = Product.query.all()
     #global userid
     #userid, fname = User.query.with_entities(User.userid, User.fname).filter(User.email == session['email']).first()
     return render_template('adminProducts.html', products=products,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin,
                            userid=userid,productCountinKartForGivenUser=productCountinKartForGivenUser,admin=False)
 else:
     try:
         #userid=request.args.get('userid')
         if isUserAdmin() != 2:
             products = ProducerProduct.query.with_entities(ProducerProduct.productid).filter(
                     ProducerProduct.producerid == userid) \
                     .join(Product, Product.productid == ProducerProduct.productid) \
                     .add_columns(Product.productid, Product.product_name, Product.description, Product.image, Product.quantity,
                                  Product.regular_price,
                                  Product.price_scale).all()
         return render_template('adminProducts.html', products=products, firstName=firstName, loggedIn=loggedIn,
                                isadmin=isadmin,
                                userid=userid, productCountinKartForGivenUser=productCountinKartForGivenUser)
     except:
         pass



 return render_template('adminProducts.html', products=products,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                        productCountinKartForGivenUser=productCountinKartForGivenUser)




@app.route("/products/new", methods=['GET', 'POST'])
def addProduct():
 if isUserAdmin():
     form = addProductForm()
     userid,fname,isadmin=User.query.with_entities(User.userid, User.fname,User.isadmin).filter(User.email == session['email']).first()
     form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]

     scaleoptions = [(1, 'Price per KG'), (2, 'Price per piece'), (3, 'Price per Liter'), (4, 'Price per KG')]
     mydict = {}
     for item in scaleoptions:
         mydict[item[0]] = item[1]
     ##logging.warning(mydict)
     form.priceingScale.choices = scaleoptions


     #form.user.choices = [(row.userid, row.fname) for row in User.query.all()]
     product_icon = "" #safer way in case the image is not included in the form
     if form.validate_on_submit():
         if form.image.data:
             product_icon = save_picture(form.image.data)
         selectedscale = mydict[form.priceingScale.data]
         product = Product(sku=form.sku.data, product_name=form.productName.data, description=form.productDescription.data, image=product_icon, quantity=form.productQuantity.data, price_scale=15, product_rating=0, product_review=selectedscale, regular_price=form.productPrice.data)

         db.session.add(product)
         db.session.commit()
         ##logging.warning('product added is:',product)
         product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
         db.session.add(product_category)
         db.session.commit()
         #flash('Product {form.productName} added successfully', 'success')

         product_producer = ProducerProduct(producerid=userid, productid=product.productid)
         db.session.add(product_producer)
         db.session.commit()
         flash('Product {form.productName} added successfully', 'success')
         #return render_template("root")
         return redirect(url_for('getProducts'))
         ##logging.warning('Product {form.productName} added successfullysuccess')
     return render_template("addProduct.html", form=form, legend="New Product",scale=scaleoptions,firstName=firstName,
                            loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                    productCountinKartForGivenUser=productCountinKartForGivenUser)
 return render_template("root")





@app.route("/user/<int:userid>/update", methods=['GET', 'POST'])
def updateProfile(userid):
     #userid = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
     user = User.query.get_or_404(userid)
     ##logging.warning('User id',userid)
     form = addUserForm()
     #form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
     #farm_icon = ""  # safer way in case the image is not included in the form
     if form.validate_on_submit():
         #if form.image_file.data:
          #   farm_icon = save_picture(form.image_file.data)
         #user.password=form.confirmpassword.data
         user.email = form.email.data
         user.fname=form.firstName.data
     #    user.image_file=farm_icon

         #user_instance = User(fname=form.fname.data, email=form.email.data, image=farm_icon)
         db.session.commit()
         flash('User added successfully', 'success')
         ##logging.warning('user added suucess')
     return render_template("addUser.html", form=form, legend="Update User",firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                        productCountinKartForGivenUser=productCountinKartForGivenUser)



@app.route("/user/<int:userid>", methods=['GET'])
def user(userid):
 user = User.query.get_or_404(userid)
 ##logging.warning('userid',userid)
 return render_template('adminUser.html', user=user,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                        productCountinKartForGivenUser=productCountinKartForGivenUser)
 return redirect(url_for('root'))

##################Product updation/Modification##########################################################33
@app.route("/product/<int:product_id>", methods=['GET'])
def product(product_id):
 if isUserAdmin():
     product = Product.query.get_or_404(product_id)
     return render_template('adminProduct.html', product=product,isadmin=2)
 return redirect(url_for('root'))




@app.route("/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
 product = Product.query.get_or_404(product_id)
 form = addProductForm()
 scaleoptions = [(1, 'Price per KG'), (2, 'Price per piece'), (3, 'Price per Liter'), (4, 'Price per KG')]
 mydict = {}
 for item in scaleoptions:
     mydict[item[0]] = item[1]
 ##logging.warning(mydict)
 form.priceingScale.choices = scaleoptions
 form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
 if form.validate_on_submit():
     if form.image.data:
         product.image = save_picture(form.image.data)
     product.product_name = form.productName.data
     product.sku = form.sku.data
     product.productDescription = form.productDescription.data
     product.quantity = form.productQuantity.data
     product.product_review = mydict[form.priceingScale.data]

     # product.price_scale = form.data.price_scale = 15
     product.regular_price = form.productPrice.data
     db.session.commit()
     product_category = ProductCategory.query.filter_by(productid=product.productid).first()
     if form.category.data != product_category.categoryid:
         new_product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
         db.session.add(new_product_category)
         db.session.commit()
         db.session.delete(product_category)
         db.session.commit()

     flash('This product has been updated!', 'success')

 return render_template("addProduct.html", form=form, legend="update Product")




@app.route("/product/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
 if isUserAdmin():
     product_category = ProductCategory.query.filter_by(productid=product_id).first()
     if product_category is not None:
         db.session.delete(product_category)
         db.session.commit()

     producer_product = ProducerProduct.query.filter_by(productid=product_id).first()
     if producer_product is not None:
         db.session.delete(producer_product)
         db.session.commit()

     Cart.query.filter_by(productid=product_id).delete()
     db.session.commit()
     product = Product.query.get_or_404(product_id)
     db.session.delete(product)
     db.session.commit()
     flash('Your product has been deleted!', 'success')
 return redirect(url_for('getProducts'))





@app.route("/users", methods=['GET'])
def getUsers():
 if isUserAdmin()==2:
     users = User.query.all()
 else:
     users = User.query.with_entities(User).filter(User.email == session['email']).all()
 return render_template('adminUsers.html', users=users,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                            productCountinKartForGivenUser=productCountinKartForGivenUser)


@app.route("/removeFromCart")
def removeFromCart():
 productId = int(request.args.get('productId'))
 removeProductFromCart(productId)
 return redirect(url_for('cart'))

@app.route("/checkoutPage")
def checkoutForm():

 cartdetails1, totalsum1, tax1, cartdetails2, totalsum2, tax2 = getusercartdetails()
 #logging.warning('cartdetails1, totalsum1, tax1, cartdetails2, totalsum2, tax2',totalsum1, tax1,  totalsum2, tax2)
 grand_total= float(totalsum1+float(tax1)+totalsum2+float(tax2))

 return render_template("checkoutPage.html", cartData=cartdetails1, grand_total=grand_total, tax=tax1)



@app.route("/createOrder", methods=['GET', 'POST'])
def createOrder():
 totalsum = request.args.get('total')
 email, username, ordernumber, address, fullname, phonenumber = extractOrderdetails(request, totalsum)
 if email:
     #sendEmailconfirmation(email, username, ordernumber, phonenumber, provider)
     sendEmailconfirmation(email,ordernumber,phonenumber)

 return render_template("OrderPage.html", username=username, ordernumber=ordernumber,email=email,
                                address=address, fullname=fullname, phonenumber=phonenumber)









#########################################################################################################
   #################*******   RENTAL EQUIPMENTS*********************#############################
#########################################################################################################

@app.route("/booking",methods=['GET','POST'])
def booking():
    #a,b,c,d,e=knowrentalprices(productid=2,numdays=3,delivery=True,driver=True)
    ##logging.warning(a,b,c,d,e)
    rent_status=''
    current_date=datetime.now()
    current_date=str(current_date).split(" ")
    current_date=current_date[0]
    #logging.warning('current_date',current_date)

    rentalproductid = request.args.get('productid')

    ##logging.warning('Rental productid',rentalproductid)


    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()

    if request.method=='POST'and loggedIn:
        rentalorder_date = request.form['orderstartdate']
        rentalreturn_date = request.form['orderenddate']

        email=session['email']

        #logging.warning('Inside post Rental productid', rentalproductid,rentalorder_date,rentalreturn_date)

    if not loggedIn:
        redirect(url_for('bookingForm'))

    if request.method=='POST' and not loggedIn:
        rentalproductid = request.form['proSel']
        email = request.form['email']
        firstName = request.form['firstName']
        rentalorder_date = request.form['orderstartdate']
        rentalreturn_date = request.form['orderenddate']
        address1 = request.form['address1']
        #rental_status = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        userid=999
        ##logging.warning('rentalproduct',rentalproduct)
        #productid= RentalProduct.query.with_entities(RentalProduct.productid).filter(RentalProduct.product_name==rentalproduct).first()

        ##logging.warning('Days',rentalorder_date,rentalreturn_date)


    rentstart_days = convertdates(rentalorder_date, current_date)
    days = convertdates(rentalorder_date, rentalreturn_date)
    rentend_days = convertdates(rentalreturn_date,current_date)
    if rentend_days >0 and rentstart_days>0:
        rental_status=1
    else:
        rental_status = 0
        #logging.warning('Order is not confirmed')


    extractAndPersistKartDetailsUsingSubquery(productId=rentalproductid, rent=True, num_days=days)

    cartdetails1, totalsum1, tax1, cartdetails2, totalsum2, tax2 = getusercartdetails()

    ##logging.warning('inside try')
    userid= User.query.with_entities(User.userid).filter(User.email==email).all()
    #logging.warning('userid:',userid)
    if not userid:
        ##logging.warning('User doesnot exist in Database,so adding user')
        user = User(fname=firstName, lname='guest', password=hashlib.md5("guest".encode()).hexdigest(),
                    address1=address1,address2='',city=city, state=state, country=country, zipcode=zipcode, email=email,
                    phone=phone, isadmin=isadmin)
        userid = User.query.with_entities(User.userid).filter(User.email == email).first()
        db.session.add(user)
        db.session.flush()
        db.session.commit()

    userid = User.query.with_entities(User.userid).filter(User.email == email).first()
    ##logging.warning('Userid',userid)

    if userid!=999:
        order = RentalOrder(rentalproductid=rentalproductid,userid=userid,rentalorder_date=rentalorder_date, rentalreturn_date=rentalreturn_date,
                  total_price=totalsum2, rental_status=rental_status)
        db.session.add(order)
        db.session.commit()

    return render_template('rentalproducts.html')

############################################################################################################################

@app.route("/check_available",methods=['POST','GET'])
def check_available():
    productid=request.args.get("productid")
    rent_status=RentalOrder.query.with_entities(RentalOrder.rental_status).filter(productid==RentalOrder.rentalproductid).first()
    if rent_status:
        return False
    else:
        return True


class addRentalCategoryForm(FlaskForm):
 category_image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png'])])
 category_name = StringField('Category Name', validators=[DataRequired()])
 submit = SubmitField('Save')



class addRentalProductForm(FlaskForm):
 category = SelectField('Rental Category:', coerce=int, id='select_category')
 productName = StringField('RentalProduct Name:', validators=[DataRequired()])
 productDescription = TextAreaField('RentalProduct Description:', validators=[DataRequired()])
 price_scale= SelectField('RentalPrice_scale:', coerce=int, id='select_scale')
 productPrice = FloatField('RentalProduct Price:', validators=[DataRequired()])
 productQuantity = IntegerField('RentalProduct Quantity:', validators=[DataRequired()])
 city = StringField('City:', validators=[DataRequired()])
 image = FileField('RentalProduct Image', validators=[FileAllowed(['jpg', 'png'])])
 submit = SubmitField('Save')

@app.route("/getrentalproducts", methods=['GET'])
def getallRentalProducts():
 products=RentalProduct.query.all()
 global userid
 #logging.warning('userid',userid)
 if isUserAdmin() == 2:
     products = RentalProduct.query.all()
     #global userid
     #userid, fname = User.query.with_entities(User.userid, User.fname).filter(User.email == session['email']).first()
     return render_template('adminRentalProducts.html', products=products,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin,
                            userid=userid,productCountinKartForGivenUser=productCountinKartForGivenUser)
 else:
     try:
         userid=request.args.get('userid')
         #logging.warning('userid',userid)
         if userid and isUserAdmin() == 1:
             #logging.warning('inside userid')
             products = RentalProducerProduct.query.with_entities(RentalProducerProduct.productid).filter(
                     RentalProducerProduct.producerid == userid) \
                     .join(RentalProduct, RentalProduct.productid == RentalProducerProduct.productid) \
                     .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.description, RentalProduct.image, RentalProduct.quantity,
                                  RentalProduct.regular_price,
                                  RentalProduct.city).all()
             #logging.warning('products',products,len(products))
         return render_template('adminRentalProducts.html', products=products, firstName=firstName, loggedIn=loggedIn,
                                isadmin=isadmin, userid=userid,
                                productCountinKartForGivenUser=productCountinKartForGivenUser)

     except:
         return redirect(url_for('farmer'))




@app.route("/rentalcategories/new", methods=['GET', 'POST'])
def addRentalCategory():
 if isUserAdmin():
     form = addCategoryForm()
     category_icon=''
     if form.validate_on_submit():
         ##logging.warning(form.category_image.data,form.category_name.data)
         if form.category_image.data:
             category_icon = save_picture(form.category_image.data)
             ##logging.warning(category_icon)

         ##logging.warning('Picture saved',category_icon)
         category = RentalCategory(category_name=form.category_name.data,category_image=category_icon)
         db.session.add(category)
         db.session.commit()
         flash('Rental Category {form.category_name.data}! added successfully', 'success')
         #return redirect(url_for('getCategories'))
     return render_template("addRentalCategory.html", form=form)


#######################################################################################################################

####################Rental product updation/modification##############################################################33
@app.route("/rentalproducts",methods=['POST','GET'])
def rentalproducts():
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    productid=99999
    list1 = []
    rent_status=0
    search=False
    check=False
    search=request.args.get('search')
    check=request.args.get('check')

    ##logging.warning('check',check)
    if check:
        productid = request.args.get("productid")
        p=RentalOrder.query.filter_by(rentalproductid=productid).first()
        ##logging.warning('productid',p)
        if p:
            rent_status = RentalOrder.query.with_entities(RentalOrder.rental_status).filter(
            productid == RentalOrder.rentalproductid).first()
            rent_status=rent_status[0]
        else:
            rent_status=0


    msg1 = "SHOWING THE FARMERS LISTING ALL LOCATION"
    msg2 = "LISTING RENTAL PRODUCTS ALL LOCATIONS"

    ##logging.warning(loggedIn, firstName, productCountinKartForGivenUser)
    locdata = User.query.all()
    catdata=RentalCategory.query.all()

    RentalproductsDataall = RentalProduct.query.all()
    ProducerData = getRentOwnersDetails()
    locationDataall = User.query.with_entities(User.city).filter(User.isadmin == 1).all()
    categoryDataall =  RentalCategory.query.join(RentalProductCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
        .join(RentalProduct, RentalProduct.productid == RentalProductCategory.productid) \
        .order_by(RentalCategory.categoryid.desc()) \
        .distinct(RentalCategory.categoryid) \
        .all()
    city_name = request.args.get('city_name')
    # #logging.warning(city_name)

    if city_name:
        ProducerData = User.query.filter(User.city == city_name).join(RentalProducerProduct,User.userid == RentalProducerProduct.producerid) \
            .add_columns(User.fname, User.userid, User.city) \
            .join(RentalProductCategory, RentalProductCategory.productid == RentalProducerProduct.productid) \
            .add_columns(RentalProductCategory.categoryid).join(RentalCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
            .add_columns(RentalCategory.category_name, RentalCategory.categoryid).all()

    '''
    if search and request.method == 'POST':
        category_name = request.form["catSel"]
        ##logging.warning('category name', category_name)
        categoryId = RentalCategory.query.with_entities(RentalCategory.categoryid).filter(
            RentalCategory.category_name == category_name).first()
        ##logging.warning('categoryId',categoryId,category_name)

        msg1 = "FARMERS LISTING OF CATEGORY:{}".format(category_name.upper())
        msg2 = "RENTAL PRODUCTS OF CATEGORY {}".format(category_name.upper())
        ProducerData= getRentOwnersDetails(loc=city_name,cat=categoryId)

        RentalproductsDataall = RentalProduct.query.join(RentalProducerProduct, RentalProduct.productid == RentalProducerProduct.productid) \
        .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.regular_price,
                     RentalProduct.image,RentalProducerProduct.producerid) \
            .join(RentalProductCategory, RentalProductCategory.productid == RentalProduct.productid) \
            .add_columns(RentalProductCategory.categoryid).filter(RentalProductCategory.categoryid == categoryId) \
            .join(RentalCategory, RentalCategory.categoryid == categoryId) \
            .add_columns(RentalCategory.category_name, RentalCategory.categoryid)\
            .join(User,User.userid==RentalProducerProduct.producerid)\
            .filter(User.city == city_name).add_columns(User.city).all()
        check=True
        '''
    RentalproductsDataall = RentalProduct.query.join(RentalProductCategory,
                                                         RentalProduct.productid == RentalProductCategory.productid) \
        .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.regular_price,
                     RentalProduct.image) \
        .join(RentalCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
        .add_columns(RentalCategory.category_name).order_by(RentalCategory.categoryid.desc()) \
        .all()
    #logging.warning('Rental products',len(RentalproductsDataall))
    for item in RentalproductsDataall:
            productid = item.productid
            p = RentalOrder.query.filter_by(rentalproductid=productid).first()
            ##logging.warning('productid', p)
            if p:
                rent_status = RentalOrder.query.with_entities(RentalOrder.rental_status).filter(
                    productid == RentalOrder.rentalproductid).first()
                rent_status = rent_status[0]
            else:
                rent_status = 0
            data=(productid,rent_status)
            list1.append(data)


    return render_template('rentalproducts.html',rentalpage=True,list1=list1,loggedIn=loggedIn,productid=productid,check=check,rent_status=rent_status,rentalproducts=RentalproductsDataall,categoryData=categoryDataall,ProducerData = ProducerData,data=locdata,catdata=catdata,msg1=msg1,msg2=msg2)

@app.route("/getrentalowners")
def getrentalowners():
    data=getRentOwnersDetails(loc="Dispur")
    RentalproductsDataall = RentalProduct.query.all()
    return render_template('home.html', rentalproducts=RentalproductsDataall,ProducerData=data)

@app.route("/bookingForm",methods=['GET','POST'])
def bookingForm():
    loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()
    firstName=firstName.upper()
    productid=request.args.get("productid")
    locdata = User.query.with_entities(User.city).all()
    categoryData = RentalCategory.query.all()
    productData = RentalProduct.query.all()
    if userid:
        productData = RentalProducerProduct.query.with_entities(RentalProducerProduct.productid).filter(
            RentalProducerProduct.producerid == userid) \
            .join(RentalProduct, RentalProduct.productid == RentalProducerProduct.productid) \
            .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.description,
                         RentalProduct.image, RentalProduct.quantity,
                         RentalProduct.regular_price,
                         RentalProduct.city).all()

    if productid:
        productData=RentalProduct.query.filter(RentalProduct.productid==productid).all()
        categoryData = RentalCategory.query.join(RentalProductCategory,RentalProductCategory.productid==productid)\
                    .add_columns(RentalCategory.categoryid,RentalCategory.category_name,RentalProductCategory.categoryid)\
                    .filter(RentalProductCategory.categoryid == RentalCategory.categoryid).all()

    return render_template('rentBooking.html', firstName=firstName,data=locdata, categoryData=categoryData, productdata=productData)



@app.route("/rentalproduct/new", methods=['GET', 'POST'])
def addRentalProduct():
 if isUserAdmin():
     form = addRentalProductForm()
     userid,fname=User.query.with_entities(User.userid, User.fname).filter(User.email == session['email']).first()
     form.category.choices = [(row.categoryid, row.category_name) for row in RentalCategory.query.all()]

     scaleoptions = [(1, 'Price/hour'), (2, 'Price/day'), (3, 'Price/week'), (4, 'Price/month')]
     mydict = {}
     for item in scaleoptions:
         mydict[item[0]] = item[1]
     ##logging.warning(mydict)
     form.price_scale.choices = scaleoptions


     #form.user.choices = [(row.userid, row.fname) for row in User.query.all()]
     product_icon = "" #safer way in case the image is not included in the form
     if form.validate_on_submit():
         if form.image.data:
             product_icon = save_picture(form.image.data)
         selectedscale = mydict[form.price_scale.data]
         product = RentalProduct(city=form.city.data,price_scale=selectedscale, product_name=form.productName.data, description=form.productDescription.data, image=product_icon, quantity=form.productQuantity.data,product_rating=0, product_review='', regular_price=form.productPrice.data)

         db.session.add(product)
         db.session.commit()
         ##logging.warning('product added is:',product)
         product_category = RentalProductCategory(categoryid=form.category.data, productid=product.productid)
         db.session.add(product_category)
         db.session.commit()
         #flash('Product {form.productName} added successfully', 'success')

         product_producer = RentalProducerProduct(producerid=userid, productid=product.productid)
         db.session.add(product_producer)
         db.session.commit()
         flash('Product {form.productName} added successfully', 'success')
         ##logging.warning('Product {form.productName} added successfullysuccess')
     return render_template("addRentalProduct.html", form=form, legend="New Product",scale=scaleoptions,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin, userid=userid,
                    productCountinKartForGivenUser=productCountinKartForGivenUser)
 return render_template("root")


@app.route("/rentalproduct/<int:product_id>", methods=['GET'])
def rentalproduct(product_id):
 if isUserAdmin():
     product = RentalProduct.query.get_or_404(product_id)
     return render_template('adminRentalProduct.html', product=product)
 return redirect(url_for('root'))


@app.route("/rentalproduct/<int:product_id>/update", methods=['GET', 'POST'])
def update_rentproduct(product_id):
 if isUserAdmin():
     form = addRentalProductForm()
     userid,fname=User.query.with_entities(User.userid, User.fname).filter(User.email == session['email']).first()
     form.category.choices = [(row.categoryid, row.category_name) for row in RentalCategory.query.all()]

     scaleoptions = [(1, 'Price/hour'), (2, 'Price/day'), (3, 'Price/week'), (4, 'Price/month')]
     mydict = {}
     for item in scaleoptions:
         mydict[item[0]] = item[1]
     ##logging.warning(mydict)
     form.price_scale.choices = scaleoptions


     #form.user.choices = [(row.userid, row.fname) for row in User.query.all()]
     product_icon = "" #safer way in case the image is not included in the form
     if form.validate_on_submit():
         if form.image.data:
             product_icon = save_picture(form.image.data)
         selectedscale = mydict[form.price_scale.data]
         product = RentalProduct(city=form.city.data,price_scale=selectedscale, product_name=form.productName.data, description=form.productDescription.data, image=product_icon, quantity=form.productQuantity.data,product_rating=0, product_review='', regular_price=form.productPrice.data)

         db.session.add(product)
         db.session.commit()
         ##logging.warning('product added is:',product)
         product_category = RentalProductCategory(categoryid=form.category.data, productid=product.productid)
         db.session.add(product_category)
         db.session.commit()
         #flash('Product {form.productName} added successfully', 'success')

         product_producer = RentalProducerProduct(producerid=userid, productid=product.productid)
         db.session.add(product_producer)
         db.session.commit()
         flash('Product {form.productName} Updated successfully', 'success')

         #flash('This product has been updated!', 'success')

 return render_template("addRentalProduct.html", form=form, legend="update Rental Product")




@app.route("/rentalproduct/<int:product_id>/delete", methods=['POST'])
def delete_rentproduct(product_id):
 if isUserAdmin():
     product_category = RentalProductCategory.query.filter_by(productid=product_id).first()
     if product_category is not None:
         db.session.delete(product_category)
         db.session.commit()

     producer_product = RentalProducerProduct.query.filter_by(productid=product_id).first()
     if producer_product is not None:
         db.session.delete(producer_product)
         db.session.commit()

     RentalCart.query.filter_by(productid=product_id).delete()
     db.session.commit()
     product = RentalProduct.query.get_or_404(product_id)
     db.session.delete(product)
     db.session.commit()
     flash('Your product has been deleted!', 'success')
 return redirect(url_for('getallRentalProducts'))



@app.route("/getallBookings", methods=['GET'])
def getallBookings():
 bookings = RentalOrder.query.all()
 loggedIn, firstName, productCountinKartForGivenUser, userid = getLoginUserDetails()

 #logging.warning('userid inside getallbookings',userid)
 if isUserAdmin() == 2:
     for item in bookings:
         print('Booking',item.orderid)
 else:
     bookings= RentalOrder.query.filter_by(userid=userid).all()
     ##logging.warning(bookings2)



     #userid, fname = User.query.with_entities(User.userid, User.fname).filter(User.email == session['email']).first()
 return render_template('ManageBookings.html', bookings=bookings,firstName=firstName, loggedIn=loggedIn, isadmin=isadmin,
                            userid=userid,productCountinKartForGivenUser=productCountinKartForGivenUser)


@app.route("/removeFromRentalCart")
def removeFromRentalCart():
 productId = int(request.args.get('productId'))
 loggedIn, firstName, productCountinKartForGivenUser, userId = getLoginUserDetails()
 kwargs = {'userid': userId, 'productid': productId}
 cart = RentalCart.query.filter_by(**kwargs).first()
 if productId is not None:
     db.session.delete(cart)
     db.session.commit()
     flash("Product has been removed from cart !!")
 return redirect(url_for('cart'))

###################################################################################
@app.route('/displayRentalCategory')
@app.route('/displayRentalCategory/<category_name>',methods=['GET', 'POST'])
def displayRentalCategory(category_name=None):
    categoryId = request.args.get("categoryid")
    producerId = request.args.get("producerId")
    if not categoryId:
        categoryId = RentalCategory.query.with_entities(RentalCategory.categoryid).filter(
            RentalCategory.category_name == category_name).first()
        categoryId = categoryId[0]
        ##logging.warning('categoryId',categoryId)
    loggedIn, firstName, noOfItems, userid = getLoginUserDetails()
    if producerId:
        productDetailsByCategoryId = RentalProduct.query.join(RentalProducerProduct) \
            .filter(RentalProducerProduct.producerid == producerId) \
            .join(RentalProductCategory, RentalProduct.productid == RentalProductCategory.productid) \
            .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.regular_price,
                         RentalProduct.image, RentalProduct.quantity) \
            .join(RentalCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
            .filter(RentalCategory.categoryid == int(categoryId)) \
            .add_columns(RentalCategory.category_name) \
            .all()
        print('entered part',productDetailsByCategoryId)
    else:
        productDetailsByCategoryId = RentalProduct.query.join(RentalProductCategory, RentalProduct.productid == RentalProductCategory.productid) \
             .add_columns(RentalProduct.productid, RentalProduct.product_name, RentalProduct.regular_price,RentalProduct.image) \
             .join(RentalCategory, RentalCategory.categoryid == RentalProductCategory.categoryid) \
             .filter(RentalCategory.categoryid == int(categoryId)) \
             .add_columns(RentalCategory.category_name) \
             .all()
    if len(productDetailsByCategoryId)!= 0:
         categoryName = productDetailsByCategoryId[0].category_name
         data = productDetailsByCategoryId
         return render_template('displayrentalCategory.html', data=data, loggedIn=loggedIn, firstName=firstName,
                                noOfItems=noOfItems, categoryName=categoryName)
    else:
         return('<h1>No results found for this category</h1>')


#######################################################################################3333
@app.route("/rentalproductDescription")
def rentalproductDescription():
 #logging.warning('inside rentalproductDescription ')
 loggedIn, firstName, noOfItems,userid= getLoginUserDetails()
 list1=[]
 rent_status=0
 start_date=current_date
 end_date=current_date
 productid = request.args.get('productid')
 #logging.warning('productid of pro',productid)
 productDetailsByProductId = getrentalProductDetails(productid)

 p = RentalOrder.query.filter_by(rentalproductid=productid).first()
 #logging.warning('Rental Order Status', p)
 if p:
     rent_status,start_date,end_date = RentalOrder.query.with_entities(RentalOrder.rental_status,
                                                   RentalOrder.rentalorder_date,RentalOrder.rentalreturn_date).filter(
         productid == RentalOrder.rentalproductid).first()

     #logging.warning('inside p,rent_status',rent_status )

 else:
     rent_status = 0
 #logging.warning('renatl status',rent_status)

 productid = request.args.get("productid")
 locdata = User.query.with_entities(User.city).all()
 categoryData = RentalCategory.query.all()
 productData = RentalProduct.query.all()

 if productid:
     productData = RentalProduct.query.filter(RentalProduct.productid == productid).all()
     categoryData = RentalCategory.query.join(RentalProductCategory, RentalProductCategory.productid == productid) \
         .add_columns(RentalCategory.categoryid, RentalCategory.category_name, RentalProductCategory.categoryid) \
         .filter(RentalProductCategory.categoryid == RentalCategory.categoryid).all()

 #return render_template('rentBooking.html', data=locdata, categoryData=categoryData, productdata=productData)

 return render_template("rentalproductDescription.html", locdata=locdata, categoryData=categoryData, productdata=productData,data=productDetailsByProductId, loggedIn=loggedIn,rent_status=rent_status,start_date=start_date,end_date=end_date)










