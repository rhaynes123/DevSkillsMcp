using DevSkillsMCP.Data;
using DevSkillsMCP.Models;
using ModelContextProtocol.Server;
using System.ComponentModel;
using System.Text;
using System.Text.Json;

namespace DevSkillsMCP.Tools;

/// <summary>
/// MCP Tools for the Developer Skills server.
/// Helps senior software developers discover, plan, and validate new skills.
/// </summary>
[McpServerToolType]
public static class DevSkillsTools
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    // ─────────────────────────────────────────────
    // TOOL: List All Recommended Skills
    // ─────────────────────────────────────────────
    [McpServerTool(Name = "skills_list_recommended")]
    [Description("List all recommended skills for a senior .NET developer to learn, optionally filtered by category. Categories: Cloud, AI, Security, Languages, DevOps, SystemDesign.")]
    public static string ListRecommendedSkills(
        [Description("Optional category filter (e.g. 'Cloud', 'AI', 'Security'). Leave empty for all.")] string? category = null,
        [Description("Response format: 'markdown' for readable output or 'json' for structured data.")] string responseFormat = "markdown")
    {
        var skills = SkillsDataStore.RecommendedSkills;

        if (!string.IsNullOrWhiteSpace(category))
        {
            skills = skills
                .Where(s => s.Category.Equals(category.Trim(), StringComparison.OrdinalIgnoreCase))
                .ToList();

            if (!skills.Any())
                return $"No skills found in category '{category}'. Valid categories: Cloud, AI, Security, Languages, DevOps, SystemDesign.";
        }

        if (responseFormat.Equals("json", StringComparison.OrdinalIgnoreCase))
            return JsonSerializer.Serialize(skills, JsonOptions);

        var sb = new StringBuilder();
        sb.AppendLine("# 🎯 Recommended Skills for Senior .NET Developers\n");

        foreach (var group in skills.GroupBy(s => s.Category))
        {
            sb.AppendLine($"## {group.Key}");
            foreach (var skill in group)
            {
                sb.AppendLine($"### {skill.Name}");
                sb.AppendLine($"- **Current → Target**: {skill.CurrentLevel} → {skill.TargetLevel}");
                if (skill.CertificationPath != null)
                    sb.AppendLine($"- **Certification Path**: {skill.CertificationPath}");
                sb.AppendLine();
            }
        }

        return sb.ToString();
    }

    // ─────────────────────────────────────────────
    // TOOL: Get Skill Detail
    // ─────────────────────────────────────────────
    [McpServerTool(Name = "skills_get_detail")]
    [Description("Get detailed information about a specific skill including learning resources, practice projects, and certification path. Use skills_list_recommended first to get skill names.")]
    public static string GetSkillDetail(
        [Description("The exact name of the skill (e.g. 'Python', 'Azure Developer Associate (AZ-204)')")] string skillName,
        [Description("Response format: 'markdown' or 'json'.")] string responseFormat = "markdown")
    {
        var skill = SkillsDataStore.RecommendedSkills
            .FirstOrDefault(s => s.Name.Equals(skillName.Trim(), StringComparison.OrdinalIgnoreCase));

        if (skill is null)
        {
            var available = string.Join(", ", SkillsDataStore.RecommendedSkills.Select(s => s.Name));
            return $"Skill '{skillName}' not found. Available skills: {available}";
        }

        if (responseFormat.Equals("json", StringComparison.OrdinalIgnoreCase))
            return JsonSerializer.Serialize(skill, JsonOptions);

        var sb = new StringBuilder();
        sb.AppendLine($"# 📚 {skill.Name}");
        sb.AppendLine($"\n**Category**: {skill.Category}");
        sb.AppendLine($"**Level**: {skill.CurrentLevel} → {skill.TargetLevel}");

        if (skill.CertificationPath != null)
            sb.AppendLine($"**Certification Path**: {skill.CertificationPath}");

        sb.AppendLine("\n## 📖 Learning Resources");
        foreach (var resource in skill.LearningResources)
            sb.AppendLine($"- {resource}");

        sb.AppendLine("\n## 🛠️ Practice Projects");
        foreach (var (project, i) in skill.PracticeProjects.Select((p, i) => (p, i + 1)))
            sb.AppendLine($"{i}. {project}");

        return sb.ToString();
    }

    // ─────────────────────────────────────────────
    // TOOL: Get Career Roadmap
    // ─────────────────────────────────────────────
    [McpServerTool(Name = "skills_get_roadmap")]
    [Description("Get the full recommended career roadmap for a Senior .NET Developer looking to grow toward Staff/Principal Engineer level, broken into phases with timelines and milestones.")]
    public static string GetCareerRoadmap(
        [Description("Response format: 'markdown' or 'json'.")] string responseFormat = "markdown")
    {
        var roadmap = SkillsDataStore.SeniorDevRoadmap;

        if (responseFormat.Equals("json", StringComparison.OrdinalIgnoreCase))
            return JsonSerializer.Serialize(roadmap, JsonOptions);

        var sb = new StringBuilder();
        sb.AppendLine($"# 🗺️ Career Roadmap: {roadmap.DeveloperProfile}\n");

        foreach (var phase in roadmap.Phases.OrderBy(p => p.Order))
        {
            sb.AppendLine($"## Phase {phase.Order}: {phase.Title} ({phase.TimeEstimate})");

            sb.AppendLine("\n**Skills to learn:**");
            foreach (var skill in phase.Skills)
                sb.AppendLine($"- {skill}");

            sb.AppendLine("\n**Milestones:**");
            foreach (var milestone in phase.Milestones)
                sb.AppendLine($"- [ ] {milestone}");

            sb.AppendLine();
        }

        return sb.ToString();
    }

    // ─────────────────────────────────────────────
    // TOOL: List Learning Resources
    // ─────────────────────────────────────────────
    [McpServerTool(Name = "skills_list_resources")]
    [Description("List featured learning resources, optionally filtered by type or difficulty. Types: course, book, platform, certification, project. Difficulty: beginner, intermediate, advanced.")]
    public static string ListLearningResources(
        [Description("Filter by resource type: 'course', 'book', 'platform', 'certification', 'project'. Leave empty for all.")] string? type = null,
        [Description("Filter by difficulty: 'beginner', 'intermediate', 'advanced'. Leave empty for all.")] string? difficulty = null,
        [Description("Only show free resources. Default: false.")] bool freeOnly = false,
        [Description("Response format: 'markdown' or 'json'.")] string responseFormat = "markdown")
    {
        var resources = SkillsDataStore.FeaturedResources.AsEnumerable();

        if (!string.IsNullOrWhiteSpace(type))
            resources = resources.Where(r => r.Type.Equals(type.Trim(), StringComparison.OrdinalIgnoreCase));

        if (!string.IsNullOrWhiteSpace(difficulty))
            resources = resources.Where(r => r.Difficulty.Equals(difficulty.Trim(), StringComparison.OrdinalIgnoreCase));

        if (freeOnly)
            resources = resources.Where(r => r.IsFree);

        var list = resources.ToList();

        if (!list.Any())
            return "No resources found matching the specified filters.";

        if (responseFormat.Equals("json", StringComparison.OrdinalIgnoreCase))
            return JsonSerializer.Serialize(list, JsonOptions);

        var sb = new StringBuilder();
        sb.AppendLine("# 🔗 Learning Resources\n");

        foreach (var resource in list)
        {
            sb.AppendLine($"### {resource.Title}");
            sb.AppendLine($"- **Type**: {resource.Type} | **Difficulty**: {resource.Difficulty} | **Free**: {(resource.IsFree ? "✅" : "💰")}");
            sb.AppendLine($"- **Time**: {resource.EstimatedTime}");
            sb.AppendLine($"- **URL**: {resource.Url}");
            sb.AppendLine($"- {resource.Description}");
            sb.AppendLine();
        }

        return sb.ToString();
    }

    // ─────────────────────────────────────────────
    // TOOL: Get Practice Challenge
    // ─────────────────────────────────────────────
    [McpServerTool(Name = "skills_get_practice_challenge")]
    [Description("Get a specific practice challenge or project idea for a given skill. Returns actionable steps to build and validate the skill through hands-on work.")]
    public static string GetPracticeChallenge(
        [Description("The skill name to get a challenge for (e.g. 'Python', 'DevSecOps / Security Engineering')")] string skillName,
        [Description("The difficulty level: 'beginner', 'intermediate', 'advanced'. Default: beginner.")] string difficulty = "beginner")
    {
        var skill = SkillsDataStore.RecommendedSkills
            .FirstOrDefault(s => s.Name.Equals(skillName.Trim(), StringComparison.OrdinalIgnoreCase));

        if (skill is null)
        {
            var available = string.Join(", ", SkillsDataStore.RecommendedSkills.Select(s => s.Name));
            return $"Skill '{skillName}' not found. Available: {available}";
        }

        // Pick project based on difficulty
        var projectIndex = difficulty.ToLower() switch
        {
            "beginner" => 0,
            "intermediate" => Math.Min(1, skill.PracticeProjects.Count - 1),
            "advanced" => skill.PracticeProjects.Count - 1,
            _ => 0
        };

        var project = skill.PracticeProjects[projectIndex];

        var sb = new StringBuilder();
        sb.AppendLine($"# 🏋️ Practice Challenge: {skill.Name}");
        sb.AppendLine($"**Difficulty**: {difficulty}\n");
        sb.AppendLine($"## Challenge");
        sb.AppendLine($"> {project}");
        sb.AppendLine("\n## How to validate completion:");
        sb.AppendLine("1. Push working code to a public GitHub repository");
        sb.AppendLine("2. Write a short README explaining what you built and why");
        sb.AppendLine("3. Share the project on LinkedIn with a brief writeup");
        sb.AppendLine("4. If applicable — get a peer or mentor to review it");

        if (skill.CertificationPath != null)
        {
            sb.AppendLine($"\n## Next step after this challenge:");
            sb.AppendLine($"📜 Follow certification path: **{skill.CertificationPath}**");
        }

        return sb.ToString();
    }

    // ─────────────────────────────────────────────
    // TOOL: Compare Skills
    // ─────────────────────────────────────────────
    [McpServerTool(Name = "skills_compare")]
    [Description("Compare two skills side by side — useful for deciding which to prioritize next in your learning journey.")]
    public static string CompareSkills(
        [Description("First skill name to compare.")] string skillNameA,
        [Description("Second skill name to compare.")] string skillNameB)
    {
        var skillA = SkillsDataStore.RecommendedSkills
            .FirstOrDefault(s => s.Name.Equals(skillNameA.Trim(), StringComparison.OrdinalIgnoreCase));

        var skillB = SkillsDataStore.RecommendedSkills
            .FirstOrDefault(s => s.Name.Equals(skillNameB.Trim(), StringComparison.OrdinalIgnoreCase));

        if (skillA is null) return $"Skill '{skillNameA}' not found.";
        if (skillB is null) return $"Skill '{skillNameB}' not found.";

        var sb = new StringBuilder();
        sb.AppendLine("# ⚖️ Skills Comparison\n");
        sb.AppendLine($"| | **{skillA.Name}** | **{skillB.Name}** |");
        sb.AppendLine("|---|---|---|");
        sb.AppendLine($"| **Category** | {skillA.Category} | {skillB.Category} |");
        sb.AppendLine($"| **Current Level** | {skillA.CurrentLevel} | {skillB.CurrentLevel} |");
        sb.AppendLine($"| **Target Level** | {skillA.TargetLevel} | {skillB.TargetLevel} |");
        sb.AppendLine($"| **Cert Path** | {skillA.CertificationPath ?? "None"} | {skillB.CertificationPath ?? "None"} |");
        sb.AppendLine($"| **# Resources** | {skillA.LearningResources.Count} | {skillB.LearningResources.Count} |");
        sb.AppendLine($"| **# Projects** | {skillA.PracticeProjects.Count} | {skillB.PracticeProjects.Count} |");

        return sb.ToString();
    }
}
