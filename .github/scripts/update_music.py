import os
import re
import random

# Combined playlist with both anime and K-pop songs
PLAYLIST = [
    # Anime songs
    ("Unravel", "Tokyo Ghoul"),
    ("Blue Bird", "Naruto Shippuden"),
    ("Again", "Fullmetal Alchemist: Brotherhood"),
    ("The Hero", "One Punch Man"),
    ("Gurenge", "Demon Slayer"),
    ("A Cruel Angel's Thesis", "Neon Genesis Evangelion"),
    ("Silhouette", "Naruto Shippuden"),
    ("Black Catcher", "Black Clover"),
    ("Kaikai Kitan", "Jujutsu Kaisen"),
    # K-pop songs
    ("Dynamite", "BTS"),
    ("Butter", "BTS"),
    ("Boy With Luv", "BTS"),
    ("Spring Day", "BTS"),
    ("DNA", "BTS"),
    ("Blood Sweat & Tears", "BTS"),
    ("Black Swan", "BTS"),
    ("Life Goes On", "BTS"),
    ("Permission to Dance", "BTS")
]

def get_current_song():
    # Get a random song from the playlist
    return random.choice(PLAYLIST)

def create_badge(song, artist):
    # Create the badge URL with proper URL encoding
    text = f"Now Playing-{song} by {artist}"
    encoded_text = text.replace(" ", "%20").replace("&", "%26")
    return f"https://img.shields.io/badge/{encoded_text}-FF69B4?style=for-the-badge&logo=youtube-music&logoColor=white"

def update_readme():
    # Read the current README.md
    readme_path = os.path.join(os.getcwd(), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Get current song
    song, artist = get_current_song()
    badge_url = create_badge(song, artist)
    new_badge = f'<img src="{badge_url}" alt="{song} by {artist}"/>'
    
    # Find and replace the existing Now Playing badge
    pattern = r'<img src="https://img\.shields\.io/badge/Now%20Playing[^>]+?/>'
    if re.search(pattern, content):
        content = re.sub(pattern, new_badge, content)
    
    # Write the updated content back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
