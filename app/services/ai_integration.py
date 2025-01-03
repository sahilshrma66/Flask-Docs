import os
import requests
import json
from urllib.parse import quote
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import logging

AI_API_KEY = os.environ["OPENAI_API_KEY"] = os.getenv("AI_API_KEY")
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_file_content(project_id, file_path, commit_sha):
    """
    Fetch the content of a specific file from the repository at a given commit.
    """
    project_id_encoded = quote(str(project_id), safe="")
    file_path_encoded = quote(file_path, safe="")
    url = f"http://10.10.1.68/api/v3/projects/{project_id_encoded}/repository/files?file_path={file_path_encoded}&ref={commit_sha}"
    headers = {"Private-Token": os.getenv("GITLAB_TOKEN")}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f"Error fetching file {file_path}: {response.status_code} - {response.text}")
        return None

    return response.text


def analyze_code_with_ai(changes, commit_sha, project_id):
    """
    Generate AI feedback for the changed files.
    """
    GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

    if not AI_API_KEY or not GITLAB_TOKEN:
        raise ValueError("Required environment variables (AI_API_KEY, GITLAB_TOKEN) are not set.")

    feedback = []

    if not changes:
        logger.info("No file changes detected.")
        return feedback

    for file in changes:
        file_content = fetch_file_content(project_id, file, commit_sha)
        if not file_content:
            logger.warning(f"No content found for file {file}. Skipping...")
            continue

        # Template expects "filename" as the variable name
        template = """# noqa
        Your are expert in the python code reivew.

        Please make sure to check the   naming conventions of methods and variables
        Please check for proper indentations.
        Only provide the data required.
        Inpout : {filename}
    The final output should be in json format like this and don't add extra text, prefix or note in answer.
    {{ "reviews": [
        {{
            "reviews": ["All Generated reviews"],
        }}
    ]
    }}
    """
        prompt = PromptTemplate(template=template)

        llm = ChatOpenAI(model_name="gpt-4o-mini", verbose=False)
        dataquality_chain = prompt | llm

        try:
            # Pass "filename" as the input key to match the template
            response = dataquality_chain.invoke({"filename": file_content})  
            print("response", response)
            feedback_data = response["reviews"][0]["reviews"]
            print(feedback_data)
            feedback.append(feedback_data)
        except Exception as e:
            logger.error(f"Error processing AI feedback for {file}: {e}")
            feedback.append({
                "file": file,
                "issues": [{"type": "Error", "message": "Failed to parse AI response"}]
            })

    print("feedback", feedback)
    exit(1)
    return feedback
