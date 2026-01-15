# Comprehensive Guide: Getting Started with Claude API Development in Python

> Based on the "Build with Claude" page from Anthropic Academy, this guide helps you start developing Claude-powered applications using Python.

---

## 1. Foundation: Understanding Claude Models

### Available Models

The latest Claude models are:

| Model | Best For | Key Characteristics |
|-------|----------|---------------------|
| **Claude Sonnet 4.5** | Most applications | Best balance of speed and capability |
| **Claude Opus 4.5** | Complex reasoning | Highest intelligence for difficult tasks |
| **Claude 4** | Legacy support | Previous generation models |

### Getting Started with Models

To choose the right model:

- 📊 Review the [model comparison chart](https://platform.claude.com/docs/en/models) to understand capabilities and differences
- 🔄 Check the model migration checklist if upgrading from Claude 4
- 📝 Follow Claude 4 prompting best practices for optimal results
- 💰 Review pricing for Claude 4 to optimize costs

---

## 2. Setup & Installation: Python SDK

### Installing the Python SDK

The Python SDK is the primary tool for Python developers. Start by:

1. **Installing the Anthropic Python SDK via pip**
   ```bash
   pip install anthropic
   ```

2. **Generating API keys from the Anthropic Console**
   - Visit [console.anthropic.com](https://console.anthropic.com)
   - Navigate to API Keys section
   - Create and securely store your key

3. **Setting up environment variables with your API key**
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

### Key Components

The Python SDK includes:

- ✅ Full support for the Messages API
- ⚡ Async/await capabilities for efficient concurrent requests
- 🔍 Type hints for better IDE support and error checking
- 🛡️ Built-in error handling and retry logic

### Alternative SDKs Available

If needed, Anthropic also provides:

- **TypeScript SDK** (JavaScript/Node.js)
- **Java SDK**
- **Go SDK**
- **Ruby SDK**

---

## 3. Core APIs & Features for Python Development

### 3.1 Messages API (Primary API)

The Messages API is the fundamental interface for communicating with Claude:

**Core Capabilities**:
- 💬 Send text messages and receive responses
- 🌊 Stream responses for real-time output
- 🔄 Handle multiple conversation turns
- 📚 Manage conversation history efficiently

**Key Features**:
- Support for different message roles (user, assistant)
- Token counting for optimization
- Temperature and other parameter controls
- Streaming responses for better UX

### 3.2 Message Batches API

For processing multiple requests efficiently:

- 📦 Submit multiple API requests at once
- 💰 Reduce costs by processing in batches
- 🎯 Ideal for batch processing jobs, evaluations, and large-scale analysis
- ⏱️ Asynchronous processing for non-time-critical tasks

### 3.3 Files API

Manage files for extended context and data handling:

- 📁 Upload and manage files for use with Claude
- 📄 Include PDFs, documents, and other file types
- ♻️ Reuse uploaded files across multiple API calls
- 🔍 Support for text extraction and document analysis

### 3.4 PDF Support

Extract and understand visual content from PDFs:

- 📖 Extract text from PDF documents
- 📊 Analyze charts, graphs, and visual information
- 🖼️ Process mixed text and image content
- 🎯 Useful for document analysis applications

### 3.5 Admin API

Manage permissions and workspace settings:

- 👥 Control user access and permissions
- ⚙️ Manage workspace configurations
- 🏢 Scale enterprise deployments
- 🔐 Handle team-based access control

---

## 4. Advanced Features for Python Developers

### 4.1 Prompt Caching

Optimize performance and reduce API costs:

- 🔄 Reuse cached prompts across multiple requests
- 💰 Significant cost reduction for repeated contexts (up to 90%)
- ⚡ Faster response times for recurring patterns
- 🛠️ Implementation: Use `cache_control` parameters in API calls

**When to Use**:
- Long system prompts repeated across requests
- Standard instruction sets used multiple times
- Knowledge bases accessed repeatedly
- Recurring document analysis tasks

### 4.2 Vision Capabilities

Harness Claude's image understanding:

- 🖼️ Analyze images and visual information
- 📝 Extract text from images (OCR)
- 📊 Analyze charts and graphs
- 🎨 Describe visual content
- 🔗 Support for base64-encoded images and URLs

### 4.3 Computer Use

Interact with desktop environments programmatically:

- 🖱️ Automate desktop interactions
- 📸 Take screenshots and analyze them
- ⌨️ Click, type, and control mouse
- 🔌 Integration with existing APIs
- 🔒 Learn how Computer Use handles data privacy

### 4.4 Extended Thinking

Improve Claude's ability to solve complex tasks:

- 🧠 Enable longer, more thoughtful reasoning
- 📈 Better performance on difficult problems
- 💻 Useful for coding, math, and complex analysis
- ⚠️ Trade-off: longer response times and higher costs

**Implementation**:
- Use extended thinking models in your API calls
- Follow extended thinking best practices
- Monitor token usage (thinking tokens are more expensive)

---

## 5. Building Applications: Patterns & Techniques

### 5.1 Tool Use (Function Calling)

Extend Claude's capabilities by connecting to external tools:

**Core Concepts**:
- 🛠️ Define tools/functions that Claude can call
- 🤖 Claude decides when and how to use tools
- 📚 Supports multiple tool definitions
- 🔌 Implement tool use with the Anthropic API

**Common Use Cases**:
- 🗄️ Database queries
- 🌐 API calls to external services
- ⚙️ Code execution
- 🧮 Calculator functions
- 🔍 Web searches

**Available Tools**:
- Code execution tool
- Text editor tool
- Web search tool
- Custom tools defined by your application

### 5.2 Agents & Agentic Systems

Build autonomous systems that understand, plan, and execute tasks:

**Architecture**:
- 🎯 Design agent patterns using Claude
- 📋 Implement JSON outputs for reliable control
- 🔗 Use the Model Context Protocol (MCP)
- 🔄 Loop-based architecture: perceive → plan → act
- 📖 Reference Anthropic Cookbook for agent patterns

**Key Components**:
- Agent loops: continuous perception and action
- Tool integration for external actions
- State management
- Decision-making logic

### 5.3 Skills

Provide detailed instructions for specific tasks:

- 📝 Define skill descriptions with examples
- 📈 Use skills to improve task-specific performance
- ✅ Best practices for skill creation
- 🔌 Implement skills in API calls

### 5.4 Retrieval Augmented Generation (RAG)

Build systems that enhance Claude's knowledge with external data:

**Core Process**:
1. 📚 Retrieve relevant information from documents
2. 🤝 Combine retrieved context with Claude's reasoning
3. 🎯 Implement customer support agents with RAG
4. 🔌 Integration options: LlamaIndex, MongoDB, etc.

**Technology Stack Options**:
- **Voyage AI** for embeddings
- **LlamaIndex** for RAG orchestration
- **MongoDB** for vector storage
- **Custom implementations**

### 5.5 Model Context Protocol (MCP)

Build advanced applications with standardized tool integration:

**Setup Options**:
- 🖥️ Set up MCP in Claude Desktop for local development
- 📦 Use Anthropic's ready-made MCP servers
- 💻 Integrate with Claude Code for IDE support
- ☁️ Set up remote MCP servers
- 🔌 Connect remote MCP from Messages API

**Features**:
- Standardized tool definitions
- Easy server setup and configuration
- Git-based community contributions
- Advanced MCP concepts for complex applications

---

## 6. Development Tools & Environments

### 6.1 Claude Code

Accelerate development with AI-assisted coding:

- 📥 Install Claude Code locally
- 🔌 Integrate with your IDE
- ☁️ Connect to Google Vertex AI or Amazon Bedrock
- 📖 Browse common workflows and patterns
- 🆘 Access documentation and troubleshooting guides

### 6.2 Claude Desktop

Development environment for testing and prototyping:

- 🧪 Local testing before production deployment
- 🔗 MCP integration for tool testing
- ⚡ Real-time feedback on responses

### 6.3 Anthropic Console

Web-based interface for:

- 🔑 API key management
- ⚙️ Workspace configuration
- 📊 Usage monitoring
- 🛠️ Developer settings

---

## 7. Optimization & Best Practices

### 7.1 Prompt Engineering

Create effective prompts that maximize Claude's performance:

**Learning Resources**:
- 🎓 Take interactive tutorials on prompt engineering
- 💪 Practice with real-world scenarios
- 🛠️ Use the prompt generator tool
- 📖 Follow established best practices

**Key Principles**:
1. ✅ Be clear and specific
2. 📝 Provide examples when helpful
3. 🏗️ Use structured formats
4. 📋 Specify output format
5. 🎯 Include relevant context

### 7.2 Evaluations

Test and improve your Claude implementation:

**Framework**:
- 🏗️ Build strong evaluation frameworks
- 🤖 Create automated evaluation systems
- 🛠️ Use the Eval Tool on Claude Console
- 📈 Measure performance improvements

**Evaluation Types**:
- ✅ Output quality assessment
- 💰 Cost-efficiency analysis
- ⚡ Latency measurements
- 😊 User satisfaction metrics

### 7.3 Model Selection

Choose the right model for your use case:

| Use Case | Recommended Model | Reason |
|----------|------------------|---------|
| Most applications | Sonnet 4.5 | Fastest, balanced performance |
| Complex reasoning | Opus 4.5 | Highest intelligence |
| High volume, simple tasks | Haiku 3.5 | Most cost-effective |

**Considerations**:
- Token limits and costs
- Use model comparison chart for detailed specs
- Balance performance vs. cost

### 7.4 Cost Optimization

Reduce API costs while maintaining quality:

1. 💾 **Implement prompt caching** for repeated contexts
2. 📦 **Use Message Batches API** for non-urgent requests
3. 📊 **Monitor token usage**
4. ✂️ **Optimize prompt length and structure**
5. 🎯 **Use appropriate models** for each task

---

## 8. Getting Your First Python Application Running

### Step-by-Step Setup

```python
# 1. Install the SDK
# pip install anthropic

# 2. Set up your API key
# export ANTHROPIC_API_KEY='your-api-key'

# 3. Create a basic application
from anthropic import Anthropic

client = Anthropic()

# 4. Make your first API call
message = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Next Steps

After your first successful call:

1. 📖 Review the full API documentation
2. 🍳 Explore the Anthropic Cookbook for code examples
3. 🚀 Try the Anthropic Quickstarts repository
4. 🛠️ Build a prototype application
5. 🧪 Test with different models and parameters
6. ⚡ Optimize based on your use case

---

## 9. Advanced Resources

### Documentation & Learning

| Resource | Description | Link |
|----------|-------------|------|
| **Full API Docs** | Complete API reference | [docs.anthropic.com](https://docs.anthropic.com) |
| **Anthropic Cookbook** | Code snippets and practical guides | [GitHub](https://github.com/anthropics/anthropic-cookbook) |
| **Quickstarts** | Pre-built application examples | [GitHub](https://github.com/anthropics/anthropic-quickstarts) |
| **Courses** | In-depth training on specific topics | [Anthropic Academy](https://www.anthropic.com/learn) |

### Community & Support

- 🎉 Hackathon resources if you're participating in events
- 📊 Workshop slides and training materials
- 👥 Developer community for questions and ideas
- 🐙 GitHub repositories for MCP and other projects

### Cloud Platform Integration

| Platform | Description |
|----------|-------------|
| **Amazon Bedrock** | Run Claude through AWS |
| **Google Cloud Vertex AI** | Run Claude on GCP |
| **Direct API** | Access through Anthropic Console |

---

## 10. Common Development Patterns

### Pattern 1: Simple Chat Application

```
1. Initialize client with API key
2. Implement message loop
3. Handle conversation history
4. Stream responses for better UX
```

### Pattern 2: Tool-Using Agent

```
1. Define available tools
2. Create agent loop
3. Handle tool calls from Claude
4. Execute tools and return results
5. Continue agent loop until completion
```

### Pattern 3: RAG System

```
1. Load and embed documents
2. Create vector store
3. Implement retrieval function
4. Build prompts with retrieved context
5. Execute Claude API with enhanced prompts
```

### Pattern 4: Batch Processing

```
1. Prepare multiple requests
2. Submit via Message Batches API
3. Monitor batch status
4. Process results asynchronously
5. Handle errors and retries
```

---

## 11. Troubleshooting & Tips

| Issue | Solution |
|-------|----------|
| **API Rate Limits** | Use batch processing for high volume |
| **High Token Costs** | Implement prompt caching and optimize prompts |
| **Slow Responses** | Use Sonnet model, check temperature settings, stream responses |
| **Tool Calling Issues** | Ensure tool definitions are clear and JSON format is correct |
| **Accuracy Problems** | Use extended thinking, improve prompts, add examples |
| **Debugging** | Use the Claude Console to test prompts, check API documentation |

---

## Quick Reference: Python SDK Essentials

### Installation
```bash
pip install anthropic
```

### Basic Usage
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-key")

message = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

### Key Methods

| Method | Description |
|--------|-------------|
| `messages.create()` | Send message and get response |
| `messages.stream()` | Get streaming responses |
| `beta.files.upload()` | Upload files |
| `batches.create()` | Process multiple requests |

---

## 🚀 Start Building

Visit [platform.claude.com](https://platform.claude.com) to get started with your first application!

This comprehensive guide covers everything you need to begin developing Claude-powered applications in Python, from basic setup to advanced patterns and optimization techniques.

---

## Additional Resources

- 📚 [Complete Training Course](README.md)
- 🚀 [Quick Start Guide](INICIO_RAPIDO.md)
- 💻 [Code Examples](modulos)
- 🎯 [Hands-On Exercises](ejercicios)
- 🏗️ [Sample Projects](proyectos)

---

## 🙏 Credits

**Created by [Future Tales](https://futuretales.ai)** - Empowering developers to build the future with AI.

This comprehensive guide was developed based on official Anthropic documentation and industry best practices.
