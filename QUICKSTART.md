# Quick Start Guide

## 🎉 Welcome to Build with Claude Training Course!

This comprehensive training course will teach you how to build AI-powered applications using Claude API and Python.

## 📚 What's Included

### 5 Complete Modules (30+ Lessons)
1. **Module 1: Foundation & Setup** - Get started with Claude API
2. **Module 2: Core API Features** - Master Messages API and streaming
3. **Module 3: Advanced Features** - Tool use, caching, batch processing
4. **Module 4: Building Applications** - Agents, RAG, MCP
5. **Module 5: Optimization** - Production best practices

### Hands-On Learning
- **15+ Exercises** with step-by-step instructions and solutions
- **5 Real-World Projects** demonstrating production patterns
- **100+ Code Examples** in Python
- **Progressive Learning Path** from beginner to advanced

## 🚀 Get Started in 5 Minutes

### Step 1: Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic python-dotenv
```

### Step 2: Configure API Key
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

Get your API key from: https://console.anthropic.com

### Step 3: Test Your Setup
```python
# test_setup.py
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

Run it:
```bash
python test_setup.py
```

## 📖 Learning Paths

### Path 1: Complete Beginner (Start Here!)
1. Read [Module 1: Foundation](./modules/module1_foundation/README.md)
2. Complete [Exercise 1: Hello Claude](./exercises/beginner/01_hello_claude.md)
3. Continue through Module 1 lessons
4. Practice with beginner exercises

**Time**: 2-3 hours

### Path 2: Experienced Developer
1. Skim Module 1 for setup
2. Deep dive into [Module 2: Core API](./modules/module2_core_api/README.md)
3. Explore [Module 3: Advanced Features](./modules/module3_advanced_features/README.md)
4. Build [Project 1: Customer Support Bot](./projects/README.md)

**Time**: 6-8 hours

### Path 3: Production Ready
1. Review Modules 1-3 quickly
2. Focus on [Module 4: Applications](./modules/module4_applications/README.md)
3. Master [Module 5: Optimization](./modules/module5_optimization/README.md)
4. Complete all projects

**Time**: 12-15 hours

## 🎯 Quick Navigation

### Essential Lessons
- [Understanding Models](./modules/module1_foundation/01_models_overview.md) - Choose the right model
- [First API Call](./modules/module1_foundation/07_first_api_call.md) - Your first steps
- [Messages API](./modules/module2_core_api/01_messages_api.md) - Core functionality
- [Streaming](./modules/module2_core_api/04_streaming_basics.md) - Real-time responses
- [Tool Use](./modules/module3_advanced_features/01_tool_use_basics.md) - Function calling
- [Prompt Caching](./modules/module3_advanced_features/05_prompt_caching.md) - Cost optimization

### Practice
- [All Exercises](./exercises/README.md) - Hands-on practice
- [Sample Projects](./projects/README.md) - Real-world examples

## 💡 What You'll Learn

### Week 1: Foundations
- ✅ Claude models and capabilities
- ✅ Python SDK setup
- ✅ API key management
- ✅ Making API calls
- ✅ Basic error handling

### Week 2: Core Features
- ✅ Messages API mastery
- ✅ Streaming responses
- ✅ Conversation management
- ✅ Working with images
- ✅ File handling

### Week 3: Advanced
- ✅ Tool use / function calling
- ✅ Prompt caching
- ✅ Batch processing
- ✅ Vision capabilities
- ✅ Extended thinking

### Week 4: Applications
- ✅ Building chatbots
- ✅ Creating agents
- ✅ RAG systems
- ✅ MCP integration
- ✅ Production patterns

## 📊 Course Statistics

- **30+** Comprehensive lessons
- **5** Major modules
- **15+** Hands-on exercises
- **5** Real-world projects
- **100+** Code examples
- **6,000+** Lines of documentation

## 🎓 Completion Checklist

### Beginner (Week 1-2)
- [ ] Complete Module 1
- [ ] Complete Module 2
- [ ] Finish 5 beginner exercises
- [ ] Build simple chatbot

### Intermediate (Week 3)
- [ ] Complete Module 3
- [ ] Finish 5 intermediate exercises
- [ ] Implement tool use
- [ ] Build streaming application

### Advanced (Week 4+)
- [ ] Complete Module 4 & 5
- [ ] Finish advanced exercises
- [ ] Build RAG system
- [ ] Deploy production app

## 🛠️ Tools & Resources

### Required
- Python 3.7+
- Anthropic API key
- Text editor/IDE

### Recommended
- VS Code or PyCharm
- Git for version control
- Virtual environment
- Terminal/command line

### Additional Resources
- [Official Claude Docs](https://platform.claude.com/docs)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Python SDK GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [MCP Documentation](https://modelcontextprotocol.io)

## 🎯 Next Steps

### Today
1. ✅ Set up your environment
2. ✅ Get your API key
3. ✅ Make your first API call
4. ✅ Start Module 1

### This Week
1. Complete Module 1 & 2
2. Do beginner exercises
3. Build simple chatbot
4. Experiment with streaming

### This Month
1. Complete all modules
2. Finish all exercises
3. Build 2-3 projects
4. Deploy one application

## 💬 Getting Help

### Documentation
- Check module READMEs
- Review code examples
- Read lesson materials

### Community
- [Discord](https://discord.gg/anthropic)
- [GitHub Discussions](https://github.com/anthropics/anthropic-sdk-python/discussions)
- [Twitter](https://twitter.com/AnthropicAI)

### Troubleshooting
- Check [API documentation](https://platform.claude.com/docs)
- Review error handling guides
- Test with simple examples

## 🎉 Ready to Start?

Begin your journey with [Module 1: Foundation & Setup](./modules/module1_foundation/README.md)

Or dive right into coding with [Exercise 1: Hello Claude](./exercises/beginner/01_hello_claude.md)

---

**Happy Learning! 🚀**

*This course was created based on official Anthropic documentation and best practices. Last updated: January 2026*
