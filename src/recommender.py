import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k songs that best match the user profile, best first."""
        prefs = _prefs_from_profile(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in one line why a song fits the user profile."""
        score, reasons = score_song(_prefs_from_profile(user), asdict(song))
        return f"{score:.2f}: " + "; ".join(reasons)


def _prefs_from_profile(user: UserProfile) -> Dict:
    """Convert a UserProfile into the preference dict used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


NUMERIC_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            row["id"] = int(row["id"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs and return (score, reasons)."""
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs.get("mood"):
        score += 2.0
        reasons.append("mood match (+2.0)")

    if "energy" in user_prefs:
        points = 2.0 * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    if song["genre"] == user_prefs.get("genre"):
        score += 1.0
        reasons.append("genre match (+1.0)")

    if "likes_acoustic" in user_prefs:
        target = 0.8 if user_prefs["likes_acoustic"] else 0.2
        points = 1.0 * (1 - abs(song["acousticness"] - target))
        score += points
        reasons.append(f"acousticness {song['acousticness']:.2f} vs target {target:.2f} (+{points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation)."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
