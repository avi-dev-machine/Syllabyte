from llama_index.llms.groq import Groq
from llama_index.core.llms import ChatMessage
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="groq_key.env")

llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

system_prompt =  """You are a knowledgeable educational assistant.

When given a study topic, you must return:

1. A very detailed and brief mind map which covers all important things with the main_topic as the root, and sub-topic as its children.
   - Each sub-topic can have its own sub-topics.
   - important formulas
   - list of dictionaries

2. Detailed Flashcards in a list, where each flashcard is a dictionary with:
   - "front": important key-words or topics.
   - "back": the answer side of the flashcard , formulas.
   - list of dictionaries

must Use MathJax format strictly for any equations and formulas but in place of "\\" use "\\\\" and don't use '$....$'. For example, "\\\\( <equation> \\\\)".

Return the entire output in the following format strictly:
plaintext
  mind_map = [
    {"id":"root", "parent":"null", "content":"main_topic"},
    {"id":"1", "parent":"root", "content":"..."},
    {"id":"2", "parent":"root", "content":"..."},
    ...
  ]

  flashcard = [
    {"front":"key-word", "back":"answer"},
    ...
  ]
just Only return mind_map and flashcards in plaintext format in the response.
"""

def generate_study_material(topic):
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=f"Topic: {topic}")
    ]
    resp = llm.chat(messages)

    try:
        s = resp.message.blocks[0].text
        start = s.find('</think>\n\n')
        if start != -1:
            s = s[start+len('</think>\n\n'):]
        else:
            # Fallback if '</think>' tag is not found
            pass

        s = s.replace('plaintext', '')

        m = s.find('mind_map =')
        f = s.find('flashcard =')

        m_str = s[m + len('mind_map = '):f].strip()
        f_str = s[f + len('flashcard = '):].strip()

        # Optional: Try skipping the double escaping unless needed
        # m_str = m_str.replace('\\','\\\\')
        # f_str = f_str.replace('\\','\\\\')

        # Collapse into single line to help JSON parsing
        m_temp = ''.join(line.strip() for line in m_str.split('\n'))
        f_temp = ''.join(line.strip() for line in f_str.split('\n'))

        mind_map = json.loads(m_temp)
        flashcard = json.loads(f_temp)

        return mind_map, flashcard

    except Exception as e:
        print(f"Error while parsing LLM output: {e}")
        raise e
# Example usage
# mind_map, flashcard = generate_study_material("Python")
# print(mind_map)
# print(flashcard)