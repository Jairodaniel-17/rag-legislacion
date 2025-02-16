from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

PROMPT_TEMPLATE = ChatPromptTemplate(
    [
        ("system", "Answer the user's question, using the context provided."),
        (
            "user",
            "User query: '{user question}' context to answer user question: '{context}'",
        ),
    ]
)


class LLMManager:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Initialize ChatOpenAI
        self.llm = ChatOpenAI(
            model_name=os.getenv("LLM_MODEL_NAME"),
            temperature=float(os.getenv("LLM_TEMPERATURE")),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the LLM
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_response_with_context(self, prompt: str, context: str) -> str:
        """
        Generate a response using the LLM with context
        """
        try:
            prompt = PROMPT_TEMPLATE.invoke(
                {"user question": prompt, "context": context}
            )
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


def test_llm_manager():
    llm_manager = LLMManager()
    while True:
        prompt = input("Enter a prompt: ")
        if prompt.lower() == "exit":
            break
        response = llm_manager.generate_response(prompt)
        print(response)
