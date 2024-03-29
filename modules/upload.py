import json
import os
from pyrogram.types import Message
import subprocess

if os.name == 'nt':
    APP = "./go-ul_x64.exe"
else:
    APP = "./go-ul_x64"

SERVICES = ['anonfiles', 'catbox', 'fileio', 'filemail', 'gofile', 'krakenfiles', 'letsupload', 'megaup',
            'mixdrop', 'pixeldrain', 'racaty', 'transfersh', 'uguu', 'wetransfer', 'workupload', 'zippyshare']

reply_message = """
**Name :** `{0}`
**Host :** `{1}`
**URL  :** {2}"""


def upload(filePath: str, serviceID: int, message: Message, progressMessage: Message):
    file_name = os.path.basename(filePath)
    print(f"Uploading `{file_name}` to {SERVICES[serviceID]}", flush=True)
    progressMessage.edit_text(
        f"Uploading to {SERVICES[serviceID]}...\n`{file_name}` ")

    subprocess.Popen([APP, SERVICES[serviceID],
                     '-f', filePath, '-j', 'response.json']).wait()

    response = json.load(open('response.json'))

    if not response['jobs'][-1]['ok']:
        message.reply_text(f"`{response['jobs'][-1]['error_text']}`")
        raise Exception(f"{response['jobs'][-1]['error_text']}")
    else:
        message.reply_text(reply_message.format(
            response['jobs'][-1]['filename'], SERVICES[serviceID], response['jobs'][-1]['url']), disable_web_page_preview=True, quote=True)
        print(f"Uploaded to {SERVICES[serviceID]}", flush=True)
    return 0
