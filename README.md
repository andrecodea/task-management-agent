# Task Management Agent

An AI-powered task management agent built with Google ADK and Gemini 2.5 Flash, integrating Trello and Google Calendar through natural language.

## Architecture

```
User (natural language)
    └── Google ADK Agent (Gemini 2.5 Flash)
            ├── Trello Tools
            └── Google Calendar Tools
```

The agent understands natural language commands and executes actions on Trello and Google Calendar via registered tools. Session state is persisted locally by the ADK.

## Stack

- **Runtime**: Python 3.13+, [uv](https://github.com/astral-sh/uv)
- **Agent Framework**: [Google ADK](https://github.com/google/adk-python)
- **LLM**: Gemini 2.5 Flash
- **Trello**: [py-trello](https://github.com/sarumont/py-trello)
- **Google Calendar**: google-api-python-client

## Setup

1. Clone the repository and install dependencies:
```bash
uv sync
```

2. Create a `.env` file in the project root:
```
TRELLO_API_KEY=your_api_key
TRELLO_SECRET=your_secret
TRELLO_TOKEN=your_token
```

3. Add your Google Calendar OAuth credentials as `credentials.json` in the project root (obtained from GCP → APIs & Services → Credentials).

4. Run the agent:
```bash
uv run adk run TaskManager
```

On first run, a browser window will open to authorize Google Calendar access. This generates `token.json` automatically.

## Roadmap

### Trello CRUD
- [x] `add_task` — create a card in a specified list
- [ ] `list_tasks` — list all cards across lists
- [ ] `update_task` — update title, description, or due date
- [ ] `complete_task` — move card to "Done"
- [ ] `delete_task` — delete a card

### Google Calendar CRUD
- [ ] `create_event` — create a calendar event
- [ ] `list_events` — list events for a given date
- [ ] `update_event` — update event details
- [ ] `delete_event` — delete an event

### GitHub Integration
- [ ] `create_issue` — create a GitHub issue and add corresponding Trello card
- [ ] `create_pull_request` — open a PR linking the resolved issue
- [ ] `close_issue` — close issue when task is completed

### Agent
- [x] Natural language task management via ADK
- [x] External prompt loaded from `instructions.md`
- [ ] Cross-integration context (e.g. "what do I have today?" combining tasks and events)
- [ ] Proactive reminders for overdue tasks
