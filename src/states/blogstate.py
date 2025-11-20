from typing import TypedDict
from pydantic import BaseModel, Field
from enum import Enum


class Blog(BaseModel):
    title: str = Field(description="the title of the blog post")
    content: str = Field(description="the main content of the blog post")


class LanguageMode(str, Enum):
    native = "native"       
    translation = "translation" 


class BlogState(TypedDict):
    topic: str
    blog: Blog
    language_mode: LanguageMode  
    language: str                
