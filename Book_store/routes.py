from logging import exception
from msilib.schema import PublishComponent
from Book_store import app
from flask import redirect, render_template, url_for, flash, session, request
import random

from Book_store.forms import LoginForm, RegisterFrom, sellingForm
from functools import wraps

from Book_store import mydb

import os

from werkzeug.utils import secure_filename


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('signIn_user'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('home_page'))
        else:
            return f(*args, *kwargs)

    return wrap

@app.route('/')
def home_page():
    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from school_books limit 4;')
    schoolResult = db.fetchall()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from jee_books limit 4;')
    jeeResult = db.fetchall()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from neet_books limit 4;')
    neetResult = db.fetchall()
    db.close()
    return render_template('index.html', schoolResult = schoolResult, jeeResult =jeeResult, neetResult = neetResult)


@app.route('/result',methods = ["GET","POST"])
def result():
    if request.method == 'POST':
        book = request.form['book']
        db = mydb.cursor()
        db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from jee_books where bookName like "%{book}%" or publicationName like "%{book}%";')
        jeeResult = db.fetchall()
        db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from neet_books where bookName like "%{book}%" or publicationName like "%{book}%";')
        neetResult = db.fetchall()
        db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from school_books where bookName like "%{book}%" or publicationName like "%{book}%";')
        schoolResult = db.fetchall()
        db.close()
        return render_template('result.html', jeeResult = jeeResult, neetResult = neetResult, schoolResult = schoolResult)
    return redirect(url_for('home_page'))

@app.route('/JEE')
def jee_page():
    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from jee_books limit 15;')
    result = db.fetchall()
    db.close()
    return render_template('jee.html', result = result)

@app.route('/Community')
def community():
    return render_template('Community.html')


@app.route('/try')
def try_page():
    return render_template('try.html')

@app.route('/Account')
def account():
    userID = session['uid']
    db = mydb.cursor()
    db.execute(f'select username, email, urlImg, mobile_no from users where user_id = {userID}')
    userInfo = db.fetchone()
    return render_template('Account.html', userInfo = userInfo)


@app.route('/Schools')
def School_page():
    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from school_books limit 15;')
    result = db.fetchall()
    db.close()
    return render_template('Schools.html', result = result)


@app.route('/NEET')
def neet_page():
    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from neet_books limit 15;')
    result = db.fetchall()
    db.close()
    return render_template('neet.html', result = result)

@app.route('/B.Tech')
def btech_page():
    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from btech_books limit 15;')
    result = db.fetchall()
    db.close()
    return render_template('btech.html', result = result)

@app.route('/ContactUs')
def contact_us():
    return render_template('ContactUs.html')

@app.route('/AboutUs')
def about_us():
    return render_template('AboutUs.html')

@app.route('/Sell_books', methods = ["GET","POST"])
def Sell_books():
    if 'uid' in session:
        form = sellingForm()
        if form.validate_on_submit():
            streamName = form.streamName.data
            bookName = form.bookname.data
            subjectName = form.subjectName.data
            className = form.className.data
            mfgYear = form.mfgYear.data
            sellingAmount = form.sellingAmount.data
            publicationName = form.publicationName.data
            quantity = form.quantity.data
            
            ## set directory where we want to save image
            imgSaveDir = os.path.join(os.path.dirname(app.instance_path), 'Book_store\static\img')

            bookImg = form.bookImage.data
            imgName = secure_filename(bookImg.filename)

            # generating random number to make unique name
            n = random.randint(1000,1000000) 
            RandNumber = str(n)
            finalImgName = RandNumber+imgName
            # we have used \\\ three slash becuase 1 to avoid f strings escape and one to avoid database query escape
            # we have not used that url because we have faced issue to show pic by that url, so we will save name ans urlimg in
            #  database
            urlImg = f"'\\\static\\\img\\\sellerImg\\\{finalImgName}'"
            bookImg.save(os.path.join(imgSaveDir, 'sellerImg',finalImgName ))

            user_id = session['uid']
            sellername = session['s_name']
            # 'Universities', 'School','Competition'
            if(streamName == "School"):
                selectTb = 'school_books'
            elif(streamName == "JEE"):
                selectTb = 'jee_books'
            elif(streamName == "NEET"):
                selectTb = 'neet_books'
            elif(streamName == "B.Tech"):
                selectTb = 'btech_books'

            db = mydb.cursor()
            db.execute(f'insert into {selectTb}(bookname, subjectName, className, mfgYear, sellingAmount, publicationName, user_id, sellername, urlImg, quantity) values ("{bookName}", "{subjectName}", {className}, {mfgYear}, {sellingAmount}, "{publicationName}",{user_id},"{sellername}","{finalImgName}",{quantity});')
            mydb.commit()
            db.close()
            flash('Your Book has Been Added SuccessFully!','success')
            return render_template('Sell_books.html', form=form)
        else:
            # flash('Make sure to enter correct details, like photo and Subject','dark')
            return render_template('Sell_books.html',form=form)
    else:
        return redirect(url_for('signIn_user'))




@app.route('/signIn',methods = ["GET","POST"])
@not_logged_in
def signIn_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password_candidate = form.password.data

        db = mydb.cursor()

        db.execute(f'select * from users where username = "{username}";')
        result = db.fetchone()
        db.close()
        

        if result:
            data = result
            password = data[3] # in database password field is at index 3
            uid = data[0]  # user_id field is at index 0
            name = data[1] # username field is at index 1

            if password == password_candidate:
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                # flash("Logged In! Successfully",'success')
                return redirect(url_for('home_page'))
            else:
                flash('Incorrect Password !','danger')
                return render_template('signIn.html',form = form)
        else:
            flash('Username not found !','danger')
            return render_template('signIn.html', form=form)

    return render_template('signIn.html', form=form)

@app.route('/logout')
def logout():
    if 'uid' in session:
        session.clear()
        flash('You are Logged out','danger')
        return redirect(url_for('home_page'))
    return redirect(url_for('signIn_user'))





@app.route('/register', methods = ["GET","POST"])
def register_user():
    form = RegisterFrom()
    if form.validate_on_submit():
        try:
            db = mydb.cursor()
            db.execute(f'insert into users(username, email, password) values("{form.username.data}", "{form.email_address.data}", "{form.password1.data}");')
            mydb.commit()
            db.close()
            flash('Your Account created Successfully. LogIn To Continue..','success')
            return redirect(url_for('home_page'))
        except:
            flash("Username or Email-address is exist!",'danger')
         
    if form.errors != {}: # there are errors:
        for err_msg in form.errors.values():
            flash(f'{err_msg}','danger')
    return render_template('register.html', form = form)


    
@app.route('/Schools/<string:Department>')
def schools_department(Department):
    if Department == 'Science':
        return render_template('Schools/Science.html')

    else:
        return "<p> Page Not Found </p>"



@app.route('/Schools/Science/<string:subject_name>')
def Science_subjects(subject_name):

    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from school_books where subjectName = "{subject_name}";')
    result = db.fetchall()
    db.close()
    if subject_name == 'Physics':
        return render_template("Schools/ScienceB/Physics.html",data = result)
    elif subject_name == 'Chemistry':
        return render_template("Schools/ScienceB/Chemistry.html",data = result)
    elif subject_name == 'Biology':
        return render_template("Schools/ScienceB/Biology.html",data = result)
    elif subject_name == 'Maths':
        return render_template("Schools/ScienceB/Maths.html",data = result)
    else:
        return "Page Not found"



@app.route('/sellerHistory')
def sell_history():
    if 'uid' in session:
        sellerId = session['uid']
        sellerName = session['s_name']
        db = mydb.cursor()
        # category = ["school_books","btech",""]
        db.execute(f'select bookName, subjectName, className, mfgYear, sellingAmount, publicationName, urlImg from school_books where user_id = {sellerId};')
        result = db.fetchall()
        if result:
            return render_template('SellerHistory.html',result =result)
        else:
            result1 = "0"
            return render_template('SellerHistory.html',result = result1)
    else:
        return "Log In First "


@app.route('/<string:product_name_id>')
def product_display(product_name_id):
    x = product_name_id.split("+")
    book_id = x[0]
    used_tb = ''
    result = []
    n = len(x)
    if n == 2:
        used_tb = x[1]
        db = mydb.cursor()
        db.execute(f'select bookName, subjectName, className, mfgYear, sellingAmount, publicationName, sellername, urlImg, quantity  from {used_tb} where book_id = {book_id};')
        result = db.fetchone()
    return render_template('PdBook_indPage.html', data = result)




@app.route('/JEE/<string:subject_name>')
def jee_subjects(subject_name):

    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from jee_books where subjectName = "{subject_name}";')
    result = db.fetchall()
    db.close()
    if subject_name == 'Physics':
        return render_template("JEE/jee-Physics.html",data = result)
    elif subject_name == 'Chemistry':
        return render_template("JEE/jee-Chemistry.html",data = result)
    elif subject_name == 'Maths':
        return render_template("JEE/jee-Maths.html",data = result)
    else:
        return "Page Not found"



@app.route('/NEET/<string:subject_name>')
def neet_subjects(subject_name):

    db = mydb.cursor()
    db.execute(f'select bookName,className,mfgYear,sellingAmount,publicationName, urlImg, quantity, book_id from neet_books where subjectName = "{subject_name}";')
    result = db.fetchall()
    db.close()
    if subject_name == 'Physics':
        return render_template("NEET/neet-Physics.html",data = result)
    elif subject_name == 'Chemistry':
        return render_template("NEET/neet-Chemistry.html",data = result)
    elif subject_name == 'Biology':
        return render_template("NEET/neet-Biology.html",data = result)
    else:
        return "Page Not found"




# before adding cart option we have to make some changes in our databse,
# - streamName, Book adding date and time, Book Selling date and time, no of books available
@app.route('/Cart')
def fetchingCartDetails():
    customer_id = session['uid']
    db = mydb.cursor()
    db.execute(f'select book_id, table_name from cart where customer_id = {customer_id}')
    cart_values = db.fetchall()
    cartItems = []
    totalAmount = 0 # we will add all books sellingAmount here while fetching and then sends it to html
    for bookAndTable in cart_values:
        BookToFetch = bookAndTable[0]
        tableFetch = bookAndTable[1]
        db.execute(f'select bookName, sellingAmount, book_id, urlImg from {tableFetch} where book_id = {BookToFetch}')
        bookDetailForCart = db.fetchone()

        # adding totalAmount
        totalAmount += bookDetailForCart[1]

        # to append tableName in bookCart we typecase db result in list from tuple
        bookCart = list(bookDetailForCart) 
        bookCart.append(tableFetch)

        # insert all values in cartItems
        cartItems.insert(1, bookCart)
    db.close()
    return render_template('Cart.html', cartItems = cartItems, totalAmount = totalAmount)


    


@app.route('/Cart/<string:product_id_tableName>')
def addCart(product_id_tableName):

    if 'uid' in session:
        db = mydb.cursor()
        customer_id = session['uid']
        x = product_id_tableName.split("+")
        n = len(x)
        if n > 1:
            bookid = x[0]
            table_name = x[1]
            db.execute(f'insert into cart(customer_id, book_id, table_name) values({customer_id}, {bookid}, "{table_name}");')
            mydb.commit()
        db.close()
        return redirect(url_for('fetchingCartDetails'))
    else:
        return redirect(url_for('signIn_user'))


@app.route('/deleteFromcart+<string:bookID_Name>')
def deleteFromCart(bookID_Name):
    customerId  = session['uid']
    db = mydb.cursor()
    x = bookID_Name.split('+')
    n = len(x)
    if n > 1:
        bookId = x[0]
        tableName = x[1]
        db.execute(f'delete from cart where book_id  = {bookId} and  customer_id = {customerId} and table_name = "{tableName}"')
        mydb.commit()
    db.close()
    return redirect(url_for('fetchingCartDetails'))

    
