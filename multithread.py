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
    'cookie': 'CloudFront-Key-Pair-Id=K1V2UN4D5000CV; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3RyZWFtLWxpdmUuanVncnUub3JnLzEwMDEwNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjM2MjA4NzE1fX19XX0_; CloudFront-Signature=KELA-Pk4UX-VlQPlbUh6X6eDt5B1Sf2ZS76LTKaXHBE2LdncKKHqBz2Zp75ams6QDWCIaLzh6DFxvBlqB4b2lCWLB-4rLP3VDdPGGaEVWIsBjXyfFXoqxeeto04CHU8i7o7HkUyR-p9PMvPArVZr4yVwn5puSieq8106oS2~S1fNUMteuyXFY3VsRPJVgILC36mCNTm8ZoEOyzx7BL4LRyjHIloUiQH-ZDQUjPMWE37I6k3v4VK6A5ojcsgP9Phxl55bj7V4ZT2irNmgO6yCard0z-tzX-jhSCL6LssMIa-PiZK-Fo5BROtUtlOEmg4~0BVnxa9l8U~YKCMP8SCHBw__; _ym_uid=1635936822981967228; _ym_d=1635936822; _iidt=BNL5ktIE/QgMt+eh22Tl3ttJfAai0NyxdWllgi/a2n7k1mUNAvWnrjTvUAdvZb8HKVLSx8INtfLUYg==; _vid_t=nz05Lf6HPy+uZEPxIg6eomhhapiokdlMSD6rePlt7iY9xyjjKY7L6xcqvB5GIK/DRyjyJbZonLlkMQ==; _gid=GA1.2.502599212.1636119004; _ym_isad=1; _dc_gtm_UA-32146946-44=1; _ga=GA1.1.464156982.1635936822; _ga_SED333H5P7=GS1.1.1636205266.12.1.1636208594.0',
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
        for file in files:
            with open(file, 'rb') as fr:
                fw.write(fr.read())
                print(f'\r{file}Merged!Total:{len(files)}', end="     ")
            os.remove(file)


download_m3u8_video('DDDamn good.mp4')
