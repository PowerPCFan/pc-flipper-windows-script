import hashlib
import requests


def upload_to_blinkbin(text: str) -> str:
    api = "https://bin.blinkl.ink"
    try:
        c = requests.get(f"{api}/api/challenge", timeout=10)
        c.raise_for_status()
        data = dict(c.json())

        challenge, difficulty = data.get("challenge"), data.get("difficulty")
        if not challenge or not difficulty:
            return ""

        nonce = 0
        zeroes = "0" * difficulty
        while True:
            sha256_hash = hashlib.sha256(f"{challenge}{nonce}".encode()).hexdigest()
            if sha256_hash.startswith(zeroes):
                break
            nonce += 1

        resp = requests.post(f"{api}/api/paste", json={
            "paste": text,
            "challenge": challenge,
            "nonce": nonce,
        }, timeout=10)
        resp.raise_for_status()
        result = dict(resp.json())

        print(result)

        paste_hash = result.get("paste_hash")
        edit_token = result.get("edit_token")  # currently unused, but it's the token that would be used to edit a paste
        if not paste_hash:
            return ""

        return f"https://bin.blinkl.ink/{paste_hash}"
    except Exception as e:
        print(f"BlinkBin upload failed: {e}")
        return ""
