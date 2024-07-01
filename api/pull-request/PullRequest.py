from fastapi import APIRouter

router = APIRouter(prefix="pulls")


# @router.get("")
# async def get_pulls(token: auth.token.AppInstallationToken):
#     appUserAuth = github.AppUserAuth.AppUserAuth(token=token.access_token,
#                                                  client_id=env.CLIENT_ID,
#                                                  client_secret=env.CLIENT_SECRET)
#     gith = github.Github(auth=appUserAuth)
#
#     return
