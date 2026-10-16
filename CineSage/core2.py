# Structured Output & Final CinaSage completion

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-120b")

# Schema
class Movie(BaseModel):
    title: str
    release_year : Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

# Parser
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ('system', """
Extract movie information from the paragraph
    {format_instructions}
"""),
("human","{paragraph}")
]
).partial(
    format_instructions=parser.get_format_instructions()
)


para = input("Give your paragraph : ")

final_prompt = prompt.invoke(
    {"paragraph" : para}
)

response = model.invoke(final_prompt)
movie_data = parser.parse(response.content)
print(movie_data)