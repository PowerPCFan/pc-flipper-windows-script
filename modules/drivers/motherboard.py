import webbrowser
import modules.misc.global_vars as gv
from urllib.parse import quote


def _normalize(input_string: str) -> str:
    return input_string.lower()

    # i dont really need this so i commented it out

    # if not input_string:
    #     return ""
    # input_string = input_string.lower()
    # input_string = regexp.sub(r"\b(technology|computer|company|co|co\.|inc|inc\.|ltd|ltd\.|corp|corporation)\b", " ", input_string)
    # input_string = regexp.sub(r"[^a-z0-9]+", " ", input_string)
    # return regexp.sub(r"\s+", " ", input_string).strip()


def get_cache() -> dict[str, str]:
    # the keys here should be human readable and exactly the same as if you were to run `print(global_vars.FULL_MOTHERBOARD_NAME.lower())`
    raw_cache = {
        "gigabyte technology co., ltd. b660m ds3h ax ddr4": "https://www.gigabyte.com/Motherboard/B660M-DS3H-AX-DDR4-rev-1x/support#dl",
        "micro-star international co., ltd. mpg b550 gaming plus (ms-7c56)": "https://www.msi.com/Motherboard/MPG-B550-GAMING-PLUS/support",
        "gigabyte technology co., ltd. b650 aorus elite ax": "https://www.gigabyte.com/Motherboard/B650-AORUS-ELITE-AX-rev-10-11/support#dl",
        "gigabyte technology co., ltd. b650 gaming x ax": "https://www.gigabyte.com/Motherboard/B650-GAMING-X-AX-rev-10-11-12/support#dl",
        "gigabyte technology co., ltd. b560m d3h": "https://www.gigabyte.com/Motherboard/B560M-D3H-rev-1x/support",
        "asustek computer inc. h81m-d": "https://www.asus.com/supportonly/h81md/helpdesk_download/",
        "gigabyte technology co., ltd. b650 gaming x ax v2": "https://www.gigabyte.com/us/Motherboard/B650-GAMING-X-AX-V2-rev-1x/support#dl"
    }

    return {_normalize(k): v for k, v in raw_cache.items()}


def show_motherboard_driver_page():
    cache = get_cache()
    key = _normalize(gv.FULL_MOTHERBOARD_NAME.strip())
    value = cache.get(key)

    if value:
        webbrowser.open_new_tab(value)
    else:
        url = f"https://duckduckgo.com/?q=motherboard+drivers+for+{quote(gv.FULL_MOTHERBOARD_NAME.strip().replace(' ', '+'))}"
        webbrowser.open_new_tab(url)
