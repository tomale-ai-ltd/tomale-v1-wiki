---
title: Exploring Spec Driven Development (SDD)- A Practical Guide with GitHub SpecKit and Copilot
source: https://levelup.gitconnected.com/exploring-spec-driven-development-sdd-a-practical-guide-with-github-speckit-and-copilot-72fd9a70535a
author:
  - "Chris Bao"
published: 2026-03-26
created: 2026-04-15
description: A blog post written by Chris Bao (microsoft) providing guidance on spec driven development, in particular in relation to 'vibe coding' or AI powered software development workflows.
tags:
  - research
approved: true
---
## Why was this added to the vault?

To bolster the available information and context regarding spec driven development, and to allow the LLM to provide greater depth in response to future queries about the SDD process.

## Introduction

When I first started working with AI coding assistants, I noticed something interesting: while these tools are incredibly powerful, they sometimes produce code that doesn’t quite match what I had in mind. Has this ever happened to you? You describe a feature, the AI generates some code, but then you spend hours debugging and adjusting it to fit your actual requirements.

I came across this problem repeatedly until I discovered Spec Driven Development (SDD). This approach transformed how I work with AI coding assistants, and in this article, I’ll share what I learned and how you can apply it in your own projects.

In this post, you’ll understand:

- What Spec Driven Development is and why it matters
- How it compares to the popular “vibe coding” approach
- The practical workflow using GitHub SpecKit and Copilot
- Real examples you can implement right away
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*4epNqPAu88pkmBL8JSaztg.png)

## What is SDD (Spec Driven Development)?

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JFkQec4-3IlKbn-TnVxWgQ.png)

Spec Driven Development (SDD) represents a fundamental shift in how we approach software development, especially in the age of AI-assisted programming. Let me break this down in simple terms.

Think about traditional software development: we typically start coding and figure things out as we go. But with SDD, we take a different approach — we create detailed specifications first, then let those specifications guide the entire development process.

In SDD, specifications serve as the definitive source of truth for what needs to be built. This is crucial: we’re separating the “what” from the “how.” The specification describes what the system should do, while the implementation determines how it will do it.

This approach establishes a clear, unambiguous contract between everyone involved — business stakeholders, product managers, developers, and yes, even AI coding agents.

Here’s what I found particularly interesting: the fundamental philosophy of SDD aligns with practices we’ve used for years — Test-Driven Development (TDD) and Behavior-Driven Development (BDD). But SDD takes the specification concept to a more comprehensive level. Instead of just user stories, SDD specifications include detailed acceptance criteria, technical constraints, architectural decisions, and implementation guidelines.

Pretty comprehensive, right? Let’s see how this compares to another popular approach…

## Benefits of SDD Compared to Vibe Coding

The rise of generative AI has popularized what I call “vibe coding” — an approach where developers interact with AI assistants through conversational prompts, often with minimal formal specification. While this approach has democratized programming to some extent, it comes with significant limitations that SDD addresses.

## The Limitations of Vibe Coding

**1\. Quality Inconsistency**

I noticed this early on: GenAI excels at pattern recognition but struggles with mind reading. The quality of AI-generated code directly correlates with the quality and clarity of your prompts and context. When prompts are vague, you get unreliable code, forcing you to spend significant time debugging AI-generated solutions rather than focusing on actual development.

Have you ever spent more time fixing AI-generated code than you would have spent writing it from scratch? That’s exactly what I’m talking about.

**2\. Context Management Challenges**

Vibe coding often results in fragmented context spread across multiple conversations. When specifications aren’t formally documented, maintaining consistency across features becomes nearly impossible — especially in team environments.

This really becomes a problem as projects grow. Different team members might ask the AI similar questions but get different results because they’re working from different mental models.

**3\. Limited Scalability**

As projects grow, the informal nature of vibe coding breaks down. What works perfectly for a prototype becomes completely unmanageable for production systems, particularly when multiple developers or AI agents are involved.

I’ve seen this happen personally — what starts as a quick AI-powered prototype can become a maintenance nightmare if you’re not careful.

## The Advantages of SDD

**1\. Clarity and Precision**

SDD eliminates ambiguity by requiring specifications to be clear, complete, and unambiguous. This precision directly translates to higher quality AI-generated code, as coding agents have well-defined requirements to work from.

The key here is that everyone — human or AI — is working from the same clear understanding. That’s a game-changer.

**2\. Maintainable Context**

Specifications serve as living documents that evolve with the codebase. When requirements change, the specification is updated first, ensuring that all stakeholders — human and AI — work from the same understanding.

This is particularly important for AI agents, which can reference the most current specifications rather than relying on potentially outdated conversations.

**3\. Verifiable Requirements**

SDD specifications include explicit acceptance criteria, enabling automated verification. This transforms specifications from passive documents into active quality gates, similar to how TDD transforms requirements into executable tests.

Smart design, right? The specification itself becomes a testable artifact.

**4\. Better Team Collaboration**

Formal specifications provide a common language that business stakeholders, product managers, and developers can all understand and validate. This reduces misunderstandings and ensures everyone is aligned on what’s being built.

I’ve found this incredibly valuable when bringing new team members up to speed — they can read the specifications and understand what’s being built without diving directly into the code.

**5\. Improved AI Agent Performance**

For AI coding agents like GitHub Copilot, well-structured specifications provide the rich context they need to generate accurate, reliable code. SDD essentially “pre-processes” the requirements into a format that AI agents can effectively consume.

This is where the magic happens. The AI doesn’t have to guess what you want — it has detailed specifications to work from.

## The General Workflow of SDD at the Theory Level

The SDD methodology follows a structured workflow that transforms abstract requirements into concrete implementations. Let me walk you through the four distinct phases.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Te2RLI4h5YCA_oYJnC1GTw.png)

## Phase 1: Specify — Defining “What”

The specify phase answers the fundamental question: “What are we building?” This phase focuses exclusively on defining behavior, requirements, and acceptance criteria without prescribing implementation details.

**Key Components:**

- **Behavioral Definitions**: Clear descriptions of what the system should do under various conditions
- **User Stories and Scenarios**: Using established patterns like Given/When/Then to describe expected behaviors
- **Acceptance Criteria**: Explicit conditions that must be met for a feature to be considered complete
- **Edge Cases and Error Conditions**: Comprehensive coverage of exceptional scenarios
- **Non-Functional Requirements**: Performance, security, scalability constraints

**Critical Principle**: The key skill in this phase is eliminating ambiguity while avoiding over-specification. Specifications should be clear enough to guide implementation but flexible enough to allow for optimal technical solutions.

I learned this the hard way — if you’re too vague, the AI can’t help you effectively. But if you’re too specific, you might miss better implementation approaches.

## Phase 2: Plan — Determining “How”

The plan phase addresses the question: “How will we build it?” This is where technical decisions are made and architectural boundaries are established.

**Key Components:**

- **Technology Stack**: Selection of languages, frameworks, databases, and tools
- **Architecture Design**: System architecture, component interactions, and data flow
- **Data Models**: Database schemas, API contracts, and data structures
- **Non-Technical Requirements**: Performance targets, security standards, scalability requirements
- **Implementation Constraints**: Specific technical limitations or requirements (e.g., “use MongoDB for persistence” or “all API endpoints require authentication”)

**Critical Principle**: The plan phase provides the technical guardrails within which implementation will occur, ensuring consistency and alignment with architectural standards.

This is where your expertise really shines — you’re making the technical decisions that guide both human developers and AI agents.

## Phase 3: Implement — Building the Solution

The implementation phase is where specifications and plans are translated into working code. A key SDD principle is working in small, validated increments rather than implementing entire specifications at once.

**Key Principles:**

- **Task Breakdown**: Decompose specifications into small, actionable tasks where each delivers a testable piece of functionality
- **Incremental Delivery**: Implement features in bite-sized chunks that can be individually verified
- **Checkpoint Validation**: Enable frequent checkpoints where humans verify alignment between code and specification
- **Progress Tracking**: Maintain visibility into what’s been completed and what remains

**Critical Principle**: Breaking work into small, testable increments allows for early feedback and course correction, reducing the risk of building the wrong thing.

This is particularly important when working with AI — you want to verify the output at regular intervals to catch issues early.

## Phase 4: Verify — Ensuring Alignment

The verify phase confirms that the implementation matches the specification and meets all acceptance criteria.

**Key Components:**

- **Automated Testing**: Tests derived from specifications that verify expected behaviors
- **Manual Review**: Human verification that implementation meets business requirements
- **Gap Analysis**: Identification of discrepancies between spec and code
- **Decision Making**: Determining whether gaps should be fixed in code or revised in specification

**Critical Principle**: When validation reveals gaps, teams face a clear decision: fix the code if it doesn’t meet the specification, or revise the specification if it’s incomplete or inaccurate. Interestingly, once a solid specification exists, vibe coding becomes much more effective for addressing implementation issues because the context is well-established.

This is where I’ve found the real power of SDD — it doesn’t eliminate the need for AI assistance, but it makes that assistance much more reliable and productive.

## The Concrete Implementation of SpecKit for SDD Workflow

GitHub SpecKit provides a practical implementation of SDD principles, integrating seamlessly with GitHub Copilot to create a powerful development workflow. Let’s explore how SpecKit operationalizes the theoretical SDD workflow.

## SpecKit Architecture

SpecKit consists of several key components that work together to implement SDD. Let me break this down for you:

**1\. Commands and Agents**

- Custom coding agents stored in the `.github` directory
- Each command corresponds to a phase in the SDD workflow
- Agents leverage GitHub Copilot’s capabilities for code generation and analysis

**2\. Templates and Helper Scripts**

- Located in the `.specify` directory
- Five core scripts that automate different aspects of the workflow:
- `check-prerequisites`: Validates that all required documentation exists
- `common`: Shared utilities and functions
- `create-new-feature`: Initializes feature branches and specification files
- `setup-plan`: Prepares planning phase artifacts
- `update-agent-context`: Maintains context for AI agents

Here’s what the SpecKit directory structure looks like:

```hs
├───.github
│   └───prompts
│           plan.prompt.md
│           specify.prompt.md
│           tasks.prompt.md
│   └───agents
│           plan.agent.md
│           specify.agent.md
│           tasks.agent.md
│
└───.specify
    ├───memory
    │       constitution.md
    ├───scripts
    │   └───powershell
    │           check-task-prerequisites.ps1
    │           common.ps1
    │           create-new-feature.ps1
    │           setup-plan.ps1
    │           update-agent-context.ps1
    │
    └───templates
            agent-file-template.md
            plan-template.md
            spec-template.md
            tasks-template.md
```

Pretty organized structure, right? Everything has its place, which makes it easy to understand and maintain.

## Speckit Command Workflow

Let’s walk through each command in detail. I’ll share what I learned from working with them.

### 1\. Constitution Command

The `constitution` command establishes the foundational principles and constraints for the development process. Think of it as setting the ground rules for your project.**What it does:**

- Creates `.specify/memory/constitution.md`
- Defines core principles (e.g., Library-First, CLI Interface, Test-First)
- Establishes constraints, security requirements, and performance standards
- Sets up governance rules and amendment processes

**Key Sections:**

- **Core Principles**: 5+ fundamental development principles with detailed descriptions
- **Additional Requirements**: Security, performance, workflow, and compliance standards
- **Governance**: How the constitution is enforced and updated
- **Version Control**: Versioning and ratification information

Here’s what a constitution looks like in practice:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rZ0PqXf-QHyoA0iJCwnTBw.png)

I found this particularly useful because it ensures consistency across the entire project, regardless of who or what is doing the implementation.

### 2\. Specify Command

The `spec` command implements the "Specify" phase of SDD, answering the "what" question.

**What it does:**

- Executes the `create-new-feature` script
- Creates feature branches and initializes specification files
- Generates structured documentation in the `specs/branch-name/` directory

**Generated Files:**

- `specs/branch-name/checklists/requirements.md`: Detailed requirements checklist
- `specs/branch-name/spec.md`: The primary specification document

**Workflow:**

1. Developer initiates a new feature
2. Script creates the appropriate directory structure
3. Templates are populated with project-specific context
4. Specification document is ready for refinement

This is where you define exactly what needs to be built, without getting into implementation details. Here’s what a specification document looks like:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ezbLicINLycZz9IvKJ9iEg.png)

### 3\. Plan Command

The `plan` command implements the "Plan" phase, addressing technical implementation details.

**What it does:**

- Executes `setup-plan` and `output-agent-content` scripts
- Generates comprehensive planning documentation
- Creates GitHub Copilot-specific instructions

**Generated Files:**

- `plan.md`: Overall implementation plan
- `research.md`: Investigation of technical options
- `data-model.md`: Database schemas and data structures
- `contracts.md`: API contracts and interfaces
- `quickstart.md`: Getting started guide
- `copilot-instructions.md`: Specific instructions for GitHub Copilot agent

**Workflow:**

1. Loads spec.md and constitution.md for context
2. Executes Phase 0 (Research)
3. Executes Phase 1 (Design)
4. Runs `update-agent-context` to maintain AI context
5. Completes the planning workflow with all documentation

The plan template goes as follows:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*fER-bXTYA6OINld-tXClkw.png)

And here’s what an actual generated plan.md looks like:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HPDRFHW-qb5p59Dymn1S5w.png)

I love how this automatically creates comprehensive documentation that guides both human developers and AI agents through the implementation process.

### 4\. Tasks Command

The `tasks` command breaks down the plan into actionable, testable increments.

**What it does:**

- Executes `check-prerequisites` script to validate readiness
- Validates that all necessary documentation exists (spec, plan, data model, etc.)
- Generates a task breakdown

**Generated Files:**

- `specs/branch-name/tasks.md`: Detailed task list with tracking

**Task Characteristics:**

- Actionable: Each task can be clearly defined and executed
- Testable: Completion can be verified
- Independent: Tasks can be worked on in parallel where possible
- Phase-based: Organized by development phase
- Time-bounded: Estimates for completion

Here’s what a task breakdown looks like:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CvOS861gZHeth7ILiObWaQ.png)

This is where the rubber meets the road — breaking down the plan into concrete, actionable steps.

### 5\. Implement Command

The `implement` command brings specifications to life by generating actual code.

**What it does:**

- Executes various commands (git operations, code generation, etc.)
- Leverages GitHub Copilot for code generation
- Updates task tracking

**Generated Artifacts:**

- Project source code
- Updated `tasks.md` with completed items marked

**Workflow:**

1. Processes task list sequentially or in parallel
2. Uses GitHub Copilot to generate code based on specifications
3. Executes git operations for version control
4. Updates progress tracking
5. Provides status on completed and remaining work

**Critical Principle**: Implement code step-by-step based on phases or tasks. Avoid generating the entire project all at once.

I learned this the hard way — generating too much code at once makes it difficult to review and verify. Better to work in small increments.

The app finally built based on the SDD workflow looks like this:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*j5OL0ZtRTvrQiKPHBAPcGA.png)

## Practical Implementation Tips

From my experience working with SpecKit, here are some key insights:

1. **Start with Familiar Projects**: Begin with a project you know well — where you understand both the business requirements and code implementation. This allows you to validate SpecKit’s output effectively.
2. **Follow Official Examples**: Track GitHub’s official projects from scratch to understand the SDD approach and SpecKit’s operating principles. This really helped me get up to speed quickly.
3. **Human in the Loop**: Do not place absolute trust in AI. Human intervention and manual verification are necessary at critical steps to gradually build confidence in the tool. This is particularly important when you’re first getting started.

## Summary

Spec Driven Development represents a significant evolution in software development methodology, particularly well-suited to the AI-assisted programming era. GitHub SpecKit provides a practical, implementable framework for applying SDD principles, integrating seamlessly with GitHub Copilot to create a powerful development workflow.

By moving from the informality of vibe coding to the structured approach of SDD, teams can achieve:

- **Higher Quality Code**: Clear specifications lead to better AI-generated code
- **Better Maintainability**: Living documentation evolves with the codebase
- **Improved Collaboration**: Common language for all stakeholders
- **Scalable Process**: Approach works from prototypes to production systems
- **AI Optimization**: Well-structured context enables better AI agent performance

As AI continues to transform software development, methodologies like SDD that provide structure and clarity will become increasingly important. GitHub SpecKit offers a practical path forward, allowing teams to embrace AI-powered development while maintaining the discipline and quality standards essential for successful software projects.

In my next articles, I’ll share more about advanced SDD techniques and how to integrate them with existing development workflows. But for now, I encourage you to try SpecKit with one of your own projects — you might be surprised at how much it transforms your AI-assisted development process.

