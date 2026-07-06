from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq( model="llama-3.3-70b-versatile",groq_api_key=groq_api_key)

#Create a prompt template
system_template="Translate the following into {language}:"

prompt_template=ChatPromptTemplate.from_messages(
    [("system",system_template),("user","{text}")]
)

# Parser - sets the output of the model into a string format, cutting off any extra information that the model may provide
parser=StrOutputParser()

#creat chain
chain=prompt_template|model|parser

#app defination
app=FastAPI(title="Language Translation API",version="1.0.0",description="This API translates text from one language to another")

# add chain routes to the app
add_routes(app,chain,path="/chain")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8001)
    