<<<<<<< HEAD
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(130))
    body = db.Column(db.String(2600))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body

        if pub_date is None:
            pub_date = datetime.utcnow()

        self.pub_date = pub_date


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    id = request.args.get('id')

    if not id:
        blogs = Blog.query.order_by(desc(Blog.pub_date)).all()

        return render_template('blog.html', title='Build a Blog', blogs=blogs)
    else:
        blogs = Blog.query.filter_by(id=id).all()

        return render_template('blog.html', title='Build a Blog', blogs=blogs)

@app.route('/newpost',  methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        title_error = ''
        body_error = ''

        if not title.strip():
            title_error = 'Please fill in a title'

        if not body.strip():
            body_error = 'Please fill in the body'

        if not title_error and not body_error:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?id={0}'.format(new_blog.id))
        else:
            return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)
    else:
        # initial view
        return render_template('newpost.html')

if __name__ == '__main__':
=======
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(130))
    body = db.Column(db.Text)
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False


#@app.route('/', methods=['POST', 'GET'])
#def index():

#    blogs = Blog.query.filter_by(completed=False).all()
#    completed_blogs = Blog.query.filter_by(completed=True).all()
#    return render_template('main-blog.html',title="Build-A-Blog", 
#        blogs=blogs, completed_blogs=completed_blogs)


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        #task_name = request.form['task']
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('main-blog.html',title="Build-A-Blog", 
        blogs=blogs, completed_blogs=completed_blogs)


@app.route('/newpost', methods=['POST', 'GET'])
#def delete_task():
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        title_error = ''
        body_error = ''

        if not title.strip():
            title_error = 'Please give your blog entry a title.'

        if not body.strip():
            body_error = 'Please type in your blog entry.'  

        if not title_error and not body_error:      
            new_blog = Blog(title, body)
            blog_id = int(request.form['blog-id'])
            print(blog_id)
            #blog_id = int(blog_id)
            blog = Blog.query.get(blog_id)
            print(blog)
            blog.completed = True
            db.session.add(blog)
            db.session.commit()

            return redirect('/blog?id={0}'.format(new_blog.id))
        else:
            return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)
    else:
        return render_template('newpost.html')            

if __name__ == '__main__':
>>>>>>> a62737f1609d3ec613291a936df161b36b58bc06
    app.run()