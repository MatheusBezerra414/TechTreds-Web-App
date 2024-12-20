import sqlite3
import logging
from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:app:%(asctime)s, %(message)s',
                    datefmt='%m/%d/%Y, %H:%M:%S')

# Function to get a database connection
connection_count = 0  # Track database connections


def get_db_connection():
    global connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    app.logger.info("Main page accessed.")
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.warning(f"404: Post ID {post_id} not found.")
        return render_template('404.html'), 404
    else:
        app.logger.info(f"Article '{post['title']}' retrieved!")
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("About Us page accessed.")
    return render_template('about.html')


# Define the healthz endpoint
@app.route('/healthz')
def healthz():
    response = {"result": "OK - healthy"}
    app.logger.info("Health check performed.")
    return jsonify(response), 200


# Define the metrics endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()

    response = {
        "db_connection_count": connection_count,
        "post_count": post_count
    }
    app.logger.info("Metrics endpoint accessed.")
    return jsonify(response), 200


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
            app.logger.warning("Post creation failed: Title is missing.")
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()

            app.logger.info(f"New article '{title}' created.")
            return redirect(url_for('index'))

    return render_template('create.html')


# Start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3111)