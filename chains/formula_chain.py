from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="groq_key.env")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def generate_formulas(topic):
    prompt = PromptTemplate.from_template("""List all key formulas related to {topic}.
Format each formula using LaTeX/MathJax syntax and markdown. Use this exact format:

## {topic}

### Formula 1:
$$formula$$

**Description:** Brief explanation of the formula

### Formula 2:
$$formula$$

**Description:** Brief explanation of the formula

Make sure to:
- Use ### for formula headings
- Put each formula on its own line between $$
- Use **Description:** for explanations
- Add blank lines between sections
""")
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content