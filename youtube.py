from pytube import YouTube, Search
import discord
import re
import asyncio
import os
from datetime import datetime, timedelta

class Youtube():

    EMPTY_QUEUE_EMB = discord.Embed(title="Nothing in the queue")
    NONE_FOUND_EMB = discord.Embed(title="Nothing found by that name")
    vc_timeout = 300 #5 minutes
    vc_timeout_in_channel = 900 #15 minutes
    max_video_length_seconds = 605 #10 minutes

    def __init__(self, client):
        self.currently_playing = "No song currently playing."
        self.queue = []
        self.client = client
        self.voice_client = None
        self.voice_channel = None
        self.curr_task = None
        self.output_path = "./yt_dls/"
        self.output_name = "curr_song.mp4"
        self.called_channel = None
        self.paused = False

    @staticmethod
    async def get_help_message(message: discord.Message) -> discord.Embed:
        emb = discord.Embed()
        emb.title = "Youtube Help"
        emb.description = "this will eventually tell you how to use youtube"
        return emb

    @staticmethod
    async def get_usage_message(message: discord.Message) -> discord.Embed:
        emb = discord.Embed()
        emb.title = "Youtube Usage"
        emb.description = "this will eventually tell you how to use youtube"
        return emb

    def get_queue_size(self) -> int:
        return len(self.queue)

    def is_queue_empty(self):
        return self.get_queue_size() == 0

    async def add_to_queue(self, search_str):
        #returns true if added sucessfully
        if not len(search_str) > 0:
            await self.called_channel.send("Invalid query")
        def prog_func(stream, chunk, bytes_remaining):
            print("Bytes left: ", bytes_remaining)
            return

        def done_func(stream, filepath):
            print("All done! Stored here: ", filepath)
            return

        results = Search(search_str)
        if not len(results.results) > 0:
            return self.NONE_FOUND_EMB

        #grab first result
        yt = results.results[0]
        if yt.length > self.max_video_length_seconds:
            await self.called_channel.send("Video is too long. Max is 10 minutes.")
            return False
        yt.register_on_progress_callback(prog_func)
        yt.register_on_complete_callback(done_func)
        self.queue += [yt]
        return True

    async def _wait_for_disconnect(self, start_time):
        #Queue is empty, no more songs. Wait until timeout.
        self.currently_playing = "No song is currently playing."
        curr_time = datetime.now()
        time_diff_in_seconds = (curr_time - start_time).seconds
        num_other_users_in_channel = len(self.voice_channel.members) - 1 #sub. 1 to account for self
        timeout = ((time_diff_in_seconds > self.vc_timeout) and (num_other_users_in_channel <= 0)) or (time_diff_in_seconds > self.vc_timeout_in_channel)
        while (not timeout):
            await asyncio.sleep(5)
            curr_time = datetime.now()
            time_diff_in_seconds = (curr_time - start_time).seconds
            num_other_users_in_channel = len(self.voice_channel.members) - 1 #sub. 1 to account for self
            timeout = ((time_diff_in_seconds > self.vc_timeout) and (num_other_users_in_channel <= 0)) or (time_diff_in_seconds > self.vc_timeout_in_channel)
        await self.stop()
        return

    async def play(self):
        if not self.is_playing():
            if self.voice_client is None:
                await self.connect_vc(self.voice_channel, self.called_channel)
            start_time = datetime.now()
            while (not self.is_queue_empty()):
                self.curr_task = asyncio.create_task(self.gen_play_next_in_queue_task())
                await self.curr_task
                self._cleanup()
            self.curr_task = asyncio.create_task(self._wait_for_disconnect(start_time))
            await self.curr_task
        else:
            await self.called_channel.send(embed=self.get_queue())
        return

    async def skip_item(self):
        if self.is_playing():
            self.cancel_playing()
            self.paused = False
            await self.play()
        else:
            await self.called_channel.send("No song is currently playing!")
        return

    async def connect_vc(self, vc, text_channel):
        if not self.voice_client is None and vc != self.voice_channel:
            await text_channel.send("I can only be in one voice channel at a time!")
        self.voice_client = await vc.connect()
        self.voice_channel = vc
        return

    async def disconnect_vc(self):
        await self.voice_client.disconnect()
        return

    async def stop(self):
        self.cancel_playing()
        await self.disconnect_vc()
        self._cleanup()
        await self.clear("all")
        self.voice_channel = None
        self.voice_client = None
        self.called_channel = None
        self.currently_playing = "No song currently playing."
        self.paused = False
        return

    def pause(self):
        if self.is_playing():
            print("pausing...")
            self.voice_client.pause()
            print("paused")
            self.paused = True
        return

    def resume(self):
        print("resuming...")
        self.voice_client.resume()
        print("resumed")
        self.paused = False
        return

    def cancel_playing(self):
        if not self.curr_task is None:
            self.curr_task.cancel()
            self.voice_client.stop()
        self.curr_task = None
        return

    def is_playing(self):
        if not self.voice_client is None:
            return self.voice_client.is_playing() or self.paused
        return False

    async def clear(self, rest_of_msg):
        ind_regex = re.compile(r"[0-9]+")
        if rest_of_msg.strip().lower() == "all":
            print("clearing everything")
            #clear everything
            self.queue = []
        elif not ind_regex.match(rest_of_msg.strip()) is None:
            #should only be one
            ind = int(re.findall(r"[0-9]+", rest_of_msg.strip())[0])
            print("clearing index: ", str(ind))
            if ind > 0:
                self.queue.pop(ind-1)
        await self.called_channel.send(embed=self.get_queue())
        return

    def _cleanup(self):
        file_loc = self.output_path + self.output_name
        if os.path.exists(file_loc):
            os.remove(file_loc)
        self.curr_task = None

    def get_queue(self):
        emb = discord.Embed()
        emb.title = "Song Player Queue"
        emb.type = "rich"
        if not self.is_queue_empty():
            indices = ''.join([str(i+1) + ".\n" for i in range(len(self.queue))])
            titles = ''.join([str(yt.title) + "\n" for yt in self.queue])
            lengths = ''.join([str(timedelta(seconds=yt.length)) + "\n" for yt in self.queue])
        else:
            indices = "0."
            titles = "No songs in queue."
            lengths = "0:00:00"
        emb.add_field(name="Index", value=indices, inline=True)
        emb.add_field(name="Song Title", value=titles, inline=True)
        emb.add_field(name="Length", value=lengths, inline=True)
        emb.add_field(name="Now Playing", value=self.currently_playing, inline=False)
        emb.colour = discord.Colour.dark_red()
        return emb

    async def _download_video_for_play(self, queue_index):
        await self.called_channel.send("Downloading next song... Can't respond until after.")
        if self.is_queue_empty():
            return self.EMPTY_QUEUE_EMB
        yt = self.queue.pop(queue_index)
        self.currently_playing = str(yt.title)
        await self.called_channel.send(embed=self.get_queue())
        audio_streams = yt.streams.filter(only_audio=True)
        #grab first audio-only stream and download
        if not len(audio_streams) > 0:
            raise IndexError("No audio streams available.")
        path = audio_streams[0].download(output_path=self.output_path, filename=self.output_name)
        return path

    async def gen_play_next_in_queue_task(self):
        file_loc = await self._download_video_for_play(0)
        if not os.path.exists(file_loc):
            print("ERROR, AUDIO FILE NOT FOUND AT ", file_loc)
        src = discord.FFmpegPCMAudio(file_loc)
        self.voice_client.play(src, after=lambda e: print("Finished song"))
        while self.is_playing():
            await asyncio.sleep(1)
        self.voice_client.stop()
        return
