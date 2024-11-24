import time
import yaml
import re
import openai
import os

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_skills_from_job(job_description, current_skills, max_retries=3, retry_delay=2):
    """
    Extract skills from a job description with a retry mechanism to handle API failures.
    
    Args:
        job_description (str): The job description.
        current_skills (dict): Current skills data to be passed to the model.
        max_retries (int): Maximum number of retries in case of failure.
        retry_delay (int): Time in seconds to wait before retrying.

    Returns:
        dict: Enhanced skills in structured format or an empty dictionary on failure.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            prompt = f"""
            Below is a list of skills grouped by categories. Restructure this list into
            a similar format, add any relevant missing skills, and ensure proper organization.

            Current Skills:
            {yaml.dump(current_skills)}
            
            Based on the following job description, extract the key technical and soft skills:
            
            {job_description}
            
            Format the response in YAML with categories like Programming Languages, AI/ML Frameworks, 
            AI Techniques, etc. Ensure it includes both the original and additional skills.
            """
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract raw content and YAML
            raw_content = response.choices[0].message.content
            match = re.search(r"```yaml\n(.*?)\n```", raw_content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                return yaml.safe_load(yaml_content)  # Parse YAML response into Python dictionary
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)  # Wait before retrying
            attempt += 1
    
    print(f"All {max_retries} attempts failed. Proceeding with default or empty skills.")
    return {"Skills": {}}  # Return an empty structure on failure
