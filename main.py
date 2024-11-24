import yaml
import argparse
from extract_skills import extract_skills_from_job
from generate_resume import generate_compact_resume
from docx_utils import update_resume_with_skills

def load_resume_skeleton(file_path="resume_skeleton.yaml"):
    """Load the resume skeleton from a YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a resume based on a job description.")
    parser.add_argument(
        "-j", "--job_description",
        type=str,
        required=True,
        help="Job description to enhance resume skills."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="enhanced_resume.docx",
        help="Output file name for the generated resume."
    )
    parser.add_argument(
        "--generate_pdf",
        action="store_true",
        help="Generate a PDF version of the resume."
    )
    args = parser.parse_args()

    # Step 1: Load Resume Skeleton
    resume_skeleton = load_resume_skeleton()

    # Step 2: Extract and Enhance Skills
    current_skills = resume_skeleton["skills"]
    enhanced_skills = extract_skills_from_job(args.job_description, current_skills)

    # Step 3: Update Resume Skeleton with Enhanced Skills
    updated_resume = update_resume_with_skills(resume_skeleton, enhanced_skills)

    # Step 4: Generate Resume
    generate_compact_resume(updated_resume, output_file=args.output, generate_pdf=args.generate_pdf)

if __name__ == "__main__":
    main()
