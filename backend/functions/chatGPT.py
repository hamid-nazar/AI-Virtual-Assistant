import openai
import dotenv
import whisper
import os
import json
from functions.tasks import get_local_time, get_flight_info, get_weather, add_reminder, remove_reminder, list_reminders
from functions.database import get_recent_messages
from functions.functions_descriptions import descriptions

dotenv.load_dotenv()

def new_output(messages):

    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    tools=descriptions,
    tool_choice="auto",)
            
    output = response.choices[0].message
    
    return output




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
  
  output = new_output(messages)
  
  print(output)
  print()
  print()
    
  while output.tool_calls:
      function_to_call = output.tool_calls[0]
      function_name = function_to_call.function.name

      if function_name == "get_local_time":
          print("GPT: called function ", function_name)
          time = get_local_time()
          messages.append({"role": "function", "name": function_name, "content": time})

      elif function_name in ["get_flight_info", "get_cheapest_flight"]:
          print("GPT: called function " + function_name)
          origin = json.loads(output.tool_calls[0].function.arguments).get("origin")
          destination = json.loads(output.tool_calls[0].function.arguments).get("destination")
          flight_info = get_flight_info(origin, destination) if function_name == "get_flight_info" else get_cheapest_flight(origin, destination)
          messages.append({"role": "function", "name": function_name, "content": flight_info})

      elif function_name == "get_weather":
          print("GPT: called function " + function_name)
          city = json.loads(output.tool_calls[0].function.arguments).get("city")
          weather = get_weather(city)
          messages.append({"role": "function", "name": function_name, "content": weather})

      elif function_name == "add_reminder":
          print("GPT: called function " + function_name)
          reminder_text = json.loads(output.tool_calls[0].function.arguments).get("reminder_text")
          reminder = add_reminder(reminder_text)
          messages.append({"role": "function", "name": function_name, "content": reminder})

      elif function_name == "list_reminders":
          print("GPT: called function " + function_name)
          reminders = list_reminders()
          messages.append({"role": "function", "name": function_name, "content": reminders})

      elif function_name == "remove_reminder":
          print("GPT: called function " + function_name)
          reminder_text = json.loads(output.tool_calls[0].function.arguments).get("reminder_text")
          reminder = remove_reminder(reminder_text)
          messages.append({"role": "function", "name": function_name, "content": reminder})

      output = new_output(messages)

  return output.content




    
      
      



""" def get_local_time():
  
  current_time = datetime.datetime.now()
  
  return current_time.strftime("%H:%M") """
  
  
  
""" def get_flight_info(origin, destination):
    Get flight information between two locations.

    # Example output returned from an API or database
    flight_info = {
        "origin": origin,
        "destination": destination,
        "datetime": str(datetime.datetime.now() + datetime.timedelta(hours=2)),
        "airline": "KLM",
        "flight": "KL643",
    }

    return json.dumps(flight_info) """
  
  
  