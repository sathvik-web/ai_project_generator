"""
File Writer: Central module for file and folder creation.
Handles all file operations for generated projects.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from schemas import GeneratedFile


class FileWriter:
    """Manages file creation and project structure setup."""
    
    def __init__(self, workspace_dir: str = "workspace"):
        """
        Initialize file writer.
        
        Args:
            workspace_dir: Base directory for all generated projects
        """
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
    
    def create_project_structure(self, 
                                project_name: str, 
                                structure: Dict[str, str]) -> Path:
        """
        Create project folder structure.
        
        Args:
            project_name: Name of the project
            structure: Dictionary mapping folder/file paths to descriptions
            
        Returns:
            Path to the created project directory
        """
        project_path = self.workspace_dir / project_name
        project_path.mkdir(exist_ok=True)
        
        # Create all required folders
        for item_path in structure.keys():
            item_full_path = project_path / item_path
            # Create parent directories if it's a file path
            if '.' in item_path.split('/')[-1]:
                item_full_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                item_full_path.mkdir(parents=True, exist_ok=True)
        
        return project_path
    
    def write_files(self, 
                   project_name: str, 
                   files: List[GeneratedFile]) -> Dict[str, bool]:
        """
        Write all generated files to project directory.
        
        Args:
            project_name: Name of the project
            files: List of generated files with content
            
        Returns:
            Dictionary mapping file paths to write success status
        """
        project_path = self.workspace_dir / project_name
        results = {}
        
        for file_obj in files:
            try:
                file_path = project_path / file_obj.path
                
                # Create parent directories
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_obj.content)
                
                results[file_obj.path] = True
                print(f"✓ Created: {file_obj.path}")
            except Exception as e:
                results[file_obj.path] = False
                print(f"✗ Failed to create {file_obj.path}: {e}")
        
        return results
    
    def write_single_file(self, 
                         project_name: str, 
                         file_path: str, 
                         content: str) -> bool:
        """
        Write a single file to project.
        
        Args:
            project_name: Project name
            file_path: Relative file path
            content: File content
            
        Returns:
            Success status
        """
        try:
            full_path = self.workspace_dir / project_name / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    def read_file(self, 
                  project_name: str, 
                  file_path: str) -> str:
        """
        Read a file from project.
        
        Args:
            project_name: Project name
            file_path: Relative file path
            
        Returns:
            File content as string
        """
        try:
            full_path = self.workspace_dir / project_name / file_path
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def get_project_path(self, project_name: str) -> str:
        """Get full path to project."""
        return str(self.workspace_dir / project_name)
    
    def project_exists(self, project_name: str) -> bool:
        """Check if project directory exists."""
        return (self.workspace_dir / project_name).exists()
    
    def get_all_files_in_project(self, project_name: str) -> List[str]:
        """Get list of all files in project."""
        project_path = self.workspace_dir / project_name
        
        if not project_path.exists():
            return []
        
        files = []
        for root, dirs, filenames in os.walk(project_path):
            for filename in filenames:
                full_path = Path(root) / filename
                relative_path = full_path.relative_to(project_path)
                files.append(str(relative_path).replace('\\', '/'))
        
        return files
    
    def delete_project(self, project_name: str) -> bool:
        """Delete entire project directory."""
        try:
            project_path = self.workspace_dir / project_name
            if project_path.exists():
                import shutil
                shutil.rmtree(project_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False
    
    def ensure_directory(self, project_name: str, directory: str) -> bool:
        """Ensure a directory exists in project."""
        try:
            dir_path = self.workspace_dir / project_name / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
