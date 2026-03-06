"""
DevSkills MCP Server - Python Implementation
=============================================
An MCP server for senior .NET developers looking to grow their skills.
Provides tools to explore recommended skills, learning resources,
practice projects, and career roadmaps.

Run with:
    pip install mcp
    python dev_skills_mcp.py

Or as a streamable HTTP server:
    python dev_skills_mcp.py --transport streamable-http --port 8000
"""

import json
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────────────────
# SERVER INITIALIZATION
# ─────────────────────────────────────────────────────────

mcp = FastMCP("dev_skills_mcp")


# ─────────────────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────────────────

class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class SkillCategory(str, Enum):
    """Valid skill categories."""
    CLOUD = "Cloud"
    AI = "AI"
    SECURITY = "Security"
    BACKEND = "Backend"
    SYSTEM_DESIGN = "SystemDesign"
    LANGUAGES = "Languages"
    DEVOPS = "DevOps"


class Difficulty(str, Enum):
    """Difficulty levels for resources and challenges."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ListSkillsInput(BaseModel):
    """Input model for listing recommended skills."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    category: Optional[str] = Field(
        default=None,
        description="Optional category filter: Cloud, AI, Security, Languages, DevOps, SystemDesign"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for readable output or 'json' for structured data"
    )


class SkillDetailInput(BaseModel):
    """Input model for getting skill details."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    skill_name: str = Field(
        ...,
        description="The exact skill name (e.g. 'Python', 'Azure Developer Associate (AZ-204)')",
        min_length=1,
        max_length=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class ListResourcesInput(BaseModel):
    """Input model for listing learning resources."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    resource_type: Optional[str] = Field(
        default=None,
        description="Filter by type: 'course', 'book', 'platform', 'certification', 'project'"
    )
    difficulty: Optional[Difficulty] = Field(
        default=None,
        description="Filter by difficulty: beginner, intermediate, advanced"
    )
    free_only: bool = Field(
        default=False,
        description="If True, only return free resources"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class PracticeChallengeInput(BaseModel):
    """Input model for getting a practice challenge."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    skill_name: str = Field(
        ...,
        description="The skill name to get a challenge for",
        min_length=1,
        max_length=100
    )
    difficulty: Difficulty = Field(
        default=Difficulty.BEGINNER,
        description="Difficulty level: beginner, intermediate, advanced"
    )


class CompareSkillsInput(BaseModel):
    """Input model for comparing two skills."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    skill_name_a: str = Field(
        ...,
        description="First skill name to compare",
        min_length=1,
        max_length=100
    )
    skill_name_b: str = Field(
        ...,
        description="Second skill name to compare",
        min_length=1,
        max_length=100
    )


class RoadmapInput(BaseModel):
    """Input model for getting the career roadmap."""
    model_config = ConfigDict(extra="forbid")

    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


# ─────────────────────────────────────────────────────────
# DATA STORE
# ─────────────────────────────────────────────────────────

SKILLS_DATA = [
    {
        "name": "Azure Developer Associate (AZ-204)",
        "category": "Cloud",
        "current_level": "Beginner",
        "target_level": "Intermediate",
        "learning_resources": [
            "Microsoft Learn: AZ-204 Learning Path",
            "Pluralsight: Developing Solutions for Azure",
            "A Cloud Guru: AZ-204 Course"
        ],
        "practice_projects": [
            "Deploy a .NET Web API to Azure App Service with CI/CD",
            "Build an Azure Function triggered by Service Bus queue",
            "Implement Azure Key Vault secrets in an existing .NET API"
        ],
        "certification_path": "AZ-900 → AZ-204 → AZ-400 (DevOps Engineer)"
    },
    {
        "name": "Azure AI Engineer Associate (AI-102)",
        "category": "AI",
        "current_level": "Beginner",
        "target_level": "Intermediate",
        "learning_resources": [
            "Microsoft Learn: AI-102 Learning Path",
            "Anthropic API Documentation",
            "OpenAI .NET SDK GitHub Repository",
            "Azure OpenAI Service Quickstart Docs"
        ],
        "practice_projects": [
            "Build a .NET chatbot using Azure OpenAI Service",
            "Create an AI-powered code reviewer using the Anthropic API",
            "Add semantic search to an existing .NET API using embeddings"
        ],
        "certification_path": "AZ-204 → AI-102"
    },
    {
        "name": "DevSecOps / Security Engineering",
        "category": "Security",
        "current_level": "Beginner",
        "target_level": "Intermediate",
        "learning_resources": [
            "Hack The Box: Starting Point Track",
            "TryHackMe: Pre-Security Path",
            "OWASP Top 10 Documentation",
            "AZ-500: Azure Security Engineer Study Guide",
            "PortSwigger Web Security Academy (free)"
        ],
        "practice_projects": [
            "Complete 10 Hack The Box 'easy' machines",
            "Run OWASP ZAP against one of your own .NET APIs",
            "Implement proper secret scanning in a GitHub Actions pipeline",
            "Add auth + rate limiting to an existing REST API"
        ],
        "certification_path": "Google Cybersecurity Cert → AZ-500 → CompTIA Security+"
    },
    {
        "name": "Python",
        "category": "Languages",
        "current_level": "Beginner",
        "target_level": "Intermediate",
        "learning_resources": [
            "Python.org Official Tutorial",
            "Advent of Code (use Python to solve challenges)",
            "FastAPI Documentation (great for .NET devs - REST API mindset)",
            "Real Python: Python for .NET Developers"
        ],
        "practice_projects": [
            "Rewrite one of your existing .NET CLI tools in Python",
            "Build a FastAPI service that mirrors a .NET REST API you built",
            "Create a Python automation script that solves a real daily problem",
            "Complete 30 days of Advent of Code in Python"
        ],
        "certification_path": "No formal cert needed — GitHub projects are sufficient validation"
    },
    {
        "name": "Infrastructure as Code (Terraform)",
        "category": "DevOps",
        "current_level": "Beginner",
        "target_level": "Intermediate",
        "learning_resources": [
            "HashiCorp Learn: Terraform on Azure",
            "Pluralsight: Terraform - Getting Started",
            "Terraform Up & Running (book by Yevgeniy Brikman)"
        ],
        "practice_projects": [
            "Provision an Azure App Service + SQL DB with Terraform",
            "Convert an existing manually-created Azure resource to Terraform IaC",
            "Set up a Terraform remote state backend in Azure Blob Storage"
        ],
        "certification_path": "HashiCorp Terraform Associate Certification"
    },
    {
        "name": "Advanced System Design",
        "category": "SystemDesign",
        "current_level": "Intermediate",
        "target_level": "Advanced",
        "learning_resources": [
            "Designing Data-Intensive Applications (Martin Kleppmann)",
            "ByteByteGo System Design Newsletter",
            "System Design Interview Vol. 1 & 2 (Alex Xu)",
            "High Scalability Blog"
        ],
        "practice_projects": [
            "Document an Architecture Decision Record (ADR) for a real system you built",
            "Design a rate limiter from scratch and publish it on GitHub",
            "Draw and narrate a system design for a loan workflow on Excalidraw",
            "Build a distributed cache layer in front of an existing .NET service"
        ],
        "certification_path": "No cert — publish design docs and case studies on GitHub/LinkedIn"
    }
]

RESOURCES_DATA = [
    {
        "title": "Hack The Box",
        "type": "platform",
        "url": "https://www.hackthebox.com",
        "difficulty": "intermediate",
        "is_free": False,
        "estimated_time": "Ongoing",
        "description": "Gamified cybersecurity platform. Start with 'Starting Point' machines for beginners."
    },
    {
        "title": "PortSwigger Web Security Academy",
        "type": "platform",
        "url": "https://portswigger.net/web-security",
        "difficulty": "beginner",
        "is_free": True,
        "estimated_time": "40-60 hours",
        "description": "Free, hands-on web security training covering OWASP Top 10 and more."
    },
    {
        "title": "Microsoft Learn",
        "type": "platform",
        "url": "https://learn.microsoft.com",
        "difficulty": "beginner",
        "is_free": True,
        "estimated_time": "Varies by path",
        "description": "Official Microsoft learning paths for all Azure certifications."
    },
    {
        "title": "Designing Data-Intensive Applications",
        "type": "book",
        "url": "https://dataintensive.net",
        "difficulty": "advanced",
        "is_free": False,
        "estimated_time": "20-30 hours",
        "description": "The definitive book on building scalable, reliable distributed systems."
    },
    {
        "title": "Advent of Code",
        "type": "platform",
        "url": "https://adventofcode.com",
        "difficulty": "intermediate",
        "is_free": True,
        "estimated_time": "1-2 hrs/day in December",
        "description": "Annual coding challenges, great for practicing Python and algorithm skills."
    }
]

ROADMAP_DATA = {
    "developer_profile": "Senior .NET Developer → Principal / Staff Engineer",
    "phases": [
        {
            "order": 1,
            "title": "Deepen Cloud (3-6 months)",
            "time_estimate": "3-6 months",
            "skills": ["AZ-204", "Docker", "Azure Container Apps", "Terraform basics"],
            "milestones": [
                "Pass AZ-204 exam",
                "Deploy a containerized .NET app to Azure",
                "Provision infrastructure with Terraform"
            ]
        },
        {
            "order": 2,
            "title": "AI Integration (3-4 months)",
            "time_estimate": "3-4 months",
            "skills": ["Azure OpenAI", "Prompt Engineering", "AI-102", "LLM API integration"],
            "milestones": [
                "Build a .NET app that calls an LLM API",
                "Pass AI-102 exam",
                "Ship an AI feature in a real project"
            ]
        },
        {
            "order": 3,
            "title": "Security Hardening (2-3 months)",
            "time_estimate": "2-3 months",
            "skills": ["HTB / TryHackMe", "OWASP Top 10", "AZ-500", "DevSecOps pipelines"],
            "milestones": [
                "Complete 10 HTB machines",
                "Pass AZ-500 exam",
                "Add SAST scanning to a CI/CD pipeline"
            ]
        },
        {
            "order": 4,
            "title": "Python + Automation (ongoing)",
            "time_estimate": "Ongoing",
            "skills": ["Python", "FastAPI", "Scripting", "Data pipelines"],
            "milestones": [
                "Publish 3 Python projects on GitHub",
                "Build a FastAPI service",
                "Complete Advent of Code in Python"
            ]
        }
    ]
}


# ─────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────

def _find_skill(skill_name: str) -> dict | None:
    """Find a skill by name (case-insensitive)."""
    return next(
        (s for s in SKILLS_DATA if s["name"].lower() == skill_name.strip().lower()),
        None
    )


def _skill_not_found_message(skill_name: str) -> str:
    """Return a helpful error message when a skill is not found."""
    available = ", ".join(s["name"] for s in SKILLS_DATA)
    return f"Skill '{skill_name}' not found. Available skills: {available}"


def _format_skill_markdown(skill: dict) -> str:
    """Format a single skill as markdown."""
    lines = [
        f"# 📚 {skill['name']}",
        f"\n**Category**: {skill['category']}",
        f"**Level**: {skill['current_level']} → {skill['target_level']}",
    ]
    if skill.get("certification_path"):
        lines.append(f"**Certification Path**: {skill['certification_path']}")

    lines.append("\n## 📖 Learning Resources")
    lines.extend(f"- {r}" for r in skill["learning_resources"])

    lines.append("\n## 🛠️ Practice Projects")
    lines.extend(f"{i+1}. {p}" for i, p in enumerate(skill["practice_projects"]))

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────────────────

@mcp.tool(
    name="skills_list_recommended",
    annotations={
        "title": "List Recommended Skills",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def skills_list_recommended(params: ListSkillsInput) -> str:
    """List all recommended skills for a senior .NET developer, optionally filtered by category.

    Args:
        params (ListSkillsInput): Filtering and format options.

    Returns:
        str: Markdown or JSON list of skills grouped by category.
    """
    skills = SKILLS_DATA

    if params.category:
        skills = [s for s in skills if s["category"].lower() == params.category.strip().lower()]
        if not skills:
            valid = ", ".join(c.value for c in SkillCategory)
            return f"No skills found in category '{params.category}'. Valid categories: {valid}"

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(skills, indent=2)

    # Group by category
    grouped: dict[str, list] = {}
    for skill in skills:
        grouped.setdefault(skill["category"], []).append(skill)

    lines = ["# 🎯 Recommended Skills for Senior .NET Developers\n"]
    for category, cat_skills in grouped.items():
        lines.append(f"## {category}")
        for skill in cat_skills:
            lines.append(f"### {skill['name']}")
            lines.append(f"- **Current → Target**: {skill['current_level']} → {skill['target_level']}")
            if skill.get("certification_path"):
                lines.append(f"- **Certification Path**: {skill['certification_path']}")
            lines.append("")

    return "\n".join(lines)


@mcp.tool(
    name="skills_get_detail",
    annotations={
        "title": "Get Skill Detail",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def skills_get_detail(params: SkillDetailInput) -> str:
    """Get detailed information about a specific skill including resources, projects, and cert path.

    Args:
        params (SkillDetailInput): Skill name and response format.

    Returns:
        str: Detailed skill info in markdown or JSON.
    """
    skill = _find_skill(params.skill_name)
    if skill is None:
        return _skill_not_found_message(params.skill_name)

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(skill, indent=2)

    return _format_skill_markdown(skill)


@mcp.tool(
    name="skills_get_roadmap",
    annotations={
        "title": "Get Career Roadmap",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def skills_get_roadmap(params: RoadmapInput) -> str:
    """Get the full career roadmap for a Senior .NET Developer growing toward Staff/Principal level.

    Args:
        params (RoadmapInput): Response format preference.

    Returns:
        str: Career roadmap with phases, timelines, and milestones in markdown or JSON.
    """
    if params.response_format == ResponseFormat.JSON:
        return json.dumps(ROADMAP_DATA, indent=2)

    lines = [f"# 🗺️ Career Roadmap: {ROADMAP_DATA['developer_profile']}\n"]

    for phase in sorted(ROADMAP_DATA["phases"], key=lambda p: p["order"]):
        lines.append(f"## Phase {phase['order']}: {phase['title']} ({phase['time_estimate']})")
        lines.append("\n**Skills to learn:**")
        lines.extend(f"- {s}" for s in phase["skills"])
        lines.append("\n**Milestones:**")
        lines.extend(f"- [ ] {m}" for m in phase["milestones"])
        lines.append("")

    return "\n".join(lines)


@mcp.tool(
    name="skills_list_resources",
    annotations={
        "title": "List Learning Resources",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def skills_list_resources(params: ListResourcesInput) -> str:
    """List featured learning resources, with optional filtering by type, difficulty, and cost.

    Args:
        params (ListResourcesInput): Filtering options and response format.

    Returns:
        str: Filtered list of learning resources in markdown or JSON.
    """
    resources = RESOURCES_DATA[:]

    if params.resource_type:
        resources = [r for r in resources if r["type"].lower() == params.resource_type.strip().lower()]
    if params.difficulty:
        resources = [r for r in resources if r["difficulty"] == params.difficulty.value]
    if params.free_only:
        resources = [r for r in resources if r["is_free"]]

    if not resources:
        return "No resources found matching the specified filters."

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(resources, indent=2)

    lines = ["# 🔗 Learning Resources\n"]
    for r in resources:
        free_icon = "✅" if r["is_free"] else "💰"
        lines.append(f"### {r['title']}")
        lines.append(f"- **Type**: {r['type']} | **Difficulty**: {r['difficulty']} | **Free**: {free_icon}")
        lines.append(f"- **Time**: {r['estimated_time']}")
        lines.append(f"- **URL**: {r['url']}")
        lines.append(f"- {r['description']}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool(
    name="skills_get_practice_challenge",
    annotations={
        "title": "Get Practice Challenge",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def skills_get_practice_challenge(params: PracticeChallengeInput) -> str:
    """Get an actionable practice challenge for a given skill with validation steps.

    Args:
        params (PracticeChallengeInput): Skill name and difficulty level.

    Returns:
        str: A specific challenge with actionable steps to build and validate the skill.
    """
    skill = _find_skill(params.skill_name)
    if skill is None:
        return _skill_not_found_message(params.skill_name)

    projects = skill["practice_projects"]
    index_map = {
        Difficulty.BEGINNER: 0,
        Difficulty.INTERMEDIATE: min(1, len(projects) - 1),
        Difficulty.ADVANCED: len(projects) - 1
    }
    project = projects[index_map[params.difficulty]]

    lines = [
        f"# 🏋️ Practice Challenge: {skill['name']}",
        f"**Difficulty**: {params.difficulty.value}\n",
        "## Challenge",
        f"> {project}",
        "\n## How to validate completion:",
        "1. Push working code to a public GitHub repository",
        "2. Write a short README explaining what you built and why",
        "3. Share the project on LinkedIn with a brief writeup",
        "4. If applicable — get a peer or mentor to review it",
    ]

    if skill.get("certification_path"):
        lines.append(f"\n## Next step after this challenge:")
        lines.append(f"📜 Follow certification path: **{skill['certification_path']}**")

    return "\n".join(lines)


@mcp.tool(
    name="skills_compare",
    annotations={
        "title": "Compare Two Skills",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def skills_compare(params: CompareSkillsInput) -> str:
    """Compare two skills side by side to help decide which to prioritize.

    Args:
        params (CompareSkillsInput): Names of the two skills to compare.

    Returns:
        str: A markdown comparison table of both skills.
    """
    skill_a = _find_skill(params.skill_name_a)
    skill_b = _find_skill(params.skill_name_b)

    if skill_a is None:
        return _skill_not_found_message(params.skill_name_a)
    if skill_b is None:
        return _skill_not_found_message(params.skill_name_b)

    lines = [
        "# ⚖️ Skills Comparison\n",
        f"| | **{skill_a['name']}** | **{skill_b['name']}** |",
        "|---|---|---|",
        f"| **Category** | {skill_a['category']} | {skill_b['category']} |",
        f"| **Current Level** | {skill_a['current_level']} | {skill_b['current_level']} |",
        f"| **Target Level** | {skill_a['target_level']} | {skill_b['target_level']} |",
        f"| **Cert Path** | {skill_a.get('certification_path', 'None')} | {skill_b.get('certification_path', 'None')} |",
        f"| **# Resources** | {len(skill_a['learning_resources'])} | {len(skill_b['learning_resources'])} |",
        f"| **# Projects** | {len(skill_a['practice_projects'])} | {len(skill_b['practice_projects'])} |",
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if "--transport" in sys.argv and "streamable-http" in sys.argv:
        port = 8000
        if "--port" in sys.argv:
            port = int(sys.argv[sys.argv.index("--port") + 1])
        mcp.run(transport="streamable_http", port=port)
    else:
        mcp.run()
