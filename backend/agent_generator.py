"""
Agent Generator: Generates complete working code files for projects.
Creates code based on project plan and user preferences.
"""

import json
from typing import List, Dict, Any
from schemas import ProjectPlan, GeneratedFile


class AgentGenerator:
    """Generates code files for projects."""
    
    # Code templates for different file types
    TEMPLATES = {
        "fastapi_main": '''"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="{{project_name}}",
    description="{{description}}",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to {{project_name}}",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
        "flask_main": '''"""
Main Flask application entry point.
"""

from flask import Flask, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    """Root endpoint."""
    return jsonify({
        "message": "Welcome to {{project_name}}",
        "status": "running"
    })

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
''',
        "streamlit_main": '''"""
Streamlit application interface.
"""

import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="{{project_name}}",
    page_icon="🚀",
    layout="wide"
)

st.title("{{project_name}}")
st.write("{{description}}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Status", value="Active")

with col2:
    st.metric(label="Version", value="1.0.0")

with col3:
    st.metric(label="API", value="Running")

st.divider()

# Main content
st.header("Main Section")
st.write("Add your application logic here.")
''',
        "requirements": '''# {{project_name}} Requirements
# Python {{python_version}}

fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
requests==2.31.0
aiohttp==3.9.1
pytest==7.4.3
black==23.12.0
flake8==6.1.0
mypy==1.7.1
''',
        "readme": '''# {{project_name}}

## Overview

{{description}}

## Features

- Modern Python backend with FastAPI
- RESTful API design
- Production-ready error handling
- Comprehensive logging
- Type hints and documentation

## Tech Stack

{{tech_stack}}

## Project Structure

```
{{project_name}}/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── .env                # Environment variables
└── tests/              # Test files
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/{{project_name}}
cd {{project_name}}
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The application will start on `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Testing

```bash
pytest tests/
```

## Development

Install development dependencies:
```bash
pip install -r requirements.txt
```

Format code with Black:
```bash
black .
```

Run linter:
```bash
flake8 .
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

MIT

## Support

For issues and questions, please create an GitHub issue.
''',
        "env": '''# Application Configuration
DEBUG=True
ENVIRONMENT=development

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_username

# Database Configuration (if needed)
DATABASE_URL=sqlite:///./app.db

# Logging
LOG_LEVEL=INFO
''',
        "gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project specific
workspace/
memory/
*.log
''',
        "model_pytorch": '''"""
PyTorch model definition.
"""

import torch
import torch.nn as nn
from typing import Tuple

class {{ProjectName}}Model(nn.Module):
    """Custom PyTorch model."""
    
    def __init__(self, 
                 input_size: int = 784,
                 hidden_size: int = 256,
                 output_size: int = 10):
        """
        Initialize model.
        
        Args:
            input_size: Input feature size
            hidden_size: Hidden layer size
            output_size: Output classes
        """
        super({{ProjectName}}Model, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

def create_model(device: str = "cpu") -> {{ProjectName}}Model:
    """Create and return model."""
    model = {{ProjectName}}Model()
    model.to(device)
    return model
''',
        "test_main": '''"""
Unit tests for main application.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
''',
        "dockerfile": '''# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
'''
    }
    
    def __init__(self):
        """Initialize code generator."""
        pass
    
    def generate_files(self, 
                      plan: ProjectPlan,
                      memory: Dict[str, Any]) -> List[GeneratedFile]:
        """
        Generate code files based on project plan.
        
        Args:
            plan: Project plan from planner
            memory: User preferences from memory
            
        Returns:
            List of generated files with content
        """
        generated_files = []
        
        for file_def in plan.files:
            content = self._generate_file_content(
                file_def,
                plan,
                memory
            )
            
            generated_file = GeneratedFile(
                path=file_def.path,
                content=content,
                reviewed=False
            )
            
            generated_files.append(generated_file)
        
        return generated_files
    
    def _generate_file_content(self, 
                               file_def,
                               plan: ProjectPlan,
                               memory: Dict[str, Any]) -> str:
        """Generate content for a single file."""
        file_type = file_def.file_type.lower()
        file_path = file_def.path.lower()
        
        # Special handling for different file types
        if "main.py" in file_path or "app.py" in file_path:
            return self._generate_main_file(plan, memory)
        elif "requirements.txt" in file_path:
            return self._generate_requirements(plan)
        elif "readme" in file_path or file_type == "md":
            return self._generate_readme(plan)
        elif ".env" in file_path:
            return self._generate_env_file(plan)
        elif ".gitignore" in file_path:
            return self._generate_gitignore()
        elif "model.py" in file_path:
            return self._generate_model(plan)
        elif "test_" in file_path and file_type == "py":
            return self._generate_test(plan)
        elif "dockerfile" in file_path.lower():
            return self._generate_dockerfile()
        else:
            # Generic Python file
            return self._generate_generic_file(file_def, plan)
    
    def _generate_main_file(self, plan: ProjectPlan, memory: Dict[str, Any]) -> str:
        """Generate main application file."""
        framework = self._detect_framework(plan.tech_stack)
        
        template_key = f"{framework}_main"
        template = self.TEMPLATES.get(template_key, self.TEMPLATES["fastapi_main"])
        
        # Replace placeholders
        content = template
        content = content.replace("{{project_name}}", plan.project_name)
        content = content.replace("{{description}}", plan.description)
        
        return content
    
    def _generate_requirements(self, plan: ProjectPlan) -> str:
        """Generate requirements.txt."""
        template = self.TEMPLATES["requirements"]
        
        tech_stack = ", ".join(plan.tech_stack)
        
        content = template
        content = content.replace("{{project_name}}", plan.project_name)
        content = content.replace("{{tech_stack}}", tech_stack)
        content = content.replace("{{python_version}}", "3.11")
        
        # Add tech-specific requirements
        if "pytorch" in [t.lower() for t in plan.tech_stack]:
            content += "\ntorch==2.1.1\ntorchvision==0.16.1\n"
        
        if "tensorflow" in [t.lower() for t in plan.tech_stack]:
            content += "\ntensorflow==2.14.0\n"
        
        if "scikit" in [t.lower() for t in plan.tech_stack]:
            content += "\nscikit-learn==1.3.2\n"
        
        if "pandas" in [t.lower() for t in plan.tech_stack]:
            content += "\npandas==2.1.1\nnumpy==1.26.2\n"
        
        return content
    
    def _generate_readme(self, plan: ProjectPlan) -> str:
        """Generate README.md."""
        template = self.TEMPLATES["readme"]
        
        tech_stack = "\n".join([f"- {tech}" for tech in plan.tech_stack])
        
        content = template
        content = content.replace("{{project_name}}", plan.project_name)
        content = content.replace("{{description}}", plan.description)
        content = content.replace("{{tech_stack}}", tech_stack)
        
        return content
    
    def _generate_env_file(self, plan: ProjectPlan) -> str:
        """Generate .env file."""
        return self.TEMPLATES["env"]
    
    def _generate_gitignore(self) -> str:
        """Generate .gitignore."""
        return self.TEMPLATES["gitignore"]
    
    def _generate_model(self, plan: ProjectPlan) -> str:
        """Generate model file."""
        if "pytorch" in [t.lower() for t in plan.tech_stack]:
            template = self.TEMPLATES["model_pytorch"]
            project_class_name = self._camel_case(plan.project_name)
            content = template.replace("{{ProjectName}}", project_class_name)
            return content
        
        # Generic model template
        return self._generate_generic_file(
            type('obj', (object,), {'path': 'model.py', 'description': 'Model'}),
            plan
        )
    
    def _generate_test(self, plan: ProjectPlan) -> str:
        """Generate test file."""
        return self.TEMPLATES["test_main"]
    
    def _generate_dockerfile(self) -> str:
        """Generate Dockerfile."""
        return self.TEMPLATES["dockerfile"]
    
    def _generate_generic_file(self, file_def, plan: ProjectPlan) -> str:
        """Generate a generic Python file."""
        description = file_def.description
        file_name = file_def.path.split('/')[-1]
        
        content = f'''"""
{file_name}

{description}
"""

# TODO: Implement {file_name.replace('.py', '')} functionality


def main():
    """Main entry point for {file_name.replace('.py', '')}."""
    pass


if __name__ == "__main__":
    main()
'''
        return content
    
    def _detect_framework(self, tech_stack: List[str]) -> str:
        """Detect primary framework from tech stack."""
        tech_lower = [t.lower() for t in tech_stack]
        
        if "fastapi" in tech_lower:
            return "fastapi"
        elif "flask" in tech_lower:
            return "flask"
        elif "streamlit" in tech_lower:
            return "streamlit"
        
        return "fastapi"
    
    def _camel_case(self, snake_str: str) -> str:
        """Convert snake_case to CamelCase."""
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)
