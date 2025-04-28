import time, re, os, requests, browser_cookie3, json, sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse

global cookies
cookies = browser_cookie3.firefox()

url_regex = '(?<=\.com/)(.+?)(?=\?|$)'
video_id_regex = '(?<=/video/)([0-9]+)'

headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}

def is_tiktok_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname == 'www.tiktok.com' or parsed_url.hostname == 'tiktok.com' or parsed_url.hostname == 'm.tiktok.com'

def get_tiktok_json(video_url, browser_name=None):
    global cookies
    if browser_name is not None:
        cookies = getattr(browser_cookie3, browser_name)(domain_name=".tiktok.com")
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    cookies = tt.cookies
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id':"__UNIVERSAL_DATA_FOR_REHYDRATION__"})
    try:
        tt_json = json.loads(tt_script.string)
    except AttributeError:
        return
    return tt_json

def save(video_url, save_video=False, browser_name="firefox"):
    if not save_video:
        return
    tt_json = get_tiktok_json(video_url, browser_name)
    def download_file(url, filename):
        headers['referer'] = 'https://www.tiktok.com/'
        response = requests.get(url, allow_redirects=True, headers=headers, cookies=cookies)
        with open(filename, "wb") as f:
            f.write(response.content)
    if not tt_json:
        print("Failed to get tiktok data")
        return
    try:
        video_id = list(tt_json['ItemModule'].keys())[0]
        data_slot = tt_json['ItemModule'][video_id]
    except (KeyError, IndexError):
        data_slot = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']

    base_filename = re.findall(url_regex, video_url)[0].replace('/', '_')

    if save_video:
        if 'imagePost' in data_slot:
            for idx, slide in enumerate(data_slot['imagePost']['images'], start=1):
                slide_filename = f"{base_filename}_slide_{idx}.jpeg"
                download_file(slide['imageURL']['urlList'][0], slide_filename)
        else:
            try:
                video_url_to_download = data_slot['video']['playAddr']
                #print(data_slot['video'])
            except KeyError:
                video_url_to_download = data_slot['video']['playAddr']
            
            video_filename = f"{base_filename}.mp4"
            download_file(video_url_to_download, video_filename)
            print("Saved video to", os.getcwd())

print("Enter the URL of the video you want to download: ")
video_url = input()

if not video_url:
    print("URL cannot be empty")
    time.sleep(2)
    exit()
else:
    if not video_url.startswith(('http://', 'https://')):
        video_url = f"https://{video_url}"
    if not is_tiktok_url(video_url):
        print(f"{video_url} is not a valid tiktok URL")
        time.sleep(2)
        exit()
    else:
        try:
            save(video_url, True, "firefox")
            print("Downloaded")
            time.sleep(1)
        except Exception as e:
            print(f"Err: {e} | Line: {sys.exc_info()[-1].tb_lineno}")
            time.sleep(2)
            exit()

# originally made by https://github.com/ripsaku
# remade by yours truly :3