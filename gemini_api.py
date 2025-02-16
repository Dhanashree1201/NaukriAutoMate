import os
from google import genai
from dotenv import load_dotenv
from helper import extract_text_from_pdf


# Load environment variables from the .env file
def load_environment_variables():
    """Load environment variables from .env file."""
    load_dotenv()


def get_google_api_key() -> str:
    """Retrieve the Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
    return api_key


def configure_google_ai(api_key: str):
    """Configure Google Generative AI with the API key."""
    genai.configure(api_key=api_key)


def get_model_configuration() -> dict:
    """Return the configuration settings for the generative model."""
    return {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1000,
        "response_mime_type": "text/plain",
    }


def create_model(generation_config: dict):
    """Create and return the generative model with system instructions."""
    # Adjusted for potential API changes; use Model class instead of GenerativeModel
    return genai.Model(
        model_name="gemini-1.5-flash",  # Ensure this is the correct model
        generation_config=generation_config,
        system_instruction=""" Answer questions based on the provided unformatted resume text. If the exact information isn't provided, infer relevant details based on similar technologies or concepts mentioned in the text. Keep answers relevant and concise. For multi-option questions, provide only the index number of the correct answer.
            Additional preferences:
            - Experience: 10 years and 6 months (10.6 years) in all relevant technologies. Please reflect this as the total experience everywhere (including CSS frameworks, JS libraries, etc.).
            - Expertise in JavaScript and TypeScript, with similar experience in all related technologies.
            - Current salary: 33,00,000 PA, Expected salary: 45,00,000 PA.
            - Notice period: 15 days.
            - Last CGPA: 8.6.
            - Preferred location: Pune.
        """
    )


def start_chat_with_resume(resume_text: str, model):
    """Start a chat session with the provided resume text."""
    return model.start_chat(
        history=[{
            "role": "user",
            "parts": [
                f"Here is the resume text:\n{resume_text}\nAnswer the following questions based on this text. Be concise in your responses, using 1 to 5 words."
            ],
        },
            {
            "role": "model",
            "parts": [
                "I have understood the provided resume text. I will now answer questions based on this data."
            ],
        }]
    )


def bard_flash_response(question: str, chat_session) -> str:
    """Send a question to the chat session and return the response."""
    try:
        response = chat_session.send_message(question)
        return response.text
    except Exception as e:
        print(f"An error occurred while processing the question: {e}")
        return "Error in response."


def main(pdf_path: str):
    """Main function to load the resume, configure the API, and handle questions."""
    try:
        load_environment_variables()

        # Step 1: Load the API key
        api_key = get_google_api_key()

        # Step 2: Configure Google AI
        configure_google_ai(api_key)

        # Step 3: Get the model configuration
        generation_config = get_model_configuration()

        # Step 4: Create the generative model
        model = create_model(generation_config)

        # Step 5: Extract text from the provided PDF resume
        resume_text = extract_text_from_pdf()

        # Step 6: Start chat with resume text
        chat_session = start_chat_with_resume(resume_text, model)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
