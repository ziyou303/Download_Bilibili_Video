import json
import re
import os
import time
import requests
import subprocess


    # 定义B站网址
url = input('请输入B站视频网页的网址:')
    # 请求头
headers = {
    'cookie' : 'buvid3=C781EF45-DBFD-8D24-8F1A-3DB828C4E1CE53476infoc; b_nut=1776584653; _uuid=E78A6691-10F79-831010-B1082-F68A45A9B1B154228infoc; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; buvid_fp=120179691eead2d5bbddfbd8801a7d97; buvid4=A9C868F2-0F4B-90C3-11E2-F732D738768654051-026041915-KnVDJ+VCo1maFfrikMswo9/6Mxl4htIvwBcuHWq7gWpQaugmTzty5tKzzy35zWtL; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzY4NDM4NTQsImlhdCI6MTc3NjU4NDU5NCwicGx0IjotMX0.4QBiAfVRNWKltm2dvJy0fXsXf0ZbgK56cVBrNZn4-m8; bili_ticket_expires=1776843794; CURRENT_FNVAL=2000; SESSDATA=9afc1539%2C1792136691%2Cf8a02%2A42; bili_jct=43af5c19b0ee239177f16fa5614f16b2; DedeUserID=3546949477206143; DedeUserID__ckMd5=23728694987ab739; home_feed_column=5; theme-tip-show=SHOWED; sid=gpxl5fg4; browser_resolution=1692-150; b_lsid=6B7AABBA_19DA4B34658',#这里填你的cookie，不填也行，但你下载的视频只有360P
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'referer' : '{}'.format(url)
}

response = requests.get(url=url, headers=headers).text

data = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>',response)[0])

    # 获取信息
title =  re.findall('title":"(.*?)","pubdate',response)[0]  #获取标题
audio_url = data['data']['dash']['audio'][0]['baseUrl']            #获取音频网址
video_url = data['data']['dash']['video'][0]['baseUrl']            #获取视频网址

'''获取文件'''
    # 过滤掉非法字符
illegal_chars = r'[<>:"/\\|?*]'
file_name = re.sub(illegal_chars, '_', title)

    # 获取视频文件
print('开始下载视频文件')
video = requests.get(url=video_url, headers=headers).content
with open('temp.mp4', 'wb') as f:   #写入视频文件
    f.write(video)
    f.close()
# 检查视频是否下载成功
if os.path.isfile('temp.mp4'.format(file_name)):
    print('视频下载成功！'.format(file_name))
else:
    exit('视频下载失败,检查一下网络帕'.format(file_name))

time.sleep(2)

    # 获取音频文件
print('开始下载音频文件')
audio = requests.get(url=audio_url, headers=headers).content
with open('temp.mp3', 'wb') as f:   #写入音频文件
    f.write(audio)
    f.close()
# 检查音频是否下载成功
if os.path.isfile('temp.mp3'.format(file_name)):
    print('音频下载成功！'.format(file_name))
else:
    exit('音频下载失败,检查一下网络帕'.format(file_name))

'''视频和音频合拼'''
    # 构建FFmpeg命令
    # -y: 覆盖输出文件而不询问
    # -i: 指定输入文件
    # -c:v copy: 视频流直接复制，不重新编码（速度快）
    # -c:a aac: 音频流编码为AAC格式（兼容性好）
    # -strict experimental: 允许使用实验性编码器（某些旧版本FFmpeg需要）

    # 检查是否存在保存文件的文件夹路径
if not os.path.exists('视频'):
    os.makedirs('视频')

    # 输出文件路径
output_path = '视频/{}.mp4'.format(file_name)

command = [
        'ffmpeg/bin/ffmpeg',
        '-y',
        '-i', 'temp.mp4',
        '-i', 'temp.mp3',
        '-acodec', 'copy',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_path
]
    # 尝试合并
try:
        # 执行命令
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"合并成功! 输出文件: {output_path}")
except subprocess.CalledProcessError as e:
        exit(f"合并失败: {e.stderr.decode('utf-8')}")

    # 删除原视频和音频
os.remove('temp.mp4')
os.remove('temp.mp3')

    # 显示和检查完成信息
if os.path.isfile('视频/{}.mp4'.format(file_name)):
    print('{}.mp4保存成功！'.format(file_name))
else:
    exit('{}.mp4保存失败,重试一下帕'.format(file_name))

input('按下回车键退出!')
