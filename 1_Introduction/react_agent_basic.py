from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, tool, AgentType
from langchain_community.tools import TavilySearchResults
import datetime

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time


tools = [search_tool, get_system_time]
#giving the agent type of zero-shot react description and it does resoning before acting
#you can also use other agent types like REACT_DOCSTORE, SELF_ASK_WITH_SEARCH
#or even CHAT_ZERO_SHOT_REACT_DESCRIPTION, CHAT_CONVERSATIONAL_REACT_DESCRIPTION
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.invoke({"input":"When was SpaceX's last launch and how many days ago was that from this instant"})

