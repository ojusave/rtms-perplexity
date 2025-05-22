import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

class PerplexitySearch:
    """
    Handles real-time information search using Perplexity's API during live meetings.
    """
    
    def __init__(self):
        """
        Initialize the Perplexity search client with API configuration.
        """
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}"
        }
        
    def search_information(self, query: str, context: str = "") -> Dict:
        """
        Search for information using Perplexity's API.
        
        Args:
            query (str): The search query
            context (str): Additional context from the meeting transcript
            
        Returns:
            Dict: Search results from Perplexity
        """
        try:
            # Construct the system message with context
            system_message = "You are a helpful assistant providing accurate, real-time information. "
            if context:
                system_message += f"Consider this context from the ongoing meeting: {context}"
            
            # Prepare the API request payload
            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            
            # Check for successful response
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error in Perplexity API call: {response.status_code}")
                return {"error": f"API call failed with status {response.status_code}"}
                
        except Exception as e:
            print(f"Error during Perplexity search: {e}")
            return {"error": str(e)}
    
    def format_search_results(self, results: Dict) -> str:
        """
        Format the search results for clear presentation in the meeting context.
        
        Args:
            results (Dict): Raw search results from Perplexity API
            
        Returns:
            str: Formatted search results
        """
        try:
            if "error" in results:
                return f"Search Error: {results['error']}"
                
            if "choices" in results and results["choices"]:
                message = results["choices"][0]["message"]["content"]
                return f"Search Results:\n{message}"
            
            return "No relevant information found."
            
        except Exception as e:
            return f"Error formatting results: {e}" 