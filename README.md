# 🪵 Wood-E

**Wood-E** is a Streamlit-based shop calculator and conversational assistant for woodworkers, built as a community utility feature of [TimberLens Creations](https://timberlenscreations.com) — makers of solid hardwood guitar stands with built-in climate hygrometers.

It combines a deterministic math engine (board footage, beam deflection, compound miters, wood movement) with a natural-language chat agent powered by the Google Gemini API, so you can either fill in a form or just describe your project in plain English.

This repo is the standalone version of the app: it runs on its own with `streamlit run app.py`, and is also the source that will be deployed as a page on [timberlenscreations.com](https://timberlenscreations.com) once it's in the git repo.

---

## Screenshots

**Chat with Wood-E** — ask a shop question in plain language and get a grounded, tool-backed answer.

![Chat with Wood-E](screenshots/chat-with-woode.png)

**Structural Deflection** — Euler-Bernoulli beam analysis for shelves, with pass/warn/fail thresholds.

![Structural Deflection](screenshots/structural-deflection.png)

**Volume & Costing** — board footage and lumber cost from part dimensions and species.

![Volume & Costing](screenshots/volume-and-costing.png)

---

## Features

Wood-E is organized into five tabs:

| Tab | Purpose | Core method |
|---|---|---|
| 💬 Chat with Wood-E | Natural-language Q&A, backed by the same deterministic tools as the other tabs | Gemini function calling over `woody_engine` |
| 📐 Structural Deflection | Shelf sag under uniform or point load | Euler-Bernoulli beam deflection |
| 🪵 Volume & Costing | Board footage and total lumber cost | Linear volumetric conversion |
| 🪚 Joinery Trigonometry | Miter and bevel angles for splayed polygon frames | Compound miter trigonometry |
| 💨 Environmental Physics | Predicted seasonal wood movement | Species tangential shrinkage coefficient |

Every tab supports both Imperial (inches/lbs) and Metric (mm/kg) units, and pulls material constants (Janka hardness, modulus of elasticity, shrinkage coefficients) from a small built-in species database.

The chat tab is the same calculators, exposed as tools to a Gemini model — the model is instructed to always call the deterministic functions rather than estimating numbers itself, so the conversational answers stay as accurate as the form-based ones.

---

## Project structure

```
.
├── app.py                  # Streamlit UI — all five tabs
├── woody_engine.py          # Deterministic math: board feet, deflection, miters, wood movement
├── woody_agent.py           # Gemini-backed chat agent, wraps woody_engine as tools
├── wood_species_db.json     # Material properties for each supported species
├── skills.md                 # Reference doc: formulas and safety thresholds the agent follows
├── requirements.txt
├── api_key.txt               # Your Gemini API key, plaintext, gitignored — not included in repo
└── .gitignore
```

## Supported species

Cherry, White Oak, Walnut, Hard Maple, and Eastern White Pine ship out of the box, each with Janka hardness, density, modulus of elasticity, and shrinkage data in `wood_species_db.json`. Add a new species by adding an entry with the same fields.

---

## Setup

Wood-E works two ways: as a standalone local app today, and as a page on timberlenscreations.com once this repo is pushed and deployed there. The local setup below is the same either way — deployment just points a host at the same `app.py`.

**Requirements:** Python 3.9+, a Google Gemini API key.

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your Gemini API key as plaintext in `api_key.txt` (in the project root):
   ```
   your-gemini-api-key-here
   ```
   This file is gitignored and never committed. For the deployed site, the key should instead be set via the host's environment/secrets so it never touches the repo.

3. Run the app locally:
   ```bash
   streamlit run app.py
   ```

4. Open the URL Streamlit prints (typically `http://localhost:8501`).

### Deploying as a TimberLens Creations page

Once this is pushed to git, it can be hosted (e.g. Streamlit Community Cloud, or any host that runs a Streamlit app) and linked from timberlenscreations.com. The only things to carry over from local setup: `requirements.txt` for dependencies, and the Gemini API key set as a secret/environment variable on the host rather than as a committed `api_key.txt`.

---

## Usage

- **Form-based tabs** (Structural Deflection, Volume & Costing, Joinery Trigonometry, Environmental Physics): pick a species in the sidebar, enter your dimensions, and read the result — color-coded green/amber/red where a safety threshold applies.
- **Chat tab**: describe your project in plain language, e.g. *"How many board feet is 10 planks of walnut 1.16"x10"x48" at $14/bf?"* Wood-E extracts the numbers and calls the matching calculator, then explains what the result means for your build.

---

## About TimberLens Creations

Wood-E is a free community tool from [TimberLens Creations](https://timberlenscreations.com), makers of premium solid hardwood guitar stands with built-in precision hygrometers, so instruments stay safe from the humidity swings this app helps you calculate around.
# Wood-E
