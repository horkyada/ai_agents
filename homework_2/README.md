# Homework 2 - AI Agent with Database Tools

N8N AI Agent workflow that can dynamically query databases and use tools to respond to user queries.

## Assignment Requirements

The assignment asks for an N8N agent that:
- ✅ Works with a database
- ✅ Uses tools
- ✅ Responds to queries via LLM

## What This Workflow Does

1. **Chat Trigger** - Provides a chat interface for user queries
2. **AI Agent** - Intelligently processes user requests and decides which tools to use
3. **MongoDB Tool** - Dynamically queries the product database based on agent decisions
4. **Ollama Model** - Powers the AI Agent with local Llama 3.2 3B model
5. **Interactive Response** - Agent can query database multiple times and provide detailed analysis

## How to Run

### Prerequisites

1. **Docker & Docker Compose**
   - Install Docker Desktop
   - Docker Compose (included with Docker Desktop)

2. **Ollama with GPT-OSS Model**
   - Ollama will run automatically in Docker with the stack
   - **Optional**: Mount local Ollama models to avoid re-downloading

### Setup Steps (Docker)

1. **Start Services**
   ```bash
   # Navigate to homework_2 directory
   cd homework_2

   # Start MongoDB and N8N containers
   docker-compose up -d
   ```

2. **Access N8N Interface**
   - Open browser: http://localhost:5678
   - N8N will start automatically (no authentication required)

3. **Configure Environment (Optional)**
   ```bash
   # Copy example environment file
   cp .env.example .env

   # Edit .env and set your N8N API key if needed
   # N8N_API_KEY=your_api_key_here
   ```

4. **Deploy Workflows (Automatic)**
   ```bash
   # Install dependencies with uv
   uv sync

   # Deploy all workflows from ./workflows folder
   uv run python deploy.py

   # Or clean deploy (removes existing workflows first)
   uv run python deploy.py --clean
   ```

   **Alternative: Manual Import**
   - In N8N interface: Workflows → Import
   - Upload `workflows/homework_2_workflow.json`
   - Workflow will be imported with all nodes

5. **Configure MongoDB Credentials**
   - Click on MongoDB node
   - Create new credential with ID: `mongodb-account`
   - Name: `MongoDB account`
   - **Connection String**: `mongodb://admin:password123@homework2-mongodb:27017/homework2?authSource=admin`
   - **Database**: `homework2`

   Note: The connection uses `homework2-mongodb` (Docker container name) instead of `localhost`

6. **Configure Ollama Credentials**
   - Click on Ollama GPT-OSS Model node
   - Add new credential:
     - **Host**: `http://homework2-ollama:11434`
   - The model will be automatically pulled when Ollama container starts

7. **Verify Database Data**
   - MongoDB starts with sample products automatically
   - Data includes 5 sample products in different categories

### Running the AI Agent

1. **Activate Workflow**
   - Toggle the workflow to "Active" state

2. **Open Chat Interface**
   - Click on the Chat Trigger node
   - Open the webhook URL provided
   - Start chatting with the AI Agent

3. **Example Queries**
   - "What products do you have in the database?"
   - "Show me all electronics products"
   - "How many products are in each category?"
   - "Find products under $200"

## Expected Output

The AI Agent can:
1. **Dynamically query** the MongoDB database based on your questions
2. **Use tools intelligently** to find specific information
3. **Provide analysis** such as:
   ```
   I found 5 products in the database:
   - 2 electronics items (headphones, laptop)
   - 1 computer (gaming laptop)
   - 1 smart home device (security camera)
   - 1 wearable (fitness tracker)

   The products range from $99.99 to $1299.99, covering various tech categories.
   ```
4. **Interactive conversation** - you can ask follow-up questions

## File Structure

```
homework_2/
├── README.md                    # This file
├── pyproject.toml              # UV project configuration
├── deploy.py                   # Automatic workflow deployment script
├── docker-compose.yml          # Docker services configuration
├── init-db.js                  # MongoDB sample data setup
└── workflows/                  # Workflows folder
    └── homework_2_workflow.json # N8N workflow for submission
```

## Cleanup

When finished testing:

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (optional - removes all data)
docker-compose down -v
```

## Using Local Ollama Models (Optional)

If you already have Ollama models downloaded locally, you can mount them to avoid re-downloading:

1. **Find your local Ollama directory:**
   ```bash
   # macOS/Linux default location
   ls ~/.ollama/models

   # Check if gpt-oss:20b model exists
   ls ~/.ollama/models/manifests/registry.ollama.ai/library/gpt-oss/
   ```

2. **Edit docker-compose.yml:**
   ```yaml
   volumes:
     # Comment out the Docker volume line:
     # - ollama_data:/root/.ollama
     # Add your local Ollama directory:
     - ~/.ollama:/root/.ollama
   ```

3. **Restart containers:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

Your local models will be immediately available in the Docker container!

## Troubleshooting

**N8N not starting**: Wait 30-60 seconds after `docker-compose up -d`
**MongoDB connection failed**: Use the exact connection string from step 5
**Workflow import failed**: Ensure you're using the provided JSON file
**Ollama models not found**: Check if you have the correct models locally or let Docker download them

## Submission

Submit the `workflows/homework_2_workflow.json` file as requested in the assignment.

## Quick Start Summary

For the impatient:

```bash
# 1. Start services
docker-compose up -d

# 2. Deploy workflows
uv sync && uv run python deploy.py

# 3. Open http://localhost:5678 and configure credentials
# 4. Run the workflow!
```