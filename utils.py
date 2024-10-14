from pypdf import PdfReader
import openai
from datetime import date
import markdown2
import os
import json

from constants import (
    SYSTEM_PROMPT,
    PROMPT_SWITCHER,
    OPEN_AI,
    OPEN_AI_ORGANIZATION,
    COMPLETIONS_TOKEN,
    CHATGPT_TOP_P,
    CHATGPT_FREQ_PENALTY,
    CHATGPT_PRE_PENALTY,
    ALLOWED_EXTENSIONS,
    AI_FAILED_ERROR,
    WRONG_PDF_ERROR,
)


class Utils:
    def __init__(self) -> None:
        try:
            self.env = os.environ.get("ENV", "local").lower()
        except:
            self.env = "local"

        if self.env == "prod":
            openai.api_key = os.environ.get(OPEN_AI)
            openai.organization = os.environ.get(OPEN_AI_ORGANIZATION)
        else:
            with open("credentials.json", "r") as file:
                credentials = json.load(file)
            openai.api_key = credentials.get(OPEN_AI)
            openai.organization = credentials.get(OPEN_AI_ORGANIZATION)

    def read_cv(self, filepath, interview_type):
        """Reads the content of a CV from a PDF file.

        Args:
            filepath (str): The file path of the PDF file to be read.
            interview_type (str): The type of interview.

        Returns:
            tuple: A tuple containing the human prompt generated based on the CV content and a boolean indicating success or failure.
        """
        try:
            reader = PdfReader(filepath)
            text = "\n".join(page.extract_text() for page in reader.pages)
            prompt = PROMPT_SWITCHER[interview_type].format(resume=text)
            return prompt, False
        except Exception as error:
            print("Error in PDF reading: ", error)
            return WRONG_PDF_ERROR, True

    def get_parsed_gpt_response(self, filepath, interview_type, job_description, job_role):
        """Retrieve parsed response from GPT model.

        Args:
            filepath (str): The file path to read chat template from.
            interview_type (str): The type of interview.
            job_description (str): The job description.
            job_role (str): The job role.

        Returns:
            tuple: A tuple containing the response and error flag.
        """
        chat_human_template, error_flag = self.read_cv(filepath, interview_type)
        if error_flag:
            return chat_human_template, error_flag

        try:
            completions = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT.format(
                            date_today=date.today(),
                            job_role=job_role,
                            job_description=job_description,
                        ),
                    },
                    {"role": "user", "content": chat_human_template},
                ],
                max_tokens=COMPLETIONS_TOKEN,
                temperature=0,
                top_p=CHATGPT_TOP_P,
                frequency_penalty=CHATGPT_FREQ_PENALTY,
                presence_penalty=CHATGPT_PRE_PENALTY,
            )

            chatgpt_response = completions.choices[0].message.content
            print(
                "Total cost of analysis of this response: ",
                (
                    completions.usage.prompt_tokens * 0.0000005
                    + completions.usage.completion_tokens * 0.0000015
                ) * 151.70,
            )
            response = {"response": self.format_markdown_to_html(chatgpt_response)}

        except Exception as error:
            print("Error in ChatGPT call: ", error)
            error_flag = True
            response = AI_FAILED_ERROR

        return response, error_flag

    def allowed_file(self, filename):
        """Check if the given filename is allowed based on the file extension.

        Args:
            filename (str): The name of the file to be checked.

        Returns:
            bool: True if the file extension is allowed, False otherwise.
        """
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def format_markdown_to_html(self, markdown_data):
        """Format markdown data to HTML.

        Args:
            markdown_data (str): The markdown data to be formatted.

        Returns:
            str: The formatted HTML string.
        """
        try:
            total_lines = markdown_data.splitlines()
            main_string = ""
            flag = False

            for i in total_lines:
                if "```" in i:
                    if flag:
                        main_string += "</code></pre>\n"
                        flag = False
                    else:
                        main_string += "<pre><code>"
                        flag = True
                else:
                    if flag:
                        main_string += i + "\n"
                    else:
                        main_string += markdown2.markdown(i)

        except Exception as error:
            print("Found error while converting markdown to html: ", error)
            return ""

        return main_string