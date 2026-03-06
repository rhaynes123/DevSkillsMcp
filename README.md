# DevSkills MCP Server

A **Model Context Protocol (MCP) server** that helps senior software developers
discover, plan, and validate new skills. Built in both **.NET** and **Python**
to serve as a learning reference for both languages.

---

## What is MCP?

The **Model Context Protocol** is an open standard (by Anthropic) that lets AI
assistants like Claude connect to external tools and data sources. An MCP server
exposes "tools" that an AI can call — like calling a REST API, but for AI agents.

Think of it this way:
- A **REST API** is called by your app
- An **MCP server** is called by an AI assistant

---

## Available Tools

| Tool | Description |
|------|-------------|
| `skills_list_recommended` | List all recommended skills, optionally by category |
| `skills_get_detail` | Deep dive on a specific skill: resources, projects, cert path |
| `skills_get_roadmap` | Full career roadmap with phases, timelines, milestones |
| `skills_list_resources` | Browse learning resources filtered by type/difficulty/cost |
| `skills_get_practice_challenge` | Get a hands-on project challenge for a skill |
| `skills_compare` | Compare two skills side-by-side to prioritize learning |

---

## 🟣 .NET Version

### Prerequisites
- [.NET 9 SDK](https://dotnet.microsoft.com/download)

### Setup & Run

```bash
cd dotnet/DevSkillsMCP
dotnet restore
dotnet run
```

### Project Structure

```
dotnet/DevSkillsMCP/
├── Program.cs                  # Entry point - MCP server wiring
├── DevSkillsMCP.csproj         # Project file with MCP SDK dependency
├── Models/
│   └── SkillModels.cs          # C# records for Skill, LearningResource, Roadmap
├── Data/
│   └── SkillsDataStore.cs      # In-memory data store
└── Tools/
    └── DevSkillsTools.cs       # All MCP tool implementations ([McpServerTool])
```

### Key .NET Concepts Used

- **`[McpServerTool]` attribute** — registers a static method as an MCP tool
- **`[McpServerToolType]` attribute** — marks a class for auto-discovery via `WithToolsFromAssembly()`
- **C# records** — immutable data models (`record Skill(...)`)
- **`AddMcpServer().WithStdioServerTransport()`** — MCP server DI setup
- **Pattern matching** — `difficulty.ToLower() switch { "beginner" => 0, ... }`

### Connecting to Claude Desktop (.NET)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dev-skills": {
      "command": "dotnet",
      "args": ["run", "--project", "/path/to/dotnet/DevSkillsMCP"]
    }
  }
}
```

---

## 🐍 Python Version

### Prerequisites
- Python 3.10+
- pip

### Setup & Run

```bash
cd python
pip install -r requirements.txt

# Run as stdio server (default - for Claude Desktop)
python dev_skills_mcp.py

# Run as HTTP server (for web/remote use)
python dev_skills_mcp.py --transport streamable-http --port 8000
```

### Project Structure

```
python/
├── dev_skills_mcp.py     # Complete single-file MCP server
└── requirements.txt      # mcp, pydantic
```

### Key Python Concepts Used

- **`FastMCP`** — high-level MCP server framework (like FastAPI but for MCP)
- **`@mcp.tool` decorator** — registers an async function as an MCP tool
- **Pydantic v2 BaseModel** — input validation with `Field()` constraints
- **`ConfigDict`** — Pydantic v2 model configuration (`str_strip_whitespace`, `extra='forbid'`)
- **`str, Enum`** — string enums for validated options like `ResponseFormat`, `Difficulty`
- **`async def`** — all tools are async for non-blocking I/O

### Connecting to Claude Desktop (Python)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dev-skills": {
      "command": "python",
      "args": ["/path/to/python/dev_skills_mcp.py"]
    }
  }
}
```

---

## .NET vs Python: Side-by-Side Comparison

| Concept | .NET | Python |
|---------|------|--------|
| Tool registration | `[McpServerTool]` attribute | `@mcp.tool()` decorator |
| Input validation | C# record params + type system | Pydantic `BaseModel` |
| Server setup | `AddMcpServer().WithStdioServerTransport()` | `FastMCP("name")` |
| Transport | Configured in `Program.cs` DI | `mcp.run(transport=...)` |
| Null safety | Nullable reference types (`string?`) | `Optional[str]` + `None` |
| Enums | `enum SkillLevel { Beginner, ... }` | `class X(str, Enum)` |
| Async | `async Task<string>` | `async def ... -> str` |
| JSON | `System.Text.Json.JsonSerializer` | `json.dumps()` |

---

## Extending This Server

Want to add your own tools? Here's the pattern:

### .NET
```csharp
[McpServerTool(Name = "skills_my_new_tool")]
[Description("What this tool does")]
public static string MyNewTool(
    [Description("Parameter description")] string myParam) 
{
    // your logic
    return "result";
}
```

### Python
```python
class MyInput(BaseModel):
    my_param: str = Field(..., description="Parameter description")

@mcp.tool(name="skills_my_new_tool")
async def my_new_tool(params: MyInput) -> str:
    """What this tool does."""
    return "result"
```

---

## Next Steps

This MCP server is a foundation. Here's how to grow it:

1. **Connect to a real database** — replace the in-memory data store with SQLite or Postgres
2. **Add Azure integration** — pull cert progress from Microsoft Learn API
3. **Add GitHub tool** — track which practice projects you've actually committed
4. **Deploy to Azure** — use streamable HTTP transport and host as an Azure Container App
5. **Add auth** — OAuth 2.1 for multi-user support

Each of those extensions maps directly to the skills recommended in the server itself. 🎯
