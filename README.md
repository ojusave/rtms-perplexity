# Real-Time Meeting Transcript Processor with Perplexity Search

This application demonstrates real-time processing of Zoom meeting transcripts using RTMS (Real-Time Media Streaming) service, integrated with Claude 3 Sonnet for action item extraction and Perplexity API for real-time information search.

## Features

- 🎯 Real-time transcript processing and analysis using Claude 3 Sonnet
- 📋 Automatic action item extraction from meeting conversations
- 🔍 Real-time information search using Perplexity API
- 🧠 Context-aware processing with rolling conversation history
- 🔄 Intelligent deduplication of action items
- 💪 Robust WebSocket connection handling

## Prerequisites

- Python 3.7 or higher
- Zoom account with RTMS enabled
- Zoom App credentials (Client ID and Client Secret)
- Zoom Secret Token for webhook validation
- Anthropic API key for Claude 3 Sonnet access
- Perplexity API key for real-time information search

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ojusave/rtms-perplexity.git
cd rtms-perplexity
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```env
ZOOM_SECRET_TOKEN=your_secret_token
ZM_CLIENT_ID=your_client_id
ZM_CLIENT_SECRET=your_client_secret
ANTHROPIC_API_KEY=your_anthropic_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
```

## Usage

1. Start the server:
```bash
python print_transcripts.py
```

2. Expose the local server (running on port 3000) using ngrok:
```bash
ngrok http 3000
```

3. Configure your Zoom App:
   - Go to the Zoom App Marketplace
   - Navigate to your app's settings
   - Set the webhook URL to your ngrok URL (e.g., `https://your-ngrok-url/webhook`)

4. Start a Zoom meeting with RTMS enabled to begin processing:
   - The server will receive and process incoming transcripts
   - Claude 3 Sonnet will analyze conversations for action items
   - Perplexity API will handle real-time information searches
   - Both transcripts and extracted information will be displayed in the console

## Architecture

The application consists of three main components:

### 1. Zoom RTMS Handler (`print_transcripts.py`)
- Manages webhook events from Zoom
- Handles WebSocket connections to Zoom's servers
- Processes real-time transcript data
- Routes transcript chunks to the LangChain processor

### 2. LangChain Processor (`langchain_processor.py`)
- Processes incoming transcript chunks
- Uses Claude 3 Sonnet (via LangChain) for conversation analysis
- Extracts action items and information needs
- Maintains a rolling window of recent transcript chunks
- Coordinates with Perplexity search for information needs

### 3. Perplexity Search (`perplexity_search.py`)
- Handles real-time information searches
- Integrates with Perplexity's API
- Provides context-aware search results
- Formats search results for meeting context

## Dependencies

```
fastapi==0.68.1
uvicorn==0.15.0
websockets==10.1
python-dotenv==0.19.0
```

## Best Practices

- Keep the `.env` file secure and never commit it to version control
- Monitor WebSocket connections for stability
- Consider implementing persistent storage for action items in production
- Regularly validate and update API credentials
- Test the system with various meeting scenarios and search queries

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024 Ojus Ave

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support

For questions or issues, please open an issue in the repository.

## Getting API Keys

### Perplexity API
1. Visit [Sonar by Perplexity](https://sonar.perplexity.ai/)
2. Click "Get Started" to create an account
3. Navigate to the API section in your dashboard
4. Generate a new API key
5. Copy the API key and add it to your `.env` file as `PERPLEXITY_API_KEY`

### Anthropic Claude API
1. Visit [Anthropic](https://www.anthropic.com/)
2. Sign up for an account and request API access
3. Once approved, generate an API key from your dashboard
4. Add the key to your `.env` file as `ANTHROPIC_API_KEY`

## LangChain Integration

This project uses LangChain for orchestrating the conversation analysis pipeline. Here's how it works:

### Key Components

1. **Conversation Chain**
   - Uses Claude 3 Sonnet as the base LLM
   - Implements memory using `ConversationBufferWindowMemory`
   - Maintains a rolling window of recent conversations

2. **Custom Prompts**
   ```python
   from langchain.prompts import PromptTemplate
   
   ACTION_ITEM_TEMPLATE = """
   Analyze the following meeting transcript and extract action items:
   {transcript}
   
   Extract action items in the following format:
   - [Assignee] Task description (Due date if mentioned)
   """
   ```

3. **Memory Management**
   ```python
   from langchain.memory import ConversationBufferWindowMemory
   
   memory = ConversationBufferWindowMemory(
       k=5,  # Keep last 5 interactions
       return_messages=True
   )
   ```

4. **Chain Configuration**
   ```python
   from langchain.chains import ConversationChain
   
   chain = ConversationChain(
       llm=claude,
       memory=memory,
       prompt=action_item_prompt
   )
   ```

### Usage Example

```python
# Process a transcript chunk
response = chain.run(transcript_chunk)

# Extract action items
action_items = response.split('\n')
```

For more details on LangChain integration, see `langchain_processor.py`. 