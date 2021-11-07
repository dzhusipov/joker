import time
import requests
import m3u8

headers = {
    'sec-ch-ua-platform': '"macOS"',
    'accept': '*/*',
    'origin': 'https://live.jugru.org',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://live.jugru.org/',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,bg;q=0.6,fr;q=0.5,ms;q=0.4',
    'cookie': 'CloudFront-Key-Pair-Id=K1V2UN4D5000CV; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3RyZWFtLWxpdmUuanVncnUub3JnLzEwMDEwNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjM2MjU4NTM0fX19XX0_; CloudFront-Signature=uzyr4kJ6SYDfZGTjE0O30pTnMKtN69QFQIjnsXqpPd-v4hgR9SozyUOtLh5ySsyy0EEEHpMNNAn68TPzJpe09qFXrq15JZ9MlEBR-yqeRR4eE-F547RBWOeEfgc7s0q5Ao4FIjVc8i~4JKrpGvyzSJAa0wcr856crur7PXHD2V76c8UlIE5oJ8huJboVeHNRW7OwIvLdIvrIcvDrWDzewD1sduMY-mHNn6rD5dBt0LWHsXzRcKvYTf7VojFStukPo2FVpD-61wyyZCm~svET72q1YO7IJ6KpzrTNOsgNPfDSjbp-X1VYwtPaBuqhBMfaSsxauAOzX18rGi-h2AjjlQ__; _ym_uid=1635936822981967228; _ym_d=1635936822; _iidt=BNL5ktIE/QgMt+eh22Tl3ttJfAai0NyxdWllgi/a2n7k1mUNAvWnrjTvUAdvZb8HKVLSx8INtfLUYg==; _vid_t=nz05Lf6HPy+uZEPxIg6eomhhapiokdlMSD6rePlt7iY9xyjjKY7L6xcqvB5GIK/DRyjyJbZonLlkMQ==; _gid=GA1.2.502599212.1636119004; _ym_isad=1; _ga=GA1.2.464156982.1635936822; _ga_SED333H5P7=GS1.1.1636258266.14.1.1636258409.0',
}


def get_real_url(url):
    # playlist = m3u8.load(uri=url, headers=headers)
    # print(playlist.data)
    return 'https://stream-live.jugru.org/100104/'


def download_m3u8_video(url, save_name):
    # real_url = get_real_url(url)
    playlist = m3u8.load('playlist.m3u8')
    real_url = 'https://stream-live.jugru.org/100104/'
    n = len(playlist.segments)
    size = 0
    start = time.time()
    for i, seg in enumerate(playlist.segments, 1):
        print(seg.absolute_uri)
        r = requests.get(real_url + seg.absolute_uri, headers=headers)
        data = r.content
        size += len(data)
        with open(save_name, "ab" if i != 1 else "wb") as f:
            f.write(data)
        print(
            f"\r Download Progress({i}/{n})，Downloaded:{size/1024/1024:.2f}MB，Download time consumed:{time.time()-start:.2f}s", end=" ")


download_m3u8_video('https://stream-live.jugru.org/100104/10007151_1920.m3u8', 'Practical steps for creating safer software.mp4')

