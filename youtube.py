from pytube import YouTube, Search
import discord
import re
import asyncio
import os
from datetime import timedelta

class Youtube():

    def __init__(self, client):
        self.currently_playing = "No song currently playing."
        self.queue = []
        self.client = client

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
        def prog_func(stream, chunk, bytes_remaining):
            print("Bytes left: ", bytes_remaining)
            return

        def done_func(stream, filepath):
            print("All done! Stored here: ", filepath)
            return

        results = Search(search_str)
        if not len(results.results) > 0:
            #TODO
            return self.NONE_FOUND_EMB

        #grab first result
        yt = results.results[0]
        yt.register_on_progress_callback(prog_func)
        yt.register_on_complete_callback(done_func)
        self.queue += [yt]
        return

    def skip_item(self):
        self.queue.pop(0)
        #run cleanup
        return

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
        if self.is_queue_empty():
            return self.EMPTY_QUEUE_EMB
        yt = self.queue.pop(queue_index)
        self.currently_playing = str(yt.title)
        audio_streams = yt.streams.filter(only_audio=True)
        #grab first audio-only stream and download
        if not len(audio_streams) > 0:
            raise IndexError("No audio streams available.")
        path = audio_streams[0].download(output_path="./yt_dls/", filename="curr_song.mp4")
        return path

    

    async def gen_play_next_in_queue_task(self):
        def cleanup_song(error):
            if os.path.exists(file_loc):
                os.remove(file_loc)
                
        file_loc = await self._download_video_for_play(0)
        if not os.path.exists(file_loc):
            print("ERROR, AUDIO FILE NOT FOUND AT ", file_loc)
        src = discord.FFmpegPCMAudio(file_loc)
        self.client.voice_clients[0].play(src, after=cleanup_song)
        while self.client.voice_clients[0].is_playing():
            await asyncio.sleep(1)
        self.client.voice_clients[0].stop()
        return
