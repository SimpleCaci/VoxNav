"""Speech recognition service for VoxNav."""

from typing import Optional

import speech_recognition as sr

from config import (
    LISTEN_TIMEOUT_SECONDS,
    PHRASE_TIME_LIMIT_SECONDS,
    AMBIENT_NOISE_ADJUST_SECONDS,
)


class SpeechService:
    """Handles microphone input and speech-to-text conversion."""

    def __init__(self) -> None:
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

    def calibrate_microphone(self) -> None:
        """Adjusts recognizer sensitivity to ambient noise."""
        print("🎤 Calibrating microphone...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(
                source,
                duration=AMBIENT_NOISE_ADJUST_SECONDS,
            )
        print("✅ Calibration complete.")

    def listen_once(self) -> Optional[str]:
        """Listens for a single phrase and returns normalized text."""
        try:
            print("🎧 Listening...")

            with self._microphone as source:
                audio_data = self._recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT_SECONDS,
                    phrase_time_limit=PHRASE_TIME_LIMIT_SECONDS,
                )

            text = self._recognizer.recognize_google(audio_data)

            normalized = text.strip().lower()

            print(f"🗣 Heard: {normalized}")

            return normalized

        except sr.WaitTimeoutError:
            print("⏱ No speech detected.")
            return None

        except sr.UnknownValueError:
            print("❌ Could not understand.")
            return None

        except sr.RequestError as error:
            print(f"⚠️ API error: {error}")
            return None

        except Exception as error:
            print(f"💥 Unexpected error: {error}")
            return None