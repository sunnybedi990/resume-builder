# Resume Builder

This project provides a modular approach to creating a professional resume using Python and `python-docx`. It supports enhancing skills based on job descriptions using OpenAI's API, organizing them into categories, and generating a polished `.docx` or `.pdf` resume document.

---

## Features

- **Skill Enhancement**: Extracts and enhances skills based on a provided job description.
- **Customizable Resume**: Uses a YAML skeleton file for customizable sections.
- **Compact Formatting**: Generates a Word document with professional formatting, including hyperlinks and section-specific designs.
- **PDF Export**: Optionally convert the `.docx` resume to `.pdf` format using **ReportLab**.
- **Flexible CLI Usage**: Accepts job descriptions and other options via command-line arguments for dynamic resume generation.

---

## Project Structure

```plaintext
resume_builder/
├── main.py                     # Entry point for the application
├── extract_skills.py           # Logic for extracting and enhancing skills
├── docx_utils.py               # Utility functions for Word document formatting
├── generate_resume.py          # Logic for generating the resume
├── generate_pdfs.py            # PDF generation logic using ReportLab
├── resume_skeleton_example.yaml # Example YAML file for the resume skeleton
├── requirements.txt            # Required Python libraries
└── README.md                   # Instructions for using the application
```

---

## Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/resume-builder.git
cd resume-builder
```

### **2. Install Dependencies**
Ensure you have Python 3.8+ installed. Install required libraries using:
```bash
pip install -r requirements.txt
```

---

### PDF Generation Setup

PDF generation is handled using **ReportLab**, which is already included in the dependencies. No additional external tools like Pandoc or pdflatex are required.

---

## Usage

### 1. **Prepare the YAML Skeleton**:
   - Locate the `resume_skeleton_example.yaml` file in the project directory.
   - Update it with your personal details, education, experience, projects, and skills.
   - Rename it to `resume_skeleton.yaml`:
     ```bash
     mv resume_skeleton_example.yaml resume_skeleton.yaml
     ```

### 2. **Run the Application Using Command-Line Arguments**:

   - Use the following arguments to generate the resume:
     - `-j/--job_description`: Provide the job description as a string.
     - `-o/--output`: Specify the output file name for the generated resume (default is `enhanced_resume.docx`).
     - `--generate_pdf`: Include this flag to generate a PDF version of the resume.

   #### Example Usage:
   - Generate a resume with a job description:
     ```bash
     python main.py -j "We need a Data Scientist with Python, SQL, and Machine Learning skills." --generate_pdf
     ```
   - Specify a custom output file name:
     ```bash
     python main.py -j "Looking for an ML Engineer with experience in PyTorch and AWS." -o "custom_resume.docx" --generate_pdf
     ```

### 3. **Output**:
   - The generated resume will be saved in the project directory as a `.docx` file.
   - If the `--generate_pdf` flag is used, a corresponding `.pdf` file will also be created.

---

## Contributing

Feel free to fork this repository and contribute by submitting a pull request. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

This project is licensed under the MIT License.