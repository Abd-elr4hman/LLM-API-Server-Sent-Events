from langchain_community.chat_models import ChatOpenAI

from langchain_core.prompts import PromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('API_KEY')

def get_chain():
    """Constructs and return a chain"""

    # llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0)
    llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            model_name = "gpt-4-turbo-preview"
        )

    # Notice that "chat_history" is present in the prompt template
    template = """
    You are a helpfull assistant
    human question: {input}
    Response:"""
    prompt = PromptTemplate.from_template(template)


    chain = (
        prompt |
        llm
    )

    return chain
