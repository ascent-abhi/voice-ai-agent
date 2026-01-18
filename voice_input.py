import speech_recognition as sr


def listen():
    r = sr.Recognizer()

    # Make it more tolerant to pauses
    r.pause_threshold = 2  # seconds of silence before stopping
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 1

    with sr.Microphone() as source:
        print("🎤 Listening...")

        # Adjust to background noise
        r.adjust_for_ambient_noise(source, duration=0.8)

        audio = r.listen(source, timeout=5, phrase_time_limit=15)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text

    except sr.WaitTimeoutError:
        print("⏳ No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
