from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# class Country(BaseModel):

#     """Information about a country"""

#     name: str = Field(description="name of the country")
#     language: str = Field(description="language of the country")
#     capital: str = Field(description="Capital of the country")
 
# structured_llm = llm.with_structured_output(Country)
# print(structured_llm.invoke("Tell me about France"))


from typing_extensions import Annotated, TypedDict
from typing import Optional


# TypedDict
class Joke(BaseModel):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


structured_llm = llm.with_structured_output(Joke)

print(structured_llm.invoke("Tell me a joke about cats"))


# json_schema = {
#     "title": "joke",
#     "description": "Joke to tell user.",
#     "type": "object",
#     "properties": {
#         "setup": {
#             "type": "string",
#             "description": "The setup of the joke",
#         },
#         "punchline": {
#             "type": "string",
#             "description": "The punchline to the joke",
#         },
#         "rating": {
#             "type": "integer",
#             "description": "How funny the joke is, from 1 to 10",
#             "default": None,
#         },
#     },
#     "required": ["setup", "punchline"],
# }
# structured_llm = llm.with_structured_output(json_schema)

# structured_llm.invoke("Tell me a joke about cats")