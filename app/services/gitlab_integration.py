
import requests
import app.config.git_config as config

def fetch_merge_request_changes(project_id, merge_request_iid):
    """
    Fetch the list of changed files in the merge request.
    """
    url = f"http://10.10.1.68/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/diffs"
    print("belore url")
    headers = {"Private-Token": config.GITLAB_TOKEN}
    print(headers)
    response = requests.get(url, headers=headers)
    print(type(response))
    print("resp", response.content)
    print("resp", response.status_code)
    response.raise_for_status()
    print("before chnges")
    changes = [change['new_path'] for change in response.json().get('changes', [])]
    print(changes)
    return changes

def post_feedback_to_gitlab(project_id, merge_request_iid, feedback):
    """
    Post AI feedback as comments in the GitLab MR discussions.
    """
    # url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/discussions"
    url = f"http://10.10.1.68/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/diffs"
    headers = {"Private-Token": config.GITLAB_TOKEN}

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
