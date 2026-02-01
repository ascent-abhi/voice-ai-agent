import speech_recognition as sr
import time


def listen(max_attempts=3, use_continuous=False):
    """
    Enhanced voice input with support for longer, more natural speech.

    Args:
        max_attempts: Maximum number of recognition attempts before giving up
        use_continuous: If True, uses continuous listening mode for very long inputs

    Returns:
        Recognized text string, or empty string if recognition fails
    """
    r = sr.Recognizer()

    # Optimized tuning for natural pauses and longer speech
    r.pause_threshold = 1.5  # Reduced from 2.0 - less wait time, faster response
    r.phrase_threshold = 0.2  # Reduced from 0.3 - more sensitive to speech start
    r.non_speaking_duration = 0.8  # Reduced from 1.0 - quicker to detect end of speech
    r.energy_threshold = 300  # Default energy threshold for better detection

    # Dynamic adjustment for longer speech patterns
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5

    with sr.Microphone() as source:
        print("🎤 Listening... (speak naturally, I'll catch longer responses)")

        # Enhanced calibration with longer duration for better noise adjustment
        print("🔧 Calibrating microphone for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1.5)
        print("✅ Ready! You can start speaking.")

        # Use continuous listening for very long responses (sales conversations)
        if use_continuous:
            return _listen_continuous(r, source)
        else:
            return _listen_standard(r, source, max_attempts)


def _listen_standard(r, source, max_attempts):
    """Standard listening mode with retry logic and extended time limits."""

    for attempt in range(max_attempts):
        try:
            # Extended timeouts for longer, more thoughtful responses
            audio = r.listen(
                source,
                timeout=10,  # Increased from 6 - wait longer for user to start speaking
                phrase_time_limit=60,  # Increased from 20 - allow up to 60 seconds of speech
            )

            # Primary recognition attempt with Google
            text = r.recognize_google(audio, language="en-US", show_all=False)
            print(f"✅ You: {text}")
            return text

        except sr.WaitTimeoutError:
            if attempt < max_attempts - 1:
                print(
                    f"⏳ No speech detected. Attempt {attempt + 1}/{max_attempts}. Listening again..."
                )
                time.sleep(0.5)
                continue
            else:
                print("⏳ No speech detected after multiple attempts.")
                return ""

        except sr.UnknownValueError:
            if attempt < max_attempts - 1:
                print(
                    f"❓ Could not understand. Attempt {attempt + 1}/{max_attempts}. Please try again..."
                )
                time.sleep(0.5)
                continue
            else:
                print("❌ Could not understand audio after multiple attempts.")
                return ""

        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            if attempt < max_attempts - 1:
                print(f"Retrying... ({attempt + 1}/{max_attempts})")
                time.sleep(1)
                continue
            else:
                return ""

    return ""


def _listen_continuous(r, source):
    """
    Continuous listening mode for very long responses.
    Collects multiple audio chunks and combines them.
    """
    print("📝 Continuous mode: I'll keep listening until you pause for 3 seconds.")
    print("💡 Say 'done' or pause for 3 seconds when finished.")

    full_text = []
    silence_count = 0
    max_silence = 3  # seconds of silence before stopping

    try:
        while silence_count < max_silence:
            try:
                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=30,  # Process in 30-second chunks
                )

                text = r.recognize_google(audio, language="en-US")

                if text.lower().strip() == "done":
                    break

                full_text.append(text)
                print(f"📝 [Chunk {len(full_text)}]: {text}")
                silence_count = 0  # Reset silence counter on successful recognition

            except sr.WaitTimeoutError:
                silence_count += 1
                if silence_count < max_silence:
                    print("⏸️  ... (listening for more)")
                    continue
                else:
                    break

            except sr.UnknownValueError:
                silence_count += 1
                if silence_count < max_silence:
                    continue
                else:
                    break

        if full_text:
            combined_text = " ".join(full_text)
            print(f"✅ Complete response: {combined_text}")
            return combined_text
        else:
            print("❌ No speech detected in continuous mode.")
            return ""

    except KeyboardInterrupt:
        print("\n⚠️  Listening interrupted by user.")
        if full_text:
            return " ".join(full_text)
        return ""
