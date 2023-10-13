import random
import time
import pyperclip
import pyautogui
from googleapiclient.discovery import build
from decouple import config

### ADD YOUR API KEY ###
api_key = config('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

### CHANGE THIS ###
search_query = 'NCT Music Video'
video_ids_cache = []
last_update_time = 0
CACHE_DURATION = 5 * 60  # 5 minutes in seconds

def get_random_video_url():
    global video_ids_cache
    global last_update_time

    # If the cache has expired or is empty, update the cache
    if not video_ids_cache or time.time() - last_update_time > CACHE_DURATION:
        search_response = youtube.search().list(
            q=search_query,
            type='video',
            part='id',
            maxResults=50
        ).execute()

        video_ids_cache = [item['id']['videoId'] for item in search_response.get('items', [])]

        last_update_time = time.time()

    # Select a random video ID from the cache
    random_video_id = random.choice(video_ids_cache)

    return f'https://www.youtube.com/watch?v={random_video_id}'

if __name__ == '__main__':
    clipboard_content = ''

    while True:
        video_url = get_random_video_url()

        while video_url == clipboard_content:
            video_url = get_random_video_url()

        print(f"New URL: {video_url}")

        if video_url:
            pyperclip.copy(video_url)
            clipboard_content = video_url
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
        
        time.sleep(1)
