import win32gui
import time
from threading import Thread
import pythoncom

__author__ = 'Steve'


class NowPlaying:
    _current_song = ""
    _player = None
    _write_to_file = True
    _running = False
    STORM_BOT_HOME = None

    @staticmethod
    def StartNowPlaying():
        if not NowPlaying._running:
            NowPlaying._running = True
            try:
                pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            except pythoncom.com_error:
                #already initialized.
                pass
            now_playing_thread = Thread(target=NowPlaying.enum_windows)
            now_playing_thread.daemon = True
            now_playing_thread.start()

    @staticmethod
    def write(text):
        if NowPlaying.STORM_BOT_HOME and NowPlaying._write_to_file:
            directory = NowPlaying.STORM_BOT_HOME
            try:
                with open(directory + '\\current_song.txt', 'w') as f:
                    print "Now playing: %s" % text
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
            if spotify in windowTitle and not len(windowTitle) < 10 and NowPlaying._player == 'spotify':
                current_song = windowTitle.replace('Spotify - '.decode('utf-8'), '')
                if not current_song == NowPlaying._current_song:
                    NowPlaying._current_song = windowTitle.replace('Spotify - '.decode('utf-8'), '')
                    NowPlaying.write(NowPlaying._current_song)