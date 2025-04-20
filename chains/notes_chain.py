from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="groq_key.env")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def generate_notes(topic):
    prompt = PromptTemplate.from_template("""Generate clear and detailed study notes on: {topic}. 
Format the response in the following way:

1. Start with a brief introduction in a paragraph
2. Then list key points, with each point:
   - Starting with '• ' (bullet point)
   - Main point text wrapped in **bold**
   - Additional details on new lines indented with spaces
   - End each point with two newlines

3. Use markdown formatting:
   - **bold** for important terms
   - Use proper line breaks between sections
   - Create clear visual hierarchy

Please ensure points are clear, concise, and well-separated.""")
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content