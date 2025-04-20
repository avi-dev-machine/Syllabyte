from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path="groq_key.env")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def generate_mcqs(topic):
    prompt = PromptTemplate.from_template("""Generate 5 multiple choice questions for {topic}.
Each question should have:
- A clear question
- 4 options (A, B, C, D)
- The correct answer marked

Format exactly as a JSON array:
[
    {{
        "question": "Question text here",
        "options": {{
            "A": "Option A text",
            "B": "Option B text",
            "C": "Option C text",
            "D": "Option D text"
        }},
        "correct": "A"
    }}
]

Make questions challenging but clear. Include both conceptual and calculation-based questions if applicable.""")
    
    try:
        chain = prompt | llm
        response = chain.invoke({"topic": topic}).content
        # Clean up any potential formatting issues
        response = response.strip()
        if not response.startswith('['):
            # Find the first '[' and remove anything before it
            response = response[response.find('['):]
        if not response.endswith(']'):
            # Find the last ']' and remove anything after it
            response = response[:response.rfind(']')+1]
        
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response}")
        raise Exception("Failed to generate valid MCQ format")
    except Exception as e:
        print(f"Error generating MCQs: {e}")
        raise