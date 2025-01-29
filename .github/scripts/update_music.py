import os
import re
import random

# Sample playlist - you can modify this or integrate with a real music API
ANIME_PLAYLIST = [
    ("Unravel", "Tokyo Ghoul"),
    ("Blue Bird", "Naruto Shippuden"),
    ("Again", "Fullmetal Alchemist: Brotherhood"),
    ("The Hero", "One Punch Man"),
    ("Gurenge", "Demon Slayer"),
    ("A Cruel Angel's Thesis", "Neon Genesis Evangelion"),
    ("Silhouette", "Naruto Shippuden"),
    ("Black Catcher", "Black Clover"),
    ("Kaikai Kitan", "Jujutsu Kaisen")
]

def get_current_song():
    # Get a random song
    return random.choice(ANIME_PLAYLIST)

def create_badge(song, anime):
    # Create the badge URL with proper URL encoding
    text = f"Now Playing-{song} by {anime}"
    encoded_text = text.replace(" ", "%20")
    return f"https://img.shields.io/badge/{encoded_text}-FF69B4?style=for-the-badge&logo=youtube-music&logoColor=white"

def update_readme():
    # Read the current README.md
    readme_path = os.path.join(os.getcwd(), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.readlines()

    # Get current song
    song, anime = get_current_song()
    new_badge = f'<img src="{create_badge(song, anime)}" alt="{song} by {anime}"/>\n'

    # Find and update the Now Playing badge in the music preferences section
    # We'll look for a line containing "Now Playing" after a line containing "Music Preferences"
    music_prefs_found = False
    for i, line in enumerate(content):
        if "Music Preferences" in line:
            music_prefs_found = True
        elif music_prefs_found and "Now Playing" in line:
            content[i] = new_badge
            break

    # Write the updated content back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(content)

if __name__ == "__main__":
    update_readme()
