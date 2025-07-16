import webbrowser
import modules.misc.global_vars as global_vars

def show_motherboard_driver_page():
    search_url = f"https://duckduckgo.com/?q=motherboard+drivers+for+{global_vars.FULL_MOTHERBOARD_NAME.replace(' ', '+')}"
    webbrowser.open_new_tab(search_url)