"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    # Adversarial profiles built to confuse the scoring rule
    "Conflicting: sad but high energy": {"genre": "folk", "mood": "sad", "energy": 0.90, "likes_acoustic": True},
    "Missing genre and mood: classical": {"genre": "opera", "mood": "serene", "energy": 0.20, "likes_acoustic": True},
    "Middle of the road": {"genre": "pop", "mood": "happy", "energy": 0.50, "likes_acoustic": False},
}

# Experiment: double the weight on energy, halve the weight on genre
ENERGY_HEAVY_WEIGHTS = {**DEFAULT_WEIGHTS, "energy": 4.0, "genre": 0.5}


def show(name: str, prefs: dict, songs: list, weights: dict = None) -> None:
    """Print the top 5 songs, scores and reasons for one profile."""
    max_score = sum((weights or DEFAULT_WEIGHTS).values())
    print(f"=== {name} ===")
    print(f"Profile: {prefs}")
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k=5, weights=weights), start=1):
        print(f"{rank}. {song['title']} ({song['genre']}, {song['mood']})  -  {score:.2f} / {max_score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        show(name, prefs, songs)

    print("######## EXPERIMENT: energy weight x2, genre weight x0.5 ########\n")
    for name in ("High-Energy Pop", "Deep Intense Rock", "Conflicting: sad but high energy"):
        show(name, PROFILES[name], songs, ENERGY_HEAVY_WEIGHTS)


if __name__ == "__main__":
    main()
