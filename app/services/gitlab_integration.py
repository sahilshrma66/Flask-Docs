
import requests
import os
from urllib.parse import quote


def fetch_merge_request_changes(project_id, merge_request_iid):
    """
    Fetch the list of changed files in the merge request.
    """
    url = f"http://10.10.1.68/api/v3/projects/{project_id}/merge_requests/{merge_request_iid}/changes"
    headers = {"Private-Token": os.getenv("GITLAB_TOKEN")}
    response = requests.get(url, headers=headers)
    # print(f"Response Body: {response.text}")
    response.raise_for_status()
    changes = [change['new_path'] for change in response.json().get('changes', [])]
    return changes

def post_feedback_to_gitlab(project_id, merge_request_iid, feedback):
    """
    Post AI feedback as comments in the GitLab MR discussions.
    """
    # url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/discussions"
    url = f"http://10.10.1.68/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/diffs"
    headers = {"Private-Token": os.getenv("GITLAB_TOKEN")}

    for file, suggestions in feedback.items():
        message = f"### AI Code Review Feedback for `{file}`\n\n{suggestions}"
        response = requests.post(
            url,
            headers=headers,
            json={"body": message}
        )
        if response.status_code == 201:
            print(f"Posted feedback for {file}")
        else:
            print(f"Failed to post feedback for {file}: {response.json()}")


# def fetch_merge_request_changes(project_id, merge_request_iid):
#     """
#     Fetch the list of changed files in the merge request using the GitLab API.
#     """
#     project_id_encoded = quote(str(project_id), safe="")
#     url = f"http://10.10.1.68/api/v3/projects/{project_id_encoded}/merge_requests/{merge_request_iid}/changes"
#     headers = {"Private-Token": os.getenv("GITLAB_TOKEN")}

#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         print(f"Error: Unable to fetch changes. Status Code: {response.status_code}")
#         print(f"Response Body: {response.text}")
#         response.raise_for_status()

#     changes = [change['new_path'] for change in response.json().get('changes', [])]
#     return changes



