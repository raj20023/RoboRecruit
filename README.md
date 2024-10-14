# Resume Analysis Application

This is a Streamlit application for analyzing resumes using GPT-4, providing recruitment support for technical and HR interview rounds.

## Features
- Upload a resume in PDF format.
- Analyze the resume for both technical and HR interview rounds.
- Calculate a resume score based on the job description and provide feedback.
- Identify mistakes in the resume and suggest improvements.

## Getting Started
### Prerequisites
To run this application, you need the following:
- Python 3.7 or above
- [Streamlit](https://streamlit.io/)
- [OpenAI API key](https://openai.com/)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/raj20023/RoboRecruit.git
   ```
2. Navigate to the project directory:
   ```bash
   cd RoboRecruit
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up your OpenAI credentials. Create a `credentials.json` file in the project directory with the following content:
   ```json
   {
     "OPEN_AI_KEY": "your_openai_api_key",
     "OPEN_AI_ORGANIZATION": "your_openai_organization_id"
   }
   ```

### Running the Application
To run the Streamlit app, use the following command:
```bash
streamlit run main.py
```
This will start the application and open it in your default web browser.

### File Structure
- `main.py`: The main file for running the Streamlit app.
- `utils.py`: Contains utility functions for handling resume uploads and GPT-4 interactions.
- `constants.py`: Defines constants used throughout the application, such as prompts, error messages, and allowed file types.

### Configuration
- **Upload Folder**: Uploaded resumes are stored in the `media` folder.
- **Allowed File Types**: Only PDF files are allowed for upload.
- **Prompts**: The application uses predefined prompts for analyzing resumes for technical and HR rounds.

## Usage
1. **Upload Resume**: Select a resume in PDF format from your computer.
2. **Enter Job Details**: Provide the job role and job description.
3. **Analyze Resume**: Click on "Analyze Resume" to get detailed feedback, resume score, and next steps.

## Error Handling
- **No File Uploaded**: Prompts the user to upload a resume.
- **Invalid PDF**: Prompts the user to upload a valid PDF file.
- **AI Failure**: Displays an error message when there is an issue connecting to the AI model.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)

## Contact
If you have any questions or issues, please feel free to contact the project maintainers.

Happy Resume Analyzing!