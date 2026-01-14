# Build with Claude: Comprehensive Training Course

Welcome to the **Build with Claude** comprehensive training course! This course will take you from beginner to advanced in building applications with Claude's API using Python.

## 🎯 Course Overview

This training program is designed for developers who want to master building AI-powered applications using Anthropic's Claude API. Whether you're a beginner just starting out or an experienced developer looking to deepen your knowledge, this course has something for everyone.

### What You'll Learn
- 🚀 Get started with Claude API and Python SDK
- 💬 Build conversational AI applications
- 🛠️ Implement tool use and function calling
- 📊 Optimize costs with prompt caching
- 🤖 Create autonomous agents
- 🔍 Build RAG (Retrieval Augmented Generation) systems
- 🎨 Work with vision and multimodal capabilities
- 📈 Optimize performance and costs
- 🏭 Deploy production-ready applications

## 📚 Course Structure

### [Module 1: Foundation & Setup](./modules/module1_foundation/README.md)
**Duration**: 2-3 hours | **Level**: Beginner

Get started with Claude API fundamentals:
- Understanding Claude models (Haiku, Sonnet, Opus)
- Installing and configuring the Python SDK
- API key management and security
- Making your first API call
- Basic request/response handling

**Key Topics**:
- [Models Overview](./modules/module1_foundation/01_models_overview.md)
- [SDK Installation](./modules/module1_foundation/05_sdk_installation.md)
- [API Keys Management](./modules/module1_foundation/06_api_keys.md)
- [First API Call](./modules/module1_foundation/07_first_api_call.md)

---

### [Module 2: Core API Features](./modules/module2_core_api/README.md)
**Duration**: 4-6 hours | **Level**: Beginner to Intermediate

Master the core features of Claude API:
- Messages API deep dive
- Streaming responses for better UX
- Managing multi-turn conversations
- Working with images and PDFs
- File management
- Error handling and retries

**Key Topics**:
- [Messages API Fundamentals](./modules/module2_core_api/01_messages_api.md)
- [Streaming Basics](./modules/module2_core_api/04_streaming_basics.md)
- Vision and multimodal capabilities
- Robust error handling patterns

**Hands-On Labs**:
- 🔬 Build a conversational chatbot
- 🔬 Implement streaming responses
- 🔬 Create an image analysis tool
- 🔬 Build a PDF analyzer

---

### [Module 3: Advanced Features](./modules/module3_advanced_features/README.md)
**Duration**: 6-8 hours | **Level**: Intermediate to Advanced

Explore advanced Claude API capabilities:
- Tool use and function calling
- Prompt caching for cost optimization
- Batch processing
- Extended thinking for complex reasoning
- Computer use (beta)

**Key Topics**:
- [Tool Use Basics](./modules/module3_advanced_features/01_tool_use_basics.md)
- [Prompt Caching](./modules/module3_advanced_features/05_prompt_caching.md)
- Message batches API
- Vision capabilities
- Extended thinking

**Hands-On Labs**:
- 🔬 Build a calculator with tool use
- 🔬 Create a web search agent
- 🔬 Implement prompt caching
- 🔬 Build an image analysis pipeline
- 🔬 Create a batch processing system

---

### [Module 4: Building Applications](./modules/module4_applications/README.md)
**Duration**: 8-10 hours | **Level**: Intermediate to Advanced

Build real-world applications with proven patterns:
- Conversational chatbots
- Autonomous agents
- RAG (Retrieval Augmented Generation)
- Model Context Protocol (MCP)
- Production patterns

**Key Topics**:
- Agent architecture and loops
- Multi-agent systems
- RAG fundamentals and optimization
- Building MCP servers and clients
- Production-ready patterns

**Hands-On Projects**:
- 🚀 Customer support chatbot
- 🚀 Code review agent
- 🚀 Document Q&A system with RAG
- 🚀 Custom MCP server
- 🚀 Multi-agent research assistant

---

### [Module 5: Optimization & Best Practices](./modules/module5_optimization/README.md)
**Duration**: 6-8 hours | **Level**: Advanced

Optimize and deploy production-ready applications:
- Advanced prompt engineering
- Cost and performance optimization
- Evaluation frameworks
- Monitoring and debugging
- Scaling strategies

**Key Topics**:
- Prompt engineering techniques
- Token and cost optimization
- Building evaluation systems
- Production error handling
- Deployment and scaling

**Capstone Project**:
- 🎓 Build a production-ready application with all best practices

---

## 🎓 Learning Path

### For Beginners
1. Start with **Module 1** to understand the basics
2. Work through **Module 2** to master core features
3. Try the hands-on labs to reinforce learning
4. Move to **Module 3** when comfortable with basics

### For Intermediate Developers
1. Review **Module 1** quickly for setup
2. Deep dive into **Module 2** and **Module 3**
3. Focus on **Module 4** for application patterns
4. Complete multiple hands-on projects

### For Advanced Developers
1. Skim **Module 1-2** for quick reference
2. Focus on **Module 3** advanced features
3. Deep dive into **Module 4** for architecture patterns
4. Master **Module 5** optimization techniques
5. Build the capstone project

## 📦 Prerequisites

### Required
- Basic Python programming knowledge (variables, functions, classes)
- Python 3.7 or higher installed
- Text editor or IDE (VS Code, PyCharm, etc.)
- Command line familiarity
- Anthropic API account ([sign up here](https://console.anthropic.com))

### Recommended
- Understanding of REST APIs
- Experience with async programming (for advanced modules)
- Familiarity with web applications
- Basic knowledge of databases (for RAG modules)

## 🛠️ Setup Instructions

### 1. Clone or Download Course Materials
```bash
cd build_with_Claude
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install anthropic python-dotenv
```

### 3. Configure API Key
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### 4. Test Your Setup
```bash
python -c "import anthropic; print('Setup successful!')"
```

## 📖 How to Use This Course

### Self-Paced Learning
- Work through modules sequentially
- Complete all hands-on labs
- Take breaks between modules
- Practice with your own projects

### Instructor-Led Training
- Follow your instructor's guidance
- Participate in group exercises
- Ask questions during Q&A sessions
- Share your projects with peers

### Quick Reference
- Use module READMEs for topic overviews
- Refer to individual lessons for detailed information
- Bookmark important code examples
- Use the exercises folder for practice

## 🎯 Hands-On Exercises

### [Beginner Exercises](./exercises/beginner/)
- Hello Claude variations
- Simple chatbot
- Text generation
- Q&A system
- Temperature experiments

### [Intermediate Exercises](./exercises/intermediate/)
- Streaming chatbot
- Image analysis tool
- Tool use implementations
- Conversation management
- Multi-turn interactions

### [Advanced Exercises](./exercises/advanced/)
- RAG system
- Autonomous agent
- Batch processing pipeline
- Custom MCP server
- Production application

## 🚀 Sample Projects

### [Projects Directory](./projects/)

1. **Customer Support Bot**
   - Streaming responses
   - Context management
   - Tool integration

2. **Document Q&A System**
   - RAG implementation
   - Vector database
   - PDF processing

3. **Code Review Agent**
   - Tool use
   - GitHub integration
   - Automated analysis

4. **Research Assistant**
   - Multi-agent system
   - Web search integration
   - Report generation

## 📚 Additional Resources

### Official Documentation
- [Anthropic Documentation](https://platform.claude.com/docs/en/home)
- [API Reference](https://platform.claude.com/docs/en/api/overview)
- [Python SDK GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

### Learning Resources
- [Build with Claude Academy](https://www.anthropic.com/learn/build-with-claude)
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Prompt Engineering Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)

### Community
- [Anthropic Discord](https://discord.gg/anthropic)
- [GitHub Discussions](https://github.com/anthropics/anthropic-sdk-python/discussions)
- [Twitter/X](https://twitter.com/AnthropicAI)

### Tools
- [Anthropic Console](https://console.anthropic.com)
- [Prompt Generator](https://console.anthropic.com/prompt-generator)
- [Claude Desktop](https://claude.ai/download)

## 💡 Tips for Success

1. **Practice Regularly**: Code along with examples
2. **Experiment**: Try variations of provided code
3. **Build Projects**: Apply concepts to real problems
4. **Read Documentation**: Refer to official docs
5. **Join Community**: Engage with other learners
6. **Take Notes**: Document your learnings
7. **Ask Questions**: Don't hesitate to seek help

## 🔍 Course Updates

This course is regularly updated to reflect:
- Latest Claude models and features
- New API capabilities
- Best practice updates
- Community feedback

**Last Updated**: January 2026
**Claude Models**: Opus 4.5, Sonnet 4.5, Haiku 3.5

## 📝 Course Completion

Upon completing this course, you will be able to:
- ✅ Build production-ready Claude applications
- ✅ Implement advanced features like tool use and RAG
- ✅ Optimize costs and performance
- ✅ Handle errors and edge cases gracefully
- ✅ Deploy and scale Claude applications
- ✅ Follow industry best practices

## 🤝 Contributing

Found an issue or want to improve the course?
- Open an issue with suggestions
- Submit corrections or improvements
- Share your project examples
- Help other learners

## 📄 License

This training course is provided for educational purposes. Code examples are provided as-is for learning and reference.

## 🙏 Acknowledgments

### Course Creation
This comprehensive training course was created and developed by **[Future Tales](https://futuretales.ai)** - Empowering developers to build the future with AI.

### Course Foundation
This course is based on:
- Official Anthropic documentation
- Community best practices
- Real-world implementation experience
- Student feedback and contributions

---

## 🚀 Ready to Get Started?

Begin your journey with [Module 1: Foundation & Setup](./modules/module1_foundation/README.md)

**Happy Learning! 🎉**

---

### Quick Navigation
- [Module 1: Foundation](./modules/module1_foundation/README.md)
- [Module 2: Core API](./modules/module2_core_api/README.md)
- [Module 3: Advanced Features](./modules/module3_advanced_features/README.md)
- [Module 4: Applications](./modules/module4_applications/README.md)
- [Module 5: Optimization](./modules/module5_optimization/README.md)
- [Exercises](./exercises/)
- [Projects](./projects/)
