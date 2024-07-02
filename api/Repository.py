from typing import Annotated

import github
import github.GitTree
import github.Repository
from fastapi import APIRouter, Header
from pydantic import BaseModel

router = APIRouter(prefix="/repositories")


base_url = "https://api.github.com"


class FilePathsRequest(BaseModel):
    filePaths: list[str]





# TODO 추후 비동기로 성능이 오를 여지가 있다면 비동기로 구현

@router.get("/{repoId}/files/paths")
def getRepoStructure(repoId: int,
                     access_token: Annotated[str, Header(convert_underscores=False)]):
    authToken = github.Auth.Token(token=access_token)
    targetGithub = github.Github(auth=authToken)

    repo = targetGithub.get_repo(repoId)
    latestCommitHash: str = repo.get_commits().get_page(0)[0].sha
    gitTree: github.GitTree.GitTree = repo.get_git_tree(latestCommitHash, recursive=True)

    filepaths: list[str] = [file.path for file in gitTree.tree]

    return filepaths


# TODO json을 트리 구조로 만들기

@router.post("/{repoId}/files/contents")
def getFiles(repoId: int,
                   access_token: Annotated[str, Header(convert_underscores=False)],
                   filePaths: FilePathsRequest):
    authToken = github.Auth.Token(token=access_token)

    targetGithub = github.Github(auth=authToken)

    repo = targetGithub.get_repo(repoId)

    fileContents = dict()

    for filePath in filePaths.filePaths:
        contents = repo.get_contents(filePath)
        fileContents[filePath] = contents.decoded_content.decode("utf-8").split("\n")

    return fileContents



