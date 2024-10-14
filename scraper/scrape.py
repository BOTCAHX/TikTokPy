import requests
from bs4 import BeautifulSoup

def tt_scrape(url):
    try:
        data = {
            'q': url,
            'lang': 'id'
        }
        headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "X-Forwarded-For": "104.21.14.35"
       }

        response = requests.post('https://tikvideo.app/api/ajaxSearch', data=data, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.json()['data'], 'html.parser')

        title = soup.select_one('.clearfix h3').get_text(strip=True)

        video = []
        audio = []

        for a in soup.select('.dl-action a'):
            text = a.get_text(strip=True)
            href = a['href']
            if 'Unduh MP4 HD' in text:
                video.append(href)
            elif 'Unduh MP3' in text:
                audio.append(href)

        if not video:
            for a in soup.select('.dl-action a'):
                text = a.get_text(strip=True)
                href = a['href']
                if 'Unduh MP4' in text:
                    video.append(href)
                    break

        if not video:
            for item in soup.select('.download-items'):
                download_url = item.select_one('a')['href']
                if download_url:
                    video.append(download_url)

        if not video:
            convert_button = soup.select_one('#ConvertToVideo')
            if convert_button:
                audio_url = convert_button['data-audiourl']
                image_data = convert_button['data-imagedata']
                if audio_url and audio_url not in audio:
                    audio.append(audio_url)
                if image_data:
                    images = [img for img in image_data.split(';') if img]
                    video.extend(images)

        return {
            'status': True,
            'title': title,
            'video': video,
            'audio': audio
        }
    except Exception as error:
        print(f'Error: {error}')
        return {
            'status': False,
            'message': str(error)
        }
