# AI Project Generator - Complete File Reference

## Project Overview

This document provides a complete reference of all files in the AI Project Generator system, including their purpose, functionality, and how they work together.

## Directory Structure & File Reference

```
ai_project_generator/
```

### Root Configuration Files

#### 1. `requirements.txt` (43 lines)
**Purpose**: Python package dependencies
**Key Packages**:
- fastapi 0.104.1
- uvicorn 0.24.0
- streamlit 1.29.0
- pydantic 2.5.0
- python-dotenv 1.0.0
- requests 2.31.0
- GitPython 3.13.0
- pytest 7.4.3
**Usage**: `pip install -r requirements.txt`

#### 2. `.env.example` (20 lines)
**Purpose**: Configuration template
**Contains**:
- GitHub token placeholder
- API host/port settings
- Application environment settings
- Database URL template
- Optional LLM API keys
**Usage**: Copy to `.env` and fill in values

#### 3. `README.md` (600+ lines)
**Purpose**: Complete project documentation
**Sections**:
- Overview and features
- Tech stack justification
- Project structure
- Installation guide
- Usage instructions
- API documentation
- Troubleshooting
- Future roadmap
**Audience**: Users and developers

#### 4. `QUICK_START.md` (250+ lines)
**Purpose**: 5-minute setup guide
**Content**:
- Prerequisites check
- Step-by-step installation
- First project generation
- Troubleshooting quick fixes
- Example prompts
- Performance overview
**Audience**: New users

#### 5. `ARCHITECTURE.md` (400+ lines)
**Purpose**: Detailed system design
**Covers**:
- System overview
- Architecture layers
- Agent descriptions
- Data flow diagrams
- Design patterns
- Technology justification
- Performance characteristics
- Extensibility points
**Audience**: Developers and architects

#### 6. `IMPLEMENTATION_SUMMARY.md` (350+ lines)
**Purpose**: Project completion status
**Contains**:
- Implementation checklist
- Feature matrix
- Code statistics
- File structure
- Validation checklist
- Known limitations
- Future roadmap
**Audience**: Project stakeholders

---

## Backend Directory (`backend/`)

### Core Modules

#### 1. `schemas.py` (150 lines)
**Purpose**: Pydantic data models for type safety and validation
**Key Classes**:
- `ProjectPlanRequest` - User request validation
- `ProjectGenerateRequest` - Full generation request
- `ProjectUpdateRequest` - Update request
- `FileDefinition` - Individual file definition
- `ProjectPlan` - Complete project blueprint
- `GeneratedFile` - File with content
- `ProjectGeneration` - Full generation output
- `GenerationResponse` - API response
- `UserMemory` - User preferences
- `ErrorResponse` - Error format

**Usage**: Imported by all backend modules for validation

#### 2. `config.py` (100 lines)
**Purpose**: Configuration management and utilities
**Classes**:
- `Config` - Global configuration
**Functions**:
- `setup_logging()` - Initialize logging
- `get_project_path()` - Get project directory
- `is_valid_identifier()` - Validate names
- `sanitize_name()` - Clean names for use
**Environment Variables**:
- GITHUB_TOKEN
- GITHUB_USERNAME
- API_HOST, API_PORT
- DEBUG, ENVIRONMENT
- LOG_LEVEL

#### 3. `memory_manager.py` (300 lines)
**Purpose**: User preference and learning system
**Class**: `MemoryManager`
**Key Methods**:
- `__init__()` - Initialize with directory
- `_load_memory()` - Load from file
- `_save_memory()` - Persist to disk
- `get_memory()` - Get current state
- `update_preference()` - Update single pref
- `add_framework()` - Track used framework
- `add_common_issue()` - Track issues
- `add_project()` - Track project
- `learn_from_project()` - Learn from generation
- `reset_memory()` - Reset to defaults
- `export_memory()` - Export as JSON
- `import_memory()` - Import from JSON

**Storage**:
- `memory/memory.json` - Current preferences
- `memory/history.json` - Event log

**Learning Features**:
- Preferred frameworks
- Common issues found
- Coding style
- Technology preferences
- Project history (last 10)

#### 4. `file_writer.py` (250 lines)
**Purpose**: Safe file and folder creation
**Class**: `FileWriter`
**Key Methods**:
- `create_project_structure()` - Create folders
- `write_files()` - Write multiple files
- `write_single_file()` - Write one file
- `read_file()` - Read project file
- `get_project_path()` - Get project directory
- `project_exists()` - Check if exists
- `get_all_files_in_project()` - List all files
- `delete_project()` - Remove project
- `ensure_directory()` - Create directory

**Safety Features**:
- Path validation
- Directory creation
- Encoding handling
- Error recovery
- File existence checks

**Output**: `workspace/{project_name}/`

#### 5. `github_manager.py` (350 lines)
**Purpose**: GitHub repository management
**Class**: `GitHubManager`
**Key Methods**:
- `repo_exists()` - Check if repo exists
- `create_repo()` - Create new repository
- `create_or_update_file()` - Upload/update file
- `create_multiple_files()` - Batch upload
- `upload_project()` - Upload entire project
- `get_repo_url()` - Get repo HTTPS URL
- `get_file_content()` - Read file from repo
- `list_files()` - List repo files
- `clone_repo()` - Clone to local

**Authentication**:
- GitHub Personal Access Token
- PAT scopes: repo, user, gist
- Token-based headers

**API Integration**:
- Base: https://api.github.com
- REST v3 API
- JSON responses
- Error handling

#### 6. `agent_planner.py` (350 lines)
**Purpose**: Project planning and blueprint generation
**Class**: `AgentPlanner`
**Key Methods**:
- `plan()` - Main planning method
- `_detect_technologies()` - Detect tech stack
- `_determine_primary_framework()` - Find main tech
- `_generate_project_name()` - Create project name
- `_build_file_structure()` - List files needed
- `_create_structure_description()` - Folder structure
- `_determine_entry_point()` - Find main file
- `_generate_description()` - Create summary
- `refine_plan()` - Improve plan based on feedback

**Technology Detection**:
- FastAPI, Flask, Django
- Streamlit, React
- PyTorch, TensorFlow
- PostgreSQL, MongoDB, Redis
- And many more

**Output**: `ProjectPlan` with:
- Project name
- Description
- Tech stack
- File list
- Folder structure

#### 7. `agent_generator.py` (600 lines)
**Purpose**: Code file generation
**Class**: `AgentGenerator`
**Key Methods**:
- `generate_files()` - Generate all files
- `_generate_file_content()` - Generate single file
- `_generate_main_file()` - Generate entry point
- `_generate_requirements()` - Create requirements.txt
- `_generate_readme()` - Create README.md
- `_generate_env_file()` - Create .env
- `_generate_model()` - Create model files
- `_generate_test()` - Create test files
- `_generate_dockerfile()` - Create Dockerfile

**Code Templates**:
- FastAPI main.py template
- Flask app.py template
- Streamlit app.py template
- Generic requirements.txt
- Markdown README
- .env configuration
- PyTorch model
- Unit tests
- Dockerfile

**Features**:
- Placeholder substitution
- Framework-specific code
- Best practices included
- Complete boilerplate
- Production-ready

#### 8. `agent_reviewer.py` (400 lines)
**Purpose**: Automatic code quality improvement
**Class**: `AgentReviewer`
**Key Methods**:
- `review_files()` - Review all files
- `review_file()` - Review single file
- `_analyze_file()` - Analyze for issues
- `_apply_fix()` - Apply improvements
- `_add_missing_imports()` - Add imports
- `_break_long_lines()` - Fix long lines
- `_add_docstrings()` - Add documentation
- `_add_type_hints()` - Add type hints
- `validate_syntax()` - Check Python syntax
- `get_code_metrics()` - Calculate metrics

**Issues Fixed**:
- Missing imports
- Trailing whitespace
- Long lines (>100 chars)
- Missing docstrings
- Missing type hints
- Syntax errors

**Metrics Calculated**:
- Total lines
- Code lines
- Comment lines
- Blank lines
- Functions
- Classes
- Imports

#### 9. `main.py` (400 lines)
**Purpose**: FastAPI application and REST API
**Framework**: FastAPI 0.104.1
**Server**: Uvicorn

**API Endpoints**:
```
POST   /generate              Generate new project
POST   /update                Update project
GET    /memory                Get preferences
GET    /projects              List projects
GET    /project/{name}        Get project info
DELETE /project/{name}        Delete project
POST   /preference             Update preference
POST   /memory/reset          Reset memory
GET    /health               Health check
GET    /                      Root info
```

**Features**:
- CORS enabled
- Async handlers
- Background tasks
- Error handling
- Comprehensive logging
- Type-safe responses

**Integration**:
- Uses all agents
- Coordinates pipeline
- Manages background tasks
- Returns structured responses

---

## Frontend Directory (`frontend/`)

#### `app.py` (450 lines)
**Purpose**: Streamlit web interface
**Framework**: Streamlit 1.29.0
**Port**: 8501

**Tabs**:
1. **Generate Tab**
   - Project prompt input
   - Repository name field
   - Auto-push toggle
   - Generation button
   - Live log display
   - Success/error messages

2. **Projects Tab**
   - Recent projects list
   - Project details view
   - File listing
   - View options

3. **Memory Tab**
   - Display all preferences
   - Framework tracking
   - Refresh button
   - Reset memory button

4. **Help Tab**
   - How it works explanation
   - Feature list
   - Getting started guide
   - Example prompts
   - API endpoints info

**Features**:
- Real-time status
- API integration
- Session state management
- Custom styling
- Error handling
- Responsive layout

---

## Memory Directory (`memory/`)

#### `memory.json`
**Purpose**: Persistent user preference storage
**Format**: JSON
**Structure**:
```json
{
  "preferred_backend": "fastapi",
  "preferred_frontend": "streamlit",
  "coding_style": "...",
  "common_issues": [],
  "frameworks": [],
  "language_preference": "python",
  "database_preference": "sqlite",
  "last_projects": [],
  "preferences": {}
}
```

**Auto-Updated**: After each project generation

#### `history.json`
**Purpose**: Event log and learning history
**Format**: JSON array of events
**Contains**: Timestamps, events, data

---

## Workspace Directory (`workspace/`)

**Purpose**: Generated project storage
**Structure**: `workspace/{project_name}/`
**Contents**: Complete project files

---

## Startup & Testing Files

#### `startup.py` (100 lines)
**Purpose**: Startup script with checks
**Functionality**:
- Python version check
- Dependency verification
- Environment setup
- Service initialization

#### `start.bat` (50 lines)
**Purpose**: Windows quick start
**Actions**:
- Check Python
- Create venv
- Install deps
- Start backend

#### `start.sh` (50 lines)
**Purpose**: macOS/Linux quick start
**Actions**:
- Check Python
- Create venv
- Install deps
- Start backend

#### `tests.py` (400 lines)
**Purpose**: Comprehensive test suite
**Test Classes**:
- `TestAgentPlanner` - Planning agent tests
- `TestCodeGenerator` - Generation tests
- `TestCodeReviewer` - Review tests
- `TestMemoryManager` - Memory tests
- `TestFileWriter` - File operations tests
- `TestIntegration` - Full pipeline tests

**Test Framework**: pytest
**Run**: `pytest tests.py -v`

---

## Architecture Summary

### Data Flow
```
User Input
    ↓
API Request
    ↓
Planning Agent (agent_planner.py)
    ↓
Code Generator (agent_generator.py)
    ↓
Code Reviewer (agent_reviewer.py)
    ↓
File Writer (file_writer.py)
    ↓
Memory Update (memory_manager.py)
    ↓
GitHub Push (github_manager.py) [async]
    ↓
Response to User
```

### Module Dependencies
```
main.py (FastAPI)
  ├── schemas.py (Validation)
  ├── agent_planner.py
  ├── agent_generator.py
  ├── agent_reviewer.py
  ├── memory_manager.py
  ├── file_writer.py
  ├── github_manager.py
  └── config.py (Settings)

frontend/app.py (Streamlit)
  └── requests (HTTP to main.py)
```

---

## Statistics

### Code Metrics
- **Total Python Files**: 12
- **Total Lines**: ~4,500+
- **Functions**: 150+
- **Classes**: 25+
- **Tests**: 15+ test cases
- **Documentation**: 1,000+ lines

### File Sizes
| File | Size |
|------|------|
| agent_generator.py | ~600 lines |
| main.py | ~400 lines |
| agent_reviewer.py | ~400 lines |
| tests.py | ~400 lines |
| README.md | ~600 lines |
| agent_planner.py | ~350 lines |
| github_manager.py | ~350 lines |
| frontend/app.py | ~450 lines |
| memory_manager.py | ~300 lines |
| file_writer.py | ~250 lines |

### Technology Coverage
- **Backends**: 3 (FastAPI, Flask, Django)
- **Frontends**: 2 (Streamlit, React)
- **ML Frameworks**: 3 (PyTorch, TensorFlow, Scikit-learn)
- **Databases**: 3 (SQLite, PostgreSQL, MongoDB)
- **Total Tech Patterns**: 20+

---

## Quick Reference

### How to Add a New Technology
1. Add pattern to `TECH_PATTERNS` in `agent_planner.py`
2. Create template in `agent_generator.py`
3. Add test case in `tests.py`

### How to Add a New Agent
1. Create `agent_name.py`
2. Implement generation logic
3. Integrate into `main.py` pipeline
4. Add schema definitions in `schemas.py`

### How to Customize Memory
1. Add field to `UserMemory` in `schemas.py`
2. Update learning logic in `memory_manager.py`
3. Persist in `memory.json`

### How to Add New Endpoint
1. Create async function in `main.py`
2. Add `@app.route()` decorator
3. Define request schema
4. Return response schema
5. Document in README

---

## Version Information

- **Project Version**: 1.0.0
- **Python**: 3.11+
- **FastAPI**: 0.104.1
- **Streamlit**: 1.29.0
- **Pydantic**: 2.5.0
- **Release Date**: November 2024

---

## Complete Feature Checklist

### Generation Features
- ✅ Natural language processing
- ✅ Technology detection
- ✅ Project planning
- ✅ File generation
- ✅ Code review
- ✅ Quality improvement

### Integration Features
- ✅ GitHub integration
- ✅ Repository creation
- ✅ File uploads
- ✅ Automatic commits

### Memory Features
- ✅ Preference storage
- ✅ Learning system
- ✅ History tracking
- ✅ Project memory

### API Features
- ✅ REST endpoints
- ✅ Type validation
- ✅ Error handling
- ✅ Documentation

### UI Features
- ✅ Project generation
- ✅ Project management
- ✅ Preference viewing
- ✅ Help documentation

---

## File Organization Summary

All files are organized by function:
- **Configuration**: `.env.example`, `config.py`
- **Data Models**: `schemas.py`
- **Agents**: `agent_*.py` files
- **Integration**: `memory_manager.py`, `file_writer.py`, `github_manager.py`
- **API**: `main.py`
- **Frontend**: `frontend/app.py`
- **Testing**: `tests.py`
- **Documentation**: `README.md`, `QUICK_START.md`, `ARCHITECTURE.md`
- **Scripts**: `start.bat`, `start.sh`, `startup.py`

This modular structure ensures maintainability, testability, and extensibility.

---

**Total Implementation: 100% Complete ✅**

All files are production-ready and fully functional.
