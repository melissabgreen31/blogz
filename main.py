from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



#Once you have made a Blog class with the necessary properties (i.e., an id, title, and body), you'll need to initialize your database:

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'main_blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session: 
    
        return redirect('/login')  

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/blog')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) == 0:
            username_error = "Please enter a username"
            return render_template('signup.html', username_error=username_error)

        if len(password) == 0:
            password_error = "Please enter a password"
            return render_template('signup.html', password_error=password_error)

        if verify != password:
            verify_error = "Passwords do not match"
            return render_template('signup.html', verify_error=verify_error)
        
        
        
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/blog')
        

    return render_template('signup.html')

@app.route('/blog', methods = ['GET', 'POST'])
def main_blog():
    if request.args.get('id'):
        id= request.args.get('id')
        blog_id = Blog.query.filter_by(id=id).first()
        
        return render_template('singlepost.html', blog= blog_id)
    
    if request.args.get('user'):
        userid= int(request.args.get('user'))
        user = User.query.filter_by(id = userid).first()
        #blog = Blog.query.filter_by(owner=user).first()
        
        return render_template('useridposts.html', user = user)
    
    blog=Blog.query.all()
    return render_template('blog.html', blog=blog)

    
    
    

@app.route('/newpost', methods = ['POST','GET'])
def create_post():
    if request.method== 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        owner = User.query.filter_by(username=session['username']).first()
        
        if len(blog_body) == 0 and len(blog_title)== 0:
            body_error = "Please fill out the blog post."
            title_error = "Please add a blog title."
            return render_template('newpost.html', body_error=body_error, title_error=title_error)

        if len(blog_body) == 0:
            body_error = "Please fill out the blog post."
            return render_template('newpost.html', body_error=body_error)
            

        if len(blog_title)== 0:
            title_error = "Please add a blog title."
            return render_template('newpost.html', title_error=title_error)


        blog = Blog(title = blog_title, body= blog_body, owner = owner)
        db.session.add(blog)
        db.session.commit()
        blog_id = blog.id
        return redirect('/blog?id={}'.format(blog_id))
    return render_template('newpost.html')

    
        

@app.route('/')
def index():
    user=User.query.all()
    if request.args.get('user') is None:
        return render_template('index.html', user=user)
        
    



if __name__ == "__main__":
    app.run()
