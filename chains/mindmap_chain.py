from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="groq_key.env")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def generate_mindmap(topic):
    prompt = PromptTemplate.from_template("""Create a hierarchical mindmap for {topic}.
Use exactly this format with proper indentation (use 2 spaces for each level):
{topic}
  Key Point 1
    Subpoint 1.1
    Subpoint 1.2
  Key Point 2
    Subpoint 2.1
      Detail 2.1.1
    Subpoint 2.2
  Key Point 3
    Subpoint 3.1
    Subpoint 3.2

Make sure to:
- Use the topic as the root node
- Use consistent 2-space indentation
- Keep points concise
- Include 3-5 main points
- Add relevant subpoints
""")
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content