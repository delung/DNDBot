from pytube import YouTube, Search
import discord
import re
import asyncio
import os

class Youtube():

    def __init__(self, client):
        self.currently_playing = ""
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
        return

    def get_queue(self):
        emb = discord.Embed()
        emb.title = "Song Player Queue"
        emb.type = "rich"
        indicies = ''.join([str(i) + ".\n" for i in range(len(self.queue))])
        titles = ''.join([yt.title + "\n" for yt in self.queue])
        lengths = ''.join([yt.length + ".\n" for i in self.queue])
        emb.add_field(name="Index", value=indices, inline=True)
        emb.add_field(name="Song Title", value=titles, inline=True)
        emb.add_field(name="Length", value=lengths, inline=True)
        emb.add_field(name="Now Playing", value = self.currently_playing, inline=False)
        emb.colour = discord.Colour.dark_red()
        return emb

    async def _download_video_for_play(self, queue_index):
        if self.is_queue_empty():
            return self.EMPTY_QUEUE_EMB
        yt = self.queue.pop(queue_index)
        self.currently_playing = yt.title
        audio_streams = yt.streams.filter(only_audio=True)
        #grab first audio-only stream and download
        if not len(audio_streams) > 0:
            raise IndexError("No audio streams available.")
        path = audio_streams[0].download(output_path="./yt_dls/", filename="curr_song")
        return path

    async def gen_play_next_in_queue_task(self):
        try:
            file_loc = self._download_video_for_play(0)
            if not os.path.exists(file_loc):
                print("ERROR, AUDIO FILE NOT FOUND AT ", file_loc)
            file = open(file_loc, "r")
            src = discord.PCMAudio(file)
            self.VoiceClient.play(src, after=lambda x: print("finished playing song"))
        except Error as e:
            raise Error(e)
            file.close()
        file.close()
        return
