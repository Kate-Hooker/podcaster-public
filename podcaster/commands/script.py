import sys
#from langchain.chat_models import ChatCohere
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama

def script(filename=None, duet=True):
    if filename:
        with open(filename, 'r') as file:
            input_text = file.read()
    else:
        if sys.stdin.isatty():
            print("Type or paste in some text and hit ctrl D to process")
        input_text = sys.stdin.read()

    if duet:
        create_duet_script(input_text)
    else:
        create_solo_script(input_text)

def create_solo_script(text):
    #model = ChatCohere(streaming=True)
    llm = Ollama(model="mistral")
    template = """create a podcast script based off the following ideas, reply with only the words for the host to speak, nothing else. The host's name is Jenny. 
    ---
    {text}
    ---
    Remember, reply only with the words the host will speak, nothing else!!
    """
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm

    for s in chain.stream({"text":text}):
        #print(s.content, end="", flush=True)
        print(s, end="", flush=True)

def create_duet_script(text):
    llm = Ollama(model="mistral")
    template = """create a podcast script based off the following ideas, reply with only the words for the hosts to speak, nothing else. The first host's name is Jenny, the second is Tim. Start with the hosts introducing themselves.
    ---
    {text}
    ---
    Remember, reply only with the words the hosts will speak, nothing else!!
    """
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm

    for s in chain.stream({"text":text}):
        #print(s.content, end="", flush=True)
        print(s, end="", flush=True)
