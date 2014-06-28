import win32gui
import time

__author__ = 'Steve'


class NowPlaying:
    _current_song = ""
    _player = None
    _running = False
    STORM_BOT_HOME = None

    @staticmethod
    def write(text):
        if NowPlaying.STORM_BOT_HOME:
            directory = NowPlaying.STORM_BOT_HOME
            try:
                with open(directory + '\\current_song.txt', 'w') as f:
                    f.write((text + "    ").encode('utf-8'))
            except Exception, e:
                print e.message

    @staticmethod
    def enum_windows():
        print NowPlaying._player
        print "running? %s" % NowPlaying._running
        win32gui.EnumWindows(NowPlaying.examine_window, None)
        while NowPlaying._running:
            time.sleep(5)
            win32gui.EnumWindows(NowPlaying.examine_window, None)

    @staticmethod
    def examine_window(hwnd, sec = None):
        if NowPlaying._running:
            windowTitle = win32gui.GetWindowText(hwnd).decode('cp1252')
            spotify = 'Spotify'.decode('utf-8')
            if spotify in windowTitle and not len(windowTitle) < 10:
                current_song = windowTitle.replace('Spotify - '.decode('utf-8'), '')
                if not current_song == NowPlaying._current_song:
                    NowPlaying._current_song = windowTitle.replace('Spotify - '.decode('utf-8'), '')
                    NowPlaying.write(NowPlaying._current_song)