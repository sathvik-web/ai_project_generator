"""
Pydantic schemas for request/response validation.
Defines all data models used in the AI Project Generator system.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ProjectPlanRequest(BaseModel):
    """Request model for project planning."""
    prompt: str = Field(..., description="Natural language project description")
    project_name: Optional[str] = Field(None, description="Optional project name override")


class ProjectGenerateRequest(BaseModel):
    """Request model for full project generation."""
    prompt: str = Field(..., description="Natural language project description")
    github_repo_name: Optional[str] = Field(None, description="GitHub repo name")
    github_token: Optional[str] = Field(None, description="GitHub personal access token")
    auto_push: bool = Field(True, description="Automatically push to GitHub")


class ProjectUpdateRequest(BaseModel):
    """Request model for updating existing projects."""
    github_repo_url: str = Field(..., description="URL of existing GitHub repo")
    update_prompt: str = Field(..., description="What to update/improve")
    github_token: Optional[str] = Field(None, description="GitHub personal access token")
    auto_push: bool = Field(True, description="Automatically push changes")
    commit_message: Optional[str] = Field("Update from AI Project Generator", description="Commit message")


class FileEditRequest(BaseModel):
    """Request model for editing file content."""
    content: str = Field(..., description="New file content")


class FilePushRequest(BaseModel):
    """Request model for pushing to GitHub."""
    message: str = Field(..., description="Commit message")
    repo_name: Optional[str] = Field(None, description="GitHub repo name")


class FileDefinition(BaseModel):
    """Definition of a single file in project plan."""
    path: str = Field(..., description="File path relative to project root")
    description: str = Field(..., description="What this file should contain")
    file_type: str = Field("py", description="File type/extension")


class ProjectPlan(BaseModel):
    """Project blueprint created by planner agent."""
    project_name: str = Field(..., description="Unique project identifier")
    description: str = Field(..., description="Project overview")
    tech_stack: List[str] = Field(..., description="Technologies to use")
    structure: Dict[str, str] = Field(..., description="Folder/file descriptions")
    files: List[FileDefinition] = Field(..., description="Files to be generated")
    entry_point: str = Field(..., description="Main entry point file")


class GeneratedFile(BaseModel):
    """A generated code file."""
    path: str = Field(..., description="File path")
    content: str = Field(..., description="File content")
    reviewed: bool = Field(False, description="Whether file has been reviewed")
    review_notes: str = Field("", description="Reviewer feedback")


class ProjectGeneration(BaseModel):
    """Complete project generation output."""
    project_name: str
    plan: ProjectPlan
    files: List[GeneratedFile]
    memory_updates: Dict[str, str] = Field(default_factory=dict)


class GenerationResponse(BaseModel):
    """Response for project generation endpoint."""
    success: bool
    message: str
    project_name: str
    repo_url: Optional[str] = None
    files_created: int
    workspace_path: str


class UpdateResponse(BaseModel):
    """Response for project update endpoint."""
    success: bool
    message: str
    files_modified: int
    repo_url: str


class MemoryEntry(BaseModel):
    """Single entry in memory system."""
    key: str
    value: str
    timestamp: str
    project_context: str = ""


class UserMemory(BaseModel):
    """User preferences and learning data."""
    preferred_backend: str = "fastapi"
    preferred_frontend: str = "streamlit"
    coding_style: str = "descriptive comments, type hints, docstrings"
    common_issues: List[str] = []
    frameworks: List[str] = []
    language_preference: str = "python"
    database_preference: str = "sqlite"
    last_projects: List[str] = []
    preferences: Dict[str, str] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: str
    code: int
