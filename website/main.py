from flask import Flask, request, url_for, redirect, render_template, send_file, flash, Response, session
from datetime import timedelta
from functions import headers, download_video, remove_watermark, find_link
from os.path import exists
import flask_session
import gunicorn
import os

app = Flask(__name__)
if not os.path.exists("downloads"):
    os.mkdir("downloads")
app.secret_key = "appsecretkey"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        link = request.form.get('link')
        if "https://www.tiktok.com/" in link and "/video/" in link:
            video_link = find_link(link)
            if video_link != None:
                down_vid = download_video(video_link)
                rw = remove_watermark(down_vid)
                if exists(down_vid):
                    os.remove(down_vid)
                session['filename'], session['progress'] = rw, 100
                return send_file(rw, as_attachment=True)
        else:
            flash("Incorrect URL", "error")
    return render_template('home.html')

@app.route('/progress')
def progress():
    s= session.get('progress')
    x = {s == None: 0, s == 100: 100}.get(True, s)
    if x == 100:
        flash(f"Downloaded {session.get('filename')}", "download")
        session.pop('progress')
        if exists(session.get('filename')):
            os.remove(session.get('filename'))
    return Response("data:" + str(x) + "\n\n", mimetype="text/event-stream")

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()