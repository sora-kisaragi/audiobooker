import httpx
import asyncio
import sys


async def check_connectivity(base_url: str, profile_name: str = "default.pt"):
    """
    Verifies if the Qwen-TTS API server is reachable and the specified profile exists.
    """
    endpoint = f"{base_url}/tts/voice-clone/profile"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # We try to get the profile or list profiles to verify connectivity
            # According to the plan, we just need to check if the server is up
            # and the profile is available.
            response = await client.get(endpoint, params={"profile": profile_name})

            if response.status_code == 200:
                print(f"✅ Success: Connected to TTS server at {base_url}")
                print(f"✅ Success: Profile '{profile_name}' is available.")
                return True
            elif response.status_code == 404:
                print(
                    f"⚠️ Warning: Connected to server, but profile '{profile_name}' not found (404)."
                )
                return False
            else:
                print(f"❌ Error: Server responded with status {response.status_code}")
                print(f"Response: {response.text}")
                return False

    except httpx.ConnectError:
        print(
            f"❌ Error: Could not connect to the server at {base_url}. Is the server running?"
        )
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


if __name__ == "__main__":
    # Default values, can be moved to config later
    URL = "http://localhost:7865"
    PROFILE = "default.pt"

    if len(sys.argv) > 1:
        URL = sys.argv[1]
    if len(sys.argv) > 2:
        PROFILE = sys.argv[2]

    print(f"Checking connectivity to {URL} with profile {PROFILE}...")
    success = asyncio.run(check_connectivity(URL, PROFILE))
    sys.exit(0 if success else 1)
