from .api import get_repositories, get_user_profile
from .analyzer import analyze_repositories
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Github Analyzer API"}

@app.get("/analyze/{username}")
def analyze(username:str):
    user = get_user_profile(username)
    if user is not None:
        repos = get_repositories(username)
        if repos is not None:
            analysis = analyze_repositories(repos)
            return analysis
        else:
            raise HTTPException(status_code=500, detail="Could not fetch repositories")
    else:
        raise HTTPException(status_code=404, detail="User not found!")
