"""
Example test file demonstrating AI Project Generator
Shows how the system generates, reviews, and validates code
"""

import pytest
import json
from pathlib import Path
from backend.agent_planner import AgentPlanner
from backend.agent_generator import AgentGenerator
from backend.agent_reviewer import AgentReviewer
from backend.memory_manager import MemoryManager
from backend.file_writer import FileWriter


class TestAgentPlanner:
    """Test project planning agent."""
    
    def test_plan_fastapi_project(self):
        """Test creating a FastAPI project plan."""
        planner = AgentPlanner()
        memory = {}
        
        prompt = "Create a FastAPI REST API with PostgreSQL"
        plan = planner.plan(prompt, memory)
        
        assert plan.project_name
        assert plan.description
        assert plan.tech_stack
        assert plan.files
        assert "fastapi" in [t.lower() for t in plan.tech_stack]
    
    def test_plan_generates_valid_files(self):
        """Test that plan includes valid file definitions."""
        planner = AgentPlanner()
        plan = planner.plan("Create a web app", {})
        
        assert len(plan.files) > 0
        for file_def in plan.files:
            assert file_def.path
            assert file_def.description
            assert file_def.file_type


class TestCodeGenerator:
    """Test code generation agent."""
    
    def test_generate_fastapi_main(self):
        """Test generating FastAPI main file."""
        planner = AgentPlanner()
        generator = AgentGenerator()
        
        plan = planner.plan("Create a FastAPI app", {})
        files = generator.generate_files(plan, {})
        
        assert len(files) > 0
        main_file = next((f for f in files if "main" in f.path), None)
        assert main_file
        assert "FastAPI" in main_file.content or "fastapi" in main_file.content


class TestCodeReviewer:
    """Test code review agent."""
    
    def test_review_detects_issues(self):
        """Test that reviewer detects code issues."""
        from backend.schemas import GeneratedFile
        
        bad_code = '''def my_function(x):
    return x * 2


def another_func(a,b,c):
    result = a+b+c
    return result  
'''
        
        file_obj = GeneratedFile(path="test.py", content=bad_code)
        reviewer = AgentReviewer()
        reviewed = reviewer.review_file(file_obj)
        
        assert reviewed.reviewed
        assert reviewed.review_notes
        assert len(reviewed.content) >= len(bad_code)  # Should add improvements


class TestMemoryManager:
    """Test user memory system."""
    
    def test_memory_loads_and_saves(self, tmp_path):
        """Test memory persistence."""
        memory = MemoryManager(str(tmp_path))
        
        # Update preference
        memory.update_preference("test_key", "test_value")
        
        # Verify saved
        assert memory.get_memory().preferences["test_key"] == "test_value"
    
    def test_memory_learns_from_project(self, tmp_path):
        """Test that memory learns from projects."""
        memory = MemoryManager(str(tmp_path))
        
        initial_count = len(memory.get_projects())
        memory.learn_from_project({
            "project_name": "test_project",
            "tech_stack": ["FastAPI", "PyTorch"]
        })
        
        assert len(memory.get_projects()) > initial_count
        assert "FastAPI" in memory.memory.frameworks


class TestFileWriter:
    """Test file writing system."""
    
    def test_create_project_structure(self, tmp_path):
        """Test creating project structure."""
        writer = FileWriter(str(tmp_path))
        
        structure = {
            "main.py": "Main file",
            "src/": "Source directory",
            "tests/": "Tests directory"
        }
        
        project_path = writer.create_project_structure("test_project", structure)
        assert project_path.exists()
    
    def test_write_files(self, tmp_path):
        """Test writing files to project."""
        from backend.schemas import GeneratedFile
        
        writer = FileWriter(str(tmp_path))
        
        # Create project structure
        writer.create_project_structure("test_project", {})
        
        # Write files
        files = [
            GeneratedFile(path="main.py", content="print('Hello')"),
            GeneratedFile(path="config.py", content="DEBUG = True")
        ]
        
        results = writer.write_files("test_project", files)
        assert results["main.py"]
        assert results["config.py"]


class TestIntegration:
    """Integration tests for full pipeline."""
    
    def test_full_generation_pipeline(self, tmp_path):
        """Test complete project generation pipeline."""
        # Setup
        planner = AgentPlanner()
        generator = AgentGenerator()
        reviewer = AgentReviewer()
        writer = FileWriter(str(tmp_path))
        
        # Plan
        prompt = "Create a simple FastAPI app"
        plan = planner.plan(prompt, {})
        
        # Generate
        files = generator.generate_files(plan, {})
        
        # Review
        reviewed_files = reviewer.review_files(files)
        
        # Write
        writer.create_project_structure(plan.project_name, plan.structure)
        results = writer.write_files(plan.project_name, reviewed_files)
        
        # Verify
        assert len(results) > 0
        assert sum(1 for v in results.values() if v) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
