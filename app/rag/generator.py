"""
Generator Module

Why we need this:
- The Retriever and Context Builder have gathered all the facts.
- The Generator sends the prompt to the Large Language Model (LLM) to write a human-readable answer.

Architecture & Design Decisions:
- Multi-tier LLM strategy: Anthropic → OpenRouter → Ollama → Gemini → Synthesizer
- We use the `openai` Python library for OpenRouter (industry-standard API format).
- max_tokens is set to 2500 for comprehensive reports.
- Temperature 0.2 balances factual accuracy with natural language.
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import anthropic

load_dotenv()

logger = logging.getLogger(__name__)

class Generator:
    def __init__(self, model: str = "meta-llama/llama-3.1-8b-instruct"):
        """
        Initializes the LLM connection with multi-tier fallback.
        """
        # If the code passes a local name like 'llama3.1', map it to the OpenRouter version
        if model == "llama3.1":
            self.model = "meta-llama/llama-3.1-8b-instruct"
        else:
            self.model = model
            
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        self.use_mock = False
        self.anthropic_client = None
        self.client = None
        
        # Prefer Anthropic Claude if key exists
        if self.anthropic_api_key:
            logger.info("Initialized LLM Generator with Anthropic Claude 3.5 Sonnet")
            self.model = "claude-3-5-sonnet-20241022"
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        elif self.api_key:
            logger.info(f"Initialized LLM Generator with OpenRouter model: {self.model}")
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key
            )
        else:
            logger.warning("No API keys found. Falling back to Mock Generator.")
            self.use_mock = True
            
        # Configure Gemini Fallback
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.has_gemini = False
        if self.gemini_api_key:
            try:
                self.gemini_client = genai.Client(api_key=self.gemini_api_key)
                self.has_gemini = True
                logger.info("Gemini 2.5 Flash Fallback is configured.")
            except Exception as e:
                logger.error(f"Failed to configure Gemini Fallback: {e}")
                
        # Configure Ollama (Local/Cloud)
        self.use_ollama = False
        self.ollama_api_key = os.getenv("OLLAMA_API_KEY")
        try:
            import ollama
            self.use_ollama = True
            logger.info("Ollama SDK is available.")
        except ImportError:
            logger.warning("Ollama SDK not installed.")

    def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        """
        Multi-tier LLM generation with intelligent fallback chain.
        Tier 1: Anthropic Claude / OpenRouter
        Tier 2: Ollama (glm-5.2:cloud)
        Tier 3: Gemini 2.5 Flash
        Tier 4: Mock synthesizer (last resort)
        """
        if self.use_mock:
            logger.info("No API keys configured. Attempting fallbacks...")
            return self._try_fallback_chain(system_prompt, user_prompt, json_mode)
            
        try:
            answer = ""
            if self.anthropic_client:
                logger.info(f"Sending request to Anthropic ({self.model})...")
                response = self.anthropic_client.messages.create(
                    model=self.model,
                    max_tokens=2500,
                    temperature=0.2,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                answer = response.content[0].text
            else:
                logger.info(f"Sending request to OpenRouter ({self.model})...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2500
                )
                answer = response.choices[0].message.content
            
            # Quality gate: reject obviously broken responses
            if not answer or len(answer.strip()) < 30:
                raise ValueError("Primary LLM returned an empty or trivially short response.")
                
            # Check for refusal patterns
            refusal_phrases = [
                "i do not have enough information",
                "i don't have enough information",
                "no formal description",
                "no data available",
                "i cannot provide",
                "i'm unable to"
            ]
            answer_lower = answer.lower()
            if any(phrase in answer_lower for phrase in refusal_phrases):
                raise ValueError("Primary LLM refused to answer or returned placeholder text.")
                
            return answer
            
        except Exception as e:
            logger.warning(f"Primary LLM Generation failed: {e}")
            return self._try_fallback_chain(system_prompt, user_prompt, json_mode)

    def _try_fallback_chain(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        """
        Attempts Ollama → Gemini → Mock in order.
        """
        # Tier 2: Try Ollama
        if getattr(self, 'use_ollama', False):
            logger.info("Trying Ollama (glm-5.2:cloud)...")
            try:
                import ollama
                response = ollama.chat(
                    model='glm-5.2:cloud',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt}
                    ]
                )
                if response and 'message' in response and response['message'].get('content'):
                    answer = response['message']['content']
                    if len(answer.strip()) > 30:
                        return answer
            except Exception as ollama_err:
                logger.warning(f"Ollama Fallback failed: {ollama_err}")

        # Tier 3: Try Gemini Fallback
        if getattr(self, 'has_gemini', False):
            logger.info("Trying Gemini 2.5 Flash...")
            try:
                if json_mode:
                    override_instruction = "\n\nCRITICAL: You MUST return ONLY valid JSON. No markdown, no explanations."
                else:
                    override_instruction = (
                        "\n\nCRITICAL: You MUST use your own internal world knowledge to provide a highly "
                        "accurate, comprehensive answer. Never say you don't have enough information. "
                        "Deliver a premium-quality intelligence report."
                    )
                prompt = f"{system_prompt}\n\n{user_prompt}{override_instruction}"
                gemini_response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                if gemini_response.text and len(gemini_response.text.strip()) > 30:
                    return gemini_response.text
            except Exception as gemini_err:
                logger.warning(f"Gemini Fallback failed: {gemini_err}")
        
        # Tier 4: Last resort - return a clear error instead of fake data
        logger.error("ALL LLM tiers failed. Returning error message.")
        return (
            "**Analysis temporarily unavailable.** All AI engines encountered errors. "
            "Please verify your API keys in the .env file and try again. "
            "Required: OPENAI_API_KEY (OpenRouter) or GEMINI_API_KEY or Ollama running locally."
        )
