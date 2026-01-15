import speech_recognition as sr


def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening... (you can speak freely)")

        # Adjust for background noise
        r.adjust_for_ambient_noise(source, duration=0.5)

        # Listen longer
        audio = r.listen(source, timeout=5, phrase_time_limit=10)

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
