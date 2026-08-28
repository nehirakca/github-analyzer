import requests
from typing import Optional,TypedDict

class User(TypedDict):
    login:str
    name:Optional[str]
    followers:int
    following:int
    public_repos:int

def get_user_profile(username:str) -> Optional[User]:
    try:
        url=f"https://api.github.com/users/{username}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("User not found!")
            return None
        elif response.status_code == 403:
            print("Access denied or rate limit exceeded!")
            return None
        else:
            print("API error!")
            return None
    except requests.exceptions.RequestException:
        return None

def get_repositories(username:str) -> Optional[list[dict]]:
    try:
        repositories=[]
        page=1
        url=f"https://api.github.com/users/{username}/repos"
        while True:
            params={
                "page":page,
                "per_page":100
            }
            response=requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                new_repositories = response.json()
                repositories.extend(new_repositories)
                if len(new_repositories) < 100:
                    break
                else:
                    page+=1
            elif response.status_code == 404:
                print("User not found!")
                return None
            elif response.status_code == 403:
                print("Access denied or rate limit exceeded!")
                return None
            else:
                print("API error!")
                return None
        return repositories
    except requests.exceptions.RequestException:
        return None