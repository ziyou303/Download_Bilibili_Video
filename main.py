import re
import os
import json
import requests
from moviepy.editor import VideoFileClip, AudioFileClip


    # 定义B站网址
url = input('请输入B站视频网页的网址:')
    # 请求头
headers = {
    'cookie' : 'buvid3=6F94F4E6-4132-3C3E-DF09-352F2D9D8C8135015infoc; b_nut=1723015035; _uuid=EC8F3D2A-5159-DA2D-367F-F10122E951CE735889infoc; enable_web_push=DISABLE; buvid4=1D9C2DAD-C2B1-9A10-E222-543C77981DB535636-024080707-XNpG6IqcuzN%2BK0svoZvmP5VgM9AzvdJWbGDwjYg7PNKk4BrfHb%2BH%2Fi0xbzVyNDxK; DedeUserID=3537114517997966; DedeUserID__ckMd5=152243b0f5227deb; header_theme_version=CLOSE; rpdid=0zbfAHVShz|1hbyB62X8|10|3w1SBAVo; hit-dyn-v2=1; CURRENT_BLACKGAP=0; fingerprint=fea1d2fc9676d62d7a7d41badca7a117; buvid_fp_plain=undefined; home_feed_column=5; browser_resolution=1872-956; LIVE_BUVID=AUTO8917231035013411; PVID=2; SESSDATA=4e13f6c6%2C1739111135%2C1041a%2A82CjBsl_9z7oJH7MJCYXivC1GNLOtUfN6JXMjFbwt-eR73vZK5lAU6VS2eUx2-yWttXkgSVnY0UXdhUXE0YXhqRzgwcjVvTFlnU1RPYjREQWJQSmlCdjNLMjVaNmsweXBrTUtHR1BpT2Q2YTNRcnBjVmx0WnlTZDBHODVpOHpqbkROR1MwNURyelBBIIEC; bili_jct=ded256eb5cfa8ba2b37c7adbfad05e11; CURRENT_QUALITY=80; b_lsid=C78E6766_19154F82A7A; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM5NjY2MzYsImlhdCI6MTcyMzcwNzM3NiwicGx0IjotMX0.6ndcYf-eJc1ghTZkclyaiedYkqa1pzBx2GxTvkzPtsc; bili_ticket_expires=1723966576; sid=4mv0hupo; CURRENT_FNVAL=4048; bp_t_offset_3537114517997966=965818624520486912; buvid_fp=6F94F4E6-4132-3C3E-DF09-352F2D9D8C8135015infoc',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'referer' : '{}'.format(url)
}
    # 获取网页代码
response = requests.get(url, headers=headers).text
    # 匹配包含视频网址和音频网址的网页代码
html = re.findall('window.__playinfo__=(.*?)</script>',response)[0]
    # 转化为json数据
html = json.loads(html)
    # 获取信息
title = re.findall('title":"(.*?)","pubdate',response)[0]   #获取标题
audio_url = html['data']['dash']['audio'][0]['baseUrl']            #获取音频网址
video_url = html['data']['dash']['video'][0]['baseUrl']            #获取视频网址

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
