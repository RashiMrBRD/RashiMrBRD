import json
import random
import re
from datetime import datetime
from pathlib import Path

def load_songs():
    with open('songs.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_random_song(songs):
    # Get current hour to determine genre
    hour = datetime.now().hour
    
    if hour >= 0 and hour < 8:  # Midnight to 8AM: Lo-fi/Anime
        genre = 'anime'
    elif hour >= 8 and hour < 16:  # 8AM to 4PM: K-pop
        genre = 'kpop'
    else:  # 4PM to Midnight: OPM
        genre = 'opm'
    
    song = random.choice(songs[genre])
    return song['title'], song['artist'], genre

def update_badge(title, artist):
    profile_path = Path('profile.md')
    content = profile_path.read_text(encoding='utf-8')
    
    # Create new badge URL
    song_text = f"{title}-{artist}".replace(' ', '_')
    new_badge = f'<img src="https://img.shields.io/badge/Now_Playing-{song_text}-FF69B4?style=for-the-badge&logo=youtube-music&logoColor=white" alt="Now Playing"/>'
    
    # Update the badge in the profile
    pattern = r'<img src="https://img\.shields\.io/badge/Now_Playing-[^"]*" alt="Now Playing"/>'
    updated_content = re.sub(pattern, new_badge, content)
    
    # Update the "Now Playing" section in the ASCII art
    now_playing_pattern = r'(Now Playing:</span> 🎧 ")[^"]*(")'
    updated_content = re.sub(now_playing_pattern, f'\\1{title} ({artist})\\2', updated_content)
    
    profile_path.write_text(updated_content, encoding='utf-8')

def main():
    songs = load_songs()
    title, artist, _ = get_random_song(songs)
    update_badge(title, artist)

if __name__ == '__main__':
    main()
