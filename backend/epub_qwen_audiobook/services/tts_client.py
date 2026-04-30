import httpx
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QwenTTSClient:
    """
    Client for interacting with the Qwen-TTS API server.
    """

    def __init__(
        self,
        base_url: str,
        profile_name: str = "default.pt",
        language: str = "japanese",
    ):
        self.base_url = base_url.rstrip("/")
        self.profile_name = profile_name
        self.language = language
        self.endpoint = f"{self.base_url}/tts/voice-clone/profile"

    async def synthesize(self, text: str, output_path: Path) -> bool:
        """
        Sends text to the TTS server and saves the resulting audio file.
        """
        payload = {
            "text": text,
            "profile": self.profile_name,
            "language": self.language,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.endpoint, json=payload)

                if response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return True
                else:
                    logger.error(
                        f"TTS API Error ({response.status_code}): {response.text}"
                    )
                    return False

        except httpx.RequestError as e:
            logger.error(f"TTS Request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during synthesis: {e}")
            return False
