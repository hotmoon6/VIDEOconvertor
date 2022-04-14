#  This file is part of the VIDEOconvertor distribution.
#  Copyright (c) 2021 vasusen-code ; All rights reserved. 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  License can be found in < https://github.com/vasusen-code/VIDEOconvertor/blob/public/LICENSE> .

import os, time, subprocess, asyncio
from datetime import datetime as dt
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata
from telethon import events

def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def ssgen(video, time_stamp):
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{hhmmss(time_stamp)}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
        
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       
        
async def screenshot(event, msg):
    Drone = event.client
    name = dt.now().isoformat("_", "seconds") + ".mp4"
    edit = await Drone.send_message(event.chat_id, "Trying to process.", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    if msg.file.name:
        name = msg.file.name
    try:
        await fast_download(name, file, Drone, edit, time.time(), "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading.") 
    pictures = []
    captions = []
    n = [220, 215, 210, 202, 199, 197, 193, 189, 185, 183, 179, 174, 163, 157, 153, 149, 142, 139, 130, 127, 123, 119, 115, 110, 102, 99, 96, 91, 87, 84, 80, 76, 71, 68, 60, 58, 53, 48, 40, 36, 31, 28, 22, 17, 14, 11, 9, 7, 4, 2]
    duration = (video_metadata(name))["duration"]
    for i in range(50):
        sshot = await ssgen(name, duration/n[i]) 
        if sshot is not None:
            pictures.append(sshot)
            captions.append(f'screenshot at {hhmmss(duration/n[i])}')
            await edit.edit(f"`{i+1}` screenshot generated.")
    if len(pictures) > 0:
        await Drone.send_file(event.chat_id, pictures, caption=captions)
    else:
        await edit.edit("No screenshots could be generated!")
    await edit.delete()
    try:
        for pic in pictures:
             os.remove(pic)
        os.remove(name)
    except Exception:
        pass
