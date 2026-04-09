# Nova — Voice Assistant

A voice-first personal assistant built in Python that listens to natural speech, routes commands to the right module, and responds out loud — powered by Gemini 2.5 Flash for open-ended questions, with dedicated handlers for calendar, weather, news, tasks, music, and web navigation.


## Quick Start

```bash
git clone https://github.com/nishant05gaurav/Nova-Assistant.git
cd Nova-Assistant

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Add your API keys to credentials.json (see Environment Variables below)
# First run opens a browser for Google Calendar OAuth — approve and continue

python run.py
```


## Demo / Preview

Nova runs in the terminal. After launch it greets you based on the time of day and starts listening. A few things you can say:

```
"What time is it?"             → speaks the current time
"Open YouTube"                 → opens youtube.com in your browser
"Play perfect"                 → opens the mapped YouTube link
"What's the weather?"          → asks current location or specific city, then speaks temp/pressure/humidity
"Tell me the news"             → reads out top headlines from India
"What are my calendar events?" → reads your next 5 Google Calendar events
"Add a to-do"                  → asks what task, then saves it to todo.txt
"Who invented the telephone?"  → routes to Gemini, speaks a 2–3 sentence answer
"Tell me a fact"               → speaks a random curated fact
"Exit"                         → shuts down
```

## Problem & Purpose

Most voice assistant projects are glorified `if/else` wrappers around a single API. Nova is different — it's a fully modular system where each capability lives in its own file, the command router in `main.py` dispatches cleanly, and the TTS layer (`speech.py`) handles cross-platform voice output without locking into a single OS. Built to go well beyond a toy project and function as a real, daily-use assistant.


## Highlights

- **Gemini 2.5 Flash integration** — open-ended questions (`who`, `what`, `why`, `how`, `tell`) are routed directly to Gemini with a prompt that constrains responses to 2–3 clear sentences. No rambling, no hallucination-padding.
- **Google Calendar via OAuth 2.0** — uses the Google Calendar API with a full OAuth flow. `token.json` is written on first auth and reused on subsequent runs. Fetches the next 5 real events from the user's primary calendar and speaks them in human-readable format.
- **Cross-platform TTS** — `speech.py` detects the OS at runtime (`Windows → sapi5`, `macOS → nsss`, `Linux → espeak`) and initializes the right engine. The assistant works out of the box on all three platforms without any config change.
- **Modular command dispatch** — `main.py` runs a priority-ordered handler chain. Each module returns `True` if it handled the command, allowing the router to skip remaining handlers. No tangled conditionals.
- **IP-based location detection for weather** — when the user says "current location", Nova hits `ipinfo.io` to resolve the city without any GPS or manual input, then passes it to OpenWeatherMap.
- **Voice-driven to-do manager** — the `TODO` class manages `todo.txt` with add, delete, show, and clear operations. The voice handler uses a second `Microphone` listen loop to capture the follow-up (the task name or item number) after the intent is understood.
- **Ambient noise calibration** — every `Microphone` listen call runs `adjust_for_ambient_noise()` before capturing, reducing false triggers in noisy environments.


## Features

- Time and date announcements
- Weather lookup — current location (auto-detected via IP) or specific city
- Top news headlines from India via NewsAPI
- Google Calendar integration — reads next 5 upcoming events with OAuth 2.0
- Voice-controlled to-do list — add, delete, show, clear, persisted to `todo.txt`
- Gemini 2.5 Flash for general knowledge questions
- Favorite music playback via mapped YouTube links
- Web navigation — opens Google, YouTube, GitHub, LinkedIn, Instagram, Twitter, Facebook
- Random motivational quotes and trivia facts
- Time-based greetings on startup
- Cross-platform TTS (Windows / macOS / Linux)


## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.x |
| Voice Input | `speech_recognition`, `PyAudio` |
| Voice Output | `pyttsx3` (sapi5 / nsss / espeak) |
| AI | Google Gemini 2.5 Flash (`google-generativeai`) |
| Calendar | Google Calendar API v3, OAuth 2.0 |
| Weather | OpenWeatherMap API |
| News | NewsAPI |
| Location | ipinfo.io |
| Web | `webbrowser`, `os.system` (fallback) |


## Project Structure

```
Nova-Assistant/
├── assistant/
│   ├── __init__.py
│   ├── calendar.py         # Google Calendar OAuth + event fetching
│   ├── favmusic.py         # Song name → YouTube URL mapping
│   ├── gemini_api.py       # Gemini 2.5 Flash prompt + response handler
│   ├── main.py             # Command router and main loop
│   ├── news_weather.py     # NewsAPI headlines + OpenWeatherMap weather
│   ├── quotes_facts.py     # Curated quotes and facts lists
│   ├── speech.py           # Cross-platform TTS (pyttsx3)
│   ├── time_date.py        # Time and date announcement
│   ├── todo_ops.py         # Voice-driven to-do manager
│   └── webs_ops.py         # Web browser navigation
├── Essential Files/
├── credentials.json        # Google OAuth client credentials (not committed)
├── token.json              # Auto-generated after first OAuth login
├── todo.txt                # Persistent task storage
└── run.py                  # Entry point
```


## Environment Variables

Add your API keys to `credentials.json` or directly in the relevant module files before running:

```
GEMINI_API_KEY          → Google Gemini API key (gemini_api.py)
NEWS_API_KEY            → NewsAPI key for top headlines (news_weather.py)
OPENWEATHER_API_KEY     → OpenWeatherMap API key (news_weather.py)
```

For Google Calendar, place your OAuth client credentials file at the project root as `credentials.json`. Download it from [Google Cloud Console](https://console.cloud.google.com/) under **APIs & Services → Credentials → OAuth 2.0 Client IDs**.

On first run, a browser window will open asking you to authorize calendar access. After approval, `token.json` is saved automatically and reused on future runs.


## Installation & Dependencies

```bash
pip install speechrecognition pyaudio pyttsx3 requests
pip install google-generativeai google-auth google-auth-oauthlib google-api-python-client
```

> On macOS, if PyAudio installation fails: `brew install portaudio` then `pip install pyaudio`  
> On Linux: `sudo apt-get install python3-pyaudio portaudio19-dev`

## Usage

Say **"exit"**, **"quit"**, or **"stop"** to shut Nova down cleanly.

To add a new website to web navigation, add a key-value pair to `site_dict` in `webs_ops.py`.

To add new music, add a `"keyword": "youtube_url"` entry to the `music` dict in `favmusic.py`.


## Contributing

Pull requests welcome. Obvious extension points: wake-word detection (currently commented out in `main.py`), multi-user calendar support, and a GUI layer on top of the voice loop.


## License

MIT License: Use it, Fork it, Build on it.


## Author

Built by [Nishant Gaurav](https://github.com/nishant05gaurav)  

[GitHub](https://github.com/nishant05gaurav) · [LinkedIn](https://shorturl.at/kWLs5) · [nishant05gaurav@gmail.com](mailto:nishant05gaurav@gmail.com)