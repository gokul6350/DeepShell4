import os
from typing import List, Tuple
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate

class ChatManager:
    def __init__(self):
        # Initialize models
        self.gemini_model = self._setup_gemini()
        self.groq_model = self._setup_groq()
        self.chat_history: List[Tuple[str, str]] = []
        
    def _setup_gemini(self) -> ChatGoogleGenerativeAI:
        """Setup Google Gemini model"""
        if "GOOGLE_API_KEY" not in os.environ:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            temperature=0.7,
            max_retries=2
        )
    
    def _setup_groq(self) -> ChatGroq:
        """Setup Groq model"""
        if "GROQ_API_KEY" not in os.environ:
            raise ValueError("Please set GROQ_API_KEY environment variable")
        
        return ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # You can change this to other available models
            temperature=0.7,
            max_retries=2
        )
    
    def _format_messages(self, system_prompt: str) -> List:
        """Format messages with chat history"""
        messages = [
            SystemMessage(content=system_prompt)
        ]
        
        # Add chat history
        for human_msg, ai_msg in self.chat_history:
            messages.append(HumanMessage(content=human_msg))
            messages.append(AIMessage(content=ai_msg))
            
        return messages
    
    async def chat_with_gemini(self, user_input: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
        """Chat with Gemini model"""
        messages = self._format_messages(system_prompt)
        messages.append(HumanMessage(content=user_input))
        
        response = await self.gemini_model.ainvoke(messages)
        self.chat_history.append((user_input, response.content))
        return response.content
    
    async def chat_with_groq(self, user_input: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
        """Chat with Groq model"""
        messages = self._format_messages(system_prompt)
        messages.append(HumanMessage(content=user_input))
        
        response = await self.groq_model.ainvoke(messages)
        self.chat_history.append((user_input, response.content))
        return response.content
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []

# Example usage
async def main():
    chat_manager = ChatManager()
    
    try:
        print("\n=== Testing Gemini Model ===")
        # First question with Gemini
        response = await chat_manager.chat_with_gemini(
            "Who was Albert Einstein?",
            "You are a knowledgeable science historian."
        )
        print("\nFirst Question: Who was Albert Einstein?")
        print("Gemini Response:", response)
        
        # Follow-up question to test memory
        response = await chat_manager.chat_with_gemini(
            "What did I ask you before?",
            "You are a knowledgeable science historian."
        )
        print("\nFollow-up Question: What did I ask you before?")
        print("Gemini Response:", response)
        
        print("\n=== Testing Groq Model ===")
        # Clear history before testing Groq
        chat_manager.clear_history()
        
        # First question with Groq
        response = await chat_manager.chat_with_groq(
            "What is quantum mechanics?",
            "You are a knowledgeable physics expert."
        )
        print("\nFirst Question: What is quantum mechanics?")
        print("Groq Response:", response)
        
        # Follow-up question to test memory
        response = await chat_manager.chat_with_groq(
            "What did I ask you before?",
            "You are a knowledgeable physics expert."
        )
        print("\nFollow-up Question: What did I ask you before?")
        print("Groq Response:", response)
        
        # Display full chat history
        print("\n=== Full Chat History ===")
        for i, (human_msg, ai_msg) in enumerate(chat_manager.chat_history, 1):
            print(f"\nExchange {i}:")
            print(f"Human: {human_msg}")
            print(f"AI: {ai_msg}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
