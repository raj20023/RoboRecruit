import streamlit as st
import os
from constants import UPLOAD_FOLDER, NO_FILE_ERROR
from utils import Utils
from werkzeug.utils import secure_filename

# Initialize Utils object
utils = Utils()

# Custom CSS to style the Streamlit interface
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f7f7f7;
        color: #333;
    }
    
    header {
        background-color: #2c3e50;
        padding: 20px 40px; /* Add padding around the header */
        color: #fff;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        height: auto;
        display: flex;
        align-items: center; /* Vertically align items */
        justify-content: center; /* Center title */
    }

    header img.robot-icon {
        width: 80px;
        margin-right: auto; /* Move the logo to the left */
        margin-top: 50px;
    }

    header h1 {
        font-size: 36px;
        font-weight: bold;
        margin-top: 50px;
    }

    .container {
        text-align: center;
        padding: 0px;
        background-color: #333;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        margin: 60px auto 0;
        max-width: 10px;
    }
    
    .upload-label {
        display: inline-block;
        padding: 10px 20px;
        background-color: #3498db;
        color: #fff;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }

    .upload-label:hover {
        background-color: #2980b9;
    }
    
    footer {
        background-color: #2c3e50;
        padding: 20px 0;
        text-align: center;
        color: #fff;
        width: 100%;
        position: fixed;
        bottom: 0;
        left: 0;
    }
    
    footer p {
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Streamlit app layout
def main():
    # Full-width header with centered content and logo aligned left
    st.markdown(
        """
        <header>
            <img class='robot-icon' src='https://img.icons8.com/color/96/000000/robot-2.png' alt='Robot Icon'/>
            <h1>RoboRecruit</h1>
        </header>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("## Upload Your Resume", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose your resume", type=["pdf"])

    # Dropdown for interview type and difficulty level
    # interview_type = st.selectbox(
    #     "Select Interview Type",
    #     ["Technical interview round", "HR interview round"],
    # )
    interview_type = "Technical interview round"

    job_role = st.text_input(
        "Job Role", placeholder="Enter the job role that you are looking for..."
    )

    # Text area for job description
    job_description = st.text_area(
        "Job Description", placeholder="Enter the detailed job description here..."
    )

    if uploaded_file is not None:
        filename = secure_filename(uploaded_file.name)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Uploaded {filename} successfully!")

        # Process the file using GPT
        if st.button("Analyze Resume"):
            resume_data, error_flag = utils.get_parsed_gpt_response(
                filepath, interview_type, job_description, job_role
            )
            if error_flag:
                st.error(resume_data["error_message"])
            else:
                # Display resume analysis result
                st.markdown(f"### Resume Analysis for {filename}")
                st.markdown(resume_data["response"], unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Full-width footer
    st.markdown(
        "<footer><p>© 2024 RoboRecruit. All rights reserved By COE-AI.</p></footer>",
        unsafe_allow_html=True,
    )


# Run the Streamlit app
if __name__ == "__main__":
    main()
