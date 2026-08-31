from typing import Optional, TypedDict
from .api import Repository, get_repositories

class AnalysisResult(TypedDict):
    languages:dict[str, int]
    total_stars:int
    repository_count:int
    most_used_language:Optional[str]
    language_distribution:dict[str, float]

def analyze_repositories(data:list[Repository]) -> AnalysisResult:
    languages={}
    language_distribution={}
    total_stars = 0
    for repo in data:
        language = repo['language']
        if language is not None:
            if language in languages:
                languages[language]+=1
            else:
                languages[language]=1
        total_stars+=repo['stargazers_count']
    repository_count = len(data)
    if languages:
        most_used_language = max(languages, key=languages.get)
        total_language_repos = sum(languages.values())
        for language, count in languages.items():
            percentage = (count/total_language_repos)*100
            language_distribution[language] = percentage
    else:
        most_used_language = None
    return{
        'languages': languages,
        'total_stars': total_stars,
        'repository_count': repository_count,
        'most_used_language': most_used_language,
        'language_distribution': language_distribution
    }