import os
from modules.misc import utils
import modules.misc.global_vars as global_vars

def save(save_location: str = os.path.join(global_vars.CURRENT_USER_DESKTOP, "spec_sheet.html")):
    styles = """

body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #1c1c1c;
    color: #ebebeb;
}

ul {
    margin: 0;
}

h2 {
    margin-bottom: 0.5rem;
}

"""


    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Spec Sheet</title>
    <style>{styles}</style>
</head>
<body>
    <h1>PC Spec Sheet</h1>
    <h2>General Information</h2>
    <ul>
        <li><strong>PC Name:</strong> {global_vars.PC_NAME.strip('-')}</li>
        <li><strong>OS:</strong> {global_vars.WINDOWS_OS_VERSION}</li>
        <li><strong>OS Architecture:</strong> {'64-bit' if global_vars.OS_IS_64BIT else '32-bit'}</li>
        <li><strong>OS Install Date:</strong> {(utils.parse_windows_timestamp(global_vars.INSTALL_TIME)).strftime("%B %d, %Y at %I:%M %p")}</li>
    </ul>
    <h2>Hardware Information</h2>
    <ul>
        <li><strong>CPU:</strong> {global_vars.CPU}</li>
        <li><strong>GPU:</strong> {global_vars.GPU}</li>
        <li><strong>RAM:</strong> {global_vars.RAM}</li>
        <li><strong>Motherboard:</strong> {global_vars.FULL_MOTHERBOARD_NAME}</li>
        <li><strong>Storage:</strong> {global_vars.STORAGE}</li>
        <li><strong>Display Information:</strong> {utils.get_display_info()}</li>
    </ul>
    <h2>Network Information</h2>
    <ul>
        <li><strong>Local IP:</strong> {global_vars.LOCAL_IP}</li>
        <li><strong>Public IP:</strong> {global_vars.PUBLIC_IP}</li>
    </ul>
</body>
</html>
"""
    with open(save_location, "w") as f:
        f.write(html)
