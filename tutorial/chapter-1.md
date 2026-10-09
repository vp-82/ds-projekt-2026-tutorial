# DS-Projekt 2026 tutorial · Chapter 1 · Frame the question before the data

Oct 7, 2026 · Václav Pechtor

## What you have at the end

After this chapter you have three things and no code: a repository, a one-page framing of your question, and a ranked list of the assumptions your plan rests on.

One example runs through the whole tutorial. A question arrived as a single sentence: "Is cycling in Zurich growing?" It came with no time span, no definition of cycling and no place. The repository [ds-projekt-2026-tutorial](https://github.com/vp-82/ds-projekt-2026-tutorial) holds the real result of every step.

Before you start you need an empty folder with git, a Python project and a GitHub repository. Ask Claude Code to set that up and move on. It is a chore and not part of the method.

Leave commits and pushes to Claude Code. Tell it to commit and push, and it writes a proper commit message. In this chapter every commit goes straight to `main`. Branches and pull requests come later, when there is code to protect.

## Frame before data

Write one page before you open any data. It says who reads the result, what they get, what is out, and when you are done.

A question as it arrives is never the question you can answer. The page forces the decisions that the question leaves open. It has five sections.

| Section | What it holds | In the example |
| --- | --- | --- |
| Why | The question as it arrived and who reads the result | A planner who has to answer in public and defend the answer |
| What | What the reader gets and the unit of the result | A table with one row per counting site and year, and one sentence above it |
| How | The data source by name and the main steps | The city's bike counter data, in two loops: all days first, then dry weekdays |
| Non-goals | What you rule out, each with its reason | No city-wide number of cyclists, no causes, no forecast |
| Done | What must exist for you to stop | Every site and year has a value or a stated reason why it cannot be compared |

The reader shapes everything that follows. A planner who must defend the answer needs to know which sites can be compared and which cannot, so the page says that nothing is dropped silently.

Result: [docs/one-pager.md](https://github.com/vp-82/ds-projekt-2026-tutorial/blob/main/docs/one-pager.md)

## Let the agent ask, and answer yourself

Claude Code interviews you and writes down only what you said. This is the prompt.

```text
I want to frame this project before touching any data.
Interview me, one question at a time, until you can write docs/one-pager.md with
the sections Why, What, How, Non-goals and Done.
Why holds the question as it arrived and who reads the result.
What holds what the reader gets and the unit of the result.
Use only my answers.
Where I have no answer yet, write "open" and do not fill the gap yourself.
Do not open or download any data.
```

It asked six questions, one for each thing the page needs: the question as it arrived, the reader, the result and its unit, the source and steps, the non-goals, and what done means.

The sentence that does the work is "Use only my answers". Without it the agent fills every gap with something plausible, and you end up with a plan you never decided on.

Here is what that sentence bought us. After the last answer the agent reported three gaps it had noticed and had not filled:

- "The city's yes/no: you didn't say what makes the answer 'yes'. For example, does more than half the sites growing count?"
- "Grew vs. shrank: you didn't say whether a small change counts as growth or needs to pass some threshold."
- "Dry weekday: loop two doesn't yet say what counts as 'dry' or which days count as weekdays."

We had no answers yet, so all three went into the page as open. "Open" is a valid answer. A gap you can see is worth more than a guess you cannot.

## Fix the rules before the results

Decide what counts as "yes" before you compute anything that could tell you.

Two of the three gaps are decision rules: what makes the answer "yes" for the city, and when a site counts as grown. If you choose these after seeing the numbers, you will choose the rule that gives the answer you like.

So the one-pager marks both with a condition. They must be decided before the first comparison is computed.

The same idea returns with every hypothesis later on: you write down what you expect before you look.

## Find your next step in your assumptions

Your plan rests on things you have not checked. List them and rate them, and the top of the list is your next step.

You rarely see your own assumptions. This is where the agent helps most.

```text
Read docs/one-pager.md.
List the assumptions the plan rests on: what must be true about the data and the
counting for the steps in How to produce the table in What.
One sentence each, at most ten, the ones that would hurt most if wrong.
Do not open any data and do not judge how likely they are.
Show me the list and wait.
I will then rate each one for importance and for how much evidence I have (high,
medium, low).
Write the result to docs/assumptions.md as a table, sorted so that important
with little evidence comes first.
```

It listed ten. Three of them:

- A counter ID means the same physical place in every year.
- A quarter hour without a count shows up as missing and not as a zero.
- A site's change comes from cycling changing and not from a detour around roadworks.

Then we added two that the agent could not get from the plan: that weather is comparable across years, and that nobody has answered the question already. The agent's list is a start. You add what only you can know.

You rate each assumption twice: how much it hurts if it is false, and how much evidence you have that it is true. Important with little evidence goes to the top.

In the example six assumptions tie at the top. Break a tie by cost, and test first what the cheapest look at the data can settle. Chapter 2 starts there.

Result: [docs/assumptions.md](https://github.com/vp-82/ds-projekt-2026-tutorial/blob/main/docs/assumptions.md)

## For your own project

1. Write down your question exactly as it reached you.
2. Run the interview prompt and answer in your own words. Say "open" when you do not know.
3. Mark every decision rule that must be fixed before you see results.
4. Run the assumptions prompt, add what the agent could not know, and rate each one.
5. Ask Claude Code to commit and push both files. Your next step is the top of the table.

---

[Overview](README.md) · Next: [Chapter 2 · Test what can break your project first](chapter-2.md)
