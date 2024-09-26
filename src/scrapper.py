import requests
from bs4 import BeautifulSoup
import json
import os


def repo_scrapper(technology):

    url = f"https://github.com/trending/{technology}?since=daily&spoken_language_code=en"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    repos = soup.find_all('article', class_='Box-row')

    repo_data = []

    # Loop through each repo and extract details.
    for repo in repos[:5]:
        # Get the repository name
        repo_name = repo.find('h2', {'class':'h3'}).text.strip().replace("\n", "").replace(" ", "")
        
        # Get the repository description 
        repo_desc = repo.find('p', {'class':'col-9 color-fg-muted my-1 pr-4'})
        repo_desc = repo_desc.text.strip() if repo_desc else 'No description available'
        
        
        # Get the repository language
        repo_lang = repo.find('span', {'class':'d-inline-block ml-0 mr-3'})
        repo_lang = repo_lang.text.strip() if repo_lang else 'N/A'
        
        # Get the repository URL
        repo_url = "https://github.com" + repo.find('h2', {'class':'h3'}).find('a')['href']
        
        # Store the extracted data in a dictionary
        repo_info = {
            "name": repo_name,
            "description": repo_desc,
            "language": repo_lang,
            "url": repo_url
        }
        
        repo_data.append(repo_info)


    return repo_data


def scrape_repos_and_get_readme(repo_data):
    updated_repo_data = []
    
    for repo in repo_data:
        # Try fetching the README from the 'main' branch
        readme_url = f"{repo['url']}/blob/main/README.md"
        response = requests.get(readme_url)
        
        # If 'main' branch doesn't work, try the 'master' branch
        if response.status_code != 200:
            readme_url = f"{repo['url']}/blob/master/README.md"
            response = requests.get(readme_url)
        

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            readme_div = soup.find('article', {"class":'markdown-body entry-content container-lg'})
            readme_content = readme_div.text.strip() if readme_div else "README content not available."
        else:
            readme_content = repo['description']
        
        updated_repo = {
            "name": repo['name'],
            "technology": repo['language'],
            "url": repo['url'],
            "description": readme_content  # Store the README content in description
        }
        
        updated_repo_data.append(updated_repo)


    return updated_repo_data
