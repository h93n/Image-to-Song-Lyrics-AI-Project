from transformers import pipeline, AutoProcessor, AutoModel
from langchain import PromptTemplate, OpenAI, LLMChain
import random
from gtts import gTTS
import pygame
from PIL import Image

def image2text(file_path):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    with open(file_path, "rb") as image_file:
        image = Image.open(image_file)
        captions = image_to_text(image)
    text = captions[0]["generated_text"]  # Access the correct key 'generated_text'
    return text

def image2lyrics(path):
# the path to image file
    image_file_path = path
    captured_text = image2text(image_file_path)

    # Define the prompt template for generating a song
    prompt_template = "I wrote a song about {topic}. It goes like this:\n\n{lyrics}\n\nI hope you like it!"
    # Initialize the OpenAI model with your API key
    llm = OpenAI(openai_api_key=API_KEY,
                 temperature=0)  # Replace with your actual API key
    # Initialize the LLMChain with the prompt template
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )
    # Generate a song based on the text extracted from the image
    # List of alternative lyrics
    alternative_lyrics = [
        "This is a song of life and dreams,\n"
        "Where laughter flows in gentle streams.\n"
        "From sunrise glow to starry night,\n"
        "We dance through time in pure delight.\n\n"
        "Chorus:\n"
        "Winds of change, a constant flow,\n"
        "In every heart, stories to sow.\n"
        "Let's embrace the unknown's call,\n"
        "Together we rise, stand tall.\n",
        "In a world of colors, vibrant and bold,\n"
        "A story of courage, forever untold.\n"
        "From mountains high to oceans wide,\n"
        "We journey together, side by side.\n\n"
        "Chorus:\n"
        "In unity's embrace, we find our way,\n"
        "Through night and day, come what may.\n"
        "With hope as our guide, we'll find the light,\n"
        "Together we'll conquer any fight.\n"
        "Beneath the stars, in the moonlit night,\n"
        "Whispers of dreams take their flight.\n"
        "Through galaxies and realms unknown,\n"
        "A symphony of wonder is softly shown.\n\n"
        "Chorus:\n"
        "Bound by the cosmos, we'll forever roam,\n"
        "Exploring mysteries, making a universe our own.\n"
        "Eternal voyagers, our hearts unite,\n"
        "In the endless journey of starry night.\n",
        "From city lights to tranquil seas,\n"
        "Life's vibrant tapestry unfolds with ease.\n"
        "A harmony of souls, diverse and grand,\n"
        "Together we create on this wondrous land.\n\n"
        "Chorus:\n"
        "Hand in hand, we paint the sky,\n"
        "Colors of hope that never shy.\n"
        "Unity's embrace, a bridge to connect,\n"
        "In this world of ours, love and respect.\n",
        "Amidst the chaos, a single voice,\n"
        "A beacon of truth, a conscious choice.\n"
        "In words that echo through time and space,\n"
        "A song of wisdom, a relentless embrace.\n\n"
        "Chorus:\n"
        "The power of change, a force so bold,\n"
        "In hearts united, the story is told.\n"
        "With courage and grace, we'll pave the way,\n"
        "In the tapestry of life, a brighter day.\n"
    ]
    # Select a random lyrics version
    selected_lyrics = random.choice(alternative_lyrics)
    generated_song = llm_chain({
        "topic": captured_text,
        "lyrics": selected_lyrics
    })

# Extract and format the text result
    song_text = generated_song["text"]
    song_text1 = song_text.replace("Chorus:", "")
    song_text1 = song_text1.replace("Bridge:", "")
    song_text1 = song_text1.replace("Verse 2:", "")

    return song_text1

def text2audio(song_text):
    # Text2Speech generation
    text = song_text
    tts = gTTS(text, lang='en')
    # Save converted audio as mp3 format
    tts.save('hello.mp3')

def play_mp3(mp3_file):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


if __name__ == '__main__':
    song_text = image2lyrics()
    print(song_text)
    text2audio(song_text)
    mp3_file_path = 'hello.mp3'
    play_mp3(mp3_file_path)

