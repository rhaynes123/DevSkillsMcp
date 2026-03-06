using DevSkillsMCP.Models;

namespace DevSkillsMCP.Data;

/// <summary>
/// In-memory data store of recommended skills and resources for
/// a Senior .NET developer looking to grow their career.
/// Tailored to the profile: C#/.NET, Kafka, Azure, REST APIs.
/// </summary>
public static class SkillsDataStore
{
    public static readonly List<Skill> RecommendedSkills = new()
    {
        new Skill(
            Name: "Azure Developer Associate (AZ-204)",
            Category: "Cloud",
            CurrentLevel: "Beginner",
            TargetLevel: "Intermediate",
            LearningResources: new()
            {
                "Microsoft Learn: AZ-204 Learning Path",
                "Pluralsight: Developing Solutions for Azure",
                "A Cloud Guru: AZ-204 Course"
            },
            PracticeProjects: new()
            {
                "Deploy a .NET Web API to Azure App Service with CI/CD",
                "Build an Azure Function triggered by Service Bus queue",
                "Implement Azure Key Vault secrets in an existing .NET API"
            },
            CertificationPath: "AZ-900 → AZ-204 → AZ-400 (DevOps Engineer)"
        ),

        new Skill(
            Name: "Azure AI Engineer Associate (AI-102)",
            Category: "AI",
            CurrentLevel: "Beginner",
            TargetLevel: "Intermediate",
            LearningResources: new()
            {
                "Microsoft Learn: AI-102 Learning Path",
                "Anthropic API Documentation",
                "OpenAI .NET SDK GitHub Repository",
                "Azure OpenAI Service Quickstart Docs"
            },
            PracticeProjects: new()
            {
                "Build a .NET chatbot using Azure OpenAI Service",
                "Create an AI-powered code reviewer using the Anthropic API",
                "Add semantic search to an existing .NET API using embeddings"
            },
            CertificationPath: "AZ-204 → AI-102"
        ),

        new Skill(
            Name: "DevSecOps / Security Engineering",
            Category: "Security",
            CurrentLevel: "Beginner",
            TargetLevel: "Intermediate",
            LearningResources: new()
            {
                "Hack The Box: Starting Point Track",
                "TryHackMe: Pre-Security Path",
                "OWASP Top 10 Documentation",
                "AZ-500: Azure Security Engineer Study Guide",
                "PortSwigger Web Security Academy (free)"
            },
            PracticeProjects: new()
            {
                "Complete 10 Hack The Box 'easy' machines",
                "Run OWASP ZAP against one of your own .NET APIs",
                "Implement proper secret scanning in a GitHub Actions pipeline",
                "Add auth + rate limiting to an existing REST API"
            },
            CertificationPath: "Google Cybersecurity Cert → AZ-500 → CompTIA Security+"
        ),

        new Skill(
            Name: "Python",
            Category: "Languages",
            CurrentLevel: "Beginner",
            TargetLevel: "Intermediate",
            LearningResources: new()
            {
                "Python.org Official Tutorial",
                "Advent of Code (use Python to solve challenges)",
                "FastAPI Documentation (great for .NET devs - REST API mindset)",
                "Real Python: Python for .NET Developers"
            },
            PracticeProjects: new()
            {
                "Rewrite one of your existing .NET CLI tools in Python",
                "Build a FastAPI service that mirrors a .NET REST API you built",
                "Create a Python automation script that solves a real daily problem",
                "Complete 30 days of Advent of Code in Python"
            },
            CertificationPath: "No formal cert needed — GitHub projects are sufficient validation"
        ),

        new Skill(
            Name: "Infrastructure as Code (Terraform)",
            Category: "DevOps",
            CurrentLevel: "Beginner",
            TargetLevel: "Intermediate",
            LearningResources: new()
            {
                "HashiCorp Learn: Terraform on Azure",
                "Pluralsight: Terraform - Getting Started",
                "Terraform Up & Running (book by Yevgeniy Brikman)"
            },
            PracticeProjects: new()
            {
                "Provision an Azure App Service + SQL DB with Terraform",
                "Convert an existing manually-created Azure resource to Terraform IaC",
                "Set up a Terraform remote state backend in Azure Blob Storage"
            },
            CertificationPath: "HashiCorp Terraform Associate Certification"
        ),

        new Skill(
            Name: "Advanced System Design",
            Category: "SystemDesign",
            CurrentLevel: "Intermediate",
            TargetLevel: "Advanced",
            LearningResources: new()
            {
                "Designing Data-Intensive Applications (Martin Kleppmann)",
                "ByteByteGo System Design Newsletter",
                "System Design Interview Vol. 1 & 2 (Alex Xu)",
                "High Scalability Blog"
            },
            PracticeProjects: new()
            {
                "Document an architecture decision record (ADR) for a real system you built",
                "Design a rate limiter from scratch and publish it on GitHub",
                "Draw and narrate a system design for UWM's loan workflow on Excalidraw",
                "Build a distributed cache layer in front of an existing .NET service"
            },
            CertificationPath: "No cert — publish design docs and case studies on GitHub/LinkedIn"
        )
    };

    public static readonly List<LearningResource> FeaturedResources = new()
    {
        new LearningResource(
            Title: "Hack The Box",
            Type: "platform",
            Url: "https://www.hackthebox.com",
            Difficulty: "intermediate",
            IsFree: false,
            EstimatedTime: "Ongoing",
            Description: "Gamified cybersecurity platform. Start with 'Starting Point' machines for beginners."
        ),
        new LearningResource(
            Title: "PortSwigger Web Security Academy",
            Type: "platform",
            Url: "https://portswigger.net/web-security",
            Difficulty: "beginner",
            IsFree: true,
            EstimatedTime: "40-60 hours",
            Description: "Free, hands-on web security training covering OWASP Top 10 and more."
        ),
        new LearningResource(
            Title: "Microsoft Learn",
            Type: "platform",
            Url: "https://learn.microsoft.com",
            Difficulty: "beginner",
            IsFree: true,
            EstimatedTime: "Varies by path",
            Description: "Official Microsoft learning paths for all Azure certifications."
        ),
        new LearningResource(
            Title: "Designing Data-Intensive Applications",
            Type: "book",
            Url: "https://dataintensive.net",
            Difficulty: "advanced",
            IsFree: false,
            EstimatedTime: "20-30 hours",
            Description: "The definitive book on building scalable, reliable distributed systems."
        ),
        new LearningResource(
            Title: "Advent of Code",
            Type: "platform",
            Url: "https://adventofcode.com",
            Difficulty: "intermediate",
            IsFree: true,
            EstimatedTime: "1-2 hrs/day in December",
            Description: "Annual coding challenges, great for practicing Python and algorithm skills."
        )
    };

    public static readonly CareerRoadmap SeniorDevRoadmap = new(
        DeveloperProfile: "Senior .NET Developer → Principal / Staff Engineer",
        Phases: new()
        {
            new RoadmapPhase(
                Order: 1,
                Title: "Deepen Cloud (3-6 months)",
                TimeEstimate: "3-6 months",
                Skills: new() { "AZ-204", "Docker", "Azure Container Apps", "Terraform basics" },
                Milestones: new()
                {
                    "Pass AZ-204 exam",
                    "Deploy a containerized .NET app to Azure",
                    "Provision infrastructure with Terraform"
                }
            ),
            new RoadmapPhase(
                Order: 2,
                Title: "AI Integration (3-4 months)",
                TimeEstimate: "3-4 months",
                Skills: new() { "Azure OpenAI", "Prompt Engineering", "AI-102", "LLM API integration" },
                Milestones: new()
                {
                    "Build a .NET app that calls an LLM API",
                    "Pass AI-102 exam",
                    "Ship an AI feature in a real project"
                }
            ),
            new RoadmapPhase(
                Order: 3,
                Title: "Security Hardening (2-3 months)",
                TimeEstimate: "2-3 months",
                Skills: new() { "HTB / TryHackMe", "OWASP Top 10", "AZ-500", "DevSecOps pipelines" },
                Milestones: new()
                {
                    "Complete 10 HTB machines",
                    "Pass AZ-500 exam",
                    "Add SAST scanning to a CI/CD pipeline"
                }
            ),
            new RoadmapPhase(
                Order: 4,
                Title: "Python + Automation (ongoing)",
                TimeEstimate: "Ongoing",
                Skills: new() { "Python", "FastAPI", "Scripting", "Data pipelines" },
                Milestones: new()
                {
                    "Publish 3 Python projects on GitHub",
                    "Build a FastAPI service",
                    "Complete Advent of Code in Python"
                }
            )
        }
    );
}
