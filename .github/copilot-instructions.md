# Voice AI Agent - Copilot Instructions

## Project Overview

A conversational voice assistant that listens to user commands, detects intents, executes tools, and responds via text-to-speech. The agent maintains conversation memory to enable multi-turn dialogue.

**Architecture**: Speech input → Intent detection → Tool execution OR LLM response → Speech output

## Key Components & Patterns

### 1. Main Control Flow (`main.py`)

- **Intent Detection**: Rule-based pattern matching (case-insensitive)
  - `"book"` → BOOKING
  - `"weather"` → WEATHER
  - `"time"` → TIME
  - Default → CHAT (delegate to LLM)
- **Tool Execution**: Built-in tools (`book_meeting`, `get_time`, `get_weather`) bypass LLM for speed
- **Memory Management**: List of message dicts with `{"role": "system|user|assistant", "content": text}`
  - Initialized with system prompt: `"You are a smart and friendly voice assistant."`
  - Appended after user input and agent response for context

### 2. Intent-Specific Tool Functions (`tools.py`)

- **DateTime Extraction**: `extract_datetime(text)` parses "tomorrow"/"today" and times (regex: `\d{1,2}\s*(am|pm)?`)
- **Stubs**: `get_time()`, `get_weather()` return hardcoded responses (placeholder for real APIs)
- **Booking**: `book_meeting(text)` calls `extract_datetime()` and formats response

### 3. Voice I/O Modules

- **Input** (`voice_input.py`):
  - Uses `speech_recognition` library with Google Speech API
  - 0.5s ambient noise adjustment, 5s timeout, 10s phrase limit
  - Returns empty string on timeout/failure (main.py skips processing)
- **Output** (`voice_output.py`):
  - gTTS (Google Text-to-Speech) → MP3
  - FFmpeg processing: speeds up audio 1.4x (`atempo=1.4` filter)
  - mpg123 playback, cleanup temporary files

## Development Workflows

### Setup

```bash
pip install python-dotenv openai SpeechRecognition pyaudio gtts
# Requires: ffmpeg, mpg123 (macOS: brew install ffmpeg mpg123)
```

### Environment Variables

- **`.env`**: `OPENAI_API_KEY` required for `client = OpenAI(api_key=...)`

### Running the Agent

```bash
python main.py
# Exits on user input "exit"
```

### Testing New Features

- Add intent keywords in `detect_intent()` first
- Implement tool in `tools.py` and import in `main.py`
- Insert execution block before LLM response (order matters: tools before chat)

## Important Conventions

### When Modifying `tools.py`

- **Always handle text input** for intent-driven tools (e.g., `book_meeting(text)` not `book_meeting()`)
- `extract_datetime()` duplicated in both `main.py` and `tools.py` — keep in sync if updating parsing logic
- Tools are blocking; design for <100ms execution (not suitable for API calls without caching)

### Speech I/O Constraints

- **Timeouts**: `listen()` returns empty string, not exceptions—check return value in main loop
- **Audio Output**: `speak()` hardcoded file paths (`response.mp3`, `fast.mp3`)—not thread-safe
- **No streaming**: Full TTS generation + playback before returning control (blocking)

### LLM Integration

- **Model**: `gpt-4o-mini` (cost-optimized for dialogue)
- **Message Format**: Standard OpenAI Chat Completions API
- **No tool_use/function_calling**: LLM is stateless responder, not decision-maker

## Extending the Agent

### Adding a New Tool

1. Define function in `tools.py` accepting `text` parameter
2. Add keyword detection in `main.py` `detect_intent()`
3. Add execution block between line 57-70 (before LLM call)
4. Return string (auto-logged and spoken)

**Example**: Weather tool currently stubs; to integrate real API:

- Update `get_weather(location)` to parse location from user text (use `extract_datetime()` pattern)
- Call weather API
- Handle failures gracefully (return user-friendly message)

### Improving Intent Detection

- Current regex-based approach scales poorly (~4 keywords)
- For >5 tools: Consider ML-based classification (scikit-learn `MultinomialNB`) or LLM intent routing
- Always validate with repeated user inputs (speech recognition variance)

## Common Debugging Patterns

- **No Audio Capture**: Check microphone permissions + `pyaudio` installation
- **gTTS Failures**: Network issue or text too long (gTTS has ~100 char limit per chunk)
- **FFmpeg Errors**: Verify `ffmpeg` in PATH; `which ffmpeg` on macOS
- **Intent Confusion**: Print detected intent + user input to identify keyword overlap (e.g., "book the weather" ambiguity)
