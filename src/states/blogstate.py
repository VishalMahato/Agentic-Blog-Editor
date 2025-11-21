from typing import TypedDict
from enum import Enum
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title: str = Field(description="the title of the blog post")
    content: str = Field(description="the main content of the blog post")


class LanguageMode(str, Enum):
    native = "native"       
    translation = "translation" 


class BlogState(TypedDict, total=False):
    topic: str
    blog: Blog
    language_mode: LanguageMode  
    language: str                
