from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId
from mongoengine import Document, StringField, DateTimeField, connect

app = Flask(__name__, static_folder='static')

connect(db='mydatabase', host='mongodb://localhost/mydatabase')

class Blogpost(Document):
    title = StringField(max_length=50)
    subtitle = StringField(max_length=50)
    author = StringField(max_length=20)
    date_posted = DateTimeField()
    content = StringField()

@app.route('/')
def index():
    posts = Blogpost.objects.order_by('-date_posted')
    return render_template('index.html', posts=posts)

@app.route('/post/<string:post_id>')
def post(post_id):
    post = Blogpost.objects.get(id=ObjectId(post_id))
    return render_template('post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    date_posted = datetime.utcnow()
    post = Blogpost(title=title, subtitle=subtitle, author=author, date_posted=date_posted, content=content)
    post.save()
    return redirect(url_for('index'))

@app.route('/delete/<string:post_id>', methods=['POST'])
def delete(post_id):
    post = Blogpost.objects.get(id=ObjectId(post_id))
    post.delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
