import gradio as gr
import whisper
from whisper import tokenizer
from pytube import YouTube

loaded_model = whisper.load_model("base")
current_size = 'base'
AUTO_DETECT_LANG = "Auto Detect"

def inference(link,language):
  yt = YouTube(link)
  path = yt.streams.filter(only_audio=True)[0].download(filename="audio.mp4")
  results = loaded_model.transcribe(path,without_timestamps=True,language=language)
  return results['text']

def change_model(size):
  if size == current_size:
    return
  loaded_model = whisper.load_model(size)
  current_size = size

def populate_metadata(link):
  yt = YouTube(link)
  return yt.thumbnail_url, yt.title

title="Youtube Whisperer"
description="Speech to text transcription of Youtube videos using OpenAI's Whisper"
block = gr.Blocks()

with block:
    gr.HTML(
        """
            <div style="text-align: center; max-width: 500px; margin: 0 auto;">
              <div>
                <h1>Youtube Whisperer</h1>
              </div>
              <p style="margin-bottom: 10px; font-size: 94%">
                Speech to text transcription of Youtube videos using OpenAI's Whisper
              </p>
            </div>
        """
    )
    with gr.Group():
        with gr.Box():
          sz = gr.Dropdown(label="Model Size", choices=['base','small', 'medium', 'large'], value='base')
          with gr.Row(mobile_collaps=False,equal_height=True):
            link = gr.Textbox(label="YouTube Link")
            available_languages = sorted(tokenizer.TO_LANGUAGE_CODE.keys())
            available_languages = [AUTO_DETECT_LANG]+available_languages
            language = gr.Dropdown(label="Language",choices=available_languages,value=AUTO_DETECT_LANG)
            
            if language==AUTO_DETECT_LANG:
              language=None

          with gr.Row().style(mobile_collapse=False, equal_height=True):
            title = gr.Label(label="Video Title", placeholder="Title")
            img = gr.Image(label="Thumbnail")
          text = gr.Textbox(
              label="Transcription", 
              placeholder="Transcription Output",
              lines=5)
          with gr.Row().style(mobile_collapse=False, equal_height=True): 
              btn = gr.Button("Transcribe")       
          
          # Events
          btn.click(inference, inputs=[link,language], outputs=[text])
          link.change(populate_metadata, inputs=[link], outputs=[img, title])
          sz.change(change_model, inputs=[sz], outputs=[])

block.launch(debug=True)