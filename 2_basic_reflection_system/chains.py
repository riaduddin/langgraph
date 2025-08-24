from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------------------
# 1. Generation Prompt
# ---------------------------
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter tech influencer assistant tasked with writing excellent posts. "
            "Generate the best twitter post possible for the user's request. "
            "If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# ---------------------------
# 2. Reflection Prompt
# ---------------------------
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. "
            "Generate critique and recommendations for the user's tweet. "
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# ---------------------------
# 3. Choose LLM (Gemini)
# ---------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# ---------------------------
# 4. Create the chains
# ---------------------------
generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
