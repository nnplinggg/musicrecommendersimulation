# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

A small command-line recommender that matches songs to a listener's mood and energy.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

**Goal:** VibeMatch suggests the five songs from a small catalog that best fit one listener's taste. It predicts "which songs would this person enjoy?" from their favorite mood, favorite genre, target energy and whether they like acoustic music.

**Intended use:** classroom exploration. It shows how a simple recommender turns data into a ranked list with reasons. It assumes the listener can describe their taste in four settings and that their taste doesn't change.

**Not intended for:** real music apps or real listeners. It should not be used to judge artists, to decide what people hear at scale, or to guess anything about a person from their taste. The catalog is far too small and the labels are too simple for that.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The recommender looks at every song in the catalog one at a time and gives it points for how well it fits what the listener asked for. A song earns 2 points if its mood matches the listener's favorite mood and 1 point if its genre matches. It also earns up to 2 points for energy: the closer the song's energy is to the level the listener wants, the more points it gets, and a song that is too calm or too intense loses points either way. Finally, it earns up to 1 point for how acoustic it sounds, compared with whether the listener prefers acoustic or electronic music. The maximum is 6 points. Each song also keeps a short list of reasons, such as "mood match", so the system can explain itself. Once every song has a score, the songs are sorted from highest to lowest and the top five are shown. I weighted mood above genre because mood describes how a song feels, while genre is only a label. This is a content-based system that runs from the command line, and it only looks at song attributes, not at what other listeners do.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs. I kept the 10 starter songs and added 8. It covers 15 genres and 14 moods, but most genres have only one song. Lofi has three, pop has two. Each song has genre, mood, energy, tempo, valence, danceability and acousticness. The scoring only uses mood, genre, energy and acousticness. Missing from the data: lyrics, language, artist popularity, era, instruments, and anything about how real people listen (skips, replays, playlists).

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- It works well when the listener's wishes agree with each other, such as Chill Lofi or Deep Intense Rock.
- Chill Lofi gave the three lofi and ambient songs I would have picked. Rock put *Storm Runner* first.
- Mood and energy together capture a lot of what a "vibe" is.
- Every result has reasons, so it is easy to see why a song ranked where it did.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**A weakness I found:** The system lets the two label matches outvote how a song actually sounds. In the "sad but high energy" test, the user asked for energy 0.9, yet the first result was *Porch Lullaby*, a very quiet folk song with energy 0.30. It won because its mood (sad), genre (folk) and acoustic feel all matched, which gave it 3 points from the labels and nearly 1 more for sounding acoustic, while the huge energy gap cost it only 1.2 points out of 2. A user with two conflicting wishes therefore always gets the label they named, not a compromise. The tiny catalog makes it worse, because there is no song that is both sad and energetic to offer instead. A second effect is that *Gym Hero* keeps appearing: its very high energy and low acousticness earn it close to half the points for almost anyone who wants loud, non-acoustic music, whatever the mood or genre.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles tested:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and three tricky ones: "sad but high energy" (conflicting wishes), "classical" with a genre and mood that don't exist in the catalog, and "middle of the road" (energy 0.5). I ran the whole catalog of 18 songs for each and looked at the top five. I judged them against my own sense of what each listener would want to hear.

**What matched my intuition:** Chill Lofi gave the three lofi and ambient tracks first (*Midnight Coding*, *Library Rain*, *Spacewalk Thoughts*), which is what I would pick. Deep Intense Rock put *Storm Runner* on top. High-Energy Pop put *Sunrise City* first, then *Rooftop Lights*.

**What surprised me:**
- *Gym Hero* showed up for both the Pop profile (3rd) and the Rock profile (2nd). In plain terms: *Gym Hero* is a loud, fast, electronic-sounding song labeled "intense". A happy-pop fan doesn't care about the label, but the loudness and the non-acoustic sound still earn it lots of points, and its genre is pop, so it gets a bonus too. A rock fan likes "intense" songs and wants loud, non-acoustic music, so it fits there too. The system never learned that a workout anthem isn't the same as a feel-good song, because it can't hear the song and only sees the numbers and labels.
- For the classical profile with a genre and mood that don't exist in the catalog, no song matched either label, so the system ranked by energy and acousticness alone. It still gave a sensible answer (*Moonlit Sonata Remix* first), but the top score was only 2.79 out of 6, which shows how little it had to go on.
- For the "sad but high energy" profile the top result was a quiet song, as described under Limitations and Bias.

**Comparing pairs of profiles:**
- *Pop vs Chill Lofi:* the pop profile gets bright, high-energy songs like *Sunrise City*, and the lofi profile gets slow, acoustic songs like *Library Rain*. Energy and acousticness point in opposite directions, so it makes sense that the two lists share no songs.
- *Pop vs Deep Intense Rock:* both want loud, non-acoustic songs, so they share *Gym Hero* and *Sunrise City*. They differ at the top because the mood label decides: happy gives *Sunrise City*, intense gives *Storm Runner*. This is valid, since only the mood and genre preferences changed.
- *Chill Lofi vs Deep Intense Rock:* these are opposites and the lists don't overlap at all, which is what I'd expect from tastes this different.
- *Pop vs "middle of the road" pop:* with the same genre and mood but energy 0.5 instead of 0.85, *Sunrise City* and *Rooftop Lights* still lead and *Velvet Hours* (energy 0.52) enters. Moving the energy target changes the lower spots, but the labels keep the top two fixed, so the system reacts to energy less than I intended.
- *"Sad but high energy" vs Rock:* the sad profile pulls in quiet and sad songs while the rock profile pulls in loud ones, even though both asked for high energy. This shows the mood label beating the energy number.

**Experiment (energy weight doubled, genre weight halved):** The maximum score rose from 6 to 7.5, so I compared rankings, not raw scores. For Pop, the top three stayed the same, but *Storm Runner* replaced *Night Drive Loop* in 4th place, a louder song that is not happier, so the results got different without being more accurate. For the sad-and-energetic profile, *Storm Runner* and *Gym Hero* rose to 2nd and 3rd, which respects the high-energy request better, though the quiet *Porch Lullaby* still stayed first. For Rock, *Neon Pulse* overtook *Iron Cathedral*, which is not better. Overall the change made the lists more energy-driven, but not clearly more accurate. The math stayed valid because every part still lies between 0 and its weight, so the maximum is just the sum of the weights.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. Give partial credit for similar moods and genres (for example, "chill" and "relaxed", or "pop" and "indie pop") instead of all-or-nothing matches.
2. Add valence as a score, so "energetic and dark" and "energetic and cheerful" can be told apart.
3. Add a diversity rule to the ranking, so the top five don't include near-duplicates, and add more songs to every genre.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

**Biggest learning moment:** The "sad but high energy" test. I expected the system to find a compromise, but it picked a quiet song because the mood and genre matches added up to more points than the energy miss cost. I learned that the weights, not the math on one feature, decide what a recommender really cares about.

**How AI helped, and when I double-checked it:** The AI helped me plan the scoring, write the code, and run tests across many profiles quickly. I still had to check its numbers. In one write-up it said an energy gap cost 1.6 points when it was really 1.2, and it described an experiment result more broadly than the output showed. I fixed both by rereading the actual terminal output. The lesson is to trust the program output over the explanation of it.

**What surprised me:** A few plain rules still feel like a real recommendation. *Sunrise City* topping the pop list felt right, and the reasons next to each song made it feel like the system understood me. It doesn't. It only adds up points.

**What I'd try next:** Add partial credit for similar moods, add valence to the score, and make the ranking avoid near-duplicates. After that I'd try adding a second listener so I could test a simple collaborative filter.
