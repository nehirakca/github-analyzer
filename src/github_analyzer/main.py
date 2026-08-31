from .api import get_repositories, get_user_profile
from .analyzer import analyze_repositories
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserResponse(BaseModel):
    login:str
    name:Optional[str]
    followers:int
    following:int
    public_repos:int

class AnalysisResponse(BaseModel):
    languages:dict[str, int]
    total_stars:int
    repository_count:int
    most_used_language:Optional[str]
    language_distribution:dict[str, float]

class GithubAnalysisResponse(BaseModel):
    user:UserResponse
    analysis:AnalysisResponse

@app.get("/")
def hello():
    return {"message": "Github Analyzer API"}

@app.get("/analyze/{username}", response_model=GithubAnalysisResponse)
def analyze(username:str):
    user = get_user_profile(username)
    if user is not None:
        repos = get_repositories(username)
        if repos is not None:
            analysis = analyze_repositories(repos)
            return {
                "user":user,
                "analysis":analysis
            }
        else:
            raise HTTPException(status_code=500, detail="Could not fetch repositories")
    else:
        raise HTTPException(status_code=404, detail="User not found!")
