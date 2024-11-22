# import streamlit as st
# import PyPDF2
# import openai
# import os
# import json

# # Set up OpenAI API Key
# openai.api_key = "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"  # Replace with your API key or set as an environment variable

# def extract_text_from_pdf(pdf_file):
#     """
#     Extract text from a PDF file.
#     """
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text
#     return text

# def generate_mcqs_from_text(text, num_questions=5):
#     """
#     Generate MCQs using OpenAI GPT API.
#     """
#     # Optional: Summarize the text if it's too long
#     if len(text) > 2000:  # Adjust the threshold as needed
#         text = summarize_text(text)

#     prompt = f"""
# Generate {num_questions} multiple-choice questions based on the following text.
# Each question should have:
# - Four options.
# - Indicate the correct answer.

# The output format should be JSON with the following structure:
# [
#     {{
#         "question": "Question text",
#         "options": ["Option A", "Option B", "Option C", "Option D"],
#         "answer": "Option A"
#     }},
#     ...
# ]

# Ensure the output is valid JSON and does not include any additional text.

# Text: {text}
# """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=1500,  # Adjust max tokens as needed
#             temperature=0.7,
#         )
#         mcqs_json = response["choices"][0]["message"]["content"].strip()
#         # Load the JSON string into a Python object
#         mcqs = json.loads(mcqs_json)
#         return mcqs
#     except Exception as e:
#         st.error(f"Error generating questions: {e}")
#         return []

# def summarize_text(text):
#     """
#     Summarize the text to reduce token usage.
#     """
#     prompt = f"Summarize the following text:\n\n{text}"
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=500,
#             temperature=0.5,
#         )
#         summary = response["choices"][0]["message"]["content"].strip()
#         return summary
#     except Exception as e:
#         return text  # Return original text if summarization fails

# def main():
#     st.title("PDF to MCQ Quiz Generator")
#     st.write("Upload a PDF file to generate a multiple-choice quiz.")

#     if 'mcqs' not in st.session_state:
#         st.session_state.mcqs = None
#     if 'user_answers' not in st.session_state:
#         st.session_state.user_answers = {}

#     uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
#     num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)

#     if uploaded_file and st.button("Generate Quiz"):
#         st.write("Processing your PDF...")
#         text = extract_text_from_pdf(uploaded_file)

#         if len(text.strip()) == 0:
#             st.error("The uploaded PDF contains no extractable text.")
#             return

#         st.write("Generating questions...")
#         mcqs = generate_mcqs_from_text(text, num_questions)
#         if mcqs:
#             st.success("Quiz generated!")
#             st.session_state.mcqs = mcqs
#             st.session_state.user_answers = {}  # Reset user answers
#         else:
#             st.error("No questions were generated. Please try again.")

#     if st.session_state.mcqs:
#         mcqs = st.session_state.mcqs
#         st.write("### Quiz:")
#         with st.form(key='quiz_form'):
#             for idx, mcq in enumerate(mcqs):
#                 st.write(f"**Question {idx + 1}: {mcq['question']}**")
#                 options = mcq['options']
#                 # Add a placeholder option
#                 options_with_placeholder = ["Select an answer"] + options

#                 # Retrieve previous answer if any
#                 prev_answer = st.session_state.user_answers.get(idx, "Select an answer")

#                 # Create a selectbox for each question
#                 user_choice = st.selectbox(
#                     label="",
#                     options=options_with_placeholder,
#                     index=options_with_placeholder.index(prev_answer) if prev_answer in options_with_placeholder else 0,
#                     key=f"question_{idx}"
#                 )
#                 # Store the user's choice if they selected an option
#                 st.session_state.user_answers[idx] = user_choice if user_choice != "Select an answer" else None
#                 st.write("")  # Add space between questions

#             # Submit button
#             submit_button = st.form_submit_button(label='Submit')

#         if submit_button:
#             st.write("---")
#             st.write("### Results:")
#             correct_count = 0
#             unanswered = 0
#             for idx, mcq in enumerate(mcqs):
#                 correct_answer = mcq['answer']
#                 user_answer = st.session_state.user_answers.get(idx)
#                 if user_answer is None:
#                     st.write(f"**Question {idx + 1}: {mcq['question']}**")
#                     st.warning("You did not select an answer for this question.")
#                     st.write(f"- Correct answer: **{correct_answer}**")
#                     unanswered += 1
#                 else:
#                     is_correct = user_answer == correct_answer
#                     if is_correct:
#                         correct_count += 1
#                     st.write(f"**Question {idx + 1}: {mcq['question']}**")
#                     st.write(f"- Your answer: **{user_answer}**")
#                     st.write(f"- Correct answer: **{correct_answer}**")
#                     if is_correct:
#                         st.success("Correct!")
#                     else:
#                         st.error("Incorrect.")
#                 st.write("")  # Add space between results

#             total_answered = len(mcqs) - unanswered
#             st.write(f"### You got {correct_count} out of {len(mcqs)} questions correct.")
#             if unanswered > 0:
#                 st.warning(f"You did not answer {unanswered} question(s).")

#     else:
#         st.info("Please upload a PDF file and click 'Generate Quiz' to get started.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import PyPDF2
import openai
import os
import json

# Set up OpenAI API Key
openai.api_key = "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"  # Replace with your API key or set as an environment variable

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def generate_mcqs_from_text(text, num_questions=5):
    """
    Generate MCQs using OpenAI GPT API.
    """
    # Optional: Summarize the text if it's too long
    if len(text) > 2000:  # Adjust the threshold as needed
        text = summarize_text(text)

    prompt = f"""
Generate {num_questions} multiple-choice questions based on the following text.
Each question should have:
- Four options.
- Indicate the correct answer.

The output format should be JSON with the following structure:
[
    {{
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Option A"
    }},
    ...
]

Ensure the output is valid JSON and does not include any additional text.

Text: {text}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,  # Adjust max tokens as needed
            temperature=0.7,
        )
        mcqs_json = response["choices"][0]["message"]["content"].strip()
        # Load the JSON string into a Python object
        mcqs = json.loads(mcqs_json)
        return mcqs
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

def summarize_text(text):
    """
    Summarize the text to reduce token usage.
    """
    prompt = f"Summarize the following text:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        return text  # Return original text if summarization fails

def main():
    st.title("PDF to MCQ Quiz Generator")
    st.write("Upload a PDF file to generate a multiple-choice quiz.")

    if 'mcqs' not in st.session_state:
        st.session_state.mcqs = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)

    if uploaded_file and st.button("Generate Quiz"):
        st.write("Processing your PDF...")
        text = extract_text_from_pdf(uploaded_file)

        if len(text.strip()) == 0:
            st.error("The uploaded PDF contains no extractable text.")
            return

        st.write("Generating questions...")
        mcqs = generate_mcqs_from_text(text, num_questions)
        if mcqs:
            st.success("Quiz generated!")
            st.session_state.mcqs = mcqs
            st.session_state.user_answers = {}  # Reset user answers
            st.session_state.quiz_submitted = False  # Reset quiz submission status
        else:
            st.error("No questions were generated. Please try again.")

    if st.session_state.mcqs:
        mcqs = st.session_state.mcqs
        st.write("### Quiz:")
        with st.form(key='quiz_form'):
            for idx, mcq in enumerate(mcqs):
                st.write(f"**Question {idx + 1}: {mcq['question']}**")
                options = mcq['options']
                # Add a placeholder option
                options_with_placeholder = ["Select an answer"] + options

                # Retrieve previous answer if any
                prev_answer = st.session_state.user_answers.get(idx, "Select an answer")

                # Determine if the radio buttons should be disabled
                disabled = st.session_state.quiz_submitted

                # Create a radio button for each question
                user_choice = st.radio(
                    label="",
                    options=options_with_placeholder,
                    index=options_with_placeholder.index(prev_answer) if prev_answer in options_with_placeholder else 0,
                    key=f"question_{idx}",
                    disabled=disabled
                )
                if not st.session_state.quiz_submitted:
                    # Store the user's choice if they selected an option
                    st.session_state.user_answers[idx] = user_choice if user_choice != "Select an answer" else None
                st.write("")  # Add space between questions

            # Submit button
            submit_button = st.form_submit_button(label='Submit')

            if submit_button and not st.session_state.quiz_submitted:
                st.session_state.quiz_submitted = True
                st.write("---")
                st.write("### Results:")
                correct_count = 0
                unanswered = 0
                for idx, mcq in enumerate(mcqs):
                    correct_answer = mcq['answer']
                    user_answer = st.session_state.user_answers.get(idx)
                    if user_answer is None:
                        st.write(f"**Question {idx + 1}: {mcq['question']}**")
                        st.warning("You did not select an answer for this question.")
                        st.write(f"- Correct answer: **{correct_answer}**")
                        unanswered += 1
                    else:
                        is_correct = user_answer == correct_answer
                        if is_correct:
                            correct_count += 1
                        st.write(f"**Question {idx + 1}: {mcq['question']}**")
                        st.write(f"- Your answer: **{user_answer}**")
                        st.write(f"- Correct answer: **{correct_answer}**")
                        if is_correct:
                            st.success("Correct!")
                        else:
                            st.error("Incorrect.")
                    st.write("")  # Add space between results

                total_answered = len(mcqs) - unanswered
                st.write(f"### You got {correct_count} out of {len(mcqs)} questions correct.")
                if unanswered > 0:
                    st.warning(f"You did not answer {unanswered} question(s).")

    else:
        st.info("Please upload a PDF file and click 'Generate Quiz' to get started.")

if __name__ == "__main__":
    main()
