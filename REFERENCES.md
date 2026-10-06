# Official References (verified October 2026)

Everything in this course maps to an official source. When a lesson and the docs disagree, **the docs win**: model lineups, prices and beta flags change faster than any course.

## Claude Developer Platform docs

| Topic | Official page | Course lessons |
|-------|---------------|----------------|
| Models overview (IDs, context, pricing, retirement) | [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | [1.1 Models](./modules/module1_foundation/01_models_overview.md), [1.2 Selection](./modules/module1_foundation/02_model_selection.md) |
| Choosing a model | [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) | [5.2 Model selection](./modules/module5_optimization/07_model_selection.md) |
| Migration guide | [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) | all modules |
| Deprecations | [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) | 1.1 |
| Pricing | [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | [1.3 Pricing](./modules/module1_foundation/03_pricing_limits.md) |
| Cost optimization | [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) | Module 3 (caching, batch), Module 5 |
| Messages API / streaming | [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming) | Module 2 |
| Adaptive thinking | [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) | [3.5 Thinking](./modules/module3_advanced_features/14_extended_thinking.md) |
| Effort | [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) | 3.5, 5.2 |
| Tool use | [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | [3.1 Tool use](./modules/module3_advanced_features/01_tool_use_basics.md) |
| Computer use | [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | [3.6 Computer use](./modules/module3_advanced_features/16_computer_use.md) |
| Prompt caching | [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Module 3 |
| Batch processing | [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) | Module 3 |
| Vision and PDFs | [Vision](https://platform.claude.com/docs/en/build-with-claude/vision), [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) | Modules 2 and 3 |
| Files API | [Files](https://platform.claude.com/docs/en/build-with-claude/files) | [2.4 File management](./modules/module2_core_api/10_file_management.md) |
| Structured outputs | [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | [2.2 Conversations](./modules/module2_core_api/03_conversations.md) |
| Token counting | [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) | 1.3 |
| Rate limits and errors | [Rate limits](https://platform.claude.com/docs/en/api/rate-limits), [Errors](https://platform.claude.com/docs/en/api/errors) | Modules 2, 4, 5 |
| Agent Skills | [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Module 4 |
| Prompt engineering | [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Module 5 |
| Release notes | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) | whole course |
| Cloud platforms | [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws) | [5.26 Cloud integration](./modules/module5_optimization/26_cloud_integration.md) |

## Claude Code and Agent SDK

- [Claude Code docs](https://code.claude.com/docs/en/overview)
- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk): Claude Code's harness as a library (Python and TypeScript)
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (Module 4 MCP lessons)
- [Mods in this repo](./MODS.md): build a live "Consumo" usage pane in Claude Code

## SDKs and samples

- [Python SDK](https://github.com/anthropics/anthropic-sdk-python), [TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

## Claude Academy (formerly Anthropic Academy)

Free, self-paced courses with certificates: [academy.claude.com/courses](https://academy.claude.com/courses) (also at [anthropic.skilljar.com](https://anthropic.skilljar.com/)).

| Academy course | Pairs with |
|----------------|-----------|
| Claude 101 | Before Module 1 (everyday use of Claude) |
| Building with the Claude API | Modules 1 to 3 and 5 |
| Introduction to Model Context Protocol | Module 4 (MCP lessons 13 to 16) |
| Claude Code in Action | Module 4 (code assistants) and [MODS.md](./MODS.md) |
| Introduction to Agent Skills | Module 4 (agents) |

> Note: the Academy catalogue grows (there are also AI Fluency and cloud/enterprise tracks). The list above comes from public search listings; the Academy site could not be opened while this course was updated, so check the catalogue for the exact current titles.

## Keeping this course current

1. Re-check the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [Release notes](https://platform.claude.com/docs/en/release-notes/overview) before each cohort.
2. Never hard-code a model ID without checking [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).
3. See [WHATS_NEW.md](./WHATS_NEW.md) for what changed in this revision.
