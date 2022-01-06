from pytube import YouTube
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from io import BytesIO

class YouTubeVideo:
  def __init__(self,url):
    self.link = url
    self.path = YouTube(self.link)
  
  def checking(self):
    try:
      self.path.check_availability()
    except:
      return False
    return True

  def PathInfo(self):
    self.title = self.path.title
    self.img = self.path.thumbnail_url

  def VideoProperties(self):
    self.formats = []
    for res in self.path.streams:
      if not res.resolution == None:
        self.formats.append([int(res.resolution.replace("p", "")), res.fps, res.itag])

    self.formats
    self.formats = map(
      lambda x: [x[2], str(x[0]) + "px - " + str(x[1]) + "fps"],
      sorted(self.formats)
    )
  def AudioProperties(self):
    self.formats = []
    for res in self.path.streams:
      if not res.abr == None:
        self.formats.append([res.abr,res.itag])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a898e0c7fcf264a8d9b862ba0cd47cfb'

@app.route('/', methods = ['GET','POST'])
def Index():
  if request.method == 'POST':
    if request.form['video-name'] == '':
      return render_template('error.html')
    session['link'] = request.form['video-name']
    option = request.form['choices']

    download_render = YouTubeVideo(session['link'])

    if not download_render.checking():
      return render_template('error.html')
    else:
      download_render.PathInfo()

      if option == 'Video':
        download_render.VideoProperties()
        return render_template('video.html', download_render = download_render)
      elif option == 'Audio':
        download_render.AudioProperties()
        return render_template('audio.html', download_render = download_render)
  return render_template('home.html')

@app.route('/download-video', methods = ['GET','POST'])
def DownloadVideo():
  if request.method == 'POST':
    res = request.form['res']
    print(res)
    buffer = BytesIO()
    download_render = YouTubeVideo(session['link'])
    download_render.PathInfo()
    download_render.VideoProperties()
    video = download_render.path.streams.get_by_itag(res)
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(
      buffer,
      as_attachment = True,
      download_name = download_render.title + '.mp4',
      mimetype = 'video/mp4'
    )

  return redirect(url_for('home'))

@app.route('/download-audio', methods = ['GET','POST'])
def DownloadAudio():
  if request.method == 'POST':
    res = request.form['res']
    print(res)
    buffer = BytesIO()
    download_render = YouTubeVideo(session['link'])
    download_render.PathInfo()
    download_render.VideoProperties()
    video = download_render.path.streams.get_by_itag(res)
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(
      buffer,
      as_attachment = True,
      download_name = download_render.title + '.mp3'
    )

  return redirect(url_for('home'))

if __name__ =='__main__':
  app.run()