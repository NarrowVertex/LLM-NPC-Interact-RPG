from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolCall ,ToolMessage
from langchain_core.runnables import Runnable
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
from datetime import datetime
import pytz
import requests
import json
import os

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults


#도시의 현재 시각
@tool
def get_time_from_city(city_name):

    """Get the current time for the given city name."""

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
class CityName(BaseModel):
    city_name: str = Field(description="City Name String")

@tool(args_schema=CityName)
def get_weather_in_city(city_name):

    """Get the current weather info for the given city name."""

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



def print_tool_info(tools):

    for tool in tools:
        print("Tool info")
        print(f"Name: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Args schema: {tool.args}")
        print(f"Returns directly?: {tool.return_direct}")
        print(f"Is Runnable?: {isinstance(tool, Runnable)}")
        print("\n")

    return




def real_tool_call(tool_call):

    tool_map = {
        "get_time_from_city":get_time_from_city,
        "get_weather_in_city":get_weather_in_city,
        "tavily_search_results_json":tavily_tool,
        "wikipedia":wikipedia_tool
    }

    name = tool_call["name"]
    args = tool_call["args"]

    output = tool_map[name].invoke(args)

    return {"output":output}



def ask_something(model, message_history, query):

    print(f"User : {query}")
    message_history.append(HumanMessage(content=query))

    while True:

        model_output = model.invoke(message_history)
        #print(model_output)

        if model_output.response_metadata["finish_reason"] == "tool_calls":

            for tool_call in model_output.tool_calls:

                tool_output = real_tool_call(tool_call)

                message_history.extend(
                    [
                        AIMessage(
                            content=f"The following is the result of {tool_call["name"]}",
                            tool_calls=[ToolCall(
                                name=tool_call["name"], 
                                args=tool_call["args"], 
                                id=tool_call["id"]
                            )]
                        ),
                        ToolMessage(
                            content=json.dumps(tool_output["output"]),
                            tool_call_id=tool_call["id"],
                            name=tool_call["name"]
                        )
                    ]
                )

        else:
            break
    
    print(f"LLM : {model_output.content}")
    message_history.append(AIMessage(content=model_output.content))

    return



def init_model(tools):

    azure_model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version = os.getenv("OPENAI_API_VERSION")
    )

    azure_model_tool_bind = azure_model.bind_tools(tools=tools, tool_choice="auto")

    return azure_model_tool_bind


if __name__ == "__main__":

    load_dotenv()

    #Many 3rd party tools in langchain
    #https://python.langchain.com/v0.2/docs/integrations/tools/

    #Wikipedia 툴
    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

    #Tavily 툴(검색 엔진)
    tavily_tool = TavilySearchResults(max_results=2)

    tools = [
        get_time_from_city,
        get_weather_in_city,
        wikipedia_tool,
        tavily_tool
    ]

    model = init_model(tools)

    message_history = [
        SystemMessage(content="You are an AI assistant that helps people to give the best answer for questions in Korean")
    ]

    human_inputs = [
        "OpenAI는 언제 설립되었지?",
        "지금 Apple 주가가 얼마인지 알려줘",
        "파리의 현재 시각을 알려줘",
        "거기 지금 날씨는 어때?",
    ]

    for input in human_inputs:
        ask_something(model,message_history,input)


