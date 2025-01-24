import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure APIs
genai.configure(api_key=os.getenv('API_KEY'))  # Google Generative AI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')  # OpenAI API Key

# Initialize the Generative AI model
model = genai.GenerativeModel("gemini-1.5-flash")

# System message for the chatbot
system_message = (
    "You are a celeb/figure connecting chatbot. Respond by giving a chain of people to "
    "connect the two celebrities/figures the user enters."
)

# Function to generate a chatbot response
def generate_chatbot_response(user_message):
    try:
        prompt = f"{system_message} User: {user_message} Response:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating chatbot response: {str(e)}"

# Function to generate an image using the new OpenAI API
def generate_image(prompt):
    try:
        response = openai.Image.create_edit(
            prompt=prompt,  # The text prompt for the image
            n=1,  # Number of images to generate
            size="1024x1024"  # Image resolution
        )
        return response['data'][0]['url']  # URL of the generated image
    except Exception as e:
        return f"Error generating image: {str(e)}"

# Main chatbot loop
if __name__ == "__main__":
    while True:
        # Get user input
        user_message = input("Enter your message (or type 'exit' to quit): ")
        
        if user_message.lower() == 'exit':
            print("Exiting the chat...")
            break
        
        # Generate and display the chatbot response
        chatbot_response = generate_chatbot_response(user_message)
        print("\nChatbot Response:", chatbot_response)
        
        # Generate and display the image URL
        image_url = generate_image(user_message)
        print("Generated Image URL:", image_url)
        print("\n")
