import os
from typing import List, Tuple, Optional, Dict, Any
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import asyncio
import platform

class LLMHandler:
    """
    A handler class for different LLM providers with a unified interface.
    Supports Gemini and Groq models.
    """
    
    SUPPORTED_PROVIDERS = {
        "gemini": {
            "class": ChatGoogleGenerativeAI,
            "env_key": "GOOGLE_API_KEY",
            "default_model": "gemini-2.0-flash-lite"
        },
        "groq": {
            "class": ChatGroq,
            "env_key": "GROQ_API_KEY",
            "default_model": "meta-llama/llama-4-scout-17b-16e-instruct"
        }
    }

    @staticmethod
    def _format_messages(chat_history: List[Tuple[str, str]], question: str) -> List:
        """Format messages with chat history for LLM input."""
        system_prompt = f"""### DeepShell AI – Your Terminal Copilot

You are **DeepShell AI**, a powerful terminal copilot designed to assist with command-line tasks on **{platform.system()} {platform.release()}** in a **{os.environ.get('SHELL', 'bash')}** environment.

- Always respond in a **concise and direct manner**.
- Address the user as "Sir"  when appropriate.
- If a terminal command needs to be executed, wrap it in triple backticks using the `run` syntax:
  
  ```run
  <command>
  ```
  

- **Handle Ambiguity**: If the user provides an ambiguous or incomplete command (e.g., "list dir"), interpret it based on common CLI patterns. For example:


- **Provide Contextual Help**: If the user is unsure or asks for help, offer concise explanations or suggestions without being verbose.

- **Dynamic Responses**: Use your understanding of common CLI patterns to interpret commands like "list dir" as `ls -la` or similar.

Examples:

User: "list dir"
Response:List files in the current directory.
```run
ls -la
```"""

        messages = [
            SystemMessage(content=system_prompt)
        ]
        # Add chat history
        for human_msg, ai_msg in chat_history:
            messages.append(HumanMessage(content=human_msg))
            messages.append(AIMessage(content=ai_msg))
        
        # Add current question
        messages.append(HumanMessage(content=question))
        return messages

    @staticmethod
    def _validate_provider(provider: str) -> None:
        """Validate if the provider is supported."""
        if provider.lower() not in LLMHandler.SUPPORTED_PROVIDERS:
            raise ValueError(f"Provider '{provider}' not supported. Supported providers: {list(LLMHandler.SUPPORTED_PROVIDERS.keys())}")

    @staticmethod
    def _check_api_key(provider: str) -> None:
        """Check if required API key is set."""
        env_key = LLMHandler.SUPPORTED_PROVIDERS[provider]["env_key"]
        if env_key not in os.environ:
            raise ValueError(f"Please set {env_key} environment variable for {provider}")

async def deepshellai(
    provider: str,
    model_name: Optional[str] = None,
    chat_history: Optional[List[Tuple[str, str]]] = None,
    question: str = ""
) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Process a question using the specified LLM provider and model.
    
    Args:
        provider (str): The LLM provider ("gemini" or "groq")
        model_name (str, optional): The specific model to use. If None, uses provider's default
        chat_history (List[Tuple[str, str]], optional): List of (human_message, ai_message) tuples
        question (str): The question to ask the LLM
    
    Returns:
        Tuple[str, List[Tuple[str, str]]]: (response, updated_chat_history)
    """
    # Initialize chat history if None
    chat_history = chat_history or []
    
    # Validate inputs
    provider = provider.lower()
    LLMHandler._validate_provider(provider)
    LLMHandler._check_api_key(provider)
    
    # Get provider configuration
    provider_config = LLMHandler.SUPPORTED_PROVIDERS[provider]
    model_class = provider_config["class"]
    
    # Use default model if none specified
    if not model_name:
        model_name = provider_config["default_model"]
    
    # Initialize the model
    llm = model_class(
        model=model_name,
        temperature=0.7,
        max_retries=2
    )
    
    try:
        # Format messages and get response
        messages = LLMHandler._format_messages(chat_history, question)
        response = await llm.ainvoke(messages)
        
        # Update chat history
        chat_history.append((question, response.content))
        
        return response.content, chat_history
    
    except Exception as e:
        raise Exception(f"Error processing request with {provider}: {str(e)}")

# Example usage
async def main():
    # Example chat history
    chat_history = [
        ("Who was Albert Einstein?", "Albert Einstein was a renowned physicist..."),
    ]
    
    try:
        # Test with Gemini
        print("\n=== Testing Gemini ===")
        response, history = await deepshellai(
            provider="gemini",
            chat_history=chat_history,
            question="What did I ask you before?"
        )
        print(f"Response: {response}")
        
        # Test with Groq
        print("\n=== Testing Groq ===")
        response, history = await deepshellai(
            provider="groq",
            chat_history=chat_history,
            question="What did I ask you before?"
        )
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 