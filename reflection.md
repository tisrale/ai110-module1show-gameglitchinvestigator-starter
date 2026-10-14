# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  * Answer:
  In the developer debug info,cleary shows game already started, with attempt 1 allowed is 8 and attemt left is 7 though I didn't any input in the history.I observed issues/bugs such as:
      - unusual Score results such not correct,not reset when new game and etc.
      - The game crashes after few attempts.
      - Attempts number displays wrong data eg.still shows 0 after multiple plays.
      - Attempts left has issues for instance, displays still 8 after guessing more than 8
      - 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

* Answer:

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Multiple|Exact attempt left|No updated attempts| None
|guess   |
|starts@1|Incremental       | from 1 to 0      | None                  |
|Crashes | works smoothly   | not responding   | None                  |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
* Answer:
1. I used Claude and deepseek.One suggestion from AI was when opening the file I just did and run in the terminal but got an error. Then AI suggested to to do from the very folder to run the game, and It worked.
2. At first, it was hard to read and get the point from what AI suggested but by getting familiarity and learning where to find a helpful suggestions from multiple of lines.  
3. While doing a walkthrough demo after bug fix and run streamlit. AI suggested I have to fix walkthrough conflicts with my known issue, before a commit but I check back and knew that it was a wrong advice by AI. And later when I wrote my though in the chat it said, "You're right. Your walkthrough is an accurate record of what the game showed you, and I was wrong to say it contradicted your known issues. The catch is that the hint you saw was wrong advice."
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
* Answer:
- I tested the fix, for instance for the bug which cause the attempts number not to update, after the fix, I went to the Game and checked whether it's really working or not, found that the Attempt start from '0' unlike what was before the fix which started from 1..I also ran pytest and all 24 testes passed.
- Yes, AI helped me understand how the code function and locate where the bugs found in the code. Also guided me how to run tests.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
* Answer:
Streamlit reruns the whole sript constantly unlike a python script runs on vs code which goes top to bottom and does its function and stops,which needs to run it again to see changes.
Session state is the storage,what survives between the updates.It give memory.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
* Answer:
- One great thing I learned form this project is that how I can leverage AI, Git commands on terminal or power shell so that I can be very comfrtable to use in future projects.
- I'd change how I verify AI output. Instead of just running the code and seeing if it works, I'd add a review step to explain every function. Basically, I'd treat AI like a fast junior developer — useful, but I'm still the one accountable.
- AI is a powerful technology that acts as a teammate for developers who know how to use it effectively.This project shifted my view of AI-generated code from a finished answer to a fast teammate whose work I still verify, test, and take ownership of before commit.