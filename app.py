import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    file_receive = request.files['file_give']
    profile_receive = request.files['profile_give']
    extension = file_receive.filename.split('.')[-1]
    profile_extension = profile_receive.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    profile_name = f'profile-{mytime}.{profile_extension}'
    save_to = f'static/{filename}'
    file_receive.save(save_to)
    profile_receive.save(f'static/{profile_name}')
    
    doc = {
        'file': filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'Data was saved'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
