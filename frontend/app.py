"""
Streamlit UI Frontend for AI Project Generator.
Provides web interface for project generation and management.
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any

# Configuration
API_URL = "http://localhost:8000"
st.set_page_config(
    page_title="AI Project Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 1em;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = False
if 'generation_logs' not in st.session_state:
    st.session_state.generation_logs = []
if 'current_memory' not in st.session_state:
    st.session_state.current_memory = {}


def check_api_connection():
    """Check if API server is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        st.session_state.api_connected = response.status_code == 200
        return st.session_state.api_connected
    except:
        st.session_state.api_connected = False
        return False


def load_memory():
    """Load current memory from API."""
    try:
        response = requests.get(f"{API_URL}/memory", timeout=5)
        if response.status_code == 200:
            st.session_state.current_memory = response.json()
            return response.json()
    except Exception as e:
        st.warning(f"Could not load memory: {e}")
    return {}


def generate_project(prompt: str, repo_name: str = None, auto_push: bool = True):
    """Generate a new project."""
    st.session_state.generation_logs = []
    
    try:
        st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Starting project generation...")
        
        payload = {
            "prompt": prompt,
            "github_repo_name": repo_name,
            "auto_push": auto_push
        }
        
        st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Sending request to API...")
        response = requests.post(f"{API_URL}/generate", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Project generated successfully")
            st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Files created: {result['files_created']}")
            
            if result.get('repo_url'):
                st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Repository: {result['repo_url']}")
            
            return result
        else:
            error = response.json().get('detail', 'Unknown error')
            st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error: {error}")
            return None
    
    except Exception as e:
        st.session_state.generation_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Connection error: {e}")
        return None


def get_recent_projects():
    """Get list of recent projects."""
    try:
        response = requests.get(f"{API_URL}/projects", timeout=5)
        if response.status_code == 200:
            return response.json().get('projects', [])
    except:
        pass
    return []


# Main UI
def main():
    # Header
    st.markdown('<div class="main-header">🚀 AI Project Generator</div>', unsafe_allow_html=True)
    st.write("Create complete software projects from natural language prompts using AI agents.")
    
    # Check API connection
    if not check_api_connection():
        st.error(
            "⚠️ Cannot connect to API server. Make sure it's running on http://localhost:8000\n"
            "\nTo start the backend server, run:\n"
            "`python backend/main.py`"
        )
        return
    
    st.success("✓ Connected to API server")
    
    # Load memory
    memory = load_memory()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Generate", "📦 Projects", "✏️ Edit & Update", "💾 Memory", "ℹ️ Help"]
    )
    
    # Tab 1: Generate New Project
    with tab1:
        st.header("Generate New Project")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            prompt = st.text_area(
                "Describe your project:",
                placeholder="e.g., Create a FastAPI text summarizer app with T5 model",
                height=100
            )
        
        with col2:
            st.subheader("Options")
            auto_push = st.checkbox("Auto-push to GitHub", value=True)
            repo_name = st.text_input("Repository name (optional)")
        
        if st.button("🚀 Generate Project", use_container_width=True):
            if not prompt:
                st.error("Please enter a project description")
            else:
                st.info("Generating project... This may take a moment.")
                result = generate_project(prompt, repo_name, auto_push)
                
                # Display logs
                st.subheader("Generation Log")
                with st.container():
                    for log in st.session_state.generation_logs:
                        st.text(log)
                
                # Display result
                if result:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown(f"### ✓ Success!")
                    st.markdown(f"**Project Name:** {result['project_name']}")
                    st.markdown(f"**Files Created:** {result['files_created']}")
                    st.markdown(f"**Workspace:** {result['workspace_path']}")
                    if result.get('repo_url'):
                        st.markdown(f"**Repository:** [{result['repo_url']}]({result['repo_url']})")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Projects
    with tab2:
        st.header("Recent Projects")
        
        projects = get_recent_projects()
        
        if projects:
            for i, project in enumerate(projects, 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(f"{i}. {project}")
                    with col2:
                        if st.button("View", key=f"view_{project}"):
                            # View project details
                            try:
                                response = requests.get(
                                    f"{API_URL}/project/{project}",
                                    timeout=5
                                )
                                if response.status_code == 200:
                                    proj_info = response.json()
                                    st.write(f"**Path:** {proj_info['path']}")
                                    st.write(f"**Files:** {proj_info['file_count']}")
                                    with st.expander("View Files"):
                                        for file in proj_info['files'][:20]:
                                            st.text(file)
                            except Exception as e:
                                st.error(f"Could not load project info: {e}")
        else:
            st.info("No projects generated yet. Create one to get started!")
    
    # Tab 3: Edit & Update Projects
    with tab3:
        st.header("Edit & Update Projects")
        
        st.markdown("### Make changes to your projects and push to GitHub")
        
        edit_mode = st.radio(
            "Choose mode:",
            ["Edit Local Project", "Update from GitHub"],
            horizontal=True
        )
        
        if edit_mode == "Edit Local Project":
            st.subheader("Edit Local Project Files")
            
            projects = get_recent_projects()
            if projects:
                selected_project = st.selectbox("Select project to edit", projects)
                
                if selected_project:
                    try:
                        response = requests.get(
                            f"{API_URL}/project/{selected_project}",
                            timeout=5
                        )
                        if response.status_code == 200:
                            proj_info = response.json()
                            files = proj_info['files']
                            
                            st.write(f"**Project:** {selected_project}")
                            st.write(f"**Files:** {len(files)}")
                            
                            # Select file to edit
                            file_to_edit = st.selectbox(
                                "Select file to edit:",
                                files,
                                key="file_selector"
                            )
                            
                            if file_to_edit:
                                st.subheader(f"Editing: {file_to_edit}")
                                
                                try:
                                    # Get file content
                                    file_content_resp = requests.get(
                                        f"{API_URL}/project/{selected_project}/file/{file_to_edit}",
                                        timeout=5
                                    )
                                    
                                    if file_content_resp.status_code == 200:
                                        file_data = file_content_resp.json()
                                        current_content = file_data.get('content', '')
                                        
                                        # Editor
                                        edited_content = st.text_area(
                                            "File content:",
                                            value=current_content,
                                            height=300,
                                            key=f"editor_{file_to_edit}"
                                        )
                                        
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            if st.button("💾 Save Changes", use_container_width=True):
                                                try:
                                                    save_resp = requests.post(
                                                        f"{API_URL}/project/{selected_project}/file/{file_to_edit}",
                                                        json={"content": edited_content},
                                                        timeout=10
                                                    )
                                                    
                                                    if save_resp.status_code == 200:
                                                        st.success("✓ File saved successfully")
                                                    else:
                                                        st.error(f"Error saving file: {save_resp.json()}")
                                                except Exception as e:
                                                    st.error(f"Error: {e}")
                                        
                                        with col2:
                                            if st.button("🔄 Reset", use_container_width=True):
                                                st.rerun()
                                    else:
                                        st.error("Could not load file content")
                                except Exception as e:
                                    st.error(f"Error loading file: {e}")
                    except Exception as e:
                        st.error(f"Could not load project: {e}")
            else:
                st.info("No projects to edit. Generate one first!")
        
        else:  # Update from GitHub
            st.subheader("Update from GitHub Repository")
            
            github_url = st.text_input(
                "GitHub Repository URL:",
                placeholder="https://github.com/username/repo-name"
            )
            
            update_prompt = st.text_area(
                "What would you like to update/improve?",
                placeholder="e.g., Add error handling, improve documentation, add new features",
                height=100
            )
            
            col1, col2 = st.columns([2, 1])
            with col1:
                auto_commit = st.checkbox("Auto-commit and push changes", value=True)
            
            with col2:
                commit_msg = st.text_input(
                    "Commit message:",
                    value="Update from AI Project Generator",
                    placeholder="Update message"
                )
            
            if st.button("🔄 Update Project", use_container_width=True):
                if not github_url or not update_prompt:
                    st.error("Please provide both repository URL and update description")
                else:
                    st.info("Updating project... This may take a moment.")
                    
                    try:
                        update_resp = requests.post(
                            f"{API_URL}/update",
                            json={
                                "github_repo_url": github_url,
                                "update_prompt": update_prompt,
                                "auto_push": auto_commit,
                                "commit_message": commit_msg
                            },
                            timeout=120
                        )
                        
                        if update_resp.status_code == 200:
                            result = update_resp.json()
                            st.success("✓ Project updated successfully!")
                            st.json(result)
                        else:
                            error = update_resp.json()
                            st.error(f"Update failed: {error.get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        st.divider()
        st.subheader("Push Changes to GitHub")
        
        col1, col2 = st.columns(2)
        
        with col1:
            push_project = st.selectbox(
                "Select project to push:",
                get_recent_projects(),
                key="push_project"
            )
        
        with col2:
            push_msg = st.text_input(
                "Commit message:",
                value="Push changes from AI Project Generator",
                key="push_msg"
            )
        
        if st.button("📤 Push to GitHub", use_container_width=True):
            if push_project and push_msg:
                try:
                    push_resp = requests.post(
                        f"{API_URL}/project/{push_project}/push",
                        json={"message": push_msg},
                        timeout=30
                    )
                    
                    if push_resp.status_code == 200:
                        result = push_resp.json()
                        st.success(f"✓ Pushed to GitHub: {result.get('repo_url')}")
                    else:
                        st.error(f"Error: {push_resp.json()}")
                except Exception as e:
                    st.error(f"Error pushing: {e}")
    
    # Tab 4: Memory & Preferences
    with tab4:
        st.header("User Memory & Preferences")
        
        if memory:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Current Preferences")
                st.json(memory)
            
            with col2:
                if st.button("🔄 Refresh", use_container_width=True):
                    memory = load_memory()
                    st.rerun()
                
                if st.button("🗑️ Reset Memory", use_container_width=True):
                    try:
                        response = requests.post(f"{API_URL}/memory/reset", timeout=5)
                        if response.status_code == 200:
                            st.success("Memory reset to defaults")
                            memory = load_memory()
                            st.rerun()
                    except Exception as e:
                        st.error(f"Could not reset memory: {e}")
    
    # Tab 5: Help
    with tab5:
        st.header("Help & Documentation")
        
        st.subheader("How It Works")
        st.markdown("""
        The AI Project Generator creates complete software projects through a multi-step process:
        
        1. **Planning:** Analyzes your prompt to determine project structure and technologies
        2. **Generation:** Creates all necessary code files
        3. **Review:** Automatically improves code quality
        4. **Writing:** Saves files to workspace
        5. **GitHub:** Optionally commits and pushes to GitHub
        
        ### Features
        
        - 🤖 AI-powered project planning
        - 📝 Automatic code generation
        - ✅ Self-improving code review
        - 💾 User preference learning
        - 🌐 GitHub integration
        - 🚀 Production-ready templates
        
        ### Getting Started
        
        1. Go to the **Generate** tab
        2. Describe your project in natural language
        3. Configure options (GitHub auto-push, repo name)
        4. Click **Generate Project**
        5. Check the generated files in workspace/
        
        ### Example Prompts
        
        - "Create a FastAPI REST API with PostgreSQL"
        - "Build a Streamlit dashboard for data visualization"
        - "Generate a PyTorch machine learning model trainer"
        - "Make a React frontend with Flask backend"
        
        ### Supported Technologies
        
        **Backends:** FastAPI, Flask, Django
        **Frontends:** Streamlit, React
        **ML:** PyTorch, TensorFlow, Scikit-learn
        **Databases:** SQLite, PostgreSQL, MongoDB
        """)
        
        st.subheader("API Endpoints")
        st.markdown("""
        - `POST /generate` - Generate new project
        - `POST /update` - Update existing project
        - `GET /memory` - Get user preferences
        - `GET /projects` - List recent projects
        - `GET /project/{name}` - Get project info
        - `POST /preference` - Update preference
        
        API Documentation available at: http://localhost:8000/api/docs
        """)
        
        st.subheader("Keyboard Shortcuts")
        st.markdown("""
        - `Ctrl+Enter` in text area - Generate project (if button supports it)
        """)


if __name__ == "__main__":
    main()
