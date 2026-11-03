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

## Evaluation Output

Output of `python -m src.main`: three realistic profiles, three adversarial ones, then the weight-shift experiment (energy weight doubled, genre weight halved). The comparison and analysis are in the Evaluation section of [model_card.md](model_card.md).

```
Loaded songs: 18

=== High-Energy Pop ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'likes_acoustic': False}
1. Sunrise City (pop, happy)  -  5.92 / 6.00
     - mood match (+2.0)
     - energy 0.82 vs target 0.85 (+1.94)
     - genre match (+1.0)
     - acousticness 0.18 vs target 0.20 (+0.98)
2. Rooftop Lights (indie pop, happy)  -  4.67 / 6.00
     - mood match (+2.0)
     - energy 0.76 vs target 0.85 (+1.82)
     - acousticness 0.35 vs target 0.20 (+0.85)
3. Gym Hero (pop, intense)  -  3.69 / 6.00
     - energy 0.93 vs target 0.85 (+1.84)
     - genre match (+1.0)
     - acousticness 0.05 vs target 0.20 (+0.85)
4. Night Drive Loop (synthwave, moody)  -  2.78 / 6.00
     - energy 0.75 vs target 0.85 (+1.80)
     - acousticness 0.22 vs target 0.20 (+0.98)
5. Concrete Crown (hip hop, confident)  -  2.78 / 6.00
     - energy 0.78 vs target 0.85 (+1.86)
     - acousticness 0.12 vs target 0.20 (+0.92)

=== Chill Lofi ===
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}
1. Midnight Coding (lofi, chill)  -  5.87 / 6.00
     - mood match (+2.0)
     - energy 0.42 vs target 0.40 (+1.96)
     - genre match (+1.0)
     - acousticness 0.71 vs target 0.80 (+0.91)
2. Library Rain (lofi, chill)  -  5.84 / 6.00
     - mood match (+2.0)
     - energy 0.35 vs target 0.40 (+1.90)
     - genre match (+1.0)
     - acousticness 0.86 vs target 0.80 (+0.94)
3. Spacewalk Thoughts (ambient, chill)  -  4.64 / 6.00
     - mood match (+2.0)
     - energy 0.28 vs target 0.40 (+1.76)
     - acousticness 0.92 vs target 0.80 (+0.88)
4. Focus Flow (lofi, focused)  -  3.98 / 6.00
     - energy 0.40 vs target 0.40 (+2.00)
     - genre match (+1.0)
     - acousticness 0.78 vs target 0.80 (+0.98)
5. Coffee Shop Stories (jazz, relaxed)  -  2.85 / 6.00
     - energy 0.37 vs target 0.40 (+1.94)
     - acousticness 0.89 vs target 0.80 (+0.91)

=== Deep Intense Rock ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}
1. Storm Runner (rock, intense)  -  5.88 / 6.00
     - mood match (+2.0)
     - energy 0.91 vs target 0.92 (+1.98)
     - genre match (+1.0)
     - acousticness 0.10 vs target 0.20 (+0.90)
2. Gym Hero (pop, intense)  -  4.83 / 6.00
     - mood match (+2.0)
     - energy 0.93 vs target 0.92 (+1.98)
     - acousticness 0.05 vs target 0.20 (+0.85)
3. Sunrise City (pop, happy)  -  2.78 / 6.00
     - energy 0.82 vs target 0.92 (+1.80)
     - acousticness 0.18 vs target 0.20 (+0.98)
4. Neon Pulse (edm, euphoric)  -  2.75 / 6.00
     - energy 0.96 vs target 0.92 (+1.92)
     - acousticness 0.03 vs target 0.20 (+0.83)
5. Iron Cathedral (metal, aggressive)  -  2.74 / 6.00
     - energy 0.97 vs target 0.92 (+1.90)
     - acousticness 0.04 vs target 0.20 (+0.84)

=== Conflicting: sad but high energy ===
Profile: {'genre': 'folk', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True}
1. Porch Lullaby (folk, sad)  -  4.67 / 6.00
     - mood match (+2.0)
     - energy 0.30 vs target 0.90 (+0.80)
     - genre match (+1.0)
     - acousticness 0.93 vs target 0.80 (+0.87)
2. Dust Road Anthem (country, nostalgic)  -  2.55 / 6.00
     - energy 0.68 vs target 0.90 (+1.56)
     - acousticness 0.81 vs target 0.80 (+0.99)
3. Storm Runner (rock, intense)  -  2.28 / 6.00
     - energy 0.91 vs target 0.90 (+1.98)
     - acousticness 0.10 vs target 0.80 (+0.30)
4. Rooftop Lights (indie pop, happy)  -  2.27 / 6.00
     - energy 0.76 vs target 0.90 (+1.72)
     - acousticness 0.35 vs target 0.80 (+0.55)
5. Sunrise City (pop, happy)  -  2.22 / 6.00
     - energy 0.82 vs target 0.90 (+1.84)
     - acousticness 0.18 vs target 0.80 (+0.38)

=== Missing genre and mood: classical ===
Profile: {'genre': 'opera', 'mood': 'serene', 'energy': 0.2, 'likes_acoustic': True}
1. Moonlit Sonata Remix (classical, melancholy)  -  2.79 / 6.00
     - energy 0.22 vs target 0.20 (+1.96)
     - acousticness 0.97 vs target 0.80 (+0.83)
2. Spacewalk Thoughts (ambient, chill)  -  2.72 / 6.00
     - energy 0.28 vs target 0.20 (+1.84)
     - acousticness 0.92 vs target 0.80 (+0.88)
3. Porch Lullaby (folk, sad)  -  2.67 / 6.00
     - energy 0.30 vs target 0.20 (+1.80)
     - acousticness 0.93 vs target 0.80 (+0.87)
4. Library Rain (lofi, chill)  -  2.64 / 6.00
     - energy 0.35 vs target 0.20 (+1.70)
     - acousticness 0.86 vs target 0.80 (+0.94)
5. Focus Flow (lofi, focused)  -  2.58 / 6.00
     - energy 0.40 vs target 0.20 (+1.60)
     - acousticness 0.78 vs target 0.80 (+0.98)

=== Middle of the road ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.5, 'likes_acoustic': False}
1. Sunrise City (pop, happy)  -  5.34 / 6.00
     - mood match (+2.0)
     - energy 0.82 vs target 0.50 (+1.36)
     - genre match (+1.0)
     - acousticness 0.18 vs target 0.20 (+0.98)
2. Rooftop Lights (indie pop, happy)  -  4.33 / 6.00
     - mood match (+2.0)
     - energy 0.76 vs target 0.50 (+1.48)
     - acousticness 0.35 vs target 0.20 (+0.85)
3. Gym Hero (pop, intense)  -  2.99 / 6.00
     - energy 0.93 vs target 0.50 (+1.14)
     - genre match (+1.0)
     - acousticness 0.05 vs target 0.20 (+0.85)
4. Velvet Hours (r&b, romantic)  -  2.76 / 6.00
     - energy 0.52 vs target 0.50 (+1.96)
     - acousticness 0.40 vs target 0.20 (+0.80)
5. Night Drive Loop (synthwave, moody)  -  2.48 / 6.00
     - energy 0.75 vs target 0.50 (+1.50)
     - acousticness 0.22 vs target 0.20 (+0.98)

######## EXPERIMENT: energy weight x2, genre weight x0.5 ########

=== High-Energy Pop ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'likes_acoustic': False}
1. Sunrise City (pop, happy)  -  7.36 / 7.50
     - mood match (+2.0)
     - energy 0.82 vs target 0.85 (+3.88)
     - genre match (+0.5)
     - acousticness 0.18 vs target 0.20 (+0.98)
2. Rooftop Lights (indie pop, happy)  -  6.49 / 7.50
     - mood match (+2.0)
     - energy 0.76 vs target 0.85 (+3.64)
     - acousticness 0.35 vs target 0.20 (+0.85)
3. Gym Hero (pop, intense)  -  5.03 / 7.50
     - energy 0.93 vs target 0.85 (+3.68)
     - genre match (+0.5)
     - acousticness 0.05 vs target 0.20 (+0.85)
4. Storm Runner (rock, intense)  -  4.66 / 7.50
     - energy 0.91 vs target 0.85 (+3.76)
     - acousticness 0.10 vs target 0.20 (+0.90)
5. Concrete Crown (hip hop, confident)  -  4.64 / 7.50
     - energy 0.78 vs target 0.85 (+3.72)
     - acousticness 0.12 vs target 0.20 (+0.92)

=== Deep Intense Rock ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}
1. Storm Runner (rock, intense)  -  7.36 / 7.50
     - mood match (+2.0)
     - energy 0.91 vs target 0.92 (+3.96)
     - genre match (+0.5)
     - acousticness 0.10 vs target 0.20 (+0.90)
2. Gym Hero (pop, intense)  -  6.81 / 7.50
     - mood match (+2.0)
     - energy 0.93 vs target 0.92 (+3.96)
     - acousticness 0.05 vs target 0.20 (+0.85)
3. Neon Pulse (edm, euphoric)  -  4.67 / 7.50
     - energy 0.96 vs target 0.92 (+3.84)
     - acousticness 0.03 vs target 0.20 (+0.83)
4. Iron Cathedral (metal, aggressive)  -  4.64 / 7.50
     - energy 0.97 vs target 0.92 (+3.80)
     - acousticness 0.04 vs target 0.20 (+0.84)
5. Sunrise City (pop, happy)  -  4.58 / 7.50
     - energy 0.82 vs target 0.92 (+3.60)
     - acousticness 0.18 vs target 0.20 (+0.98)

=== Conflicting: sad but high energy ===
Profile: {'genre': 'folk', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True}
1. Porch Lullaby (folk, sad)  -  4.97 / 7.50
     - mood match (+2.0)
     - energy 0.30 vs target 0.90 (+1.60)
     - genre match (+0.5)
     - acousticness 0.93 vs target 0.80 (+0.87)
2. Storm Runner (rock, intense)  -  4.26 / 7.50
     - energy 0.91 vs target 0.90 (+3.96)
     - acousticness 0.10 vs target 0.80 (+0.30)
3. Gym Hero (pop, intense)  -  4.13 / 7.50
     - energy 0.93 vs target 0.90 (+3.88)
     - acousticness 0.05 vs target 0.80 (+0.25)
4. Dust Road Anthem (country, nostalgic)  -  4.11 / 7.50
     - energy 0.68 vs target 0.90 (+3.12)
     - acousticness 0.81 vs target 0.80 (+0.99)
5. Sunrise City (pop, happy)  -  4.06 / 7.50
     - energy 0.82 vs target 0.90 (+3.68)
     - acousticness 0.18 vs target 0.80 (+0.38)
```

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



