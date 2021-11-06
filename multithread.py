import glob
from concurrent.futures import ThreadPoolExecutor
import m3u8
import os
import requests

headers = {
    'sec-ch-ua-platform': '"macOS"',
    'accept': '*/*',
    'origin': 'https://live.jugru.org',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://live.jugru.org/',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,bg;q=0.6,fr;q=0.5,ms;q=0.4',
    'cookie': 'CloudFront-Key-Pair-Id=K1V2UN4D5000CV; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3RyZWFtLWxpdmUuanVncnUub3JnLzEwMDEwNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjM2MjE0OTU4fX19XX0_; CloudFront-Signature=RM704jXpLoc1fbpU3ScshYzZiU9Eg5HFB6kigW0HPxu94Fj6bMZXBRnacmNH9uSZXHXhHow8H8j~4Tk-VnKjQkRtFJCajxXaBKcLzWU9Z-XclRuDBH30D9dxgRoFqFPGPvL8TF~tq2CS9tIG9esr54meOmpOCls8Bcpx2-QMK-C6uioRGuPl-ovMS49iCqWG11PBqlH9bxT6h7l2O5Jvk2UWtqwWm-iQ8uw9Wtu-Cy3bD6ppAG-m7kbErgy4EtEXFGk4ucPaUP33s5thnXto5atGrnPQrODU2vhBTEPcMo-2i-xpVATgZ~lZOUowy95oZpMByIKpAyOYzUvyI-31bw__; _ym_uid=1635936822981967228; _ym_d=1635936822; _iidt=BNL5ktIE/QgMt+eh22Tl3ttJfAai0NyxdWllgi/a2n7k1mUNAvWnrjTvUAdvZb8HKVLSx8INtfLUYg==; _vid_t=nz05Lf6HPy+uZEPxIg6eomhhapiokdlMSD6rePlt7iY9xyjjKY7L6xcqvB5GIK/DRyjyJbZonLlkMQ==; _gid=GA1.2.502599212.1636119004; _ym_isad=1; _ga=GA1.2.464156982.1635936822; _ga_SED333H5P7=GS1.1.1636211963.13.1.1636213563.0',
}


def download_ts(url, i):
    r = requests.get(url, headers=headers)
    data = r.content
    with open(f"tmp/{i:0>5d}.ts", "ab") as f:
        f.write(data)
    print(f"\r{i:0>5d}.ts Downloaded", end="  ")


def download_m3u8_video(save_name, max_workers=2000):
    if not os.path.exists("tmp"):
        os.mkdir('tmp')

    real_url = 'https://stream-live.jugru.org/100104/'
    playlist = m3u8.load('playlist.m3u8')
    # key = requests.get(playlist.keys[-1].uri, headers=headers).content

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for i, seg in enumerate(playlist.segments):
            pool.submit(download_ts, real_url + seg.absolute_uri, i)

    with open(save_name, 'wb') as fw:
        files = glob.glob('tmp/*.ts')
        files.sort()
        for file in files:
            with open(file, 'rb') as fr:
                fw.write(fr.read())
                print(f'\r{file}Merged!Total:{len(files)}', end="     ")
            os.remove(file)


def test():
    files = glob.glob('tmp/*.ts')
    files.sort()
    print(files)


download_m3u8_video('Расширяем возможности kotlinx.serialization с помощью Arrow Meta.mp4')
