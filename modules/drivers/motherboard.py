import re as regexp
import webbrowser
import modules.misc.global_vars as global_vars


def _normalize(input_string: str) -> str:
    if not input_string:
        return ""
    input_string = input_string.lower()
    # drop generic corporate words
    input_string = regexp.sub(r"\b(technology|computer|company|co|co\.|inc|inc\.|ltd|ltd\.|corp|corporation)\b", " ", input_string)
    # remove punctuation, collapse spaces
    input_string = regexp.sub(r"[^a-z0-9]+", " ", input_string)
    return regexp.sub(r"\s+", " ", input_string).strip()


def get_cache() -> dict[str, str]:
    # the keys here should be human readable and exactly the same as if you were to run `print(global_vars.FULL_MOTHERBOARD_NAME.lower())`
    raw_cache = {
        "gigabyte technology co., ltd. b660m ds3h ax ddr4": "https://www.gigabyte.com/Motherboard/B660M-DS3H-AX-DDR4-rev-1x/support",
        "gigabyte technology co., ltd. b650 aorus elite ax": "https://www.gigabyte.com/Motherboard/B650-AORUS-ELITE-AX-rev-10-11/support#dl"
    }

    return {_normalize(k): v for k, v in raw_cache.items()}


def show_motherboard_driver_page():
    raw_name = global_vars.FULL_MOTHERBOARD_NAME.strip()
    key = _normalize(raw_name)
    cache = get_cache()

    if key in cache:
        webbrowser.open_new_tab(cache[key])
    else:
        webbrowser.open_new_tab(f"https://duckduckgo.com/?q=motherboard+drivers+for+{raw_name.replace(' ', '+')}")
