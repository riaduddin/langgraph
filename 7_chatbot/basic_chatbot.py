from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

# class BasicChatState(TypedDict):        
#     messages: list[Annotated[HumanMessage, add_messages]]

class BasicChatState(TypedDict):        
    # messages: Annotated[list, add_messages]
     # allow both human + ai messages in the history
    messages: Annotated[list[HumanMessage | AIMessage], add_messages]

#instead of TypedDict
# class BasicChatState(BaseModel):        
#     messages: Annotated[list, add_messages]

# def chatbot(state: BasicChatState):
#     print("Chatbot State:", state)
#     return {
#         "messages": [llm.invoke(state["messages"])]
#     }

def chatbot(state: BasicChatState):
    print("Node sees state:", state)   # Only latest input + prior AI response
    response = llm.invoke(state["messages"])
    return {"messages": [response]}     # This gets appended automatically

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()
while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)],
        })
        print(result)
        for msg in result["messages"]:
            role = "User" if isinstance(msg, HumanMessage) else "Bot"
            print(f"{role}: {msg.content}")
