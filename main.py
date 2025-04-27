import io
import sys
import rich
import time
from rich import print
from rich.console import Console
from urllib.parse import urlparse

console = Console()

old_stdout = sys.stdout
sys.stdout = io.StringIO()

import pyktok as pyk

sys.stdout = old_stdout

def is_tiktok_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname == 'www.tiktok.com' or parsed_url.hostname == 'tiktok.com' or parsed_url.hostname == 'm.tiktok.com'

console.clear()

console.print(f"""\n\n
             ⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠿⠿⢿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠘⣿⣆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠘⢿⣷⣄⣀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠙⠛⠿⢿⣿                        [bold deep_sky_blue3]TIKTOK VIDEO DOWNLOADER[/bold deep_sky_blue3]
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⢸⣿⡇⠀⠀⣴⣦⣄⡀⠀⠀⢸⣿                           [bold deep_sky_blue3]GITHUB.COM/RIPSAKU[/bold deep_sky_blue3]
⠀⠀⠀⢀⣠⣶⣾⠿⢿⣿⡇⠀⢸⣿⡇⠀⠀⣿⣿⠻⠿⣿⣶⣾⣿
⠀⠀⣰⣿⠟⠉⠀⠀⢸⣿⡇⠀⢸⣿⡇⠀⠀⣿⣿⠀⠀⠀⠀⠀⠁
⠀⣾⡿⠃⠀⠀⣠⣴⣾⣿⠇⠀⢸⣿⡇⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀
⢸⣿⠃⠀⠀⣼⡿⠋⠀⠀⠀⠀⢸⣿⡇⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀
⣿⣿⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀
⢸⣿⡀⠀⠀⢿⣷⡀⠀⠀⠀⢀⣼⣿⠁⠀⠀⣿⡟⠀⠀⠀⠀⠀⠀
⠈⢿⣧⡀⠀⠈⠻⢿⣷⣶⣾⡿⠟⠁⠀⠀⣼⡿⠃⠀⠀⠀⠀⠀⠀
⠀⠈⢻⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠉⠻⢿⣷⣦⣤⣤⣤⣴⣶⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""", style="purple")

console.print(f"[bold royal_blue1]Video link: [/bold royal_blue1]", end="")
video_url = input()

if not video_url:
    console.print("[bold red]Error:[/bold red] URL cannot be empty.")
    time.sleep(2.4)
    exit()
else:
    if not video_url.startswith(('http://', 'https://')):
        video_url = f"https://{video_url}"

    if not is_tiktok_url(video_url):
        console.print(f"[bold red]Error:[/bold red] '{video_url}' is not a valid TikTok URL.")
        time.sleep(2.4)
        exit()
    else:
        try:
            pyk.save_tiktok(video_url, True, '')
            console.print("[bold green]Download completed![/bold green]")
        except Exception as e:
            console.print(f"[bold red]Download error:[/bold red] {e}")
            console.print("[italic yellow]The video might be private, deleted, or the URL is incorrect.[/italic yellow]")
            time.sleep(2.4)
            exit()

#github.com/ripsaku