import openai
import app.config.git_config as config

def analyze_code_with_ai(changes):
    """
    Generate AI feedback for the changed files.
    """
    openai.api_key = config.AI_API_KEY
    feedback = {}

    for file in changes:
        # Simulate fetching file content (In a real case, use GitLab API to fetch content)
        file_content = f"Simulated content of {file}"  # Replace with real content fetch
        prompt = f"Review the following code for best practices:\n\n{file_content}"

        response = openai.Completion.create(
            model="gpt-4o-mini",
            prompt=prompt,
            max_tokens=500
        )
        feedback[file] = response['choices'][0]['text'].strip()
    print(feedback)

    return feedback
