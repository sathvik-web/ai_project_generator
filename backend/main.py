"""
FastAPI Backend: Main API server for AI Project Generator.
Provides endpoints for project generation, updates, and memory management.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import agents and managers
from schemas import (
    ProjectGenerateRequest, ProjectUpdateRequest, GenerationResponse,
    UpdateResponse, ErrorResponse, FileEditRequest, FilePushRequest
)
from memory_manager import MemoryManager
from file_writer import FileWriter
from github_manager import GitHubManager
from agent_planner import AgentPlanner
from agent_generator import AgentGenerator
from agent_reviewer import AgentReviewer


# Initialize FastAPI app
app = FastAPI(
    title="AI Project Generator",
    description="Intelligent agent that creates complete software projects from natural language",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers and agents
memory_manager = MemoryManager("memory")
file_writer = FileWriter("workspace")
planner = AgentPlanner()
generator = AgentGenerator()
reviewer = AgentReviewer()

# Get configuration from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")


@app.get("/")
async def root():
    """Root endpoint with system info."""
    return {
        "service": "AI Project Generator",
        "status": "running",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "memory": "loaded" if memory_manager.memory else "error"
    }


@app.post("/generate", response_model=GenerationResponse)
async def generate_project(
    request: ProjectGenerateRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a complete new project from prompt.
    
    Args:
        request: Project generation request with prompt
        background_tasks: Background task handler for GitHub push
        
    Returns:
        Generation response with repo URL and file count
    """
    try:
        logger.info(f"Generating project from prompt: {request.prompt[:50]}...")
        
        # Step 1: Plan the project
        project_plan = planner.plan(
            request.prompt,
            memory_manager.get_memory_dict(),
            request.github_repo_name
        )
        logger.info(f"✓ Project plan created: {project_plan.project_name}")
        
        # Step 2: Generate code files
        generated_files = generator.generate_files(
            project_plan,
            memory_manager.get_memory_dict()
        )
        logger.info(f"✓ Generated {len(generated_files)} files")
        
        # Step 3: Review and improve code
        reviewed_files = reviewer.review_files(generated_files)
        logger.info(f"✓ Code review completed")
        
        # Step 4: Write files to workspace
        project_path = file_writer.create_project_structure(
            project_plan.project_name,
            project_plan.structure
        )
        
        write_results = file_writer.write_files(
            project_plan.project_name,
            reviewed_files
        )
        files_created = sum(1 for success in write_results.values() if success)
        logger.info(f"✓ Wrote {files_created} files to workspace")
        
        # Step 5: Update memory with project info
        memory_manager.learn_from_project({
            "project_name": project_plan.project_name,
            "tech_stack": project_plan.tech_stack,
            "style_notes": memory_manager.memory.coding_style
        })
        logger.info(f"✓ Memory updated")
        
        # Step 6: Push to GitHub if requested
        repo_url = None
        if request.auto_push and GITHUB_TOKEN and GITHUB_USERNAME:
            background_tasks.add_task(
                _push_to_github,
                project_plan.project_name,
                str(project_path),
                request.github_repo_name or project_plan.project_name,
                project_plan.description
            )
            repo_url = f"https://github.com/{GITHUB_USERNAME}/{request.github_repo_name or project_plan.project_name}"
            logger.info(f"✓ GitHub push scheduled")
        
        return GenerationResponse(
            success=True,
            message=f"Project {project_plan.project_name} generated successfully",
            project_name=project_plan.project_name,
            repo_url=repo_url,
            files_created=files_created,
            workspace_path=str(project_path)
        )
    
    except Exception as e:
        logger.error(f"Error generating project: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Project generation failed: {str(e)}"
        )


@app.post("/update", response_model=UpdateResponse)
async def update_project(
    request: ProjectUpdateRequest,
    background_tasks: BackgroundTasks
):
    """
    Update an existing project from GitHub or locally.
    
    Args:
        request: Project update request with GitHub URL and update prompt
        background_tasks: Background task handler
        
    Returns:
        Update response with file count
    """
    try:
        logger.info(f"Starting project update: {request.github_repo_url}")
        
        # Extract repo name from URL
        repo_url_parts = request.github_repo_url.rstrip('/').split('/')
        repo_name = repo_url_parts[-1]
        github_user = repo_url_parts[-2]
        
        # Create a temporary project name for the update
        update_project_name = f"{repo_name}_updated"
        
        # Step 1: Clone or create update plan
        logger.info(f"Planning updates for {repo_name}...")
        update_plan = planner.plan(
            request.update_prompt,
            memory_manager.get_memory_dict(),
            update_project_name
        )
        logger.info(f"✓ Update plan created")
        
        # Step 2: Generate updated files
        logger.info(f"Generating updated files...")
        generated_files = generator.generate_files(
            update_plan,
            memory_manager.get_memory_dict()
        )
        logger.info(f"✓ Generated {len(generated_files)} files")
        
        # Step 3: Review updated code
        logger.info(f"Reviewing updated code...")
        reviewed_files = reviewer.review_files(generated_files)
        logger.info(f"✓ Code review completed")
        
        # Step 4: Update memory
        memory_manager.learn_from_project({
            "project_name": update_project_name,
            "tech_stack": update_plan.tech_stack,
            "style_notes": memory_manager.memory.coding_style
        })
        
        # Step 5: If auto_push is true, schedule GitHub update
        if request.auto_push:
            if not GITHUB_TOKEN:
                logger.warning("GitHub token not configured")
            else:
                # For now, we'll create a local copy with updates
                # In a full implementation, this would push directly to GitHub
                project_path = file_writer.create_project_structure(
                    update_project_name,
                    update_plan.structure
                )
                file_writer.write_files(update_project_name, reviewed_files)
                
                background_tasks.add_task(
                    _push_to_github,
                    update_project_name,
                    str(project_path),
                    repo_name,
                    request.commit_message or "Update from AI Project Generator"
                )
                logger.info(f"✓ GitHub push scheduled")
        
        return UpdateResponse(
            success=True,
            message=f"Project {repo_name} update completed",
            files_modified=len(reviewed_files),
            repo_url=request.github_repo_url
        )
    
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Project update failed: {str(e)}"
        )


@app.get("/memory")
async def get_memory():
    """Get current user memory and preferences."""
    return memory_manager.get_memory_dict()


@app.post("/memory/reset")
async def reset_memory():
    """Reset memory to defaults."""
    memory_manager.reset_memory()
    return {"message": "Memory reset to defaults", "memory": memory_manager.get_memory_dict()}


@app.get("/projects")
async def get_recent_projects():
    """Get list of recently generated projects."""
    return {
        "projects": memory_manager.get_projects()
    }


@app.get("/project/{project_name}")
async def get_project_info(project_name: str):
    """Get information about a specific project."""
    project_path = file_writer.get_project_path(project_name)
    
    if not file_writer.project_exists(project_name):
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_name} not found"
        )
    
    files = file_writer.get_all_files_in_project(project_name)
    
    return {
        "project_name": project_name,
        "path": project_path,
        "files": files,
        "file_count": len(files)
    }


@app.delete("/project/{project_name}")
async def delete_project(project_name: str):
    """Delete a project."""
    if file_writer.delete_project(project_name):
        return {"message": f"Project {project_name} deleted"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_name} not found"
        )


@app.get("/project/{project_name}/file/{file_path:path}")
async def get_file_content(project_name: str, file_path: str):
    """Get content of a specific file in project."""
    if not file_writer.project_exists(project_name):
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_name} not found"
        )
    
    content = file_writer.read_file(project_name, file_path)
    
    if content is None or content == "":
        raise HTTPException(
            status_code=404,
            detail=f"File {file_path} not found"
        )
    
    return {
        "project_name": project_name,
        "file_path": file_path,
        "content": content
    }


@app.post("/project/{project_name}/file/{file_path:path}")
async def update_file_content(
    project_name: str,
    file_path: str,
    request: FileEditRequest
):
    """Update content of a specific file in project."""
    if not file_writer.project_exists(project_name):
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_name} not found"
        )
    
    success = file_writer.write_single_file(
        project_name,
        file_path,
        request.content
    )
    
    if success:
        logger.info(f"✓ Updated file: {project_name}/{file_path}")
        return {
            "success": True,
            "message": f"File {file_path} updated",
            "project_name": project_name,
            "file_path": file_path
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update file {file_path}"
        )


@app.post("/project/{project_name}/push")
async def push_project_to_github(
    project_name: str,
    request: FilePushRequest,
    background_tasks: BackgroundTasks
):
    """Push project changes to GitHub."""
    if not file_writer.project_exists(project_name):
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_name} not found"
        )
    
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        raise HTTPException(
            status_code=400,
            detail="GitHub credentials not configured. Set GITHUB_TOKEN and GITHUB_USERNAME in .env"
        )
    
    repo_name = request.repo_name or project_name
    project_path = file_writer.get_project_path(project_name)
    
    background_tasks.add_task(
        _push_to_github,
        project_name,
        project_path,
        repo_name,
        f"Update: {request.message}"
    )
    
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
    
    return {
        "success": True,
        "message": f"Push to {repo_name} scheduled",
        "repo_url": repo_url,
        "project_name": project_name
    }



@app.post("/preference")
async def set_preference(key: str, value: str):
    """Update a user preference."""
    memory_manager.update_preference(key, value)
    return {
        "message": f"Preference {key} updated",
        "value": value
    }


def _push_to_github(
    project_name: str,
    project_path: str,
    repo_name: str,
    description: str
):
    """Push project to GitHub (background task)."""
    try:
        if not GITHUB_TOKEN or not GITHUB_USERNAME:
            logger.warning("GitHub credentials not configured")
            return
        
        github = GitHubManager(GITHUB_TOKEN, GITHUB_USERNAME)
        
        # Create repository
        logger.info(f"Creating repository: {repo_name}")
        github.create_repo(repo_name, description)
        
        # Upload project files
        logger.info(f"Uploading files to {repo_name}")
        upload_results = github.upload_project(repo_name, project_path)
        
        success_count = sum(1 for v in upload_results.values() if v)
        logger.info(f"✓ GitHub push completed: {success_count} files uploaded")
        
    except Exception as e:
        logger.error(f"Error pushing to GitHub: {e}")


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Project Generator API...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
