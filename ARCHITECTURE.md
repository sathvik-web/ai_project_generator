# AI Project Generator - Architecture & Design Document

## System Overview

AI Project Generator is a modular, agent-based system that transforms natural language project descriptions into complete, production-ready software projects. The system uses a pipeline architecture with specialized agents handling different aspects of project generation.

## Core Principles

1. **Modularity**: Each component is independent and reusable
2. **Extensibility**: Easy to add new agents, templates, and technologies
3. **Quality**: Automatic code review and improvement
4. **Learning**: System learns user preferences over time
5. **Production-Ready**: All generated code follows best practices
6. **User-Centric**: Web UI for easy interaction

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Component**: `frontend/app.py` (Streamlit)

Responsibilities:
- User input collection
- Project generation triggering
- Result visualization
- Memory inspection
- Project management UI

Features:
- Multi-tab interface (Generate, Projects, Memory, Help)
- Real-time generation logs
- API integration
- Responsive design

### 2. API Layer (Backend)

**Component**: `backend/main.py` (FastAPI)

Endpoints:
```
POST   /generate              - Generate new project
POST   /update                - Update existing project
GET    /memory                - Get user preferences
GET    /projects              - List recent projects
GET    /project/{name}        - Get project details
DELETE /project/{name}        - Delete project
POST   /preference             - Update preference
POST   /memory/reset          - Reset memory
GET    /health               - Health check
GET    /                      - Root endpoint
```

Features:
- Async request handling
- CORS support
- Background tasks for GitHub push
- Comprehensive logging
- Error handling with proper HTTP codes

### 3. Agent Layer

Four specialized agents working in sequence:

#### A. Agent Planner (`agent_planner.py`)

**Purpose**: Understand requirements and create project blueprint

**Process**:
1. Extract keywords from prompt
2. Detect technologies and frameworks
3. Generate project name
4. Build file structure
5. Create project plan JSON

**Output**:
```json
{
  "project_name": "text_summarizer",
  "description": "...",
  "tech_stack": ["Python", "FastAPI", "T5"],
  "structure": {"main.py": "...", "models/": "..."},
  "files": [...],
  "entry_point": "main.py"
}
```

**Technology Detection**:
- FastAPI, Flask, Django
- Streamlit, React
- PyTorch, TensorFlow, Scikit-learn
- PostgreSQL, MongoDB, Redis
- Docker, GitHub Actions

#### B. Agent Generator (`agent_generator.py`)

**Purpose**: Generate complete, working code files

**Process**:
1. Iterate through plan files
2. Match file type to template
3. Customize with project details
4. Apply memory preferences
5. Generate complete content

**Code Templates**:
- FastAPI main.py
- Flask app.py
- Streamlit app.py
- requirements.txt
- README.md
- .env files
- Model files
- Test templates
- Dockerfile

**Features**:
- Template-based generation
- Placeholder substitution
- Framework-specific customization
- Boilerplate code
- Best practices included

#### C. Agent Reviewer (`agent_reviewer.py`)

**Purpose**: Validate and improve generated code

**Automatic Improvements**:
- Syntax validation
- Missing imports detection
- Type hint addition
- Docstring generation
- Trailing whitespace removal
- Long line breaking
- Code metrics calculation

**Quality Metrics**:
- Total lines of code
- Function count
- Class count
- Import statements
- Comment coverage

**Validation**:
- Python syntax compilation check
- Import resolution
- Function signature validation

#### D. Memory Manager (`memory_manager.py`)

**Purpose**: Store and learn user preferences

**Storage Structure**:
```json
{
  "preferred_backend": "fastapi",
  "preferred_frontend": "streamlit",
  "coding_style": "descriptive comments...",
  "common_issues": ["missing_imports"],
  "frameworks": ["FastAPI", "PyTorch"],
  "language_preference": "python",
  "database_preference": "sqlite",
  "last_projects": ["project1", "project2"],
  "preferences": {}
}
```

**Learning Capabilities**:
- Tracks used frameworks
- Records common issues
- Updates preferred tools
- Remembers project history
- Learns coding patterns

**Persistence**:
- JSON file storage (`memory/memory.json`)
- Event history logging (`memory/history.json`)
- Automatic updates after each project

### 4. Integration Layer

#### A. File Writer (`file_writer.py`)

**Responsibilities**:
- Create project directories
- Write code files safely
- Manage file paths
- Handle encoding
- Verify operations

**Operations**:
```python
create_project_structure()  # Create folders
write_files()              # Write all files
write_single_file()        # Write one file
read_file()               # Read project file
delete_project()          # Remove project
```

#### B. GitHub Manager (`github_manager.py`)

**Responsibilities**:
- Create repositories
- Upload files
- Commit and push
- Handle authentication
- Manage version control

**GitHub Operations**:
```
create_repo()           # Create new repository
repo_exists()          # Check repo status
create_or_update_file() # Upload single file
upload_project()       # Upload entire project
clone_repo()           # Clone to local
```

**Authentication**:
- Uses GitHub Personal Access Token
- PAT scopes: repo, user, gist
- Automatic error handling

#### C. Schema Definitions (`schemas.py`)

**Purpose**: Data validation with Pydantic

**Key Models**:
- `ProjectPlanRequest` - Input for planning
- `ProjectGenerateRequest` - Full generation request
- `ProjectPlan` - Blueprint output
- `GeneratedFile` - Single file with metadata
- `GenerationResponse` - API response
- `UserMemory` - User preferences storage

**Validation Benefits**:
- Type safety
- Automatic validation
- Documentation
- IDE support

### 5. Data Layer

**Storage**:
- `memory/memory.json` - User preferences
- `memory/history.json` - Event log
- `workspace/` - Generated projects

**Formats**:
- JSON for configuration
- Python for code
- Markdown for docs

## Data Flow

### Project Generation Flow

```
1. User Prompt
        ↓
2. Planner Agent
   - Detect tech
   - Create blueprint
   - Plan files
        ↓
3. Generator Agent
   - Generate code
   - Use templates
   - Add boilerplate
        ↓
4. Reviewer Agent
   - Validate syntax
   - Fix issues
   - Improve quality
        ↓
5. File Writer
   - Create structure
   - Write files
   - Verify success
        ↓
6. Memory Update
   - Learn preferences
   - Update stats
   - Log event
        ↓
7. GitHub Push (async)
   - Create repo
   - Upload files
   - Commit & push
        ↓
8. Response
   - Success status
   - Project info
   - Repository URL
```

### Memory Flow

```
Project Generation
        ↓
Extract Information
  - Tech stack
  - Project name
  - Preferences
        ↓
Update Memory
  - Add frameworks
  - Add project
  - Update prefs
        ↓
Persist to Disk
  - Write JSON
  - Log history
        ↓
Future Generations
  Use learned preferences
```

## Design Patterns

### 1. Pipeline Pattern
Sequential processing through specialized agents:
```
Input → Planner → Generator → Reviewer → Writer → Output
```

### 2. Strategy Pattern
Different templates for different technologies:
```
FastAPI Strategy
Flask Strategy
Streamlit Strategy
```

### 3. Template Method Pattern
File generation uses templates with variable substitution:
```
Template + Context = Generated Code
```

### 4. Singleton Pattern
Managers (MemoryManager, FileWriter) are instantiated once and reused

### 5. Factory Pattern
File writer creates appropriate structures based on requirements

## Technology Stack Justification

### Backend: FastAPI
- Modern Python framework
- Async support
- Automatic API docs
- Built-in validation
- High performance

### Frontend: Streamlit
- Rapid UI development
- No JavaScript needed
- Easy interactivity
- Great for data apps
- Clean interface

### Storage: JSON
- Human readable
- No database setup
- Easy versioning
- Sufficient for current scale
- Future: Can migrate to DB

### GitHub API
- No additional services
- Direct repository control
- Personal access tokens
- REST-based
- Well documented

## Extensibility Points

### Adding New Technologies

1. **Add to TECH_PATTERNS** in `agent_planner.py`
2. **Create template** in `agent_generator.py`
3. **Add to frameworks list**
4. **Create test cases**

### Adding New Agents

1. Create new `agent_*.py` file
2. Implement generation logic
3. Integrate into pipeline in `main.py`
4. Add schema definitions

### Customizing Memory

1. Add fields to `UserMemory` schema
2. Update learning logic
3. Persist new fields
4. Use in generation

## Performance Characteristics

### Generation Time

| Stage | Time |
|-------|------|
| Planning | ~1s |
| Generation | ~2-3s |
| Review | ~1-2s |
| Writing | ~1s |
| GitHub (async) | ~2-5s |
| **Total** | ~7-15s |

### Memory Usage

- Base system: ~100-150 MB
- Per project: ~50-100 MB
- Memory file: <1 MB
- Scales linearly with projects

### Concurrency

- FastAPI handles multiple concurrent requests
- Background tasks for GitHub operations
- No blocking operations
- Async throughout

## Security Considerations

### Authentication
- GitHub PAT for repository access
- Token stored in environment
- No hardcoding credentials

### Code Safety
- Syntax validation before saving
- No arbitrary code execution
- Safe file operations
- Path traversal prevention

### Data Protection
- Memory file contains only preferences
- No sensitive data in workspace
- Clean generated code
- Proper error messages

## Error Handling

### Strategy
1. Validation at each layer
2. Meaningful error messages
3. Graceful degradation
4. Logging for debugging
5. HTTP-appropriate status codes

### Recovery
- Failed generation doesn't corrupt memory
- Partial writes cleaned up
- Retry-friendly design
- User feedback provided

## Testing Strategy

### Unit Tests
- Individual agent tests
- Manager functionality tests
- Schema validation tests

### Integration Tests
- Full pipeline tests
- File operations tests
- Memory persistence tests

### Manual Testing
- Different prompt types
- GitHub integration
- Error scenarios
- Performance monitoring

## Monitoring & Logging

### Logging Levels
- INFO: Status updates
- WARNING: Configuration issues
- ERROR: Operation failures
- DEBUG: Detailed information

### Logged Events
- Project generation start/end
- Agent processing steps
- File operations
- GitHub operations
- Memory updates
- API requests/responses

### Metrics
- Generation time
- Success rate
- File counts
- Technology usage
- Error frequency

## Future Enhancements

### Phase 2
- LLM integration for smarter code generation
- Multi-language support
- Advanced code templates
- Database schema generation
- Unit test generation

### Phase 3
- Web-based code editor
- Real-time collaboration
- Project versioning
- Deployment automation
- Analytics dashboard

### Phase 4
- Mobile app
- IDE plugins
- Enterprise features
- Custom agents
- Advanced analytics

## Deployment Considerations

### Development
```bash
python backend/main.py
streamlit run frontend/app.py
```

### Production
- Use production ASGI server (Gunicorn, Uvicorn)
- Environment-specific configs
- Database for memory (PostgreSQL recommended)
- CDN for frontend assets
- Monitoring and alerting
- Backup strategies

### Containerization
- Dockerfile ready
- Multi-stage builds
- Minimal image size
- Security scanning

## Conclusion

The AI Project Generator is designed as a scalable, maintainable system that can be extended with new capabilities while maintaining clean architecture and separation of concerns. The modular agent-based approach allows for easy testing, debugging, and enhancement.

Key strengths:
- Clear separation of concerns
- Easy to test and debug
- Simple to extend
- Production-ready code generation
- Learning system for preferences
- GitHub integration
- User-friendly interface

The system is ready for both personal use and enterprise deployment with appropriate scaling and database considerations.
