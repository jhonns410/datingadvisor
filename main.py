from flask import Flask, render_template, request,jsonify

app = Flask(__name__)

# Imports
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools, initialize_agent, AgentType
import os
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "752c3239732bda98710306c7dcaa7c29dac6251287cc91f7b1aa712bd8f34880"


# First, let's load the language model we're going to use to control the agent.
chat = ChatOpenAI(temperature=0.9)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
llm = ChatOpenAI(temperature=0.9)
tools = load_tools(["serpapi", "llm-math"], llm=llm)


# Set up the conversation structure using the ChatPromptTemplate.
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("As a dating advisor, offer insights and guidance to individuals struggling with dating, helping them understand their goals, improve communication, and expand their social circles to increase their chances of finding a fulfilling connection."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Create the ConversationChain with the memory, prompt, and language model.
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        user_input = request.json['message']
        
        if user_input.lower() == "q":
            response = "Goodbye!"
        else:
            response = conversation.predict(input=user_input)
            response = response # Join the response points with double newlines
        
        return jsonify(response=response)
    
    return render_template('index.html')

# Rest of your code...

if __name__ == '__main__':
    app.run()