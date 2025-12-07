import webbrowser
import modules.misc.global_vars as gv
from urllib.parse import quote


def _normalize(input_string: str) -> str:
    # not too useful rn but makes it easier to expand on later
    return input_string.lower()


def get_cache() -> dict[str, str]:
    # the keys here should be human readable and exactly the same
    # as if you were to run `print(global_vars.FULL_MOTHERBOARD_NAME.lower())`
    raw_cache = {
        "gigabyte technology co., ltd. b660m ds3h ax ddr4": "https://www.gigabyte.com/Motherboard/B660M-DS3H-AX-DDR4-rev-1x/support#dl",  # noqa: E501
        "micro-star international co., ltd. mpg b550 gaming plus (ms-7c56)": "https://www.msi.com/Motherboard/MPG-B550-GAMING-PLUS/support",  # noqa: E501
        "gigabyte technology co., ltd. b650 aorus elite ax": "https://www.gigabyte.com/Motherboard/B650-AORUS-ELITE-AX-rev-10-11/support#dl",  # noqa: E501
        "gigabyte technology co., ltd. b650 gaming x ax": "https://www.gigabyte.com/Motherboard/B650-GAMING-X-AX-rev-10-11-12/support#dl",  # noqa: E501
        "gigabyte technology co., ltd. b560m d3h": "https://www.gigabyte.com/Motherboard/B560M-D3H-rev-1x/support",  # noqa: E501
        "asustek computer inc. h81m-d": "https://www.asus.com/supportonly/h81md/helpdesk_download/",  # noqa: E501
        "gigabyte technology co., ltd. b650 gaming x ax v2": "https://www.gigabyte.com/us/Motherboard/B650-GAMING-X-AX-V2-rev-1x/support#dl"  # noqa: E501
    }

    return {_normalize(k): v for k, v in raw_cache.items()}


def show_motherboard_driver_page():
    cache = get_cache()
    key = _normalize(gv.FULL_MOTHERBOARD_NAME.strip())
    value = cache.get(key)

    if value:
        webbrowser.open_new_tab(value)
    else:
        board = quote(gv.FULL_MOTHERBOARD_NAME.strip().replace(' ', '+'))
        url = f"https://duckduckgo.com/?q=motherboard+drivers+for+{board}"
        webbrowser.open_new_tab(url)
