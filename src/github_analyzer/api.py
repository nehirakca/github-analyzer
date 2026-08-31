import requests
from typing import Optional, TypedDict

class User(TypedDict):
    login:str
    name:Optional[str]
    followers:int
    following:int
    public_repos:int

class Repository(TypedDict):
    language:Optional[str]
    stargazers_count:int

def api_request(url:str, params:Optional[dict] = None) -> Optional[dict | list]:
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_user_profile(username:str) -> Optional[User]:
    url=f"https://api.github.com/users/{username}"
    return api_request(url)

def get_repositories(username:str) -> Optional[list[Repository]]:
    repositories=[]
    page=1
    url=f"https://api.github.com/users/{username}/repos"
    while True:
        params={
            "page":page,
            "per_page":100
        }
        new_repositories = api_request(url, params)
        if new_repositories is not None:
            repositories.extend(new_repositories)
            if len(new_repositories) < 100:
                break
            else:
                page+=1
        else:
            return None
    return repositories