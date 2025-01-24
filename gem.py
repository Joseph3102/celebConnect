import google.generativeai as genai1
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Configure the API with your key
genai1.configure(api_key=os.getenv('API_KEY'))

# Initialize the model (use the "gemini-1.5-flash" model or whichever is appropriate)
model = genai1.GenerativeModel("gemini-1.5-flash")

# System message to guide the model to respond in pirate speak
system_message = "You are a celeb/ figure connector chatbot. Respond only in chains of people that connect the two people that the user types up."



client = genai.Client(api_key=os.getenv('API_KEY'))

def generate_image(message_from_term):
    print("Available models:")
    for model_info in genai1.list_models():  
        print(model_info)
        # Use genai1.list_models()
        if 'generateImage' in model_info.supported_generation_methods:
            print(f"- {model_info.name}: {model_info.description}")
            print(f"  Supports generateImage")
    
    
    responseI = client.models.generate_image(
        model='gemini-2.0-flash-exp',
        prompt=message_from_term,
        config=types.GenerateImageConfig(
            negative_prompt= 'people',
            number_of_images= 1,
            include_rai_reason= True,
            output_mime_type= 'image/jpeg'
        )
    )

    return responseI.generated_images[0].image.show()
# Function to generate responses in pirate speak
def generate_response(user_message):
    # Combine the system message with the user's input to guide the model's response
    prompt = f"{system_message} User: {user_message} Response:"

    # Generate the response using the model
    response = model.generate_content(prompt)

    return response.text

# Example of interacting with the chatbot
if __name__ == "__main__":
    while True:
        # Get user input
        message = input("Type in two figures/celebrities (or type 'exit' to quit): ")
        
        if message.lower() == 'exit':
            print("Exiting the chat...")
            break
        else:
            responseI = generate_image(message)
        # Get the pirate response
        response = generate_response(message)
        
        # Print the pirate response
        print("Response:", response)
