from flask import Flask, request, send_from_directory, send_file, render_template
import youtube_cut_api

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/download')
def cut_and_join():
    return render_template('download.html')
    #return send_file('./Dookudu_Ms_Narayana.mp4', as_attachment=True)
    #return send_from_directory('.', 'Dookudu_Ms_Narayana.mp4')

@app.route('/video', methods = ['POST'])
def cut_and_join2():
    data = request.form
    print data
    id = data['video_id']
    name = data['video_name']
    intervals = data['intervals']
    print id, name, intervals
    youtube_cut_api.editor(id, name, intervals)
    return send_file('./{}.mp4'.format(name.replace(' ', '_')), as_attachment=True)

if __name__=='__main__':
    app.run()