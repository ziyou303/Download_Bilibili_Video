import re
import os
import json
import requests
from moviepy.editor import VideoFileClip, AudioFileClip


    # 定义B站网址
url = input('请输入B站视频网页的网址:')
    # 请求头
headers = {
    'cookie' : '这里要输入你账号的cookie，不然下不了',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'referer' : '{}'.format(url)
}

headers1 = {
    'cookie' : 'buvid3=E8333023-BAED-684F-C6B8-45894E5CFE3312181infoc; b_nut=1731770012; _uuid=2DE4275D-53AF-1C106-815F-7BDA57C36610B13761infoc; enable_web_push=DISABLE; home_feed_column=5; buvid4=AAC834C0-8223-E61B-BF76-37BED732586912973-024111615-7c0bHSTUoYGTSSqtnVY1jT4KjzGzeXr4sy7hI1XlJ1SGdrdOqrTdNeJysu0d0Y6Q; header_theme_version=CLOSE; DedeUserID=3537114517997966; DedeUserID__ckMd5=152243b0f5227deb; rpdid=0zbfAHVShC|n5fwkkHA|33f|3w1Tcl8t; CURRENT_QUALITY=80; LIVE_BUVID=AUTO8117323496333340; fingerprint=9ae7fedc9d0f609b0c5b5589d95158a6; buvid_fp_plain=undefined; buvid_fp=9ae7fedc9d0f609b0c5b5589d95158a6; SESSDATA=7492d85f%2C1748443778%2C4755f%2Ab2CjDHSNRoOmcLsmZ0wlernBS4ROkAEpzRxsBJWa6vHo0nMxc0cjQ8av_s49r97ulaBD0SVlNKOFRHNEdJR0VwdE1FY2poUFM1b00xWW1keGtoN0lOak83WkI5WHJTcVMyOEpzRHJqMmhlOVU1WHJqVGdqblIxaUZQX0tOSXpjNHBJaGF1VmFyWW9BIIEC; bili_jct=9a2e2dd38478554a2f12f9e99d589fb5; CURRENT_FNVAL=4048; browser_resolution=1912-954; b_lsid=C32A9CFD_1937D73D30A; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMyMzU4NzYsImlhdCI6MTczMjk3NjYxNiwicGx0IjotMX0.U2KUn879V3BZLrWB_UFX3Ug2L_-BNTXe0V9rAwpHPxc; bili_ticket_expires=1733235816; sid=7yfo7wp3; PVID=2; bp_t_offset_3537114517997966=1005630351424356352',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

    # 获取网页代码
response = requests.get(url, headers=headers).text

data = re.findall('60}}},(.*?),"p":1,"cidMap',response)

data = str(data).replace("'", '"')

aid = re.findall('aid":(.*?),"bvid',data)[0]
bvid = re.findall('bvid":"(.*?)","cid',data)[0]
cid = re.findall('cid":(.*?)"]',data)[0]

url1 = 'https://api.bilibili.com/x/player/wbi/playurl?avid={}&bvid={}&cid={}&qn=80&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&is_main_page=true&need_fragment=false&isGaiaAvoided=false&session=ce24d836e0470ec643e237b5588721a1&voice_balance=1&web_location=1315873&dm_img_list=[%7B%22x%22:805,%22y%22:-460,%22z%22:0,%22timestamp%22:2,%22k%22:123,%22type%22:0%7D]&dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ&dm_cover_img_str=QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNzMwICgweDAwMDA0NjgyKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC&dm_img_inter=%7B%22ds%22:[%7B%22t%22:2,%22c%22:%22dmlkZW8tY29udGFpbmVyLX%22,%22p%22:[341,71,327],%22s%22:[280,12893,-5696]%7D],%22wh%22:[5006,7337,112],%22of%22:[290,580,290]%7D&w_rid=d5a55302c169872db392c54399f67e86&wts=1732980373'.format(aid,bvid,cid)

html = requests.get(url1,headers=headers1).text

    # 转化为json数据
html = json.loads(html)
    # 获取信息
title = re.findall('title":"(.*?)","pubdate',response)[0]   #获取标题
audio_url = html['data']['dash']['audio'][0]['baseUrl']            #获取音频网址
video_url = html['data']['dash']['video'][1]['baseUrl']            #获取视频网址

    # 输出信息
#print(title)
#print(audio_url)
#print(video_url)

'''获取文件'''
    # 获取视频文件
video = requests.get(url=video_url, headers=headers).content
    # 获取音频文件
audio = requests.get(url=audio_url, headers=headers).content

    # 过滤掉非法字符
illegal_chars = r'[<>:"/\\|?*]'
file_name = re.sub(illegal_chars, '_', title)

'''写入文件'''
with open('{}.mp4'.format(file_name), 'wb') as f:   #写入视频文件
    f.write(video)
    f.close()

with open('{}.mp3'.format(file_name), 'wb') as f:   #写入音频文件
    f.write(audio)
    f.close()

'''显示和检查下载'''
    # 检查视频是否下载成功
if os.path.isfile('{}.mp4'.format(file_name)):
    print('{}.mp4保存成功！'.format(file_name))
else:
    exit('{}.mp4保存失败,重试一下帕'.format(file_name))

    # 检查音频是否下载成功
if os.path.isfile('{}.mp3'.format(file_name)):
    print('{}.mp3保存成功！'.format(file_name))
else:
    exit('{}.mp3保存失败,重试一下帕'.format(file_name))

'''视频和音频合拼'''

    # 读取视频和音频文件
video_clip = VideoFileClip('{}.mp4'.format(file_name))
audio_clip = AudioFileClip('{}.mp3'.format(file_name))

    # 将音频设置到视频中，如果视频原本有音乐，可以选择.set_audio(audio_clip, 0)来替换
final_clip = video_clip.set_audio(audio_clip)

    # 检查是否存在保存文件的文件夹路径
if not os.path.exists('视频'):
    os.makedirs('视频')

    # 输出文件路径
output_path = '视频/{}.mp4'.format(file_name)

    # 保存合成的视频
final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', threads=10)

    # 删除原视频和音频
os.remove('{}.mp4'.format(file_name))
os.remove('{}.mp3'.format(file_name))

    # 显示和检查完成信息
if os.path.isfile('视频/{}.mp4'.format(file_name)):
    print('{}.mp4保存成功！'.format(file_name))
else:
    exit('{}.mp4保存失败,重试一下帕'.format(file_name))

input('按下回车键退出!')
