from flask import Flask, render_template, request
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from PIL import Image

app = Flask(__name__)

def generate_poem(text_input=None, base64_image=None):
  text_data="Write a poem for this image"
  if base64_image:
     image_data = Part.from_data(
        mime_type="image/png",
        data=base64.b64decode(base64_image)     
     ) 
     if text_input:
        text_data=text_input
  else:
     image_data="write the poem about this"
     text_data = text_input

  vertexai.init(project="alealferez-project-2", location="us-central1")
  model = GenerativeModel("gemini-1.5-pro-preview-0409")

  responses = model.generate_content(
      [image_data,text_data],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  poem = "" # Initialize the poem variable
  for response in responses:
    poem += response.text # Concatenate the poem

  return poem # Return the generated poem


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 2,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Route accessed")
    if request.method == 'POST':
        text_input = request.form['text_input']
        image_input= request.files.get('image_input')
        if not text_input and not image_input:
           error_message = "Please dear, provide either text or an image"
           return render_template('index.html', error=error_message)
        if image_input:
            image_data =image_input.read()
            base64_image=base64.b64encode(image_data)
            poem = generate_poem(text_input, base64_image)
        else:
         poem = generate_poem(text_input)
        return render_template('index.html', poem=poem) 
    else:
        print("Route accessed")
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 