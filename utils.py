from pypdf import PdfReader
import openai
from datetime import date
import markdown2
import os
import json

from constants import (
    SYSTEM_PROMPT,
    PROMPT_SWITCHER,
    LEVELS_SWITCHER,
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
            self.env = os.environ.get("ENV").lower()
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
            level (int): The level of the CV.

        Returns:
            tuple: A tuple containing the human prompt generated based on the CV content and a boolean indicating success or failure.
        """
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += "\n" + page.extract_text()
            prompt = PROMPT_SWITCHER[interview_type].format(
                resume=text
            )
            return prompt, False
        except Exception as error:
            print("Error in PDF reading: ", error)
            return WRONG_PDF_ERROR, True

    def get_parsed_gpt_response(
        self, filepath, interview_type, job_description, job_role
    ):
        """Retrieve parsed response from GPT model.

        Args:
            filepath (str): The file path to read chat template from.
            level (int): The level of chat template to read.

        Returns:
            tuple: A tuple containing the response and error flag.
        """
        chat_human_template, error_flag = self.read_cv(
            filepath, interview_type
        )
        if error_flag:
            return chat_human_template, error_flag

        today_date = date.today()
        try:
            completions = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT.format(
                            date_today=today_date,
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
                )
                * 151.70,
            )
            mark_data = self.format_markdown_to_html(chatgpt_response)
            response = {"response": mark_data}

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
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def format_markdown_to_html(self, markdown_data):
        """Format markdown data to HTML.

        Args:
            markdown_data (str): The markdown data to be formatted.

        Returns:
            str: The formatted HTML string.
        """
        total_lines = markdown_data.splitlines()
        main_string = ""

        try:
            flag = False
            code_end = False

            for i in total_lines:
                if flag and "```" in i:
                    sub_string = "</code></pre>\n"
                    flag = False
                    code_end = True
                elif "```" in i:
                    flag = True
                    i = "<pre><code>"
                if flag:
                    sub_string = i + "\n"
                elif not code_end:
                    sub_string = markdown2.markdown(i)
                main_string += sub_string
                code_end = False

        except Exception as error:
            print("Found error while converting markdown to html: ", error)

        return main_string
