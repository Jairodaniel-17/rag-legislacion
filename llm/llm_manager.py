import os
from typing import Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rich.console import Console

console = Console()

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
    """LLM Manager class to generate responses using the LLM model."""

    def __init__(self):
        """LLM Manager class to generate responses using the LLM model."""
        load_dotenv()

        # Initialize ChatOpenAI
        self.llm = ChatOpenAI(
            model_name=os.getenv("LLM_MODEL_NAME"),
            temperature=float(os.getenv("LLM_TEMPERATURE")),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )

    def generate_response(self, prompt: str) -> str:
        """Generate a response using the LLM."""
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_response_with_context(self, prompt: str, context: str) -> str:
        """Generate a response using the LLM with context."""
        try:
            prompt = PROMPT_TEMPLATE.invoke({"user question": prompt, "context": context})
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def stream_generate_response_with_context(
        self, prompt: str, context: str
    ) -> Optional[None | str]:
        """Generate a response using the LLM with context and stream the response."""
        try:
            prompt = PROMPT_TEMPLATE.invoke({"user question": prompt, "context": context})
            self.llm = ChatOpenAI(
                model_name=os.getenv("LLM_MODEL_NAME"),
                temperature=float(os.getenv("LLM_TEMPERATURE")),
                api_key=os.getenv("LLM_API_KEY"),
                base_url=os.getenv("LLM_BASE_URL"),
                streaming=True,
            )
            for chunk in self.llm.stream(prompt):
                console.print(chunk.content, end="", style="bold green", justify="full")
            console.print("\n")
        except Exception as e:
            return f"Error generating response: {str(e)}"


def test_llm_manager():
    """Test the LLMManager class."""
    llm_manager = LLMManager()
    while True:
        prompt = input("Enter a prompt: ")
        if prompt.lower() == "exit":
            break
        response = llm_manager.generate_response(prompt)
        print(response)
