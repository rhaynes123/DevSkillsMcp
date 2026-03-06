namespace DevSkillsMCP.Models;

public record Skill(
    string Name,
    string Category,
    string CurrentLevel,
    string TargetLevel,
    List<string> LearningResources,
    List<string> PracticeProjects,
    string? CertificationPath
);

public record LearningResource(
    string Title,
    string Type,       // "course", "book", "platform", "certification", "project"
    string Url,
    string Difficulty, // "beginner", "intermediate", "advanced"
    bool IsFree,
    string EstimatedTime,
    string Description
);

public record CareerRoadmap(
    string DeveloperProfile,
    List<RoadmapPhase> Phases
);

public record RoadmapPhase(
    int Order,
    string Title,
    string TimeEstimate,
    List<string> Skills,
    List<string> Milestones
);

public enum SkillLevel
{
    Beginner,
    Intermediate,
    Advanced,
    Expert
}

public enum SkillCategory
{
    Cloud,
    AI,
    Security,
    Backend,
    SystemDesign,
    Languages,
    DevOps
}
