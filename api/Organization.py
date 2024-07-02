from typing import Annotated

import requests
from fastapi import APIRouter, Header
from pydantic import BaseModel

router = APIRouter(prefix="/orgs")
base_url = "https://api.github.com"


class RepositoryMetadata(BaseModel):
    id: int
    name: str
    url: str


@router.get("/repositories")
def getOrgRepositories(access_token: Annotated[str, Header(convert_underscores=False)], orgName: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    repositories = []

    page = 1
    params = {"per_page": 100, "page": page}

    while True:
        response = requests.get(url=f'{base_url}/orgs/{orgName}/repos',
                                headers=headers,
                                params=params)

        repos = response.json()
        if not repos:
            break

        for repo in repos:
            repositoryMetadata = RepositoryMetadata(url=repo["html_url"],
                                                    name=repo['name'],
                                                    id=repo['id'])

            repositories.append(repositoryMetadata)
        params["page"] += 1


    return repositories
