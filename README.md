# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real-world recommenders work

Platforms like Spotify and YouTube combine two ideas. **Collaborative filtering** predicts what you'll like from other people's behavior: likes, skips, replays, watch time and playlist membership. **Content-based filtering** predicts it from the item itself: audio features such as tempo and energy, plus text such as playlist descriptions. Real systems blend both, because behavior data is powerful but fails on new songs (the cold-start problem), while content data works on day one but can trap a listener in a bubble of near-identical tracks.

My version is purely **content-based**. It has one user profile and no data about other listeners, so it can't do collaborative filtering. It prioritizes **mood and energy**, because those describe the "vibe" of a song better than its genre label does. Genre is a smaller bonus.

### Features used

**`Song`** (from `data/songs.csv`): `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`. Scoring uses `mood`, `energy`, `genre` and `acousticness`. The other numeric features are kept for later experiments.

**`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy` (0.0 to 1.0) and `likes_acoustic` (true or false). The functional version in `main.py` passes the same information as a dict with the keys `genre`, `mood`, `energy` and `likes_acoustic`.

### Catalog and test profiles

The catalog in `data/songs.csv` now has 18 songs. I added eight with genres and moods the starter file lacked (hip hop, classical, metal, r&b, country, reggae, edm, folk). Two fill gaps in the starter data: a quiet, sad song (*Porch Lullaby*) and a fairly energetic acoustic one (*Dust Road Anthem*).

The main profile is a dictionary, and I use two contrasting ones to check that the system can tell very different tastes apart:

```python
chill_lofi   = {"genre": "lofi", "mood": "chill", "energy": 0.40, "likes_acoustic": True}
intense_rock = {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False}
```

I ran the recipe below by hand on both profiles. The top 5 for each are almost entirely different: *Midnight Coding* and *Library Rain* lead for chill lofi, and *Storm Runner* then *Gym Hero* lead for intense rock. So the profile is not too narrow for that distinction. It did show two weak spots:

- A "sad and quiet" profile ranks *Porch Lullaby* first, but *Moonlit Sonata Remix* (mood `melancholy`) misses the top 5 even though it fits the feel, because mood only matches on the exact label.
- For intense rock, *Iron Cathedral* (metal, `aggressive`) lands fifth, behind a happy pop song, for the same reason.

The profile also has no valence target, so "energetic and dark" can't be told apart from "energetic and cheerful". Adding `target_valence` is an experiment I plan to try.

### Algorithm Recipe

**Scoring Rule (one song, maximum 6.0 points):**

| Component | Points | How it is calculated |
|---|---|---|
| Mood match | +2.0 | 2.0 if `song.mood == favorite_mood`, otherwise 0 |
| Energy closeness | up to +2.0 | `2.0 * (1 - abs(song.energy - target_energy))` |
| Genre match | +1.0 | 1.0 if `song.genre == favorite_genre`, otherwise 0 |
| Acousticness closeness | up to +1.0 | `1.0 * (1 - abs(song.acousticness - target))`, where the target is 0.8 if `likes_acoustic` and 0.2 if not |

Energy uses the distance to the user's target, not "higher is better". A user who wants energy 0.4 should prefer a 0.35 song over a 0.93 song. Each reward also produces a short reason string, such as "mood match (+2.0)", which becomes the explanation for the recommendation.

**Ranking Rule (the whole list):** score every song in the catalog, sort by score from highest to lowest, and return the top `k` (default 5) with their explanations. Scoring judges one song on its own, and ranking turns those scores into an ordered shortlist. They are kept separate so either one can be changed without touching the other.

**Data flow:**

```
Input: user prefs (genre, mood, target energy, likes acoustic)
   |
Process: for each song in songs.csv -> score_song() -> (score, reasons)
   |
Output: sort by score descending -> top k songs + explanations
```

**Why mood outweighs genre:** I weighted mood above genre, the reverse of a common starting point (+2.0 genre, +1.0 mood). Mood describes how a song feels, while genre is a production label. Several genres in the catalog have only one song, so a heavy genre weight would nearly force the same top result every time. I plan to test both weightings under Experiments.

### Expected biases

- **Mood label dependence:** the exact-match mood bonus is all or nothing. "Chill" and "relaxed" are close in feel but earn no partial credit, so a good relaxed song can lose to a mediocre chill one.
- **Energy dominates the numbers:** energy, tempo, acousticness and danceability are highly correlated in this catalog, so the system effectively sorts songs on one loud-vs-quiet axis.
- **Small catalog:** with 10 songs, the top 5 will often include near-duplicates, such as the three lofi tracks, and gaps like quiet-but-sad music have no good match.
- **Single static profile:** the user never changes, and the system has no skips or likes to learn from. Real systems adapt to behavior, and mine can't.
- **No context:** a person picks music for an activity (studying, working out), which the numeric features don't capture.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default pop/happy profile:

```
Loaded songs: 18
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo  -  Score: 5.94 / 6.00
     - mood match (+2.0)
     - energy 0.82 vs target 0.80 (+1.96)
     - genre match (+1.0)
     - acousticness 0.18 vs target 0.20 (+0.98)

2. Rooftop Lights by Indigo Parade  -  Score: 4.77 / 6.00
     - mood match (+2.0)
     - energy 0.76 vs target 0.80 (+1.92)
     - acousticness 0.35 vs target 0.20 (+0.85)

3. Gym Hero by Max Pulse  -  Score: 3.59 / 6.00
     - energy 0.93 vs target 0.80 (+1.74)
     - genre match (+1.0)
     - acousticness 0.05 vs target 0.20 (+0.85)

4. Night Drive Loop by Neon Echo  -  Score: 2.88 / 6.00
     - energy 0.75 vs target 0.80 (+1.90)
     - acousticness 0.22 vs target 0.20 (+0.98)

5. Concrete Crown by Dre Valley  -  Score: 2.88 / 6.00
     - energy 0.78 vs target 0.80 (+1.96)
     - acousticness 0.12 vs target 0.20 (+0.92)
```

The top result, *Sunrise City*, is pop and happy with energy close to the target, so it scores almost the maximum. *Rooftop Lights* ranks second on mood and energy alone, and *Gym Hero* ranks third on its genre match without the right mood.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



