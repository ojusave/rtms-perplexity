# External Dependencies
from langchain_anthropic import ChatAnthropic  # Claude 3 integration
from langchain.prompts import ChatPromptTemplate  # For structuring prompts
from collections import deque  # For maintaining a fixed-size transcript history
import os
from dotenv import load_dotenv
from perplexity_search import PerplexitySearch  # Import our new search module

# Load API key from environment
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize LangChain components using LCEL (LangChain Expression Language)
# Claude 3 Sonnet is used with temperature=0 for consistent, deterministic outputs
llm = ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=0)

# Define the prompt template for action item extraction and information needs
prompt = ChatPromptTemplate.from_template("""
Analyze the following meeting transcript snippet for:
1. Action items: Extract explicit or implicit action items, including tasks that need to be done
2. Information needs: ONLY identify explicit requests for information or research. Do NOT include tasks or action items as information needs.
   Example of information need: "What was the user growth last quarter?"
   NOT an information need: "I need to report the outage" (this is a task)

Transcript:
{transcript_chunk}

Please provide your analysis in this format:
Action Items:
- [List items here]

Information Needs:
- [List ONLY explicit information requests here, not tasks]
""")

# Create a processing chain using LCEL pipe operator
analysis_chain = prompt | llm

class TranscriptProcessor:
    """
    Processes real-time meeting transcripts to extract action items and handle information searches.
    """
    
    def __init__(self):
        """
        Initialize the processor with:
        - recent_chunks: Rolling window of last 10 transcript segments
        - action_items: List of unique action items found so far
        - search_client: Perplexity search client for real-time information
        """
        self.recent_chunks = deque(maxlen=10)
        self.action_items = []
        self.search_client = PerplexitySearch()

    def analyze_transcript(self, transcript_chunk: str) -> dict:
        """
        Process a transcript chunk through Claude to identify action items and information needs.
        
        Args:
            transcript_chunk (str): Text segment from the meeting transcript
            
        Returns:
            dict: Contains extracted action items and search queries
        """
        try:
            result = analysis_chain.invoke({"transcript_chunk": transcript_chunk})
            content = result.content
            
            # Parse the response into sections
            sections = content.split("\n\n")
            action_items = []
            info_needs = []
            
            for section in sections:
                if section.startswith("Action Items:"):
                    action_items = [item.strip("- ") for item in section.split("\n")[1:] if item.strip()]
                elif section.startswith("Information Needs:"):
                    info_needs = [item.strip("- ") for item in section.split("\n")[1:] if item.strip()]
            
            return {
                "action_items": action_items,
                "info_needs": info_needs
            }
        except Exception as e:
            print(f"Error analyzing transcript: {e}")
            return {"action_items": [], "info_needs": []}

    def process_new_transcript_chunk(self, chunk: str):
        """
        Handle incoming transcript chunks in real-time.
        
        This method:
        1. Logs the new chunk
        2. Adds it to the rolling context window
        3. Processes the merged recent context
        4. Identifies action items and information needs
        5. Performs real-time searches when needed
        
        Args:
            chunk (str): New transcript segment from the Zoom RTMS
        """
        print("New Transcript Chunk Received:\n", chunk.strip())
        
        # Add new chunk to rolling context window
        self.recent_chunks.append(chunk)
        merged_text = " ".join(self.recent_chunks)
        
        try:
            # Analyze the transcript for both action items and information needs
            analysis = self.analyze_transcript(merged_text)
            
            # Process action items
            for item in analysis["action_items"]:
                if item not in self.action_items:
                    self.action_items.append(item)
                    print("New Action Item:", item)
            
            # Handle information needs with real-time search
            if analysis["info_needs"]:  # Only search if there are actual information needs
                for query in analysis["info_needs"]:
                    print(f"\nSearching for information: {query}")
                    search_results = self.search_client.search_information(
                        query=query,
                        context=chunk  # Pass current chunk as context
                    )
                    formatted_results = self.search_client.format_search_results(search_results)
                    print(formatted_results)
                
        except Exception as e:
            print("Processing error:", e) 