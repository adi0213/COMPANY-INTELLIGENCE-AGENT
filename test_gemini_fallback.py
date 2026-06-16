import asyncio
import logging
from app.rag.generator import Generator

logging.basicConfig(level=logging.INFO)

async def test():
    # Force an invalid model to trigger OpenRouter failure
    gen = Generator(model="invalid-model-that-will-fail-1234")
    
    print("\n--- Testing Gemini Fallback ---")
    system = "You are a helpful assistant."
    user = "Here is the retrieved context regarding the company:\n\nNo relevant context found.\n\nQuestion: What does Google do?\n\nAnswer the question based ONLY on the context above."
    
    # We pass a prompt that has "No relevant context found."
    # The normal LLM might say "I do not have enough information", which triggers tier 2.
    # But since the model name is invalid, Tier 1 will throw an exception and trigger Tier 2 directly.
    
    res = gen.generate(system, user)
    print("\nRESULT:")
    print(res)

if __name__ == "__main__":
    asyncio.run(test())
