from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog")
with mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(30) primary key,mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
    cursor.execute("create table if not exists login (username varchar(30) primary key,password varchar(20))")
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route('/')
def home():
    return render_template('homepage.html')
@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        address=request.form['address']
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into registration values(%s,%s,%s,%s,%s)',[username,mobile,address,email,password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/addposts',methods=['GET','POST'])
def addposts():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        
        print(title)
        print(content)
        
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts(title,content) values(%s,%s)',(title,content))
        mydb.commit()
        cursor.close()
    return render_template('addposts.html')
@app.route('/viewposts')
def viewposts():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewposts.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM posts WHERE id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewposts'))
@app.route('/update_post/<int:id>',methods=['GET','POST'])
def update_post(id):
    print(id)
    if request.method=='POST':
        title=request.form.get('title')
        content=request.form.get('content')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('update posts set title=%s,content=%s where id=%s',(title,content,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewposts'))
    else:
        cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.close()
    return render_template('update.html',post=post)
app.run()