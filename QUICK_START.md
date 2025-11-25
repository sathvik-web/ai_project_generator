# 🚀 Quick Start Guide - AI Project Generator

Get up and running in 5 minutes!

## Step 1: Prerequisites Check

Verify you have Python 3.11+:

```bash
python --version
# Python 3.11.x or higher required
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Takes about 1-2 minutes.

## Step 3: Configure Environment (Optional but Recommended)

To enable GitHub integration:

1. **Get GitHub Token**:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token"
   - Select scopes: `repo`, `user`, `gist`
   - Copy token

2. **Create `.env` file**:
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit .env and add:
   GITHUB_TOKEN=your_token_here
   GITHUB_USERNAME=your_username
   ```

*Note: System works without GitHub config, but can't push to repositories.*

## Step 4: Run Backend

```bash
# Option A: Windows
start.bat

# Option B: macOS/Linux
bash start.sh
chmod +x start.sh
./start.sh

# Option C: Manual
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## Step 5: Run Frontend (New Terminal)

Keep backend running. In a **new terminal**:

```bash
streamlit run frontend/app.py
```

Browser opens at `http://localhost:8501`

## First Generation

1. Open http://localhost:8501 in browser
2. Go to **Generate** tab
3. Enter prompt:
   ```
   Create a FastAPI REST API with SQLite database
   ```
4. Click **Generate Project**
5. Check the logs - project generates in ~10 seconds
6. Find generated files in `workspace/` folder

## Common Prompts to Try

### Web APIs
```
Create a FastAPI REST API with user authentication and PostgreSQL
```

### Dashboards
```
Build a Streamlit dashboard that shows sales metrics and charts
```

### ML Models
```
Generate a PyTorch image classification model with training code
```

### Full Stack
```
Create a React frontend with Flask backend and SQLite database
```

### Web Scrapers
```
Build a web scraper that fetches stock prices and stores them
```

## File Locations

After generation, check:

```
workspace/
└── project_name/          # Your generated project
    ├── main.py            # Entry point
    ├── requirements.txt   # Dependencies
    ├── README.md          # Documentation
    └── ... other files
```

## API Documentation

While backend is running:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Troubleshooting

### "Port already in use"
```bash
# Change port in .env
API_PORT=8001
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "GitHub error"
- Check token in `.env`
- Verify GitHub username
- Test token permissions

### "API won't start"
- Check Python version: `python --version`
- Check port: `netstat -ano | findstr :8000` (Windows)
- Check logs for errors

## Next Steps

1. ✅ Run your first project generation
2. 📖 Read full README.md for detailed documentation
3. 🔧 Configure GitHub integration for repo creation
4. 🧪 Try different project types
5. 💾 View generated code in workspace/

## Architecture Quick View

```
┌─────────────────────────────────────────┐
│         Your Browser                    │
│    http://localhost:8501               │
│  (Streamlit Frontend)                  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    http://localhost:8000                │
│    (FastAPI Backend)                    │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ Agent Pipeline                   │  │
│  │ Planner → Generator → Reviewer   │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ Storage                          │  │
│  │ Memory (JSON) + Workspace        │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  workspace/     │
        │  (Generated     │
        │   Projects)     │
        └─────────────────┘
```

## Features Summary

✅ AI-powered project planning
✅ Automatic code generation  
✅ Self-improving code review
✅ User preference learning
✅ GitHub integration
✅ REST API backend
✅ Web UI frontend
✅ Type hints & docstrings
✅ Production-ready templates
✅ Multi-framework support

## Estimated Time

| Task | Time |
|------|------|
| Prerequisites check | 2 min |
| Install dependencies | 2-3 min |
| Configure .env | 3 min |
| Start backend | 1 min |
| Start frontend | 1 min |
| First generation | 10-15 sec |
| **Total** | **~8-10 min** |

## Support

- 📖 Full docs: `README.md`
- 🔍 API docs: http://localhost:8000/api/docs
- 🐛 Issues: Check backend logs
- 💬 Questions: Read backend code comments

## Tips & Tricks

### Performance
- Generation time: 7-15 seconds typical
- Memory learns after each project
- Workspace grows with each generation

### Quality
- All generated code has type hints
- Code is reviewed automatically
- Syntax validated before saving

### Development
- Edit `.env` to change settings
- Check `memory/memory.json` for preferences
- Use API directly for automation

---

**You're all set! Start generating projects! 🎉**

Got a project idea? Try it:
```
http://localhost:8501
```

Questions? Check README.md for detailed documentation.

Happy coding! 🚀
