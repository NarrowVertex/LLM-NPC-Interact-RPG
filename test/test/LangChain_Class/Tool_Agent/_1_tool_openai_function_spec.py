from openai import AzureOpenAI
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
import json
import pytz
import requests
import os


#도시의 현재 시각
def get_time_from_city(city_name):

    geolocator = Nominatim(user_agent="timezone_finder")
    location = geolocator.geocode(city_name)
    
    if not location:
        return None
    
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    
    if timezone_str:        
        # # Get the timezone for the city
        timezone_info = pytz.timezone(timezone_str)

        # Get the current time in the timezone
        now = datetime.now(timezone_info)
        current_time = now.isoformat()

        return {"current_time":current_time}

    else:
        return None



#도시의 현재 날씨
def get_weather_in_city(city_name):
    geolocator = Nominatim(user_agent="weather_checker")
    location = geolocator.geocode(city_name)
    
    if not location:
        return None

    params = {
        "lat": location.latitude,
        "lon": location.longitude,
        "units": "metric",
        "lang":  "en",
        "appid": os.getenv("WEATHER_API_KEY")
    }
    url = "https://api.openweathermap.org/data/2.5/weather?{}".format("&".join([f"{k}={v}" for k, v in params.items()]))
    response = requests.get(url).json()


    return_data = {
        "country": response["sys"]["country"],
        "region": response["name"],
        "weather_main": response["weather"][0]["main"],
        "weather_description": response["weather"][0]["description"],
        "current_temperature_celsius": response["main"]["temp"],
        "feel_like_temperature_celsius": response["main"]["feels_like"],
        "max_temperature_celsius": response["main"]["temp_max"],
        "min_temperature_celsius": response["main"]["temp_min"],
        "humidity": response["main"]["humidity"],
        "cloudiness": response["clouds"]["all"],
        "wind": response["wind"]["speed"]
    }

    return return_data


def real_function_call(name, args):

    function_map = {
        "get_time_from_city":get_time_from_city,
        "get_weather_in_city":get_weather_in_city
    }

    output = function_map[name](**json.loads(args))

    return {"function_output":output}



def ask_something(model_info, message_history, query):

    print(f"User : {query}")
    message_history.append({"role": "user","content": query})

    while True:

        response = model_info["model"].chat.completions.create(
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            temperature=0,
            messages=message_history,
            tools=model_info["functions"],
            tool_choice="auto"
        )

        #print(response)

        #Function Call (Tool Call)이 필요한 경우
        if response.choices[0].finish_reason == "tool_calls":

            response_message = response.choices[0].message

            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments

                function_output = real_function_call(function_name, function_args)

                #LLM 응답을 등록
                message_history.append(
                    {
                        "role": response_message.role, #assistant(ai)
                        "name": function_name,
                        "content": function_args
                    }
                )

                message_history.append({"role": "function", "name":function_name, "content": json.dumps(function_output)})
                
        else:
            break        

    content_str = response.choices[0].message.content
    message_history.append({"role": "assistant","content": content_str})
    
    print(f"LLM : {content_str}")
    
    return


def init_model():

    #Function Specification (GPT에 제공하는 함수 정보) 
    function_spec = [
        {
            "type": "function",
            "function": {
                "name": "get_time_from_city",
                "description": "Get the current time from the city name.",
                "parameters": { #parameters는 JSON Schema 형식을 따른다
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The city name."
                        }
                    },
                    "required": ["city_name"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather_in_city",
                "description": "Get the current weather information in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The city name"
                        }
                    },
                    "required": ["city_name"],
                }
            }            
        }        

    ]

    model = AzureOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    return {"model":model, "functions":function_spec}

if __name__ == "__main__":
    load_dotenv()
    model_info = init_model()

    #Initial Message History
    message_history = [
        {
            "role": "system", 
            "content": "You are an AI assistant that helps people to give the best answer for questions in Korean."
        }
    ]

    human_inputs = [
        "뉴욕의 현재 날씨를 알려줘",
        "거기 지금 몇시지?"
    ]

    for input in human_inputs:
        ask_something(model_info, message_history, input)
    

