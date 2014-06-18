import win32gui
import time

__author__ = 'Steve'


class NowPlaying:
    _current_song = ""
    _player = None
    _running = False

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
                NowPlaying._current_song = windowTitle.replace('Spotify - '.decode('utf-8'), '')
                print NowPlaying._current_song