from flask import Flask, request, jsonify
from app.services.gitlab_integration import fetch_merge_request_changes, post_feedback_to_gitlab
from app.services.ai_integration import analyze_code_with_ai
import app.config.git_config as config

app = Flask(__name__)

@app.route('/gitlab-webhook', methods=['POST'])
def webhook():
    # Validate webhook request
    secret = request.headers.get('X-Gitlab-Token')
    if secret != config.GITLAB_SECRET:
        return "Unauthorized", 401

    event = request.json

    # Check if the event is for merge request
    if event.get('object_kind') == 'merge_request':
        project_id = event['object_attributes']['target_project_id']
        merge_request_iid = event['object_attributes']['iid']
        merge_request_url = event['object_attributes']['url']
        user_name = event['user']['name']

        print(f"Processing MR {merge_request_iid} by {user_name}: {merge_request_url}")

        # Fetch the changed files
        changes = fetch_merge_request_changes(project_id, merge_request_iid)

        print("this si below analizer")

        # Generate AI feedback
        feedback = analyze_code_with_ai(changes)

        print("beford feedback")

        # Post feedback to GitLab
        post_feedback_to_gitlab(project_id, merge_request_iid, feedback)

        return jsonify({"status": f"Feedback posted for MR {merge_request_iid}"}), 200

    return "Event not handled", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
