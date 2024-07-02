from typing import Annotated, List, Dict, Union

import github
import github.GitTree
import github.Repository
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/repositories")


base_url = "https://api.github.com"


class FilePathsRequest(BaseModel):
    filePaths: list[str]

class JsonTreeNode(BaseModel):

        type: Union[str | None] = None
        path: str
        name: str
        children: List['JsonTreeNode'] = []


# TODO 추후 비동기로 성능이 오를 여지가 있다면 비동기로 구현

@router.get("/{repoId}/files/paths")
def getRepoStructure(repoId: int,
                     access_token: Annotated[str,
                     Header(convert_underscores=False)]) -> JsonTreeNode:
    try:
        authToken = github.Auth.Token(token=access_token)
        targetGithub = github.Github(auth=authToken)

        repo : github.Repository.Repository = targetGithub.get_repo(repoId)
        latestCommitHash: str = repo.get_commits().get_page(0)[0].sha
        gitTree: github.GitTree.GitTree = repo.get_git_tree(latestCommitHash, recursive=True)

        filepaths: list[str] = [file.path for file in gitTree.tree]
    except github.GithubException as e:

        raise HTTPException(status_code=e.status, detail=str(e))

    return createFileDirectory(filepaths)

def createFileDirectory(filePaths: list[str]) -> JsonTreeNode:

    root = JsonTreeNode(name="", path="", type="directory")
    nodes: Dict[str, JsonTreeNode] = dict()
    nodes[""] = root
    prev = root

    for filePath in filePaths:
        pathDiv: list[str] = filePath.split("/")

        if len(pathDiv) == 1:
            node = JsonTreeNode(name=pathDiv[-1], path=filePath)
            root.children.append(node)
            nodes[filePath] = node

        else:
            node = JsonTreeNode(name=pathDiv[-1], path=filePath)
            nodes["/".join(pathDiv[:-1])].children.append(node)
            nodes[filePath] = node
    for node in nodes.values():
        if len(node.children) != 0:
            node.type = "directory"
        else:
            node.type = "file"

    return root

@router.post("/{repoId}/files/contents")
def getFiles(repoId: int,
             access_token: Annotated[str, Header(convert_underscores=False)],
             filePaths: FilePathsRequest):

    try:
        authToken = github.Auth.Token(token=access_token)

        targetGithub = github.Github(auth=authToken)

        repo = targetGithub.get_repo(repoId)

        fileContents = dict()

        for filePath in filePaths.filePaths:
            contents = repo.get_contents(filePath)
            fileContents[filePath] = contents.decoded_content.decode("utf-8").split("\n")

        return fileContents
    except github.GithubException as e:
        raise HTTPException(status_code=e.status, detail=str(e))



