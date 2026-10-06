# Sample Projects

Four complete, runnable projects built on the Claude API. Each has a CLI, sample data, a README with an architecture diagram, and an **offline test suite that uses a fake client**, so you can run the tests and most demos without an API key or any cost.

| # | Project | Run offline | Tests |
|---|---------|-------------|-------|
| 1 | [Customer Support Bot](./1_customer_support_bot/) | `python main.py --dry-run` | 26 |
| 2 | [Document Q&A (RAG)](./2_document_qa_system/) | `python main.py search "refund"` (retrieval only) | 27 |
| 3 | [Code Review Agent](./3_code_review_agent/) | `python main.py --diff examples/sample.diff --dry-run` | 64 |
| 4 | [Research Assistant](./4_research_assistant/) | `python main.py --offline-demo "your question"` | 31 |

Quick start for any project:
```bash
cd projects/<project>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q                      # offline
cp .env.example .env           # add ANTHROPIC_API_KEY for live runs
python main.py --help
```

> **Honest status:** the code was verified against the installed SDK's signatures and the official docs, and tested with fake clients, but it was **not run against the live API**. Expect to adjust small details (model behaviour, tool versions, cache thresholds) on first live run. Each README lists what is unverified. Project 5 below is still planned.

## 🚀 Available Projects

### 1. [Customer Support Chatbot](./1_customer_support_bot/)
**Level**: Intermediate | **Time**: 3-4 hours

A customer support chatbot with:
- Streaming responses for real-time interaction
- Conversation history and context management
- Tool use for accessing knowledge base
- Ticket creation integration
- Multi-language support

**Technologies**: Claude API, Streaming, Tool Use, File Storage

**Key Features**:
- Natural conversation flow
- Context-aware responses
- Escalation to human agents
- Analytics and logging

---

### 2. [Document Q&A System](./2_document_qa_system/)
**Level**: Advanced | **Time**: 4-6 hours

RAG-based system for answering questions about documents:
- PDF and text document processing
- Vector database for semantic search
- Prompt caching for efficiency
- Multi-document support

**Technologies**: Claude API, RAG, Vector DB, Prompt Caching

**Key Features**:
- Upload multiple documents
- Semantic search
- Citation of sources
- Cost-optimized with caching

---

### 3. [Code Review Agent](./3_code_review_agent/)
**Level**: Advanced | **Time**: 4-5 hours

Autonomous agent for reviewing code:
- GitHub integration
- Multi-file analysis
- Automated suggestions
- Best practices checking

**Technologies**: Claude API, Tool Use, GitHub API, Async

**Key Features**:
- Pull request analysis
- Inline code comments
- Security vulnerability detection
- Performance suggestions

---

### 4. [Research Assistant](./4_research_assistant/)
**Level**: Advanced | **Time**: 5-6 hours

Multi-agent system for research tasks:
- Web search integration
- Information synthesis
- Report generation
- Source tracking

**Technologies**: Claude API, Multi-Agent, Web APIs, Tool Use

**Key Features**:
- Autonomous research
- Multiple information sources
- Structured reports
- Fact checking

---

### 5. MCP Weather Server (planned, not yet included)
**Level**: Intermediate | **Time**: 2-3 hours

Custom MCP server for weather information:
- REST API integration
- Multiple data sources
- Claude Desktop integration
- Error handling

**Technologies**: MCP, Claude API, REST APIs

**Key Features**:
- Real-time weather data
- Forecast information
- Location search
- Historical data

---

## 📋 Project Structure

The skeletons currently contain `README.md`, `requirements.txt` and `main.py`. A finished project would grow into this structure:

```
project_name/
├── README.md              # Project overview and setup
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── src/                  # Source code
│   ├── main.py          # Entry point
│   ├── config.py        # Configuration
│   └── ...              # Other modules
├── tests/               # Test files
│   └── test_*.py
├── docs/                # Additional documentation
│   ├── architecture.md
│   └── api.md
└── examples/            # Usage examples
    └── example_*.py
```

## 🎯 How to Use Projects

### Step 1: Choose a Project
Select a project that matches your:
- Skill level
- Available time
- Learning goals
- Interest area

### Step 2: Set Up Environment
```bash
cd project_name
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Step 3: Configure
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

### Step 4: Run the Project
```bash
python main.py   # or python src/main.py once you adopt the structure above
```

### Step 5: Study and Modify
- Read through the code
- Understand the architecture
- Make modifications
- Add new features

## 🎓 Learning Path

### For Beginners
1. Start with simpler modules from exercises
2. Study project code thoroughly
3. Make small modifications
4. Build your own version

### For Intermediate Developers
1. Start with Customer Support Bot or MCP Weather
2. Implement all features
3. Add extensions
4. Deploy to production

### For Advanced Developers
1. Tackle Code Review Agent or Research Assistant
2. Optimize for production
3. Add advanced features
4. Contribute improvements

## 💡 Project Ideas

Want to build your own project? Here are some ideas:

### Beginner Projects
- [ ] Personal journal with AI summaries
- [ ] Language learning chatbot
- [ ] Recipe generator and meal planner
- [ ] Daily news summarizer
- [ ] Flashcard study assistant

### Intermediate Projects
- [ ] Email auto-responder
- [ ] Social media content generator
- [ ] Meeting notes analyzer
- [ ] Technical documentation writer
- [ ] SQL query generator

### Advanced Projects
- [ ] Multi-agent game master for RPGs
- [ ] Automated testing suite generator
- [ ] Legal document analyzer
- [ ] Financial report generator
- [ ] Personal AI tutor with curriculum

## 🛠️ Common Patterns

### Pattern 1: Conversational Application
```python
import anthropic

# Initialize conversation
conversation = []
client = anthropic.Anthropic()

# Loop
while True:
    user_input = get_user_input()
    conversation.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=conversation
    )

    conversation.append({"role": "assistant", "content": response.content[0].text})
```

### Pattern 2: Tool-Based Agent
```python
# Define tools
tools = [define_tool_1(), define_tool_2()]

# Agent loop
while not done:
    response = client.messages.create(model="claude-sonnet-5-5", max_tokens=1024,
                                      tools=tools, messages=messages)

    if response.stop_reason == "tool_use":
        # Execute each tool_use block, append the assistant turn and a
        # user turn containing tool_result blocks, then loop again
        result = execute_tool(...)
    else:
        done = True
```

### Pattern 3: RAG System
```python
# Setup (embeddings come from a third-party provider such as Voyage AI;
# Anthropic does not offer an embeddings endpoint)
vectordb = setup_vector_database()
documents = load_documents()
vectordb.add(documents)

# Query
def query(question):
    # Retrieve relevant documents
    docs = vectordb.search(question)

    # Generate answer with context
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=f"Use these documents: {docs}",
        messages=[{"role": "user", "content": question}]
    )

    return response.content[0].text
```

### Pattern 4: Batch Processing
```python
# Prepare requests
requests = [create_request(item) for item in items]

# Submit batch
batch = client.messages.batches.create(requests=requests)

# Monitor progress
while batch.processing_status != "ended":
    time.sleep(10)
    batch = client.messages.batches.retrieve(batch.id)

# Process results (match by custom_id; order is not guaranteed)
for entry in client.messages.batches.results(batch.id):
    ...
```

## 📊 Project Comparison

| Project | Difficulty | Time | Key Technologies | Best For Learning |
|---------|-----------|------|------------------|-------------------|
| Customer Support | ⭐⭐ | 3-4h | Streaming, Tools | Conversational AI |
| Document Q&A | ⭐⭐⭐ | 4-6h | RAG, Caching | Information Retrieval |
| Code Review | ⭐⭐⭐ | 4-5h | Agents, APIs | Autonomous Systems |
| Research Assistant | ⭐⭐⭐ | 5-6h | Multi-Agent | Complex Workflows |
| MCP Weather | ⭐⭐ | 2-3h | MCP, APIs | Tool Integration |

## 🎯 Completion Checklist

Track your project completions:

- [ ] Project 1: Customer Support Chatbot
- [ ] Project 2: Document Q&A System
- [ ] Project 3: Code Review Agent
- [ ] Project 4: Research Assistant
- [ ] Project 5: MCP Weather Server

### Bonus Achievements
- [ ] Complete all projects
- [ ] Add custom features to each project
- [ ] Deploy one project to production
- [ ] Build your own project from scratch
- [ ] Contribute to open source

## 🤝 Contribution Guidelines

Want to contribute a project?

### Requirements
1. Complete, working code
2. Clear documentation
3. Requirements.txt
4. Example usage
5. Tests (optional but recommended)

### Steps
1. Create project in new directory
2. Follow structure guidelines
3. Include detailed README
4. Test thoroughly
5. Submit for review

## 📚 Additional Resources

### Code Examples
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Anthropic Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

### Documentation
- [Claude API Docs](https://platform.claude.com/docs/en/home)
- [MCP Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)

### Community
- [Discord Community](https://discord.gg/anthropic)
- [GitHub Discussions](https://github.com/anthropics/anthropic-sdk-python/discussions)

## 🎉 Next Steps

1. Choose your first project
2. Set up your environment
3. Study the code
4. Build and modify
5. Share your results!

---

**Ready to build?** Start with [Project 1: Customer Support Chatbot](./1_customer_support_bot/README.md)
