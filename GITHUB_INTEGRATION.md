# GitHub Integration Guide

## Complete GitHub Integration for AI Project Generator

This guide explains how to use the complete GitHub integration features to create, edit, and manage projects directly through the web UI.

---

## Setup

### 1. Create GitHub Personal Access Token

1. Go to [GitHub Settings - Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name: "AI Project Generator"
4. Select scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `public_repo` (access public repositories)
   - ✅ `workflow` (update GitHub Actions)
5. Click "Generate token"
6. **Copy the token immediately** (you won't be able to see it again)

### 2. Configure Environment Variables

Create or edit `.env` file in the project root:

```bash
GITHUB_TOKEN=your_copied_token_here
GITHUB_USERNAME=your_github_username
```

Example:
```bash
GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz
GITHUB_USERNAME=sathvik-web
```

### 3. Restart the Application

```bash
# Stop the current application (Ctrl+C)
# Then restart:
python backend/main.py
# In another terminal:
streamlit run frontend/app.py
```

---

## Features

### Tab 1: Generate New Projects

**Generate and Optionally Push to GitHub**

1. **Describe Your Project**
   - Write a natural language description
   - Example: "Create a FastAPI REST API with PostgreSQL and JWT authentication"

2. **Configure Options**
   - **Auto-push to GitHub**: Automatically creates a GitHub repo and pushes code
   - **Repository name**: Custom name for the GitHub repository (optional)

3. **Generate Project**
   - Click "🚀 Generate Project"
   - Watch the real-time generation log
   - View results:
     - Project name
     - Number of files created
     - Workspace location
     - GitHub repository link (if pushed)

**Example Prompts:**
```
Create a Streamlit dashboard that visualizes stock market data

Build a FastAPI backend with PostgreSQL, JWT authentication, and Docker support

Generate a PyTorch model trainer with data validation and logging

Make a React frontend with Redux state management and TypeScript
```

---

### Tab 2: Projects

**View and Manage Generated Projects**

1. **View Recent Projects**
   - Lists all recently generated projects
   - Shows project count

2. **Project Details**
   - Click "View" to see:
     - Project path on disk
     - File count
     - List of generated files
   - Browse all files in the project

3. **Use Cases**
   - Quick access to project information
   - Verify what was generated
   - Plan edits

---

### Tab 3: Edit & Update Projects

#### Option A: Edit Local Project Files

**Modify Individual Files**

1. **Select Project**
   - Choose from recent projects dropdown
   - UI shows file count and project path

2. **Select File**
   - Browse all files in the project
   - Click to load file content

3. **Edit Content**
   - Full text editor for file content
   - Syntax-aware editing (Python, JSON, etc.)
   - Real-time changes

4. **Save Changes**
   - Click "💾 Save Changes" to update the file
   - Confirmation message appears
   - File is immediately saved to disk

5. **Push to GitHub** (see below)

**Example Workflows:**
- Fix bugs in generated code
- Add missing imports
- Update configuration values
- Add new functions or classes
- Modify documentation

#### Option B: Update from GitHub Repository

**Intelligent Project Enhancement**

1. **Provide Repository URL**
   - Paste GitHub repository URL
   - Example: `https://github.com/username/my-project`

2. **Describe Updates**
   - What should be improved?
   - Example: "Add error handling, improve logging, add unit tests"

3. **Configure Commit**
   - **Auto-commit and push**: Automatically commits and pushes changes
   - **Commit message**: Custom commit message (default provided)

4. **Update Project**
   - Click "🔄 Update Project"
   - AI analyzes the update request
   - Generates improvements
   - Reviews code quality
   - Commits and pushes if auto-commit enabled

**Smart Features:**
- Maintains existing code structure
- Adds improvements without breaking changes
- Respects project conventions
- Automatically creates commits

---

### Push Changes to GitHub

**Manually Push Local Changes**

1. **Select Project**
   - Choose the project to push
   - UI shows project path

2. **Provide Commit Message**
   - Describe what changed
   - Default: "Push changes from AI Project Generator"

3. **Push to GitHub**
   - Click "📤 Push to GitHub"
   - If repo doesn't exist, it will be created
   - All changes are committed and pushed
   - Success message shows repository URL

**Supported Scenarios:**
- Push newly generated projects
- Push locally edited files
- Push updates from other sources
- Create new repositories automatically

---

## Example Workflows

### Workflow 1: Generate and Push to GitHub

1. Go to **Generate** tab
2. Enter: "Create a FastAPI REST API with SQLAlchemy ORM and Pydantic validation"
3. Check "Auto-push to GitHub"
4. Enter repo name: "my-api-project"
5. Click "🚀 Generate Project"
6. ✅ Project generated and pushed to GitHub in 15 seconds

### Workflow 2: Generate Locally, Then Edit and Push

1. Go to **Generate** tab
2. Enter project description
3. **Uncheck** "Auto-push to GitHub"
4. Click "🚀 Generate Project" → generates locally
5. Go to **Edit & Update** tab → **Edit Local Project**
6. Select the project
7. Edit files as needed
8. Click "💾 Save Changes"
9. Go to **Push Changes to GitHub** section
10. Enter commit message
11. Click "📤 Push to GitHub"

### Workflow 3: Improve Existing GitHub Project

1. Go to **Edit & Update** tab
2. Select "Update from GitHub"
3. Paste repository URL: `https://github.com/user/existing-project`
4. Enter update: "Add comprehensive error handling, improve documentation, add logging"
5. Check "Auto-commit and push changes"
6. Click "🔄 Update Project"
7. ✅ Project improved and pushed back to GitHub

### Workflow 4: Local Edit and Commit

1. Go to **Edit & Update** tab → **Edit Local Project**
2. Select project from dropdown
3. Select a file to edit
4. Make changes in the editor
5. Click "💾 Save Changes"
6. Edit more files as needed
7. Go to **Push Changes to GitHub**
8. Enter: "Fix bugs and improve code quality"
9. Click "📤 Push to GitHub"

### Workflow 5: View, Edit, and Update in One Session

1. Go to **Projects** tab
2. Click "View" on a project to see details
3. Go to **Edit & Update** tab → **Edit Local Project**
4. Select same project
5. Edit specific files
6. Save each file
7. Push to GitHub with comprehensive commit message

---

## API Endpoints

### Project Generation
```
POST /generate
Request: {
  "prompt": "string",
  "github_repo_name": "string (optional)",
  "auto_push": boolean
}
Response: {
  "success": boolean,
  "project_name": "string",
  "repo_url": "string (optional)",
  "files_created": number,
  "workspace_path": "string"
}
```

### Get File Content
```
GET /project/{project_name}/file/{file_path}
Response: {
  "project_name": "string",
  "file_path": "string",
  "content": "string"
}
```

### Update File Content
```
POST /project/{project_name}/file/{file_path}
Request: {
  "content": "string"
}
Response: {
  "success": boolean,
  "message": "string",
  "project_name": "string",
  "file_path": "string"
}
```

### Push to GitHub
```
POST /project/{project_name}/push
Request: {
  "message": "string",
  "repo_name": "string (optional)"
}
Response: {
  "success": boolean,
  "message": "string",
  "repo_url": "string",
  "project_name": "string"
}
```

### Update from GitHub
```
POST /update
Request: {
  "github_repo_url": "string",
  "update_prompt": "string",
  "auto_push": boolean,
  "commit_message": "string (optional)"
}
Response: {
  "success": boolean,
  "message": "string",
  "files_modified": number,
  "repo_url": "string"
}
```

---

## Troubleshooting

### Problem: "GitHub credentials not configured"

**Solution:**
1. Create `.env` file in project root
2. Add: `GITHUB_TOKEN=your_token`
3. Add: `GITHUB_USERNAME=your_username`
4. Restart the application

### Problem: "Repository already exists"

**Solution:**
- The system automatically detects existing repos
- Either:
  - Use a different repository name
  - Delete the existing repo on GitHub first
  - Or let the system update the existing repo

### Problem: Files not saving to disk

**Solution:**
1. Check workspace directory permissions
2. Ensure workspace/ folder exists
3. Check disk space
4. Verify file path is valid
5. Try creating a new project

### Problem: GitHub push fails silently

**Solution:**
1. Verify GitHub token is valid (not expired)
2. Check token has `repo` scope
3. Verify username is correct
4. Check network connectivity
5. View application logs for details

### Problem: Large files timeout

**Solution:**
1. Increase timeout in browser (may take 2-3 minutes for large projects)
2. Generate smaller projects and edit incrementally
3. Split large projects into modules

### Problem: "Cannot find project" error

**Solution:**
1. Go to **Projects** tab to verify project exists
2. Check workspace/ directory manually
3. Regenerate the project
4. Check project name exactly (case-sensitive)

---

## Best Practices

### 1. GitHub Repository Naming
- Use lowercase with hyphens: `my-awesome-project`
- Avoid special characters
- Make it descriptive
- Example: `fastapi-todo-api`, `streamlit-dashboard`, `pytorch-classifier`

### 2. Commit Messages
- Be descriptive: "Add user authentication" (good)
- Avoid generic: "Update files" (bad)
- Include context: "Fix bug in validation and add logging"
- Follow convention: "Add feature", "Fix bug", "Update docs"

### 3. File Editing
- Edit one file at a time
- Save after each edit
- Test before pushing
- Don't delete critical files

### 4. Updating Projects
- Be specific in update description
- Example good: "Refactor authentication, add logging, fix edge cases"
- Example bad: "Make better"
- Review changes before auto-push if unsure

### 5. GitHub Token Security
- ✅ Use personal access tokens (not passwords)
- ✅ Limit token scope to minimum needed
- ✅ Regenerate tokens periodically
- ❌ Never commit `.env` with tokens
- ❌ Never share tokens in messages

### 6. Large Projects
- Generate modular projects (separate frontend/backend)
- Edit in sections
- Push frequently to avoid losing work
- Consider splitting into multiple repos

---

## Advanced Usage

### Batch Processing
```
1. Generate multiple projects in sequence
2. Each one is independent
3. Edit and push individually
4. All stay in memory/memory.json for reference
```

### Project Templates
```
1. Generate a base project once
2. Clone it locally
3. Edit and customize
4. Push different versions to different repos
```

### CI/CD Integration
```
1. Generate project with GitHub push enabled
2. GitHub automatically receives:
   - All source files
   - README.md
   - requirements.txt (if Python)
   - Dockerfile (if needed)
3. Set up GitHub Actions workflows separately
4. CI/CD pipeline runs automatically
```

### Rapid Prototyping
```
1. Generate initial version
2. Edit key files in UI
3. Push to GitHub
4. Test and gather feedback
5. Update project via Update feature
6. Iterate quickly
```

---

## Security Considerations

### Credentials
- GitHub tokens are sensitive
- Store in `.env` only (never in code)
- `.env` is in `.gitignore` (don't push it)
- Regenerate tokens if compromised

### Code Generation
- Generated code is reviewed automatically
- May need manual security audit for production
- Always review AI-generated code before deployment

### Repository Access
- Token gives access to your GitHub account
- Be careful about running code from untrusted projects
- Use private repos for sensitive projects

---

## What's Being Done Behind the Scenes

### When You Generate a Project:
1. ✅ Natural language prompt analyzed
2. ✅ Technology stack detected
3. ✅ Project structure planned
4. ✅ Code files generated
5. ✅ Code quality reviewed automatically
6. ✅ Syntax validated
7. ✅ Import statements checked
8. ✅ Type hints added (if needed)
9. ✅ Docstrings generated
10. ✅ Files saved to workspace/
11. ✅ GitHub repo created (if auto-push enabled)
12. ✅ All files uploaded to GitHub
13. ✅ User preferences learned

### When You Edit a File:
1. ✅ File loaded from disk
2. ✅ Content displayed in editor
3. ✅ Your changes captured
4. ✅ Validated (basic checks)
5. ✅ Saved to disk immediately

### When You Push to GitHub:
1. ✅ Repository checked (created if needed)
2. ✅ All project files gathered
3. ✅ Changes committed with message
4. ✅ Pushed to main branch
5. ✅ Status returned with GitHub URL

### When You Update from GitHub:
1. ✅ Project cloned or analyzed
2. ✅ Update description processed
3. ✅ New improvements generated
4. ✅ Code reviewed and validated
5. ✅ Changes committed and pushed

---

## Success Examples

### Example 1: FastAPI REST API
```
Prompt: "Create a FastAPI REST API with PostgreSQL, JWT auth, and OpenAPI docs"
Generated: 15 files in 12 seconds
Pushed: Repository created automatically
Updated: "Add rate limiting and caching"
Result: Production-ready API
```

### Example 2: Streamlit Dashboard
```
Prompt: "Build a Streamlit app for analyzing sales data with charts and filters"
Generated: 8 files in 8 seconds
Edited: Added custom CSS in UI
Pushed: To https://github.com/user/sales-dashboard
Result: Deployed on Streamlit Cloud
```

### Example 3: ML Model Trainer
```
Prompt: "Create a PyTorch model trainer with data loading, validation, and metrics"
Generated: 12 files in 10 seconds
Updated: "Improve error handling and add TensorBoard logging"
Pushed: To GitHub with Dockerfile
Result: Ready for training and deployment
```

---

## Support

- Check the **Help** tab in the application
- Review `README.md` for general info
- Check `QUICK_START.md` for setup help
- View `ARCHITECTURE.md` for technical details
- API docs at: `http://localhost:8000/api/docs`

---

**Happy coding with GitHub integration! 🚀**
