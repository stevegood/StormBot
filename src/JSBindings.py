__author__ = 'Steve'

from now_playing import NowPlaying


class JSBindings:

    data = None

    def __init__(self, bindings):
        # add all the functions to the browser
        print "__init__"
        bindings.SetFunction("initSettings", self.initSettings)
        bindings.SetFunction("setMusicPlayer", self.setMusicPlayer)

    def initSettings(self, data):
        self.data = data
        self.setMusicPlayer(data['player'], data['now_playing']['save_to_file'])
        NowPlaying.StartNowPlaying()

    def setMusicPlayer(self, player, writeToFile):
        print "set the player to %s" % player
        NowPlaying._player = player
        NowPlaying._write_to_file = writeToFile