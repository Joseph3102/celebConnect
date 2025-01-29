import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

# Configure APIs
genai.configure(api_key=os.getenv('API_KEY'))  # Google Generative AI API Key
API_KEY = os.getenv('OPENAI_API_KEY')  # OpenAI API Key
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')  # YouTube API Key

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

# Function to search for YouTube videos
def search_youtube_videos(query):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return "No videos found."
    except Exception as e:
        return f"Error fetching YouTube video: {str(e)}"

if __name__ == "__main__":
    while True:
        # Get user input
        user_message = input("Enter your message (or type 'exit' to quit): ")
        
        if user_message.lower() == 'exit':
            print("Exiting the chat...")
            break
        
        # Generate chatbot response
        chatbot_response = generate_chatbot_response(user_message)
        print("\nChatbot Response:", chatbot_response)
        
        # Search for YouTube video
        video_url = search_youtube_videos(user_message)
        print("\nYouTube Video URL:", video_url)
        print("\n")
