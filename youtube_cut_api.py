#!/usr/bin/env python
# coding: utf-8
#from __future__ import print_function
import nltk
import requests
import urllib
import subprocess
#from moviepy.editor import VideoFileClip, concatenate_videoclips
import datetime
import time
import os
from multiprocessing.pool import ThreadPool


def time_to_secs(time):
    arr = time.split(':')
    if len(arr)==2:
        return int(arr[0])*60+int(arr[1])
    else:
        return int(arr[0])*3600+int(arr[1])*60+int(arr[2])


def refine_inervs(intervals):
    final_intervals = []
    for interval in intervals:
        arr = []
        start = int(interval[0])
        end = int(interval[1])
        print start, end
        while end - start > 600:
            arr.append(str(start))
            arr.append(str(start+600))
            final_intervals.append(arr)
            start = start + 600
            arr = []
        arr.append(str(start))
        arr.append(str(end))
        final_intervals.append(arr)
    return final_intervals

def combine(videos_names_file, video_name):
    subprocess.call("ffmpeg -f concat -i {} -vcodec copy -acodec copy {}".format(videos_names_file, video_name), shell=True)
    '''
    clip1 = VideoFileClip("myvideo.mp4")
    #clip2 = VideoFileClip("myvideo2.mp4").subclip(50, 60)
    clip3 = VideoFileClip("myvideo3.mp4")
    final_clip = concatenate_videoclips([clip1, clip3])
    final_clip.write_videofile("my_concatenation.mp4")
    '''


def download(url, video_name):
    r = requests.get(url, stream=True)
    with open(video_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=2000):
            fd.write(chunk)



def cut(id, start, end, video_name):
    download_url = 'https://ytcutter.com'
    api_url = 'https://ytcutter.com/ytcutter.php?a=form1'
    data = {
        "videoId": id,
        "startTime": start,
        "endTime": end,
        "quality": "hd1080",
        "format": "video"
    }
    try:
        response = requests.post(api_url, data=data)
        print response.json()
        downloadId = response.json()['id']
        print downloadId
        progress_url = 'https://ytcutter.com/ytcutter.php?a=progress&downloadId={}'.format(downloadId)
        while True:
            resp = requests.get(progress_url)
            if resp.json()['progress'] == 100:
                print resp.json()['urls'][0]
                download_url = download_url + urllib.quote(resp.json()['urls'][0])
                print download_url
                break
        time.sleep(3)
        download(download_url, video_name)
    except Exception as e:
        print(e)
        cut(id, start, end, video_name)

def helper(args):
    return cut(*args)

def editor(video_id, video_name, intervals1):
    video_id = video_id
    secs = str(time.time()).split('.')[0]
    intervals = []
    params = []
    intervals_file = 'intervals_{}.txt'.format(secs)
    open(intervals_file, 'wb+').write(intervals1)
    for line in open(intervals_file, 'r').readlines():
        if line.strip()!='':
            interval = []
            for i in line.strip().split(' '):
                if i.strip()!='':
                    if ':' in i:
                        interval.append(str(time_to_secs(i.strip())))
                    else:
                        interval.append(str(i.strip()))
            intervals.append(interval)
    print intervals
    intervals = refine_inervs(intervals)
    print intervals
    video_name = video_name.replace(' ', '_') + '_time_{}'.format(secs)
    videos_names_file_name = video_name + '.txt'
    if os.path.exists(video_name+'.mp4'):
        os.rename(video_name+'.mp4', video_name+'_1.mp4')
    count = 1
    #open('video_files_names.txt', 'wb+').write("")
    if len(intervals)==1:
        cut(video_id, intervals[0][0],  intervals[0][1], video_name + ".mp4")
    else:
        for i in intervals:
            param = ()
            param += (video_id, )
            param += (i[0], )
            param += (i[1], )
            param += (video_name + "_" + str(count) + ".mp4",)
            params.append(param)
            open(videos_names_file_name, 'a+').write("file {}\n".format(video_name + "_" + str(count) + ".mp4"))
            count = count + 1
        print params
        results = ThreadPool(len(params)).map(helper, params)
        for result in results:
            print 'file downloaded'
        combine(videos_names_file_name, video_name + '.mp4')
    os.rename(video_name + '.mp4', video_name.split('_time_')[0] + '.mp4')
    #subprocess.call('rm *.txt;rm *.mp4', shell=True)





'''
invalid youtube vvideo url
hanlde file names ...if users provide sanme video name simultaneously
'''

#ffmpeg -f concat -i video_files_names.txt -vcodec copy -acodec copy combined.mp4

'''
url parsing fialing here -> https://www.youtube.com/watch?time_continue=3490&v=Y_51wKtAnWI
s=u'"/tmp/నాకు నరకం చూపించడానికి కృష్ణ వంశీ పుట్టాడు-Actor Sivaji Raja _ Frankly With TNR _ iDream Filmnagar 60s - 2m60s (9shf0TkZZOY).mp4"'
print s.encode('utf-8')
print urllib.quote(s.decode('utf-8'), safe='')
'''







