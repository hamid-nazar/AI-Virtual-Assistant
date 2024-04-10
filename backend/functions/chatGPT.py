import base64
import io
import openai
from decouple import config
import dotenv
import whisper
import os
import json
import numpy as np
import soundfile as sf
import datetime

from functions.database import get_recent_messages, store_messages
from functions.functions_descriptions import descriptions, function_description_get_flight_info

dotenv.load_dotenv()



# openai.api_key = os.getenv("OPENAI_API_KEY")

openai_client = openai.OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")


whisper_client = whisper.load_model("base")


def convert_speech_to_text(audio_file):
  try:
    
    transcript = openai_client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file)

    message_text = transcript.text
    
    
    print(transcript)
  
    return message_text
  
  except Exception as e:
    print(e)
    return



def get_chat_response(message):
  
  messages = get_recent_messages()
  user_masege = {"role": "user", "content": message}
  messages.append(user_masege)
  
  print(messages)
  
  try:
    
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages)
    
    message_text = response["choices"][0]["message"]["content"]
    
    return message_text
    
  except Exception as e:
    print(e)
    return
  
  
  
  
# alternative
  



def chat(message):
    #model="gpt-3.5-turbo-0613",
    messages = get_recent_messages()
    
    messages.append({"role": "user", "content": message})
    
    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    functions=descriptions,
    function_call="auto",)

    print(response)
    
    output = response.choices[0].message
    
    print(output)
    
    function_call = output.function_call
    
    
    if function_call:
        
        function_name = function_call.name
        
        if function_name == "get_local_time":
          
          print("GPT: called function ",function_call.name)
        
            
          chosen_function = eval(function_call.name)
            
            
          time = chosen_function()
          
          
          messages.append({"role": "function", "name": output.function_call.name, "content": time})
        
    
          response = fix_format(messages)
            
          return response
          
        elif function_name == "get_flight_info":

          
          params = json.loads(output.function_call.arguments)
          
          print("GPT: called function " +function_call.name)
          
          origin = json.loads(output.function_call.arguments).get("loc_origin")
          destination = json.loads(output.function_call.arguments).get("loc_destination")
          
          
          chosen_function = eval(function_name)
          
          flight = chosen_function(origin, destination)
          
          messages.append({"role": "function", "name": output.function_call.name, "content": flight})
          
          response = fix_format(messages)
          
          
          return response
          
        
    
    else:
        print("Function does not exist")
        print("GPT: " + response.choices[0].message.content)
        
        return response.choices[0].message.content;
      
      
      
      

def fix_format(messages):

    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=descriptions,
    function_call="auto",)
            
    response = response.choices[0].message.content
    print("GPT: " + response)
    
    return response
      
def get_local_time():
  
  current_time = datetime.datetime.now()
  
  return current_time.strftime("%H:%M")
  
  
  
def get_flight_info(origin, destination):
    """Get flight information between two locations."""

    # Example output returned from an API or database
    flight_info = {
        "origin": origin,
        "destination": destination,
        "datetime": str(datetime.datetime.now() + datetime.timedelta(hours=2)),
        "airline": "KLM",
        "flight": "KL643",
    }

    return json.dumps(flight_info)
  
  
  