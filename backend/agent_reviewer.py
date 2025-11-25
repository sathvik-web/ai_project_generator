"""
Agent Reviewer: Self-improvement loop for generated code.
Reviews, validates, and improves code quality automatically.
"""

import re
from typing import List, Dict, Tuple
from schemas import GeneratedFile


class AgentReviewer:
    """Reviews and improves generated code."""
    
    # Common issues and fixes
    ISSUES = {
        "missing_imports": {
            "pattern": r"^from|^import",
            "description": "Check for missing imports"
        },
        "syntax_error": {
            "pattern": r"syntax|error|exception",
            "description": "Check for syntax errors"
        },
        "docstring": {
            "pattern": r'"""',
            "description": "Check for docstrings"
        },
        "type_hints": {
            "pattern": r"-> ",
            "description": "Check for type hints"
        }
    }
    
    def __init__(self):
        """Initialize reviewer."""
        pass
    
    def review_files(self, files: List[GeneratedFile]) -> List[GeneratedFile]:
        """
        Review and improve all generated files.
        
        Args:
            files: List of generated files
            
        Returns:
            Improved files with review notes
        """
        reviewed_files = []
        
        for file_obj in files:
            reviewed_file = self.review_file(file_obj)
            reviewed_files.append(reviewed_file)
        
        return reviewed_files
    
    def review_file(self, file_obj: GeneratedFile) -> GeneratedFile:
        """
        Review a single file and apply improvements.
        
        Args:
            file_obj: Generated file
            
        Returns:
            Improved file object
        """
        issues = self._analyze_file(file_obj)
        improved_content = file_obj.content
        
        # Apply fixes based on issues
        for issue_type, details in issues.items():
            if details["found"]:
                improved_content = self._apply_fix(
                    improved_content, 
                    issue_type, 
                    file_obj.path
                )
        
        file_obj.content = improved_content
        file_obj.reviewed = True
        file_obj.review_notes = self._generate_review_notes(issues)
        
        return file_obj
    
    def _analyze_file(self, file_obj: GeneratedFile) -> Dict[str, Dict]:
        """Analyze file for common issues."""
        content = file_obj.content
        file_type = file_obj.path.split('.')[-1].lower()
        
        issues = {
            "missing_imports": {"found": False, "count": 0},
            "syntax_errors": {"found": False, "count": 0},
            "missing_docstrings": {"found": False, "count": 0},
            "missing_type_hints": {"found": False, "count": 0},
            "trailing_whitespace": {"found": False, "count": 0},
            "long_lines": {"found": False, "count": 0},
        }
        
        if file_type != "py":
            return issues
        
        lines = content.split('\n')
        
        # Check for imports
        has_imports = any(line.strip().startswith(('import ', 'from ')) for line in lines)
        if not has_imports and 'TODO' not in content:
            issues["missing_imports"]["found"] = True
            issues["missing_imports"]["count"] = 1
        
        # Check for docstrings
        docstring_count = content.count('"""')
        function_count = content.count('def ')
        if function_count > docstring_count // 2:
            issues["missing_docstrings"]["found"] = True
            issues["missing_docstrings"]["count"] = function_count - (docstring_count // 2)
        
        # Check for type hints in function definitions
        for line in lines:
            if 'def ' in line and '->' not in line and 'TODO' not in line:
                issues["missing_type_hints"]["found"] = True
                issues["missing_type_hints"]["count"] += 1
        
        # Check for trailing whitespace
        for line in lines:
            if line.endswith(' ') or line.endswith('\t'):
                issues["trailing_whitespace"]["found"] = True
                issues["trailing_whitespace"]["count"] += 1
        
        # Check for long lines
        for line in lines:
            if len(line) > 100:
                issues["long_lines"]["found"] = True
                issues["long_lines"]["count"] += 1
        
        return issues
    
    def _apply_fix(self, 
                  content: str, 
                  issue_type: str, 
                  file_path: str) -> str:
        """Apply fixes for detected issues."""
        lines = content.split('\n')
        
        if issue_type == "missing_imports":
            content = self._add_missing_imports(content, file_path)
        
        elif issue_type == "trailing_whitespace":
            lines = [line.rstrip() for line in lines]
            content = '\n'.join(lines)
        
        elif issue_type == "long_lines":
            content = self._break_long_lines(content)
        
        elif issue_type == "missing_docstrings":
            content = self._add_docstrings(content)
        
        elif issue_type == "missing_type_hints":
            content = self._add_type_hints(content)
        
        return content
    
    def _add_missing_imports(self, content: str, file_path: str) -> str:
        """Add commonly missing imports."""
        # Standard imports that are commonly needed
        standard_imports = "import logging\nfrom typing import Dict, List, Optional, Any\n"
        
        if "# Standard imports" not in content:
            lines = content.split('\n')
            
            # Find insertion point (before other imports or at top)
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('"""'):
                    # Skip docstring
                    for j in range(i + 1, len(lines)):
                        if '"""' in lines[j]:
                            insert_idx = j + 1
                            break
                    break
            
            # Insert standard imports if not present
            if insert_idx < len(lines):
                lines.insert(insert_idx, "\n# Standard imports")
                lines.insert(insert_idx + 1, standard_imports)
                content = '\n'.join(lines)
        
        return content
    
    def _break_long_lines(self, content: str) -> str:
        """Break lines longer than 100 characters."""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if len(line) > 100 and '# ' not in line:
                # Try to break at logical points
                if '(' in line and ')' in line:
                    fixed_line = self._break_at_parens(line)
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _break_at_parens(self, line: str) -> str:
        """Break line at parentheses."""
        # Simple approach - add newlines after commas in function calls
        if line.count('(') == 1 and line.count(',') > 0:
            # Indent for continuation
            indent = len(line) - len(line.lstrip())
            parts = line.split(',')
            return (',\n' + ' ' * (indent + 4)).join(parts)
        return line
    
    def _add_docstrings(self, content: str) -> str:
        """Add missing docstrings to functions."""
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            fixed_lines.append(line)
            
            # Check if this is a function definition
            if re.match(r'\s*def\s+\w+\s*\(', line):
                # Check if next line is not a docstring
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not next_line.startswith('"""') and next_line:
                        # Add docstring
                        indent = len(line) - len(line.lstrip()) + 4
                        func_name = re.search(r'def\s+(\w+)', line)
                        if func_name:
                            docstring = f'{" " * indent}"""Function documentation."""'
                            fixed_lines.append(docstring)
            
            i += 1
        
        return '\n'.join(fixed_lines)
    
    def _add_type_hints(self, content: str) -> str:
        """Add basic type hints to functions."""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if re.match(r'\s*def\s+\w+\s*\(', line) and '->' not in line:
                # Add return type hint
                if line.rstrip().endswith(':'):
                    line = line.rstrip()[:-1] + ' -> Any:'
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _generate_review_notes(self, issues: Dict[str, Dict]) -> str:
        """Generate review notes from issues found."""
        notes = []
        
        for issue_type, details in issues.items():
            if details["found"]:
                count = details.get("count", 0)
                formatted_type = issue_type.replace('_', ' ').title()
                notes.append(f"{formatted_type}: {count} instance(s) fixed")
        
        if not notes:
            return "✓ Code quality checks passed"
        
        return "✓ Fixed: " + ", ".join(notes)
    
    def validate_syntax(self, file_obj: GeneratedFile) -> Tuple[bool, str]:
        """
        Validate Python syntax.
        
        Args:
            file_obj: Generated file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_obj.path.endswith('.py'):
            return True, ""
        
        try:
            compile(file_obj.content, file_obj.path, 'exec')
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def get_code_metrics(self, file_obj: GeneratedFile) -> Dict[str, int]:
        """Calculate code metrics for file."""
        content = file_obj.content
        lines = content.split('\n')
        
        metrics = {
            "total_lines": len(lines),
            "code_lines": sum(1 for line in lines if line.strip() and not line.strip().startswith('#')),
            "comment_lines": sum(1 for line in lines if line.strip().startswith('#')),
            "blank_lines": sum(1 for line in lines if not line.strip()),
            "functions": content.count('def '),
            "classes": content.count('class '),
            "imports": sum(1 for line in lines if line.strip().startswith(('import ', 'from '))),
        }
        
        return metrics
