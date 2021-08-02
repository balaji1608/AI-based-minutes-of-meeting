from flask import Flask,render_template,url_for,request,flash,redirect,jsonify,send_file
from flask_cors import CORS, cross_origin
import speech_recognition as sr
import os
import sys
sys.path.insert(0, os.getcwd()+"/helpers")
import YoutubeHelper as yt
import TextSummarization as ts
import json
from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'mp3','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    '''
    import ssl 
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 
    context.load_cert_chain('certificate.crt', 'private.key')

           '''
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/',methods=["POST"])
def upload_file():
   if request.method == 'POST':
      if 'file' not in request.files:
          return render_template('index.html',message="No File Uploaded")
      f = request.files['file']
      if f.filename == '':
          return render_template('index.html',message="No File Uploaded")
      if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)  
            f.save(os.path.join("uploads", 'temp.wmv'))
            
            return render_template('index.html',message="Uploaded Successfully, Generating Notes....")
      return render_template('index.html',message="Invalid Format")



@app.route('/downloadfile/<text>', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def testfn(text):
    print("INSIDE FLASK")
    ext_summary = ts.extractive_summary(text)
    print("EXTRACTIVE DONE")
    abs_summary = ts.abstractive_summary(text)
    print("EXTRACTIVE DONE")    
    ts.generate_pdf(ext_summary,abs_summary)
    f =  open("./static/notes.pdf" ,'rb')
    return send_file(f ,attachment_filename='minutes_of_meeting.pdf')




@app.route('/youtube/', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_youtube_transcripts():
    url = request.data.decode('utf-8')
    text = yt.get_transcripts(url)
    return text


@app.route('/audio/', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def convert_audio():
    src = "C:/Users/KISHAN/Documents/Meets Summarization/EDI-2/Flask/static/notes.mp3"
    dst = "C:/Users/KISHAN/Documents/Meets Summarization/EDI-2/Flask/static/notes.wav"
    
    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    r = sr.Recognizer()
    with sr.AudioFile("./static/notes.wav") as source:
        audio = r.record(source)

    try:
        s = r.recognize_google(audio)
        print("Text: "+s)
    except Exception as e:
        print("Exception: "+str(e))
    return s

if __name__ == "__main__":
    print('started')
    app.run(debug=False)









    