import os
from pprint import pprint
import faculty
import requests

profile = faculty.config.resolve_profile()
access_token = faculty.session._get_access_token(profile)
user_auth_header = {}
user_auth_header["Authorization"] = f"Bearer {access_token.token}"

project_id = os.environ["FACULTY_PROJECT_ID"]

halide_url = f"https://halide.{profile.domain}"

list_apps_response = requests.get(
    "{}/project/{}/app".format(halide_url, project_id), headers=user_auth_header
)

pprint(list_apps_response)
all_apps_id = [app["appId"] for app in list_apps_response.json()]
pprint(list_apps_response.json())
