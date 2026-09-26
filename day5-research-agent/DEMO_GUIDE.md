# Day 5 Research Agent - Demo Guide

## 🕵️ About This Lab

A fully autonomous research agent that plans, searches, analyzes, writes, reviews, and saves research reports. The agent uses a local sample knowledge base and demonstrates the multi-step agentic workflow.

**Key Concept:** AI agents can break complex tasks (research) into smaller steps, call tools (search), and iterate toward a complete solution without human intervention.

---

## 🚀 Quick Start

```bash
# Navigate to the directory
cd day5-research-agent

# Activate virtual environment (if not already activated)
source venv/bin/activate

# Ensure .env file exists with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run the Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📚 Sample Knowledge Base

The agent searches from a local knowledge base with 6 pre-built sources:

1. **AI in Education** — personalized learning, tutoring, student privacy concerns
2. **AI for Small Business** — customer support, marketing, automation, inventory
3. **AI Agents Overview** — multi-step task systems, tools, workflow logic, guardrails
4. **Responsible AI Basics** — safety, fairness, privacy, transparency, oversight
5. **RAG and Knowledge Assistants** — retrieval-augmented generation for knowledge bases
6. **AI in Customer Support** — ticketing, routing, summarization, human review

---

## 📋 Demo Scenarios & Sample Topics

### **Understanding Deterministic vs Non-Deterministic Steps**

Before running scenarios, understand that the agent has both types of steps:

| Step Type | 🔍 Deterministic | ⚙️ Non-Deterministic |
|-----------|-----------------|----------------------|
| **Happens in** | Search, Save | Plan, Analyze, Write, Review |
| **Always produces** | Same sources for same topic | Different wording, structure, emphasis each run |
| **Why?** | Uses keyword matching (algorithm) | Uses LLM (probabilistic AI model) |
| **What to expect** | Identical results every run | Similar content, different phrasing |
| **Testing implication** | Verify sources are relevant | Verify core concepts are covered |

**Important:** When testing, don't expect word-for-word identical reports. Instead, verify that:
- ✅ Same sources are retrieved (deterministic)
- ✅ Core concepts are covered (content-wise consistent)
- ✅ No hallucinations appear (facts grounded in sources)
- ✅ Structure follows the prompt format (always has sections like "Executive Summary")

---

### **Scenario 1: AI in Business Applications**
*Best for testing agent planning and multi-source synthesis*

**Topic:** `"How can small businesses use AI for customer support?"`

**Expected Agent Workflow:**
1. ✅ **Plan** ⚙️ *Non-Deterministic (LLM)* — Outlines approach (define use cases, benefits, challenges, implementation tips)
2. ✅ **Search** 🔍 *Deterministic (Keyword matching)* — Always retrieves: AI for Small Business, AI in Customer Support, Responsible AI
3. ✅ **Analyze** ⚙️ *Non-Deterministic (LLM)* — Extracts key findings (common use cases, tools, guardrails)
4. ✅ **Write** ⚙️ *Non-Deterministic (LLM)* — Generates report with introduction, findings, recommendations
5. ✅ **Review** ⚙️ *Non-Deterministic (LLM)* — Validates clarity, checks for hallucinations, improves flow
6. ✅ **Save** 🔍 *Deterministic (File I/O)* — Report saved to `reports/how_can_small_businesses_use_ai_for_customer_support_YYYYMMDD_HHMMSS.md`

**What to Look For:**
- ✅ Report mentions 3+ concrete use cases (answering FAQs, routing tickets, summarization)
- ✅ Includes concerns like human oversight, complexity, integration
- ✅ Sources are properly attributed
- ✅ No made-up facts about real tools or services

**Note on Variability:** Each run will produce slightly different wording in Plan, Analysis, and Report (LLM is probabilistic). But the sources retrieved will always be the same 3-4 sources. If you run this scenario twice, you'll see different text but same content structure.

---

### **Scenario 2: AI Agent Fundamentals**
*Tests understanding of agent architecture and guardrails*

**Topic:** `"What are AI agents and how do they work?"`

**Expected Agent Workflow:**
- **Plan** ⚙️ *Non-Deterministic (LLM)* — Covers definition, architecture, examples, benefits, risks
- **Search** 🔍 *Deterministic (Keyword matching)* — Always retrieves: AI Agents Overview + Responsible AI + others matching keywords
- **Analyze** ⚙️ *Non-Deterministic (LLM)* — Extracts components (model, tools, memory, workflow, guardrails)
- **Write** ⚙️ *Non-Deterministic (LLM)* — Explains agent loop, decision-making, tool calling
- **Review** ⚙️ *Non-Deterministic (LLM)* — Checks technical accuracy and clarity for beginners
- **Save** 🔍 *Deterministic (File I/O)* — Report saved with timestamp

**What to Look For:**
- ✅ Clearly explains the agent loop (plan → search → analyze → write → review)
- ✅ Mentions tools and how agents use them
- ✅ Addresses guardrails and safety
- ✅ Uses language appropriate for beginners

**Note on Variability:** The sources found will always be the same (AI Agents Overview is highly relevant). But explanations will vary. Run this twice to see how the LLM rephrases the same concepts differently.

---

### **Scenario 3: Responsible AI and Governance**
*Tests agent's ability to gather and synthesize ethical considerations*

**Topic:** `"What are the key principles of responsible AI?"`

**Expected Agent Workflow:**
- **Plan** ⚙️ *Non-Deterministic (LLM)* — Identifies framework (fairness, safety, privacy, transparency, human oversight)
- **Search** 🔍 *Deterministic (Keyword matching)* — Always retrieves: Responsible AI Basics as primary + other relevant sources
- **Analyze** ⚙️ *Non-Deterministic (LLM)* — Extracts principles and real-world implications
- **Write** ⚙️ *Non-Deterministic (LLM)* — Describes each principle with examples
- **Review** ⚙️ *Non-Deterministic (LLM)* — Ensures balanced, practical tone
- **Save** 🔍 *Deterministic (File I/O)* — Report saved

**What to Look For:**
- ✅ Report covers 4+ key principles
- ✅ Explains why each principle matters (business, user safety, reputation)
- ✅ Mentions concrete implementation steps
- ✅ Grounded in provided sources, not generic advice

**Note on Variability:** Responsible AI Basics will always be retrieved. LLM may emphasize different principles on different runs. The framework stays consistent, but prioritization and examples vary.

---

### **Scenario 4: Educational AI Applications**
*Tests retrieval and report generation for specific domain*

**Topic:** `"How is AI changing education and what are the risks?"`

**Expected Agent Workflow:**
- **Plan** ⚙️ *Non-Deterministic (LLM)* — Outlines opportunities (personalization, tutoring) and risks (privacy, bias, accuracy)
- **Search** 🔍 *Deterministic (Keyword matching)* — Always retrieves: "AI in Education" + "Responsible AI Basics" (always same 2-4 sources)
- **Analyze** ⚙️ *Non-Deterministic (LLM)* — Connects technical capabilities to educational outcomes and concerns
- **Write** ⚙️ *Non-Deterministic (LLM)* — Balances benefits and risks in structured report
- **Review** ⚙️ *Non-Deterministic (LLM)* — Ensures fair, evidence-based framing
- **Save** 🔍 *Deterministic (File I/O)* — Report saved

**What to Look For:**
- ✅ Mentions specific use cases (personalized practice, lesson summarization)
- ✅ Addresses student privacy and data protection
- ✅ Discusses potential bias in AI systems
- ✅ Recommends oversight and responsible policies

**Note on Variability:** Education + AI terms guarantee consistent source retrieval. But how risks are framed, depth of analysis, and recommendation priority will differ between runs.

---

### **Scenario 5: RAG and Knowledge Systems**
*Tests agent's ability to explain technical concepts*

**Topic:** `"What is RAG and why would a company use it?"`

**Expected Agent Workflow:**
- **Plan** ⚙️ *Non-Deterministic (LLM)* — Defines RAG, compares to fine-tuning, lists use cases
- **Search** 🔍 *Deterministic (Keyword matching)* — Always retrieves: "RAG and Knowledge Assistants" (highly relevant) + 2-3 others
- **Analyze** ⚙️ *Non-Deterministic (LLM)* — Identifies benefits (factual accuracy, up-to-date info, lower cost)
- **Write** ⚙️ *Non-Deterministic (LLM)* — Explains mechanics, provides examples
- **Review** ⚙️ *Non-Deterministic (LLM)* — Checks technical correctness
- **Save** 🔍 *Deterministic (File I/O)* — Report saved

**What to Look For:**
- ✅ Clearly explains retrieval-augmented generation mechanism
- ✅ Lists relevant use cases (knowledge bases, policies, manuals)
- ✅ Explains why RAG reduces hallucinations
- ✅ Compares to other approaches (fine-tuning, prompting)

**Note on Variability:** RAG Basics source is always retrieved (high relevance). Technical depth and comparison emphasis will vary. Run twice to see different explanations of the same core concepts.

---

---

## ⚡ Complete Pipeline: Inputs → Processing → Outputs

```
STEP 1: PLAN
├─ Inputs: Topic only
├─ Processing: LLM creates research plan
├─ Output: Plan document (stored but not used yet!)
└─ LLM Role: "research planning assistant"

STEP 2: SEARCH
├─ Inputs: Topic (Plan ignored ❌)
├─ Processing: Keyword matching on sources
├─ Output: 4 ranked sources (deterministic ✅)
└─ No LLM involved

STEP 3: ANALYZE
├─ Inputs: Topic + 4 Sources (Plan ignored ❌)
├─ Processing: LLM extracts insights from sources
├─ Output: Analysis (findings, risks, limitations)
└─ LLM Role: "research analyst"

STEP 4: WRITE ← ✅ PLAN FIRST USED HERE!
├─ Inputs: Topic + Plan + Analysis + Sources
├─ Processing: LLM synthesizes everything
├─ Output: Structured research report
└─ LLM Role: "professional research report writer"

STEP 5: REVIEW
├─ Inputs: Topic + Report (Plan not used ❌)
├─ Processing: LLM checks quality
├─ Output: Review feedback
└─ LLM Role: "careful report reviewer"

STEP 6: SAVE
├─ Inputs: Report + Review
├─ Processing: Save to disk
├─ Output: Markdown file in reports/ directory
└─ No LLM involved
```

## 📊 What Each Step Uses (Complete Matrix)

| Step | Topic | Plan | Sources | Findings | LLM Call |
|------|-------|------|---------|----------|----------|
| **Plan** | ✅ Input | - | - | - | ✅ #1 |
| **Search** | ✅ Input | ❌ | - | - | ❌ |
| **Analyze** | ✅ Input | ❌ | ✅ Input | - | ✅ #2 |
| **Write** | ✅ Input | ✅ **Input** | ✅ Input | ✅ Input | ✅ #3 |
| **Review** | ✅ Input | ❌ | ❌ | - | ✅ #4 |
| **Save** | ❌ | ❌ | ❌ | ❌ | ❌ |

**Key Insight:** Only the WRITE step uses the plan to synthesize all information into a coherent report.

---

## 🧪 Testing Checklist

- [ ] **Agent Execution**
  - [ ] App loads without errors
  - [ ] Text input accepts research topic
  - [ ] "Run Research Agent" button is clickable
  - [ ] Agent runs and completes without timeout
  - [ ] Shows "Agent completed the task" success message

- [ ] **Agent Steps Display**
  - [ ] All 6 steps show: Plan → Search → Analyze → Write → Review → Save
  - [ ] Each step has a ✅ checkmark
  - [ ] Details are accurate (e.g., "Retrieved 4 sources")
  - [ ] Steps appear in correct order

- [ ] **Research Plan**
  - [ ] "View Research Plan" expander is functional
  - [ ] Plan is structured with clear outline/bullets
  - [ ] Plan is relevant to the topic entered
  - [ ] Plan is written in accessible language

- [ ] **Retrieved Sources**
  - [ ] "View Retrieved Sources" expander works
  - [ ] Shows 4 sources with title, source, URL, score
  - [ ] Sources are ranked by relevance score
  - [ ] Content snippets are readable and relevant
  - [ ] Scores make sense for the topic

- [ ] **Source Analysis**
  - [ ] "View Source Analysis" expander displays findings
  - [ ] Findings synthesize multiple sources
  - [ ] Identifies key themes and connections
  - [ ] Analysis is grounded (doesn't add new information)

- [ ] **Final Report**
  - [ ] Report is well-structured with clear sections
  - [ ] Report has introduction, body, conclusion
  - [ ] Uses information from retrieved sources
  - [ ] No hallucinations (all facts are in sources)
  - [ ] Clear, professional tone

- [ ] **Report Quality**
  - [ ] Report is 200+ words and substantive
  - [ ] Includes specific examples from sources
  - [ ] Agent Review Notes section is present
  - [ ] Review feedback is constructive and accurate

- [ ] **Write Step Specific**
  - [ ] Report has all 8 sections (Executive Summary, Key Findings, Use Cases, Risks, Recommendations, Sources, Takeaway)
  - [ ] Report uses findings from step 3 analysis
  - [ ] Report follows the plan's research goals
  - [ ] Sources are cited at the end
  - [ ] Recommendations are practical and actionable
  - [ ] No new facts invented (only from provided sources)

- [ ] **Download Feature**
  - [ ] "Download Research Report" button appears
  - [ ] Downloaded file is named "research_report.md"
  - [ ] File saves to your downloads folder
  - [ ] File contains the full report in markdown format

- [ ] **File Persistence**
  - [ ] Report is saved to `reports/` directory
  - [ ] File name includes topic + timestamp
  - [ ] File path shown in caption is correct
  - [ ] Can navigate to `reports/` and find the file

- [ ] **Determinism Testing**
  - [ ] Run the same topic twice
  - [ ] **Sources should be identical** (deterministic search)
  - [ ] **Report wording will differ** (non-deterministic LLM)
  - [ ] Core findings and structure should be similar (same sections, concepts)
  - [ ] No hallucinations in either run (facts grounded in sources both times)

---

## 📊 What You're Testing

1. **Agent Planning:** Can the agent break down a complex research task into steps?
2. **Information Retrieval:** Does search find relevant sources?
3. **Source Synthesis:** Can the agent connect findings across multiple sources?
4. **Report Generation:** Does the agent write clear, structured reports?
5. **Self-Review:** Can the agent review its own work for accuracy?
6. **Persistence:** Are reports properly saved to disk?
7. **Multi-Step Workflow:** Does the entire agentic loop complete successfully?

---

## 🧠 Where LLM Gets Invoked

The research agent makes **4 LLM API calls** during its workflow. Understanding this architecture helps you trace where each output comes from.

### **LLM Call Flow**

```
User Input (research topic)
    ↓
1️⃣  LLM Call #1: PLAN
    └─ Prompt: build_research_plan_prompt()
    └─ Role: "research planning assistant"
    └─ Output: Research plan with key questions
    ↓
2️⃣  SEARCH (NO LLM CALL)
    └─ Uses: search_tool.py (local keyword search)
    └─ Output: Top 4 relevant sources
    ↓
3️⃣  LLM Call #2: ANALYZE
    └─ Prompt: build_source_analysis_prompt()
    └─ Role: "research analyst"
    └─ Input: Topic + Retrieved sources
    └─ Output: Key findings and insights
    ↓
4️⃣  LLM Call #3: WRITE
    └─ Prompt: build_report_prompt()
    └─ Role: "professional research report writer"
    └─ Input: Plan + Findings + Sources
    └─ Output: Full structured research report
    ↓
5️⃣  LLM Call #4: REVIEW
    └─ Prompt: build_review_prompt()
    └─ Role: "careful report reviewer"
    └─ Input: Topic + Generated report
    └─ Output: Review feedback and improvements
    ↓
6️⃣  SAVE (NO LLM CALL)
    └─ Uses: Python file I/O
    └─ Output: Report file to disk
```

### **Code Locations**

| File | Function | LLM Invocations |
|------|----------|-----------------|
| [research_agent.py](research_agent.py#L28) | `call_llm(prompt)` | Central entry point that calls `ask_ai()` |
| [research_agent.py](research_agent.py#L45) | `create_plan()` | **LLM Call #1** — builds research plan |
| [research_agent.py](research_agent.py#L62) | `analyze_sources()` | **LLM Call #2** — analyzes retrieved sources |
| [research_agent.py](research_agent.py#L69) | `write_report()` | **LLM Call #3** — writes the final report |
| [research_agent.py](research_agent.py#L82) | `review_report()` | **LLM Call #4** — reviews report quality |
| [llm_service.py](llm_service.py#L9) | `ask_ai(messages)` | Actual LLM API call handler |
| [agent_prompts.py](agent_prompts.py) | `build_*_prompt()` | Prompt templates for each LLM call |

### **LLM Configuration**

The LLM provider and model are controlled by environment variables in `.env`:

```bash
# Option 1: OpenAI (recommended for testing)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-mini  # or gpt-4, gpt-3.5-turbo, etc.

# Option 2: Ollama (local, no API key needed)
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=llama3.2:1b  # or any local model
```

### **How Search Query is Determined**

⚠️ **Current Behavior (Beginner Agent):**

The search does **NOT** use the plan to refine the query. Instead:

```python
# research_agent.py - Line 52-53
def search(self):
    sources = search_sources(self.topic, max_results=4)
    #                         ^ Uses original user input directly
    #                         NOT the plan created in step 1!
```

**Flow:**
```
User Input: "How can small businesses use AI for customer support?"
    ↓
Step 1 (Plan): Creates detailed research plan
    └─ But this plan is NOT used for search
    ↓
Step 2 (Search): Uses original user input topic
    └─ Keyword matching on: "small businesses", "AI", "customer support"
    ↓
Step 3 (Analyze): Uses retrieved sources (not informed by plan)
```

**Real-World Limitation:** If the plan suggests researching "ROI metrics" and "integration challenges", the search won't specifically look for those because it's using the original topic.

### **What Does the Analyze Step Actually Do?**

⚠️ **Important:** The analyze step does NOT use the plan either!

**Analyze Step Inputs:**
```python
def analyze_sources(self, sources):
    prompt = build_source_analysis_prompt(
        self.topic,      # ← Original user input (same as search!)
        sources          # ← The 4 sources retrieved
    )
    # Does NOT pass self.plan here!
```

**Analyze Prompt Structure:**
```
You are a research analyst.

Your task: Analyze the sources below for the research topic.

Research topic: [ORIGINAL TOPIC - e.g., "How can small businesses use AI?"]

Sources:
Source 1: [title, url, content]
Source 2: [title, url, content]
Source 3: [title, url, content]
Source 4: [title, url, content]

Rules:
- Use only the provided sources
- Do not invent facts
- Identify useful insights
- Mention limitations if sources are incomplete

Output format:
## Key Findings
## Useful Details
## Risks or Limitations
## Source Notes
```

**What's Being Analyzed:**
- ✅ **The 4 retrieved sources** — extracted content
- ✅ **Against the original topic** — context for what matters
- ❌ **NOT the plan** — even though plan exists, it's not used
- ❌ **NOT plan-specific questions** — no reference to research questions

**Example Output:**
```
## Key Findings
- AI can handle FAQs, reducing support costs
- Chatbots need human handoff for complex issues
- Multiple sources emphasize importance of human oversight

## Useful Details
- Customer support mentioned in 3 of 4 sources
- Responsible AI Basics source notes guardrail importance
- Integration challenges not deeply covered in sources

## Risks or Limitations
- Sources focus on high-level benefits, less on implementation details
- No specific tools or costs mentioned in sources
- Limited coverage of compliance/regulatory aspects

## Source Notes
- Source 1 (AI in Customer Support): Most directly relevant
- Source 4 (Responsible AI): Emphasizes guardrails
- Coverage gaps: ROI, specific tools, integration timelines
```

---

### **How a More Sophisticated Agent Would Work**

A production agent would:

```python
# Better approach (not in this beginner agent)
def search(self):
    # Extract key questions from plan
    search_queries = extract_questions_from_plan(self.plan)
    # search_queries = ["ROI of AI in customer support", "integration challenges", ...]
    
    # Do multiple searches for different aspects
    all_sources = []
    for query in search_queries:
        sources = search_sources(query, max_results=2)
        all_sources.extend(sources)
    
    # Deduplicate and return top 4
    return deduplicate(all_sources)[:4]
```

**Benefits of plan-aware search:**
- ✅ Targeted searches for specific sub-questions
- ✅ Better coverage of plan's research goals
- ✅ More relevant sources for analysis

### **Complete Flow: What Each Step Uses**

Here's the FULL picture of what gets passed through the pipeline:

```
User Input: "How can small businesses use AI for customer support?"

Step 1: PLAN
├─ Input: [TOPIC]
├─ LLM Role: "research planning assistant"
├─ Output: Detailed research plan with key questions
└─ ❓ Plan is created but NOT used in next steps

Step 2: SEARCH
├─ Input: [TOPIC] ← NOT plan questions
├─ Search Tool: Keyword matching (deterministic)
├─ Output: 4 most relevant sources
└─ ❌ Ignores plan, uses original topic

Step 3: ANALYZE
├─ Input: [TOPIC] + [4 SOURCES]
├─ LLM Role: "research analyst"
├─ Task: Extract insights from sources
├─ Output: Key findings, risks, limitations
└─ ❌ Ignores plan, analyzes sources against topic

Step 4: WRITE
├─ Input: [TOPIC] + [PLAN] + [FINDINGS] + [SOURCES]
├─ LLM Role: "professional research report writer"
├─ Task: Synthesize into structured report
├─ Output: Full research report
└─ ✅ FINALLY uses the plan!

Step 5: REVIEW
├─ Input: [TOPIC] + [REPORT]
├─ LLM Role: "careful report reviewer"
├─ Task: Check clarity, accuracy, usefulness
├─ Output: Review feedback
└─ ❌ Ignores plan

Step 6: SAVE
├─ Input: [REPORT] + [REVIEW]
├─ Task: Save to disk
├─ Output: Markdown file
└─ No LLM involved
```

**Key Insight:**
- 📋 Plan is created in Step 1
- 🔍 Search (Step 2) ignores the plan
- 📊 Analysis (Step 3) ignores the plan
- ✍️ Report writing (Step 4) finally uses the plan
- 📝 Review (Step 5) ignores the plan

**Why This Matters:**
The plan is underutilized. A better agent would:
1. Create plan
2. Extract key questions from plan
3. Use questions to guide search (multiple searches)
4. Use plan to structure analysis
5. Use plan to organize report

---

### **System Message**

All 4 LLM calls use the same system message to ensure consistency:

```
You are a careful, practical AI research agent.
Use only provided information. Do not invent facts.
```

This instructs the LLM to:
- ✅ Use only information from sources or context
- ✅ Avoid hallucinations and making up facts
- ✅ Be practical and actionable in recommendations

### **Visual: What Analyze Step Receives**

```
┌─────────────────────────────────────────────────────────┐
│                  ANALYZE STEP INPUTS                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  INPUT 1: Topic (Original User Input)                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ "How can small businesses use AI for customer   │   │
│  │  support?"                                       │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  INPUT 2: 4 Retrieved Sources (with content)            │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Source 1: AI in Customer Support                 │   │
│  │ Content: "AI can improve support by answering   │   │
│  │ questions, routing tickets, summarizing issues" │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ Source 2: AI for Small Business                  │   │
│  │ Content: "Small businesses can use AI for       │   │
│  │ customer support, marketing, automation..."     │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ Source 3: Responsible AI Basics                  │   │
│  │ Content: "Responsible AI focuses on safety,     │   │
│  │ fairness, transparency, privacy..."             │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ Source 4: (varies based on keyword match)        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ❌ NOT Analyzed:                                        │
│  └─ The Plan (created in step 1 but ignored here)       │
│  └─ Plan's research questions                           │
│  └─ Plan's suggested information to collect             │
│                                                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  ANALYZE STEP PROCESS                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  LLM reads the topic and all 4 sources                  │
│           ↓                                              │
│  LLM extracts insights from sources                     │
│           ↓                                              │
│  LLM groups insights into sections:                     │
│    • Key Findings (main points from sources)            │
│    • Useful Details (specific facts)                    │
│    • Risks or Limitations (gaps, concerns)              │
│    • Source Notes (which sources are relevant)          │
│           ↓                                              │
│  Output: Analysis document (text)                       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### **What Gets Analyzed vs What Doesn't**

| What's Being Analyzed | ✅ or ❌ |
|-----------------------|-----------|
| Content from retrieved sources | ✅ Yes |
| How sources relate to the topic | ✅ Yes |
| Connections between sources | ✅ Yes |
| Gaps/limitations in sources | ✅ Yes |
| **The Plan** | ❌ No |
| **Plan's research questions** | ❌ No |
| **Plan's information goals** | ❌ No |

---

### **What Does the WRITE Step Do?**

This is where everything comes together! The write step is the **first step to actually use the plan**.

**Write Step Inputs (4 sources):**

```python
def write_report(self, plan, findings, sources):
    prompt = build_report_prompt(
        topic=self.topic,        # ← Original user input
        plan=plan,               # ← ✅ FIRST USE of plan!
        findings=findings,       # ← Analysis from step 3
        sources=sources          # ← The 4 retrieved sources
    )
    report = self.call_llm(prompt)
    return report
```

**All 4 Inputs to Write:**

```
┌─────────────────────────────────────────────────────────┐
│                WRITE STEP INPUTS                         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. TOPIC (Original user input)                          │
│  "How can small businesses use AI for customer support?" │
│                                                           │
│  2. PLAN (Created in step 1)                             │
│  ## Research Goal                                         │
│  Understand how small businesses implement AI...          │
│                                                           │
│  ## Key Questions                                         │
│  - What are common use cases?                             │
│  - What are implementation challenges?                    │
│  - How much does it cost?                                 │
│  - What guardrails are needed?                            │
│                                                           │
│  3. FINDINGS (Analysis from step 3)                       │
│  ## Key Findings                                          │
│  - AI can handle FAQs, routing, summarization             │
│  - Human handoff needed for complex issues               │
│  - Responsible AI practices are critical                  │
│                                                           │
│  ## Useful Details                                        │
│  - 3 of 4 sources mention customer support              │
│  - Responsible AI source emphasizes guardrails           │
│                                                           │
│  ## Risks or Limitations                                  │
│  - Cost and ROI not covered in sources                    │
│  - Implementation details sparse                          │
│                                                           │
│  4. SOURCES (Retrieved in step 2)                         │
│  1. AI in Customer Support — local://ai-customer-support  │
│  2. AI for Small Business — local://ai-small-business     │
│  3. Responsible AI Basics — local://responsible-ai        │
│  4. AI Agents Overview — local://ai-agents-overview       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Write Prompt Instructions:**

```
You are a professional research report writer.

Write a clear research report using the research plan 
and findings below.

Rules:
- Use only the information provided
- Do not invent statistics or citations
- Keep the report beginner-friendly
- Include a practical recommendations section
- Include the source list at the end

Output format:
# Research Report: [TOPIC]
## Executive Summary
## Key Findings
## Practical Use Cases
## Risks and Limitations
## Recommendations
## Source List
## Final Takeaway
```

**Write Step Process:**

```
LLM receives all 4 inputs
        ↓
LLM reads the plan (research goals + questions)
        ↓
LLM reads the findings (analysis of sources)
        ↓
LLM reads the sources (for reference/validation)
        ↓
LLM synthesizes into structured sections:
  ├─ Executive Summary (overview)
  ├─ Key Findings (from analysis)
  ├─ Practical Use Cases (how to apply)
  ├─ Risks and Limitations (from analysis)
  ├─ Recommendations (actionable advice)
  ├─ Source List (citations)
  └─ Final Takeaway (conclusion)
        ↓
Output: Complete research report (markdown)
```

**Example Output Structure:**

```markdown
# Research Report: How can small businesses use AI for customer support?

## Executive Summary
[Overview synthesizing plan + findings]

## Key Findings
[Organized findings from step 3 analysis]
- AI handles FAQs, routing, summarization
- Human review needed for complex cases
- Responsible AI practices are critical

## Practical Use Cases
[Concrete applications based on findings]
1. Chatbots for FAQ handling
2. Ticket routing to right department
3. Customer issue summarization

## Risks and Limitations
[From findings + analysis]
- Cost and ROI not well covered in sources
- Implementation complexity varies
- Staff training required

## Recommendations
[Actionable next steps]
1. Start with FAQ automation
2. Plan human-in-the-loop approach
3. Implement responsible AI practices

## Source List
1. AI in Customer Support — local://...
2. AI for Small Business — local://...
3. Responsible AI Basics — local://...
4. AI Agents Overview — local://...

## Final Takeaway
[Summary and key insight]
```

**Key Differences from Analyze:**

| Step | Uses Topic | Uses Plan | Uses Sources | Uses Findings |
|------|-----------|-----------|------------|--------------|
| **Analyze** | ✅ | ❌ No | ✅ | ❌ None |
| **Write** | ✅ | ✅ **YES** | ✅ | ✅ **YES** |

---

### **Tracking LLM Performance**

**During testing, you can observe:**

1. **Plan Quality:** Does the plan ask relevant research questions?
2. **Analysis Depth:** Does the analysis synthesize across multiple sources?
3. **Report Structure:** Is the report well-organized with clear sections?
4. **Review Accuracy:** Are the review notes constructive and valid?

**Performance indicators:**

- **Fast LLM:** Responses in 2-4 seconds (OpenAI API)
- **Slow LLM:** Responses in 8-15 seconds (local Ollama model or first request)
- **Timeout:** If any step takes > 60 seconds, check your LLM provider configuration

---

## 💡 Advanced Testing

### Test Different Topics
Try topics that map to different sources:
1. **Small business focused:** "How can startups save money using AI?"
   - Should emphasize cost reduction and automation
   
2. **Education focused:** "What's the future of AI in schools?"
   - Should surface education concerns and opportunities
   
3. **Technical focused:** "Explain RAG architecture and its advantages"
   - Should provide technical depth and use cases
   
4. **Ethical focused:** "What should companies do to implement AI responsibly?"
   - Should emphasize governance and oversight

### Test Topic Variations
1. **Broad topic:** "Tell me about AI"
   - Should return general sources covering multiple areas
   
2. **Narrow topic:** "How do AI agents handle errors?"
   - Should retrieve most relevant sources, may have limited coverage
   
3. **Out-of-domain topic:** "Best practices for learning guitar"
   - Should still produce report (using general sources as fallback)
   - May mention limited sources available in knowledge base

### Test Report Quality
1. **Check for hallucinations:** Read the report and verify every claim appears in "View Retrieved Sources"
2. **Check citations:** See if report references where information came from
3. **Check consistency:** Ask same topic twice, compare reports
4. **Check review notes:** Are suggestions from review actually applied?

### Test Workflow Completion
1. Check that all 6 agent steps complete
2. Verify file was created in `reports/` directory
3. Try downloading the report
4. Open the saved markdown file and verify format

### Test Determinism vs Non-Determinism
This is important for understanding LLM behavior:

**Step 1: Run Topic A Twice**
```
Topic: "How can small businesses use AI for customer support?"
Run 1 → Check sources retrieved
Run 2 → Check sources retrieved
```
- 🔍 **Expected (Deterministic Search):** Same 3-4 sources both times
- ⚙️ **Expected (Non-Deterministic LLM):** Different wording in Plan, Analysis, Report
- ✅ **Verify:** Sources list is identical; report content is similar but rephrased

**Step 2: Run Topic B Twice**
```
Topic: "What is RAG and why would a company use it?"
Run 1 → Save report as report_1.md
Run 2 → Save report as report_2.md
```
- 🔍 **Compare sources:** Should always include "RAG and Knowledge Assistants"
- ⚙️ **Compare reports:** Will have different phrasing but same core concepts
- 📊 **Measure consistency:** Count sections (should both have: Summary, Findings, Use Cases, Risks, etc.)

**Step 3: Run Out-of-Domain Topic**
```
Topic: "Best exercises to build muscle fast"
```
- 🔍 **Expected:** No matching sources; falls back to all 6 general sources
- ⚙️ **Expected:** Report will mention AI-related sources but apply to fitness context
- ❌ **Red flag:** If report has hallucinated fitness facts not in sources

### Compare Outputs: Analyze vs Write
This helps understand what the write step adds:

**Example Topic:** "How can small businesses use AI?"

**Step 3 Output (Analyze):**
```
## Key Findings
- Chatbots can handle FAQs
- AI helps with marketing and automation
- Human review is important

## Useful Details
- Customer support mentioned in 3 sources
- Cost and ROI not covered

## Risks or Limitations
- Implementation complexity varies
- Staff training needed
- Limited source coverage on specific tools

## Source Notes
- Most relevant: AI for Small Business
- Balanced view: Responsible AI
```

**Step 4 Output (Write) - Same Input:**
```
# Research Report: How can small businesses use AI?

## Executive Summary
Small businesses can leverage AI to improve customer support, 
reduce costs, and improve efficiency. However, implementation 
requires careful planning and responsible AI practices...

## Key Findings
Based on analysis of sources, small businesses benefit from:
- Chatbot automation for FAQs
- Ticket routing and prioritization
- Customer issue summarization
- Process automation across departments

## Practical Use Cases
1. Auto-response to common questions
2. Intelligent ticket routing to departments
3. Priority detection for urgent issues
4. Document and email automation

## Risks and Limitations
- Implementation can be complex
- Staff needs training on new systems
- Responsible AI practices are critical
- ROI varies by use case

## Recommendations
1. Start with FAQ automation (quick win)
2. Plan human-in-the-loop approach
3. Implement responsible AI guidelines
4. Train staff on new tools

## Source List
1. AI for Small Business
2. AI in Customer Support
3. Responsible AI Basics
4. AI Agents Overview

## Final Takeaway
Small businesses should start with low-risk, high-impact 
AI applications while maintaining human oversight and 
responsible practices.
```

**Key Differences:**

| Aspect | Analyze Output | Write Output |
|--------|---|---|
| **Structure** | 4 sections (findings, details, risks, notes) | 8 sections (summary, findings, use cases, risks, recommendations, sources, takeaway) |
| **Purpose** | Extract insights from sources | Synthesize into actionable report |
| **Audience** | Internal analysis | End user / stakeholder |
| **Tone** | Analytical | Professional & instructional |
| **Actionability** | Lists findings | Includes specific recommendations |
| **Uses Plan** | ❌ No | ✅ Yes |
| **Format** | Structured notes | Polished report |

---

### Observe Plan vs Search Mismatch (Advanced)
This test reveals how the beginner agent works vs production agents:

**Test Setup:**
```
Topic: "How should companies implement responsible AI?"
```

**What You'll Observe:**

1. **View Research Plan:** Plan might outline:
   ```
   ## Key Questions
   - What does responsible AI mean?
   - How to implement fairness checks?
   - What governance structures are needed?
   - How to audit AI systems?
   ```

2. **View Retrieved Sources:** Search retrieves based on **original topic only**:
   ```
   Sources found: 
   1. Responsible AI Basics
   2. AI Agents Overview
   3. AI in Customer Support
   (NOT specific to "governance" or "auditing" from the plan)
   ```

3. **Expected Behavior:**
   - ⚠️ Plan asks 4 research questions, but search doesn't use these questions
   - ⚠️ Search uses the original topic, not the detailed plan
   - ✅ Analysis still works because it synthesizes the sources retrieved
   - ✅ Report is still good, but might not fully address all plan questions

**Why This Matters (Learning Opportunity):**

- **Current Agent:** Uses original topic throughout (simple, beginner-friendly)
  ```
  Topic → Plan → [Topic] → Search → [Topic] → Analyze
  ```

- **Production Agent:** Would use plan to refine search
  ```
  Topic → Plan → [Plan Questions] → Multi-Query Search → Analyze
  ```

- **Trade-off:** Simplicity vs Coverage
  - ✅ Simple: Easier to understand, consistent behavior
  - ❌ Limited: Plan doesn't inform search strategy

---

## 🔍 What to Look For (Indicators of Success)

✅ **Good Signs:**
- Agent completes all 6 steps in sequence
- Retrieved sources are relevant to the topic
- Report synthesizes information from multiple sources
- No information appears that isn't in the knowledge base
- Report has clear structure (intro, body, conclusion)
- Review feedback is accurate and constructive
- Downloaded file matches what you see in the app
- Report files save with correct timestamps

❌ **Red Flags:**
- Agent gets stuck or times out (> 60 seconds usually)
- Retrieved sources are completely unrelated
- Report contains facts not in the sources (hallucinations)
- All retrieved sources have very low relevance scores
- Report is too short or lacks detail (< 100 words)
- Missing agent steps or steps run out of order
- Downloaded file is empty or corrupted
- File doesn't save to `reports/` directory
- Same topic gives wildly different reports each run

---

## 📝 Notes

### Performance
- First request may take 8-15 seconds (model initialization)
- Subsequent requests typically take 4-8 seconds
- Slowest step is usually report writing and review

### Architecture
- Agent is non-interactive (single run, no back-and-forth)
- Search tool is local/mock with 6 pre-built sources
- Real-world agents would use live APIs (Google, Bing, etc.)
- Reports use Markdown format for readability

### Knowledge Base
- Sample sources are intentionally diverse and interconnected
- Topics that match multiple sources usually get better synthesis
- Out-of-domain topics still work (model uses fallback sources)

### File Storage
- Reports saved to `reports/` directory
- File names are sanitized for filesystem safety
- Timestamps prevent file overwrites
- Reports are plain-text markdown (human-readable)

---

## 🎯 Key Takeaways

After testing this agent, you should understand:
1. **Agent Loop:** How agents break complex tasks into steps
2. **Tool Calling:** How agents use external tools (search)
3. **Self-Improvement:** How agents can review and improve their own work
4. **Synthesis:** How to combine multiple sources into one coherent output
5. **Workflow:** Real-world agents follow structured processes, not random steps
6. **Planning vs Execution Gap:** Beginners agents may create plans but not use them to refine subsequent steps
7. **Determinism:** Which parts of the pipeline are deterministic (search) vs probabilistic (LLM outputs)

---

**Happy testing! 🎉**
