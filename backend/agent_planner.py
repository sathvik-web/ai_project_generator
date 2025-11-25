"""
Agent Planner: Creates project blueprints from natural language prompts.
Decides project structure, files, and folder organization.
"""

import json
from typing import Dict, List, Any
from schemas import ProjectPlan, FileDefinition


class AgentPlanner:
    """Creates project plans from user prompts."""
    
    # Predefined templates for common project types
    TEMPLATES = {
        "fastapi": {
            "tech_stack": ["Python", "FastAPI", "Uvicorn", "Pydantic"],
            "files": [
                {"path": "main.py", "description": "FastAPI application entry point"},
                {"path": "requirements.txt", "description": "Python dependencies"},
                {"path": "README.md", "description": "Project documentation"},
            ],
            "entry_point": "main.py"
        },
        "flask": {
            "tech_stack": ["Python", "Flask", "Werkzeug"],
            "files": [
                {"path": "app.py", "description": "Flask application entry point"},
                {"path": "requirements.txt", "description": "Python dependencies"},
                {"path": "README.md", "description": "Project documentation"},
            ],
            "entry_point": "app.py"
        },
        "streamlit": {
            "tech_stack": ["Python", "Streamlit"],
            "files": [
                {"path": "app.py", "description": "Streamlit application"},
                {"path": "requirements.txt", "description": "Python dependencies"},
                {"path": "README.md", "description": "Project documentation"},
            ],
            "entry_point": "app.py"
        },
        "react": {
            "tech_stack": ["JavaScript", "React", "Node.js"],
            "files": [
                {"path": "package.json", "description": "Project configuration"},
                {"path": "public/index.html", "description": "HTML entry point"},
                {"path": "src/index.js", "description": "React entry point"},
                {"path": "README.md", "description": "Project documentation"},
            ],
            "entry_point": "public/index.html"
        }
    }
    
    # Technology patterns
    TECH_PATTERNS = {
        "fastapi": ["fastapi", "fast api", "api"],
        "flask": ["flask", "web app"],
        "streamlit": ["streamlit", "dashboard", "web ui"],
        "react": ["react", "frontend", "ui"],
        "typescript": ["typescript", "ts"],
        "pytorch": ["pytorch", "torch"],
        "tensorflow": ["tensorflow", "tf"],
        "scikit": ["scikit", "sklearn"],
        "django": ["django"],
        "sqlalchemy": ["sqlalchemy", "sql", "database"],
        "postgresql": ["postgres", "postgresql"],
        "mongodb": ["mongodb", "mongo"],
        "redis": ["redis", "cache"],
    }
    
    def __init__(self):
        """Initialize planner agent."""
        pass
    
    def plan(self, 
            prompt: str,
            memory: Dict[str, Any],
            project_name_override: str = None) -> ProjectPlan:
        """
        Create project plan from prompt.
        
        Args:
            prompt: Natural language project description
            memory: User preferences from memory system
            project_name_override: Optional project name override
            
        Returns:
            ProjectPlan object with structure and files
        """
        # Extract keywords and detect technologies
        prompt_lower = prompt.lower()
        detected_tech = self._detect_technologies(prompt_lower)
        
        # Determine primary framework
        primary_framework = self._determine_primary_framework(detected_tech)
        
        # Generate project name
        project_name = project_name_override or self._generate_project_name(prompt_lower)
        
        # Build file structure
        files = self._build_file_structure(
            detected_tech, 
            primary_framework, 
            prompt_lower
        )
        
        # Create structure description
        structure = self._create_structure_description(files)
        
        # Determine entry point
        entry_point = self._determine_entry_point(files, primary_framework)
        
        plan = ProjectPlan(
            project_name=project_name,
            description=self._generate_description(prompt),
            tech_stack=detected_tech,
            structure=structure,
            files=files,
            entry_point=entry_point
        )
        
        return plan
    
    def _detect_technologies(self, prompt: str) -> List[str]:
        """Detect technologies from prompt."""
        detected = []
        
        for tech, patterns in self.TECH_PATTERNS.items():
            for pattern in patterns:
                if pattern in prompt:
                    tech_display = tech.upper() if len(tech) <= 5 else tech.title()
                    if tech_display not in detected:
                        detected.append(tech_display)
                    break
        
        # Add defaults if none detected
        if not detected:
            detected = ["Python", "FastAPI"]
        
        return detected
    
    def _determine_primary_framework(self, tech_stack: List[str]) -> str:
        """Determine primary framework from tech stack."""
        tech_lower = [t.lower() for t in tech_stack]
        
        if any(t in tech_lower for t in ["fastapi", "flask", "django"]):
            if "fastapi" in tech_lower:
                return "fastapi"
            elif "flask" in tech_lower:
                return "flask"
            elif "django" in tech_lower:
                return "django"
        
        if "streamlit" in tech_lower:
            return "streamlit"
        
        if "react" in tech_lower:
            return "react"
        
        return "fastapi"  # default
    
    def _generate_project_name(self, prompt: str) -> str:
        """Generate project name from prompt."""
        # Extract meaningful words
        words = prompt.split()
        
        # Filter and clean words
        filtered_words = [
            w.lower() for w in words 
            if len(w) > 3 and w.isalpha()
        ][:3]
        
        project_name = "_".join(filtered_words) if filtered_words else "generated_project"
        
        # Ensure valid Python identifier
        project_name = project_name.replace("-", "_")
        
        return project_name or "generated_project"
    
    def _build_file_structure(self,
                             tech_stack: List[str],
                             framework: str,
                             prompt: str) -> List[FileDefinition]:
        """Build list of files needed for project."""
        files = []
        
        # Start with framework template
        template = self.TEMPLATES.get(framework, self.TEMPLATES["fastapi"])
        base_files = template.get("files", [])
        
        for file_def in base_files:
            files.append(FileDefinition(
                path=file_def["path"],
                description=file_def["description"],
                file_type=file_def["path"].split('.')[-1]
            ))
        
        # Add additional files based on tech stack
        if "pytorch" in [t.lower() for t in tech_stack]:
            files.append(FileDefinition(
                path="model.py",
                description="PyTorch model definition",
                file_type="py"
            ))
        
        if "tensorflow" in [t.lower() for t in tech_stack]:
            files.append(FileDefinition(
                path="model.py",
                description="TensorFlow model definition",
                file_type="py"
            ))
        
        # Add config file if needed
        if "config" in prompt.lower() or "settings" in prompt.lower():
            files.append(FileDefinition(
                path="config.py",
                description="Configuration management",
                file_type="py"
            ))
        
        # Add database files if mentioned
        if any(db in prompt.lower() for db in ["database", "db", "sql", "mongo"]):
            files.append(FileDefinition(
                path="database.py",
                description="Database configuration and models",
                file_type="py"
            ))
        
        return files
    
    def _create_structure_description(self, files: List[FileDefinition]) -> Dict[str, str]:
        """Create folder structure description."""
        structure = {}
        
        # Add files
        for file_def in files:
            structure[file_def.path] = file_def.description
        
        # Add common folders
        structure["src/"] = "Source code directory"
        structure["tests/"] = "Test files"
        
        return structure
    
    def _determine_entry_point(self, 
                               files: List[FileDefinition], 
                               framework: str) -> str:
        """Determine application entry point."""
        for file_def in files:
            if file_def.path in ["main.py", "app.py"]:
                return file_def.path
        
        # Fallback
        return files[0].path if files else "main.py"
    
    def _generate_description(self, prompt: str) -> str:
        """Generate project description from prompt."""
        # Take first 150 chars as description
        description = prompt[:150]
        if len(prompt) > 150:
            description += "..."
        return description
    
    def refine_plan(self, 
                   plan: ProjectPlan, 
                   feedback: str) -> ProjectPlan:
        """
        Refine project plan based on feedback.
        
        Args:
            plan: Original plan
            feedback: User feedback
            
        Returns:
            Refined project plan
        """
        # This would use LLM in production
        # For now, we'll do basic modifications
        
        feedback_lower = feedback.lower()
        
        # Add files based on feedback
        if "test" in feedback_lower:
            if not any("test" in f.path for f in plan.files):
                plan.files.append(FileDefinition(
                    path="tests/test_main.py",
                    description="Unit tests",
                    file_type="py"
                ))
        
        if "docker" in feedback_lower:
            if "Dockerfile" not in plan.structure:
                plan.files.append(FileDefinition(
                    path="Dockerfile",
                    description="Docker container configuration",
                    file_type="dockerfile"
                ))
        
        if "github" in feedback_lower or "ci" in feedback_lower:
            if ".github" not in str(plan.structure):
                plan.files.append(FileDefinition(
                    path=".github/workflows/ci.yml",
                    description="GitHub CI/CD workflow",
                    file_type="yml"
                ))
        
        return plan
