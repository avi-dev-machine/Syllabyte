
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatGroq(model='llama-3.3-70b-versatile', api_key='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')



# Define system prompt
system_prompt = """You are a knowledgeable educational assistant.

When given a study topic, you must return:

1. A very detailed and brief mind map which covers all important things with the main_topic as the root, and sub-topic as its children.
   - Each sub-topic can have its own sub-topics.
   - minimum 30 topics as node
   - list of dictionaries

Return the entire output in the following format strictly:
[{{"id":"root", "parent":"null", "content":"main_topic"}},{{"id":"1", "parent":"root", "content":"..."}},{{"id":"2", "parent":"root", "content":"..."}},{{"id":"3", "parent":"1", "content":"..."}},{{"id":"4", "parent":"1", "content":"..."}},{{"id":"5", "parent":"2", "content":"..."}},{{"id":"6", "parent":"2", "content":"..."}},{{"id":"7", "parent":"3", "content":"..."}},]
"""

def get_general_mindmap(topic_name):
    # Create the prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('user', '{topic}')
    ])

    messages = prompt_template.format_messages(topic=topic_name)
    response = llm.invoke(messages)
    response = response.content.strip()

    response = response.replace("\\", "\\\\")
    res_temp = ''
    for line in response.split('\n'):
        line = line.strip()
        res_temp += line
    data = json.loads(res_temp)
    return data