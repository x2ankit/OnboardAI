# Agent Flow Diagram

## 🐚 The Planner (Oogway)
The brain of the system, thinking step by step.

## 🐼 The Executor (Po)
The action center, transforming ideas into reality.

## 🐍 The Validator (Viper)
The safety net, ensuring every result is perfect.

## 🔁 Agent Flow Sequence

```mermaid
sequenceDiagram
    participant User as "User (Client Data)"
    participant State as "StateManager"
    participant Oogway as "Planner (Oogway)"
    participant Po as "Executor (Po)"
    participant Tools as "Simulated Tools"
    participant Viper as "Validator (Viper)"

    User->>State: Provide Client Information
    loop Until Action == DONE or ABORT
        State->>Oogway: Ask: "What's the next step?"
        Oogway-->>State: Reply: "SEND_EMAIL" (as JSON)
        State->>Po: Request: "Run SEND_EMAIL"
        Po->>Tools: Call Tool: send_email()
        Tools-->>Po: Return result
        Po-->>State: Provide tool output
        State->>Viper: Ask: "Is this result valid?"
        Viper-->>State: Reply: "CONTINUE" (Verified!)
        State->>State: Record Step in History
    end
    State->>User: Generate Final report.md
```

## 🧠 Decision Examples

### Case 1: Standard Success
Planner: SEND_EMAIL
Executor: SUCCESS
Validator: CONTINUE

### Case 2: Missing Critical Data
Planner: SEND_EMAIL (thinking the data exists)
Executor: ERROR: Email is null
Validator: ABORT: Missing critical info

### Case 3: Duplicate Client
Planner: CREATE_AIRTABLE_RECORD
Executor: SUCCESS (record exists)
Validator: CONTINUE (triggers warning, but doesn't stop)
