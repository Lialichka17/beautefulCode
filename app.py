from flask import Flask, request, jsonify, render_template, session
import xml.etree.ElementTree as ET
import os
import hashlib

app = Flask(__name__)
app.secret_key = b'your_secret_key_here'

# Paths to XML files
data_folder = os.path.join(app.root_path, 'data')
users_xml_path = os.path.join(data_folder, 'users.xml')
posts_xml_path = os.path.join(data_folder, 'posts.xml')

# Initialize XML file if not exists
def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
    except FileNotFoundError:
        print(f"XML file not found at {file_path}. Creating a new one.")
        root = ET.Element('root')
        tree = ET.ElementTree(root)
        tree.write(file_path)
    return tree

def save_xml(tree, file_path):
    try:
        tree.write(file_path)
        print(f"XML file saved successfully at {file_path}.")
    except Exception as e:
        print(f"Error saving XML file at {file_path}: {e}")

def get_users_tree():
    global users_tree
    if 'users_tree' not in globals():
        users_tree = load_xml(users_xml_path)
    return users_tree

def get_posts_tree():
    global posts_tree
    if 'posts_tree' not in globals():
        posts_tree = load_xml(posts_xml_path)
    return posts_tree

def add_user_to_xml(username, password):
    users_tree = get_users_tree()
    root = users_tree.getroot()

    new_user = ET.SubElement(root, 'user')
    ET.SubElement(new_user, 'username').text = username
    ET.SubElement(new_user, 'password').text = hashlib.sha256(password.encode()).hexdigest()

    save_xml(users_tree, users_xml_path)

def check_user(username):
    users_tree = get_users_tree()
    root = users_tree.getroot()

    for user in root.findall('user'):
        if user.find('username').text == username:
            return True

    return False

def authenticate_user(username, password):
    users_tree = get_users_tree()
    root = users_tree.getroot()

    for user in root.findall('user'):
        if user.find('username').text == username:
            hashed_password = user.find('password').text
            if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
                return True

    return False

def add_post_to_xml(topic, content, author):
    posts_tree = get_posts_tree()
    root = posts_tree.getroot()

    new_post = ET.SubElement(root, 'post')
    new_post.set('id', str(len(root) + 1))
    ET.SubElement(new_post, 'topic').text = topic
    ET.SubElement(new_post, 'content').text = content
    ET.SubElement(new_post, 'author').text = author

    save_xml(posts_tree, posts_xml_path)

@app.route('/')
def index():
    posts_tree = get_posts_tree()
    root = posts_tree.getroot()
    posts = []

    for post in root.findall('post'):
        post_data = {
            'topic': post.find('topic').text,
            'content': post.find('content').text,
            'author': post.find('author').text
        }
        posts.append(post_data)

    return render_template('index.html', posts=posts)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    if check_user(username):
        return jsonify({'success': False, 'message': 'Username already exists'})

    add_user_to_xml(username, password)

    return jsonify({'success': True, 'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate_user(username, password):
        session['username'] = username
        return jsonify({'success': True, 'message': 'Logged in successfully'})

    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Login required'})

    topic = request.form['topic']
    content = request.form['content']
    author = session['username']

    add_post_to_xml(topic, content, author)

    return jsonify({'success': True, 'message': 'Post created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
