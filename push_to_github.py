"""
GitHub Push Script - Upload ai_project_generator to GitHub

This script uploads the entire ai_project_generator project to GitHub.
"""

import os
import sys
from pathlib import Path
import requests
import json
import base64

# Configuration
GITHUB_USERNAME = "sathvik-web"
REPO_NAME = "ai_project_generator"
PROJECT_PATH = Path.cwd()

def get_github_token():
    """Get GitHub token from environment or user input."""
    token = os.getenv("GITHUB_TOKEN")
    
    if not token or token == "your_github_token_here":
        print("\n" + "="*60)
        print("GitHub Token Required")
        print("="*60)
        print("\nTo push to GitHub, you need a Personal Access Token:")
        print("1. Visit: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Give it a name: 'AI Project Generator'")
        print("4. Select these scopes:")
        print("   ✓ repo")
        print("   ✓ public_repo")
        print("   ✓ workflow")
        print("5. Click 'Generate token'")
        print("6. Copy the token (you won't see it again)")
        print("\n" + "="*60)
        
        token = input("\nPaste your GitHub token here: ").strip()
        
        if not token:
            print("❌ No token provided. Exiting.")
            sys.exit(1)
        
        # Save to .env
        with open(".env", "r") as f:
            env_content = f.read()
        
        env_content = env_content.replace("GITHUB_TOKEN=your_github_token_here", f"GITHUB_TOKEN={token}")
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print(f"\n✓ Token saved to .env file")
    
    return token


def create_repo(token):
    """Create GitHub repository if it doesn't exist."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if repo exists
    check_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}"
    response = requests.get(check_url, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Repository '{REPO_NAME}' already exists")
        return response.json()
    
    # Create new repo
    create_url = "https://api.github.com/user/repos"
    data = {
        "name": REPO_NAME,
        "description": "AI Project Generator - Intelligent agent system that creates complete projects",
        "private": False,
        "auto_init": True
    }
    
    print(f"\n📝 Creating repository '{REPO_NAME}'...")
    response = requests.post(create_url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✓ Repository created successfully!")
        return response.json()
    else:
        print(f"❌ Failed to create repository: {response.json()}")
        sys.exit(1)


def upload_file(token, file_path, repo_url):
    """Upload a single file to GitHub."""
    relative_path = file_path.relative_to(PROJECT_PATH)
    github_path = str(relative_path).replace("\\", "/")
    
    # Skip certain files
    skip_patterns = [".env", "__pycache__", ".git", "workspace", "memory", ".venv", "venv"]
    if any(pattern in github_path for pattern in skip_patterns):
        return None
    
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        # Check if binary file
        try:
            content_str = content.decode("utf-8")
            is_binary = False
        except:
            is_binary = True
        
        if is_binary:
            print(f"  ⊘ Skipping binary: {github_path}")
            return None
        
        # Prepare upload
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Check if file exists
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{github_path}"
        response = requests.get(url, headers=headers)
        
        sha = None
        if response.status_code == 200:
            sha = response.json().get("sha")
        
        # Upload file
        encoded_content = base64.b64encode(content_str.encode()).decode()
        upload_data = {
            "message": f"Add {github_path}",
            "content": encoded_content
        }
        
        if sha:
            upload_data["sha"] = sha
        
        response = requests.put(url, headers=headers, json=upload_data)
        
        if response.status_code in [200, 201]:
            print(f"  ✓ {github_path}")
            return True
        else:
            print(f"  ✗ Failed: {github_path}")
            return False
    
    except Exception as e:
        print(f"  ✗ Error uploading {github_path}: {e}")
        return False


def upload_all_files(token):
    """Upload all project files to GitHub."""
    print(f"\n📦 Uploading project files...")
    print("="*60)
    
    uploaded = 0
    skipped = 0
    
    for file_path in PROJECT_PATH.rglob("*"):
        if file_path.is_file():
            result = upload_file(token, file_path, REPO_NAME)
            if result is True:
                uploaded += 1
            elif result is None:
                skipped += 1
    
    print("="*60)
    print(f"\n✓ Upload complete!")
    print(f"  Files uploaded: {uploaded}")
    print(f"  Files skipped: {skipped}")
    
    return uploaded


def push_to_github():
    """Main function to push project to GitHub."""
    print("\n" + "="*60)
    print("  AI Project Generator - GitHub Push")
    print("="*60)
    
    # Get token
    token = get_github_token()
    
    if not token.startswith("ghp_"):
        print("\n⚠️  Warning: Token doesn't look valid (should start with 'ghp_')")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != "y":
            print("Cancelled.")
            sys.exit(1)
    
    # Create repository
    repo = create_repo(token)
    repo_url = repo.get("html_url", f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    
    # Upload files
    uploaded = upload_all_files(token)
    
    # Success message
    print("\n" + "="*60)
    print("✨ SUCCESS!")
    print("="*60)
    print(f"\n📍 Repository URL:")
    print(f"   {repo_url}")
    print(f"\n📊 Project Details:")
    print(f"   Repository: {REPO_NAME}")
    print(f"   Owner: {GITHUB_USERNAME}")
    print(f"   Files uploaded: {uploaded}")
    print(f"\n✓ Your project is now on GitHub!")
    print(f"✓ You can access it at: {repo_url}")
    
    # Create README link
    print(f"\n💡 Next steps:")
    print(f"   1. Visit: {repo_url}")
    print(f"   2. Verify all files are there")
    print(f"   3. Update the README if needed")
    print(f"   4. Share the link!")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    push_to_github()
