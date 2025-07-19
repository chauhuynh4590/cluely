# Cluely – Current State, Challenges & Solution Overview

---

## 🟦 Section 1. Current Cluely Flow

**Current Workflow Overview:**

Cluely serves as a virtual assistant that helps users understand web pages. The process is as follows:

- The user submits a question about a website.
- Cluely captures a live screenshot of the current web page.
- Using large language models (LLM) and visual context, Cluely analyzes the screenshot.
- Cluely generates and returns a detailed text response to the user.

```
+-------+      1. Ask Question      +---------------------+
| User  |------------------------->|  Cluely (Backend)   |
+-------+                          +---------------------+
                                         |
                                         | 2. Capture Screenshot
                                         v
                                 +----------------------+
                                 |  Website Screenshot  |
                                 +----------------------+
                                         |
                                         | 3. Analyze with LLM
                                         v
                                 +----------------------+
                                 |  LLM Analysis        |
                                 +----------------------+
                                         |
                                         | 4. Generate Answer
                                         v
+-------+      5. Return Answer   +---------------------+
| User  |<-----------------------|  Cluely (Backend)   |
+-------+                        +---------------------+
```



---

## 🟧 Section 2. Problems with Current Flow

### Key Limitations

| Problem                   | Description                                                  | Impact on User                   |
|---------------------------|--------------------------------------------------------------|----------------------------------|
| ❌ No Action Capability    | Cluely only returns text, not real actions                   | User must do everything manually |
| ⚠️ Surface-Level Guessing | Cluely makes assumptions based on screenshots, not deep understanding | Answers may be incomplete or wrong |


---

## 🟩 Section 3. Quick Overview: Two Solutions

|                           | 🖱️ Web Interaction Agent                                 | ⚡ API-based Execution                             |
|---------------------------|----------------------------------------------------------|---------------------------------------------------|
| **Knowledge Source**      | RAG on Help Desk Center docs                            | RAG on Help Desk Center docs + API docs           |
| **Action Method**         | Browser Automation:<br> <ul><li><a href="https://github.com/handrew/browserpilot">browserpilot</a></li><li><a href="https://github.com/lavague-ai/LaVague">LaVague</a></li><li><a href="https://python.langchain.com/docs/integrations/providers/hyperbrowser/">HyperBrowser</a></li></ul> | Direct API Calls                                  |
| **How it Works**          | Loop: Define actions → Execute in browser → Check result → Repeat until done | Loop: Define actions → Call API(s) → Check result → Repeat until done |
| **Best For**              | Any website (UI-based tasks)                            | Systems with public/internal APIs                 |
| **Speed/Reliability**     | Slower, UI can change                                   | Fast, stable if API maintained                    |

### Visual Comparison

```
[User Request]
     |
     v
+---------------------+        +---------------------+
|  Web Agent Solution |   OR   |   API Solution      |
+---------------------+        +---------------------+
| 1. RAG: Help Desk   |        | 1. RAG: Help Desk   |
| 2. Browser Auto.    |        | 2. RAG: API Docs    |
| 3. UI Actions       |        | 3. API Call         |
+---------------------+        +---------------------+
```

---

## 🟦 Section 4. Solution 1: Web Interaction Agent

### What Is It?
A closed-loop automation system where Cluely observes the website, retrieves relevant guidance, makes decisions using an LLM, and performs actions via browser automation. The process repeats—adapting to feedback—until the task is successfully completed or cannot proceed.

### Key Components
- **User Request:** The starting point; user instructs Cluely to perform a task.
- **Cluely Agent:** Captures a screenshot and DOM structure of the website to understand the current state.
- **RAG (Retrieval-Augmented Generation):** Queries the Help Desk Center documents for context and guidance related to the user’s request.
- **LLM Engine:** Analyzes the screenshot, DOM, and RAG output to decide the next best action.
- **Browser Automation Tool:** Executes the decided action (click, type, navigate, etc.) in the browser. Examples: [browserpilot](https://github.com/handrew/browserpilot), [LaVague](https://github.com/lavague-ai/LaVague), [HyperBrowser](https://python.langchain.com/docs/integrations/providers/hyperbrowser/).
- **Website State & Success Check:** After each action, the system checks if the task is complete. If not, the loop restarts with a new screenshot and updated guidance.

### Step-by-Step Process
1. **User Request:** User asks Cluely to perform a task on a website.
2. **Screenshot & DOM:** Cluely Agent captures the current state of the page.
3. **Query RAG:** Cluely Agent queries the Help Desk Center for relevant guidance.
4. **LLM Decision:** LLM Engine analyzes all information and decides the next action.
5. **Perform Action:** Browser Automation Tool executes the action in the browser.
6. **Check Website State:** System checks if the desired outcome is achieved.
7. **Success?**
    - **Yes:** Task is complete; report success to user.
    - **No:** Loop back to step 2 with updated context and try again.

### Architecture Overview

```
+---------------------+
|    User Request     |
+---------------------+
           |
           v
+---------------------+
|   Cluely Agent      |
+---------------------+
| 1. Screenshot & DOM |
| 2. Query RAG Help   |
+---------------------+
           |
           v
+---------------------+
|      LLM Engine     |
+---------------------+
| 3. Make Decision    |
+---------------------+
           |
           v
+-------------------------+
|  Browser Automation     |
+-------------------------+
| 4. Perform Action       |
+-------------------------+
           |
           v
+---------------------+
|   Website State     |
+---------------------+
           |
      Success?
        /    \
      Yes    No
      |       |
   [Done]     |
               |
               v
      +---------------------+
      |   Cluely Agent      |
      +---------------------+
      |(Re-screenshot, etc.)|
      +---------------------+
```

- The loop continues: If success, the flow ends. If not, Cluely Agent re-observes, re-queries, and tries again until the task is complete.

### Step-by-Step Sequence Diagram
```
User        Cluely Agent   RAG    LLM Engine   Browser Auto   Website
 |               |         |         |             |            |
 |---Request---->|         |         |             |            |
 |               |--Scrn-->|         |             |            |
 |               |--Query->|         |             |            |
 |               |<--Docs--|         |             |            |
 |               |--------->|--Decision-->|         |            |
 |               |         |         |--Action---->|            |
 |               |         |         |             |--Perform-->| 
 |               |         |         |             |<--Result---| 
 |               |<------------------Error/Fail-----------------|
 |               |--(Loop: re-screenshot, re-query, new decision)|
 |<--Final Report-|         |         |             |            |
```

---

## 🟧 Section 5. Solution 2: API-based Execution

### What Is It?
A fully automated system where Cluely leverages both Help Desk and API documentation to directly generate and execute API calls, bypassing the user interface for speed, reliability, and precision.

### Key Components
- **User Request:** Initiates the process with a task or question.
- **Cluely Agent:** Interprets the request, understands the current state, and manages the workflow.
- **RAG (Retrieval-Augmented Generation):** Queries Help Desk Center docs and API documentation for relevant information and endpoint details.
- **LLM Engine:** Synthesizes retrieved knowledge and context to decide on the next API action, including parameter construction.
- **API Executor:** Executes the API call(s) as determined by the LLM.
- **System State & Success Check:** After each API call, checks if the desired outcome is achieved; if not, loops back for another decision.

### Step-by-Step Process
1. **User Request:** User asks Cluely to perform a task.
2. **Query RAG:** Cluely Agent fetches relevant guidance from Help Desk and API docs.
3. **LLM Decision:** LLM Engine analyzes all information and decides the next API call.
4. **Execute API Call:** API Executor performs the API call as directed.
5. **Check System State:** System checks if the task is complete (via API response or follow-up query).
6. **Success?**
    - **Yes:** Task is complete; report success to user.
    - **No:** Loop back to step 2 with updated context and try again.

### Architecture Overview
```
+---------------------+
|    User Request     |
+---------------------+
           |
           v
+---------------------+
|   Cluely Agent      |
+---------------------+
           |
           v
+---------------------+
|      RAG Engine     |
+---------------------+
| 1. Help Desk Docs   |
| 2. API Docs         |
+---------------------+
           |
           v
+---------------------+
|     LLM Engine      |
+---------------------+
| 3. Decide API Call  |
+---------------------+
           |
           v
+---------------------+
|    API Executor     |
+---------------------+
| 4. Call API         |
+---------------------+
           |
           v
+---------------------+
|   System State      |
+---------------------+
           |
      Success?
        /    \
      Yes    No
      |       |
   [Done]     |
               |
               v
      +---------------------+
      |   Cluely Agent      |
      +---------------------+
      |(Re-query, new call) |
      +---------------------+
```
- The loop continues: If success, the flow ends. If not, Cluely Agent re-queries and tries again until the task is complete.

```
User      Cluely Agent    RAG Engine    LLM Engine    API Executor    System
 |             |             |             |              |             |
 |---Request-->|             |             |              |             |
 |             |--Query----->|             |              |             |
 |             |<--Docs------|             |              |             |
 |             |------------>|--Decision-->|              |             |
 |             |             |             |--Call------->|             |
 |             |             |             |              |--Exec------>|
 |             |             |             |              |<--Result----|
 |             |<-------------------Error/Fail--------------------------|
 |             |--(Loop: re-query, new decision/call)                  |
 |<--Final Report-|         |             |              |             |
```

---

## 🟨 Section 6. Comparative Summary, Hybrid Approach & Recommendations

| Feature         | Web Interaction Agent                | API-based Execution                  |
|----------------|--------------------------------------|--------------------------------------|
| **Speed**      | Slower (UI-driven)                   | Faster (direct API calls)            |
| **Reliability**| UI changes may break flows           | Stable if API maintained             |
| **Scope**      | Any website (even w/o API)           | Only systems with accessible APIs    |
| **Complexity** | Emulates user, handles UI quirks     | Needs accurate API docs, error-handling|
| **Implementation** | Browser automation + LLM         | RAG API docs + LLM                   |

### Hybrid Approach: Best of Both Worlds
A robust solution combines both methods:
- **Primary:** Use API-based execution whenever possible for speed and reliability.
- **Fallback:** Seamlessly switch to the Web Interaction Agent if APIs are unavailable, incomplete, or return errors.
- **Dynamic Decision:** The system intelligently chooses the optimal method for each step, maximizing task success and user satisfaction.
- **Example:** Start with API calls to fetch data; if an API fails or lacks required functionality, automatically revert to browser automation to complete the task.

### Recommendations & Next Steps
- **Short-term:** Build and pilot the Web Interaction Agent for broad coverage.
- **Long-term:** Integrate API-based execution and develop robust hybrid switching logic.
- **Goal:** Achieve seamless, dynamic selection between methods for every user task.

#### Next Steps
- Prototype the Web Interaction Agent.
- Integrate RAG on API documentation and build API execution capabilities.
- Design and test the hybrid decision engine.
- Pilot with real user tasks, focusing on scenarios where fallback is needed.

---

**Thank you for reviewing!**


---
