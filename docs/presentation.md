---
marp: true
theme: default
class: invert
size: 16:9
style: |
  img {background-color: transparent!important;}
  a:hover, a:active, a:focus {text-decoration: none;}
  header a {color: #ffffff !important; font-size: 30px;}
  footer {color:rgb(255, 255, 255);}
header: '[&#9671;](#1 " ")'
footer: 'Accenture 2025'
paginate: true
---

<!-- backgroundImage: "linear-gradient(to bottom,rgb(161, 0, 255),rgb(136, 0, 141))" -->
<!-- color: white -->
<!-- _class: lead -->

<!-- _speaker: Reminder, the _speaker element is used in order to define speaker notes. -->
<!-- _speaker: Good luck on the presentation champ -->

# IVR Development Stack: ADK, A2A, and Gemini Live
Presented By: Bear BlinSchauer

---

## Table Of Contents
- Introduction
- Architecture Overview
- Agent Development Kit (ADK) [to slide 1](./presentation.html#1)
- Agent To Agent Protocol (A2A)
- Gemini Live API
- Model Context Protocol (MCP)
- Putting It All Together: Demo Walkthrough
- Deployment & Operations
- Final thoughts, Team Learning

---

<!-- _class: lead -->
# Introduction

---

## What is Googles Agent Development Stack?

- A modern, modular platform for building intelligent, voice-driven customer experiences.
- Combines Google’s Agent Development Kit (ADK), the Agent-to-Agent (A2A) protocol, MCP, and Gemini Live API.
- Software driven method of enabling seamless, real-time collaboration between AI agents and users via voice and text.

---

## Why Does This Matter?

- **Faster, smarter customer service:** Automate and enhance IVR (Interactive Voice Response) systems with advanced AI.
- **Interoperability:** Open standards (A2A/MCP) allow agents from different vendors and platforms to work together.
- **Real-time, multimodal:** Gemini Live enables natural, low-latency voice and text interactions.
- **SWE Approach** Higher flexibility and design control. Faster iteration.

---

## What Will You Learn Today?

- The core technologies powering next-generation IVR systems.
- How ADK, A2A, and Gemini Live work together in a unified stack.
- A live demo
- Key concepts, architecture, and practical implementation tips.
- Actionable steps to get started.

---

## Key Takeaways

- The ADK IVR stack is flexible, extensible.
- Open standards and Google’s AI tools make it easy to build, scale, and integrate.
- You’ll leave with a clear understanding of the stack and how to start building with it.

<!-- _class: lead -->
---

# Architecture Overview

---

## Google's Agentic AI IVR Stack
- ADK: builds the agents, like a customer service bot.
- A2A: enables teamwork, allowing the bot to escalate issues to a billing agent built on adiferent platform
- Gemini Live: Acts as a layer to convert human speech into usable AI tokens in real time.
- MCP: Connects agents to data and external APIs
- LLM's: Any models can work with ADK. Gemini models are better equipped for tool use. (According to google)
- A CI System Such as Cloud Build & Agent Orchestration will be needed to roll out the project once built. 

---
## How this all works together

*{Put a diagram of how all of the components will work together here.}* 

![](./aistack..svg)


---
<!-- _class: lead -->

# Agent Development Kit (ADK)
*Google’s Toolkit for Building AI Assistants*

---

## About ADK
ADK or App Development Kit is agentic chatbot framework made by google.
ADK consists of an SDK which helps developers designed and deploy AI Agents. Currently ADK is best supported in python. ADK also has java bindings.

ADK is …
- Model Agnostic
- Deployment Agnostic
- Interoperable with other technolgy

---

## What ADK can do
ADK is a technology which can be used in order to configure agents in a SWE oriented fashion. ADK allows the creation of agentic AI driven agents with the ability to be integreted into systems such as IVR. ADK offers team high flexibility in building new AI agents.

---

## ADK core capabilities

- Orchestration
- Multiple subagents (No A2A needed)
- Tools
- Deployment: Integrated with google CI (Agent Engine).
- Testing: ADK provides test framework for testing agents.
- Security: Can sanatize user inputs via callbacks.

---

**Implementing Capabilities:**
- Orchestration works via the llm decisions by multi-agents during execution or by the decisions of developers. ADK uses the sequential, loop and parallel agent types to manage orchestration.
- Tools work via python functions. Agents will read the docstrings attached to python functions in order to understand how to interface with these functions. Additionally users have access to a tool ecosystem maintained by google. 
- Developers define the core behaviour and logic via agent prompts (similar to playbooks) and python methods.
- Manage agent lifecycles, state, and memory. ADK offers short term session state memory and long term knowledge options
- Integrate agents with data. ADK has some built in functions to deal with MCP.
- Safety Input and tool argument guardrails with before_model_callback and before_tool_callback
    Both of these are really simple callback functions which are supplied tool calling context or response context to filter out responses which the team would like to avoid. ADK wil look for an additional optional response for each failed sanitization check.
    While by default this approach favors regex, using an additional llm with the google.genai library could also work very well.
---

## ADK SDK

- ADK provides developers with a rich SDK. The ADK SDK consists of a well documented API.
- During playbook development a simple web UI is already provided for testing agents.

---

## ADK compared to dialogflow playbooks

ADK works in a very similar manner to dialogflow agents but there are some differences
- An ADK agent powered by an llm is analagous to a playbook.
- Developers will handle additional routing on their own with python.
- Compared to playbooks, as of now playbooks does not have examples capabilities. Developers will need to introduce few shot prompting instead.
- ADK does not handle NLU intent detection.

---
# ADK in-depth

---

**Docs**
- https://google.github.io/adk-docs/
- https://github.com/google/adk-samples

ADK examples can be found in the agent garden in GCP.

---

With recent innovations ADK is beginning to add support for live voice via the **Gemini Live** API

In order to use arbitrary models along with gemini, ADK utilizes the LiteLLM library.

Agents can act as powerful reasoning skill agents or determenistic routing agents depending on the context. Determenistic agents are called workflow agents.

---

### Key Ideas
- Agent: Worker unit for tasks
- Tools:
    - Tools can be either python functions or tools built into ADK by google. 
    - AIs have the option to use google search without any extra setup which is a powerful way to easily make more accurate responses. 
    - Documentation strings are essential to creating a tool in ADK. The bots will be reading these strings in order to determine how to interface with them.
- Callbacks:
    - Functions which can be called before or after a agent, model interation, or tool use. These callbacks are given the agent context and can be used for logging and sanitization. 
- Session management: 
    - Context is the session
    - History is a log of chat events
    - State represents agents working memory
- Events: 
    - Basic units of data representing conversation flow. (reply, user messaged, tool use) Together events will form the conversation history.

---

### Key Ideas Cont.

---

### Important Data Types, Classes and Functions
- Callbacks: custom code snippets written into points in the agents process allowing for checks, logging or behavior modifications. set the callback in agent initialization, -> before_model_callback=block_keyword_guardrail
- Grounding: ADK agents can be "Grounded" by using google search as a tool. 
- Memory: Memory is different from state. Allows agents to recall information across multiple sessions.
    - SessionService: Responsible for managing conversation history and state for different users and sessions. 
    - The InMemorySessionService is a simple implementation that stores everything in memory, suitable for testing and simple applications. It keeps track of the messages exchanged. 
    - Session state: Tied to a specific user session. Persists information across multiple conversational turns within that session. 
    - Agents are able to insert data into the session state with the output key parameter. Agents have access to elements of the session state by putting the state data name in curly brackets.
- Artifact managment: There are classes desinged to allow agents to handle files or binary data.
    - ToolContext: Provides the context for a tool invocation, provides access to the invocation context, function call ID, event actions, and authentication response. Provides memory retrieval methods and methods for listing artifacts.
- Runner: This data class is responsible for handling all execution flow, orchestrates agent interactions based on events and coordinates with backend services. 
- Agent: Agent class is a label for the llm class. There are llm agents and workflow agents.
    - LlmAgent: This class is the most essential class for quickly creating agents. Every ADK package should have a root_agent object exposed for the ADK SDK and front end tools to use. 
    - Sequential Agent: Agent class which will execute sub agents in order. Useful for determenistic steps where tasks need to be completed in order. 
    - Loop Agent: This is a specialized agent class which runs sequential agents until a specific condition is met. 
    - Parallel Agent: Runs agents asyncronously. If the output of agent work is data, a merger agent might be necessary.
    - Custom Agents: ADK allows users to inherit from the BaseAgent class in order to create agents with more complex state managment or determenistic flows. 
        Overriding the _run_async_impl method is the primary way of defining behavior on agent invocation.
        The heart of any custom agent is the _run_async_impl method. This is where you define its unique behavior.
    - Driving classes: You can create a class whith a has a relationship with many agents and handles orchestration.       
        Making custom classes or inheriting BaseAgent is very useful to handle complex things like A2A interaction. 

### Agent Deployment
Deploying to cloud is essential to building the agent. Google offers many different options Vertex AI comes with an sdk to help with CI/CD configurations. 
Agents are accesible through a specialized agent engine UI 

https://google.github.io/adk-docs/deploy/agent-engine/



# Agent to Agent Protocol (A2A)

# Gemini live API

# Demo Walkthrough

# Getting accustomed to the ADK development environment



3 Putting It All Together: Demo Walkthrough


# A2A in-depth
*The Universal Language for AI Collaboration*

**Docs**
- https://github.com/a2aproject/A2A/blob/main/docs/tutorials/python/1-introduction.md
- https://github.com/a2aproject/a2a-samples

## About A2A
While Originally Owned by google, Ownership of the A2A protocol has moved over to the linux foundation who is committed to keeping this technology open source. 

A2A is an Open standard, common language for AI agent communication and collaboration.
A2A works with tools such as:
- Google ADK
- LangGraph
- CrewAI
- Genkit

At a high level A2A is used to:
- Offer direct, standardized communication and collaboration between different AI agents, even if they are running as separate services or on different machines.
- Agents to discover each other's capabilities (via Agent Cards) and delegate tasks. This is crucial for our Orchestrator agent to interact with the specialized Planner, Social, and Platform agents.
- Form a network of collaborating asynchronous AI agents. 

**From the blog:**
- A2A is built on existing standards (HTTP, SSE, JSON-RPC)
- Complements the MCP protocol which is made by Anthropic
- Very new Tech, may face issues on the bleeding edge.
- Google has partnered with over 50 businesses one of them being accenture. Ths means that there is almost certainly someone in KX who is an expert on the topic.
*Scott Alfieri, Is specifically quoted in the announcement blog. He is an AGBG global lead*

## A2A deeper dive

**A2A Facilitates the interaction between 3 key parties:**
- End User: A human
- Client Agent: Responsible for creating requests and handling end user actions. As client agent you:
    - Fetch and understand agent cards. 
    - Send messages
    - Process responses. 
    - Handle & Manage Task IDs for Tasks which take time and ping for Task completion.
- Remote Agent: Responsible for acting on requests made, take correct action. As a server/remote agent you:  
    - Host agent cards with skills and capability info
    - Handle Incoming agent requests and execute them via agentExecutor.

**Main Capabilities of A2A** 
1. Agent Discovery:
    - Before an A2A can do anything on the protocol it first needs to define what is can do and how other agents would interact with its capabilities.
    - Agents can advertise their capabilities using an "Agent Card" in JSON format, allowing the client agent to identify the best agent for a task.
    - Agent cards act as a robots.txt to help classify and index agents available on an A2A network.
    - This means clients know when and how to utilize agents
2. UX Negotiation:
    - Clients and agents will agree on communication methods.
    - The client and remote agent to negotiate the proper format and user interface capabilities.
3. Task Management:
    - Clients and agents have mechanisms to communicate task status, changes and dependencies throughout task execution.
    - The "Task" object is defined by the protocol and has a lifecycle.
4. Collaboration:
    - Agents can send messages to each other to convey context, responses, artifacts, or user instructions.
    - Dynamic interactions.
    - Agents request clarifications from the end user as well

**A2A Agent interaction pipeline:**
	End-User -> Client -> Client Agent -> Agent Mesh
Interaction Timeline:
1. Agent discovery: Client Agent will search remote agent to find capabilities thru agent.json file
2. Interactions: Bots will send JSON RPC messages to each other over https. Inside are A2A Objects:
	a. Messages, One turn in the operation. 
		i. Roles (user/agent)
		ii. Parts (text, file or JSON)
	b. Agent Executor. Class which links the protocol plumbing to agent logic.
	c. Task Objects: 
		i. Contains ID and status
		ii. Client agent can call tasks get function to query task completion status
		iii. Eventually returns task as completed with summary in task.artifacts
3. Streaming: Server agent can push updates to a task as they happen instead relying on polling and sending all in one once done.


### Important Classes, Data Types, and functions
**Agent Skills:** (Can be created as python classes)
Describes a specific capability or function which the agent can perform. 
- Id: skill identifier
- Name: human readable name
- Description: A detailed explanation of what the skill does
- Tags: keywords for categorization & discovery
- Examples: Sample use cases & prompts
- I/O Modes: Supported Media for I/O (text, or JSON, etc.)

**Agent Card:** (Can be created as python classes, or JSON classes)
JSON document which A2A server makes publicly available, usually stored at .well-known/agent.json (analagous to robots.txt or business card)
Agent cards are a crucial part of creating an agent network. 
- Name, Description, Version: Basic Identity Info
- Url: Endpoint where the A2A service can be reached
- Capabilities: Specified supported A2A features (streaming, pushnotifications etc.)
- Default I/O modes: Default Media types for agent
- Skills: list of the AgentSkill objects outline earlier. 

**Agent Executor:**
Core logic of how A2A agents process requests & generate responses. The A2A sdk provides the abstract class ```a2a.server.agent_execution.AgentExecutor``` to implement
Links the A2A protocol plumbing together. (A2A SDK & logic of our agent)
SDK will handle http, json rpc & event management. 
The AgentExecutor executor class has two main methods:
-  Execute(self, contecxt: RequestContext, event_queue: EventQueue) Handles requests which expect a response or an even stream. Users input is contents, and event queue is used to send back data objects. 
-  Cancel(self, context: RequestContext, event_queue: EventQueue): Handles requests to cancle running tasks. 
Event queues are objects which queue up data to be sent

**Task Object:**
Job which an agent needs to do. Has an ID and a status on the progress for every task. 
An agent can periodically call tasks get in order to get the task status of another agent. 
A completed task will contain a summary in a file named task.artifacts. 

### Servince A2A Content
A2A sdk provides the A2AStarletteApplication class to simplify getting an A2A compliant HTTP server running. This class uses Starlette for the web server and is run in conjunction with a server such as Uvicorn

The DefaultRequestHandler is a class which will take whichever AgentExecutor and TaskStore which are provided and then apply the appropiate routing for new A2A RPC calls based on the info given. 
TaskStore Class is used to manage the lifecycle of tasks, useful for stateful interactions, streaming and resusbscription. Task stores are required
A2AStarletteApplication is a class which will take in the agent card and request handler objects, then the proper endpoints and files will be exposed.
Ucivorn.run(Server_builder.build()) the A2AStarletteApplication has a build method to construct the application. The application is then run using uvicorn.run for http access.
The host and port numbers are specified to uvicorn as well. Make sure this matches the url in agent card.

### Additional Tools in A2A SDK
A2A Python Library (a2a-python):
- a2a-python is the concrete library used to make our ADK agents speak the A2A protocol. It provides server-side components needed to:
	- Expose our agents as A2A-compliant servers.
	- Automatically handle serving the "Agent Card" for discovery.
	- Receive and manage incoming task requests from other agents (like the Orchestrator)

A2A Inspector:
- The A2A Inspector is a web-based debugging tool used to connect to, inspect, and interact with A2A-enabled agents. 
- While not part of the final production architecture, it is an essential part of development workflow. 
- It provides:
	- Agent Card Viewer: To fetch and validate an agent's public capabilities.
	- Live Chat Interface: To send messages directly to a deployed agent for immediate testing.

Debug Console: To view the raw JSON-RPC messages being exchanged between the inspector and the agent.

# Gemini live in-depth
*Low latency, two-way voice interactions.*

## About Live API
Gemini live offers:
- Real time multimodal understanding (video and audio)
- Integration with tools such as function calling and grounding with google search. 
- Low latency -> almost human like interactions
- Multilingual
- With native audio:
    - Gemini can understand the users toneof voice
- Context awarness, disregards ambient conversations.

Audio must be in these formats:
- Input audio: Raw 16-bit PCM audio at 16khz, little-endian
- Output audio: Raw 16-bit PCM audio at 24kHz, little-endian

ADK natively supports using gemini live but you will need to use a gemini model which supports the Live API. 
See https://cloud.google.com/vertex-ai/generative-ai/docs/live-api a list of model options.
Right now the Gemini live API is only supported with the gemini-lice-2.5-flash models.

## Using the API

**Implementation options:**
- Server-to-server. Backend will connected to the live API using websockets. Clients will send streams of data to your server which then forwards it to the API.
- Client-to-server. Frontend code will connect directly to googles servers using websockets to stream data. 
Client to server is more performant and easier to set up. 

**Docs:**
https://ai.google.dev/gemini-api/docs/live-guide


Here is a Diagram of a possible agent stack. 

![alt text](images/image.png)

# MCP in-depth


# Deployment & Operations

# Team Learning, Final thoughts

---
<!-- _class: lead -->

# Team Learning

In order to adopt an ADK system people on the team will need to adopt some key skills and be able to adapt to a software driven workstream.

---

- **Git:** Using git will be a required skill for any software driven project. In order to avoid conflicts git basics and best practices are advised to take into consideration. 
- **Python:** (Minimal python knowledge is required to write agent prompts)
    - Python basics: variables, math, dictionaries etc.
    - Python classes. (OOP design)
    - Asyncronous python
- **JSON:** Neededed to write agent cards.
- **Web:** Need to understand API basics and websocket for streaming. (Gemini live/ A2A).
- 

---
<!-- _class: lead -->

## Creating a development environment.

---

---
<!-- _class: lead -->

# Final Thoughts

As we’ve explored today, Google’s Agent Development Stack—comprising ADK, A2A, MCP, and the Gemini Live API—represents a powerful shift in how we build, deploy, and scale intelligent agents.

---

## Key reflections

- Modular by Design: Each component is purpose-built but interoperable, enabling flexible, scalable agent architectures.
- Open Standards: Protocols like A2A and MCP are paving the way for cross-platform, multi-agent collaboration.
- Voice-First: Gemini Live and ADK bring real-time, multimodal interaction to the forefront of customer experience.
- Developer-Centric: With Python-first SDKs, callback hooks, and CI/CD support, this stack empowers engineers to build with precision and control.

---

# Thank You
Let’s continue exploring, building, and learning together.
Questions? Ideas? Let’s talk.

---

# Extra Notes

-
-
-
-
-
-
-
-
-
-
-


- Python and software development basics: (Minimal python knowledge is required in order to write agent prompts.)
- Command line basics (to set up adk testing servers)
- Google cloud console and ADK deployment.
- Basic JSON knowledge (to write agent cards.)
- Documentation understanding
- Understanding of web for A2A servers.
- Understanding of websocket and live audio streaming for gemini live implementations.


**Study guide for ADK & A2A python**
*Prompt developer*
- Elementary python (Variables, math, print logging, etc.)
- Basics of functions
- Docstrings
- Basics of python dictionaries. (dictionaries are very similar to JSON objects.)
- Python module interaction
*Agent Orchestration developer*
- Asyncronous functions & Asyncio
- Basics of python classes. (Classes are templates for objects, objects are groupings of function and variable data.)
- Intermediate classes knowledge, inheritance, writing classes, factory methods.


