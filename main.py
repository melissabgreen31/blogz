from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
db = SQLAlchemy(app)



#Once you have made a Blog class with the necessary properties (i.e., an id, title, and body), you'll need to initialize your database:

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

   



@app.route('/blog', methods = ['GET', 'POST'])
def main_blog():
    #if there;s an id, show one post
    #if theres not, show all posts
    blog=Blog.query.all()
    if request.args.get('id')== True:
        single_blog = Blog.query.filter_by(id).all()
        return render_template('blog.html', single_blog=blog)
    else:
        return render_template('blog.html', blog=blog)


    


@app.route('/newpost', methods = ['POST','GET'])
def create_post():
    if request.method== 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        
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


        blog = Blog(title = blog_title, body= blog_body)
        db.session.add(blog)
        db.session.commit()
    return render_template('newpost.html')

    
        

@app.route('/')
def index():
    return redirect('/blog')



if __name__ == "__main__":
    app.run()
