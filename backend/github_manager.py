"""
GitHub Manager: Handles GitHub repository operations.
Manages repo creation, file uploads, commits, and pushes.
"""

import base64
import requests
import json
from typing import Optional, List, Dict, Any
from pathlib import Path


class GitHubManager:
    """Manages GitHub repository operations using REST API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, github_token: str, github_username: str):
        """
        Initialize GitHub manager.
        
        Args:
            github_token: GitHub personal access token
            github_username: GitHub username
        """
        self.token = github_token
        self.username = github_username
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def _request(self, 
                method: str, 
                endpoint: str, 
                data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make API request to GitHub.
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response JSON
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Handle different status codes
            if response.status_code in [200, 201, 204]:
                return response.json() if response.text else {}
            else:
                error_msg = response.json().get('message', response.text)
                raise Exception(f"GitHub API error: {error_msg}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
    
    def repo_exists(self, repo_name: str) -> bool:
        """Check if repository exists."""
        try:
            self._request("GET", f"/repos/{self.username}/{repo_name}")
            return True
        except:
            return False
    
    def create_repo(self, 
                   repo_name: str, 
                   description: str = "", 
                   private: bool = False,
                   auto_init: bool = True) -> Dict[str, Any]:
        """
        Create new GitHub repository.
        
        Args:
            repo_name: Repository name
            description: Repository description
            private: Whether repo is private
            auto_init: Initialize with README
            
        Returns:
            Repository data
        """
        if self.repo_exists(repo_name):
            print(f"Repository {repo_name} already exists")
            return self._request("GET", f"/repos/{self.username}/{repo_name}")
        
        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": auto_init
        }
        
        result = self._request("POST", "/user/repos", data)
        print(f"✓ Created repository: {repo_name}")
        return result
    
    def create_or_update_file(self,
                             repo_name: str,
                             file_path: str,
                             content: str,
                             message: str,
                             branch: str = "main") -> Dict[str, Any]:
        """
        Create or update a file in repository.
        
        Args:
            repo_name: Repository name
            file_path: Path to file in repo
            content: File content
            message: Commit message
            branch: Target branch
            
        Returns:
            File creation/update response
        """
        # Encode content to base64
        encoded_content = base64.b64encode(content.encode()).decode()
        
        # Check if file exists
        try:
            existing = self._request("GET", 
                f"/repos/{self.username}/{repo_name}/contents/{file_path}?ref={branch}")
            sha = existing.get("sha")
        except:
            sha = None
        
        data = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }
        
        if sha:
            data["sha"] = sha
        
        result = self._request("PUT",
            f"/repos/{self.username}/{repo_name}/contents/{file_path}",
            data)
        
        return result
    
    def create_multiple_files(self,
                             repo_name: str,
                             files: Dict[str, str],
                             branch: str = "main") -> Dict[str, bool]:
        """
        Create/update multiple files in one go.
        
        Args:
            repo_name: Repository name
            files: Dictionary mapping file paths to content
            branch: Target branch
            
        Returns:
            Dictionary mapping file paths to success status
        """
        results = {}
        
        for file_path, content in files.items():
            try:
                self.create_or_update_file(
                    repo_name,
                    file_path,
                    content,
                    f"Add/update {file_path}",
                    branch
                )
                results[file_path] = True
                print(f"✓ Uploaded: {file_path}")
            except Exception as e:
                results[file_path] = False
                print(f"✗ Failed to upload {file_path}: {e}")
        
        return results
    
    def upload_project(self,
                      repo_name: str,
                      project_path: str,
                      branch: str = "main") -> Dict[str, bool]:
        """
        Upload entire project to repository.
        
        Args:
            repo_name: Repository name
            project_path: Local project directory
            branch: Target branch
            
        Returns:
            Dictionary mapping files to upload status
        """
        files_to_upload = {}
        project_path = Path(project_path)
        
        # Collect all files
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                # Skip hidden files and common non-essential files
                if file_path.name.startswith('.'):
                    continue
                if file_path.name in ['__pycache__', '.pyc']:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    # For binary files, skip
                    continue
                
                # Get relative path
                rel_path = file_path.relative_to(project_path)
                repo_file_path = str(rel_path).replace('\\', '/')
                files_to_upload[repo_file_path] = content
        
        # Upload files
        return self.create_multiple_files(repo_name, files_to_upload, branch)
    
    def commit_and_push(self,
                       repo_name: str,
                       message: str,
                       branch: str = "main") -> bool:
        """
        Commits are made automatically with file uploads.
        This is a helper to verify the push status.
        
        Args:
            repo_name: Repository name
            message: Commit message
            branch: Target branch
            
        Returns:
            Success status
        """
        try:
            # GitHub API automatically commits when files are created/updated
            # This method just verifies the repository exists
            self._request("GET", f"/repos/{self.username}/{repo_name}")
            return True
        except:
            return False
    
    def get_repo_url(self, repo_name: str) -> str:
        """Get HTTPS URL for repository."""
        return f"https://github.com/{self.username}/{repo_name}"
    
    def clone_repo(self, repo_name: str, local_path: str) -> bool:
        """
        Clone repository to local path.
        
        Args:
            repo_name: Repository name
            local_path: Local directory to clone to
            
        Returns:
            Success status
        """
        try:
            import subprocess
            url = self.get_repo_url(repo_name)
            result = subprocess.run(
                ["git", "clone", url, local_path],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Clone failed: {e}")
            return False
    
    def get_repo_info(self, repo_name: str) -> Dict[str, Any]:
        """Get repository information."""
        return self._request("GET", f"/repos/{self.username}/{repo_name}")
    
    def get_file_content(self, 
                        repo_name: str, 
                        file_path: str,
                        branch: str = "main") -> str:
        """Get content of file from repository."""
        try:
            response = self._request("GET",
                f"/repos/{self.username}/{repo_name}/contents/{file_path}?ref={branch}")
            
            if "content" in response:
                return base64.b64decode(response["content"]).decode('utf-8')
            return ""
        except:
            return ""
    
    def list_files(self, 
                   repo_name: str, 
                   path: str = "",
                   branch: str = "main") -> List[str]:
        """List files in repository directory."""
        try:
            if path:
                endpoint = f"/repos/{self.username}/{repo_name}/contents/{path}?ref={branch}"
            else:
                endpoint = f"/repos/{self.username}/{repo_name}/contents?ref={branch}"
            
            response = self._request("GET", endpoint)
            
            if isinstance(response, list):
                return [item["name"] for item in response]
            return []
        except:
            return []
