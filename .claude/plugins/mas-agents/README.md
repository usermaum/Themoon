# MAS Agents Plugin

> **Multi-Agent System** for TheMoon Coffee Roasting Management Platform

This plugin provides three specialized autonomous agents that work together as a coordinated team.

## 🤖 Available Agents

### Agent 2: Frontend Specialist (Cyan)
**Specialty**: React, TypeScript, Tailwind CSS, UI/UX Design

**Use for**:
- Creating/modifying React components
- Tailwind CSS styling and animations
- UI/UX improvements
- Frontend build issues

**Skills**: `frontend-design`, `feature-dev`

**Example Usage**:
```
"Create a dashboard component with charts"
"Fix the button hover animation"
"@Agent2 improve the 404 page design"
```

---

### Agent 3: Backend Engineer (Green)
**Specialty**: FastAPI, SQLAlchemy, PostgreSQL, Clean Architecture

**Use for**:
- API endpoint development
- Database schema and models
- Repository pattern implementation
- Backend business logic

**Skills**: `feature-dev`, `code-review`

**Example Usage**:
```
"Add date filtering to the roasting logs API"
"Create a new blend management endpoint"
"@Agent3 add output_weight parameter to API"
```

---

### Agent 4: System Maintainer (Red)
**Specialty**: Debugging, Code Review, Quality Assurance, System Config

**Use for**:
- Fixing errors and bugs
- Code review and PR analysis
- Build failures
- Cross-cutting issues
- WSL/environment problems

**Skills**: `pr-review-toolkit`, `code-review`, `commit-commands`

**Example Usage**:
```
"Review my code before PR"
"npm build is failing"
"@Agent4 fix the CORS error"
"Run quality checks on the codebase"
```

---

## 🔄 Agent Collaboration

Agents can request help from each other:

**Agent 2 → Agent 3** (Frontend needs backend change):
```
@Agent3: API endpoint /api/beans needs a 'roast_level' filter parameter
```

**Agent 3 → Agent 2** (Backend notifies frontend of API change):
```
@Agent2: Added 'total_weight' field to RoastingLogSchema
```

**Agent 2/3 → Agent 4** (Escalation for debugging):
```
@Agent4: Build failing with strange TypeScript error
@Agent4: Database migration issue
```

---

## 🚀 How to Use

### Method 1: Automatic Triggering
Simply describe what you need. Claude will automatically select the right agent:

```
"Create a new roasting chart component"  → Agent 2 (Frontend)
"Add filtering to the beans API"         → Agent 3 (Backend)
"Fix the build error"                    → Agent 4 (Maintainer)
```

### Method 2: Explicit Agent Call
Use `@AgentN` to explicitly invoke an agent:

```
@Agent2 create a coffee-themed loading spinner
@Agent3 optimize the roasting log queries
@Agent4 review changes in my last 3 commits
```

### Method 3: Task Tool
Use Claude Code's Task tool:

```typescript
Task tool with subagent_type: "mas-agents:agent-2-frontend"
Task tool with subagent_type: "mas-agents:agent-3-backend"
Task tool with subagent_type: "mas-agents:agent-4-maintainer"
```

---

## 📋 Agent Responsibilities

| Area | Agent 2 | Agent 3 | Agent 4 |
|:-----|:--------|:--------|:--------|
| React Components | ✅ | ❌ | 🔧 |
| Tailwind CSS | ✅ | ❌ | 🔧 |
| FastAPI Endpoints | ❌ | ✅ | 🔧 |
| Database Models | ❌ | ✅ | 🔧 |
| Code Review | ❌ | ✅ | ✅ |
| Bug Fixing | 🔧 | 🔧 | ✅ |
| Build Issues | ❌ | ❌ | ✅ |
| System Config | ❌ | ❌ | ✅ |

✅ = Primary Responsibility
🔧 = Can help if needed
❌ = Not their domain

---

## 🎯 Best Practices

1. **Let agents do their job**: Don't micromanage, trust their expertise
2. **Use explicit calls for complex tasks**: `@Agent3 ...` ensures right agent
3. **Agents collaborate**: They'll coordinate with each other automatically
4. **Agent 4 is the safety net**: When stuck, escalate to Agent 4
5. **Check AGENTS.md**: Full protocol documentation in `.agent/AGENTS.md`

---

## 📁 Plugin Structure

```
.claude/plugins/mas-agents/
├── plugin.json           # Plugin manifest
├── README.md            # This file
└── agents/
    ├── agent-2-frontend.md     # Frontend specialist
    ├── agent-3-backend.md      # Backend engineer
    └── agent-4-maintainer.md   # System maintainer
```

---

## 🔗 Integration with Project

This plugin integrates with:
- **AGENTS.md**: Main MAS protocol document
- **Frontend-design skill**: Agent 2's primary tool
- **PR-review-toolkit skill**: Agent 4's primary tool
- **Clean Architecture**: All agents follow repository pattern

---

## 📝 Version History

**v1.0.0** (2025-12-27)
- Initial release
- 3 specialized agents (Frontend, Backend, Maintainer)
- Full collaboration protocol
- Integration with Claude Marketplace skills

---

**Created by**: TheMoon Project Team
**Documentation**: See `.agent/AGENTS.md` for full MAS protocol
**License**: Internal use (TheMoon Project)
