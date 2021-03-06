# CEF Python 3 based Twitch Bot

# Checking whether python architecture and version are valid, otherwise an obfuscated error
# will be thrown when trying to load cefpython.pyd with a message "DLL load failed".
import platform
from warnings import catch_warnings
from JSBindings import JSBindings

if platform.architecture()[0] != "32bit":
    raise Exception("Architecture not supported: %s" % platform.architecture()[0])

import os
from os.path import expanduser
import sys
from cefpython3 import cefpython_py27 as cefpython

import cefwindow
import win32con
import win32gui
from now_playing import NowPlaying
import time
import json

DEBUG = False
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
STORM_BOT_HOME = expanduser("~/StormBot")
SB_CACHE_PATH = STORM_BOT_HOME + "/data"

def GetApplicationPath(file=None):
    import re, os
    # If file is None return current directory without trailing slash.
    if file is None:
        file = ""
    # Only when relative path.
    if not file.startswith("/") and not file.startswith("\\") and (not re.search(r"^[\w-]+:", file)):
        if hasattr(sys, "frozen"):
            path = os.path.dirname(sys.executable)
        elif "__file__" in globals():
            path = os.path.dirname(os.path.realpath(__file__))
        else:
            path = os.getcwd()
        path = path + os.sep + file
        path = re.sub(r"[/\\]+", re.escape(os.sep), path)
        path = re.sub(r"[/\\]+$", "", path)
        return path
    return str(file)

def ExceptHook(excType, excValue, traceObject):
    import traceback, os, time, codecs
    # This hook does the following: in case of exception write it to
    # the "error.log" file, display it to the console, shutdown CEF
    # and exit application immediately by ignoring "finally" (_exit()).
    errorMsg = "\n".join(traceback.format_exception(excType, excValue,
                                                    traceObject))
    errorFile = GetApplicationPath("error.log")
    try:
        appEncoding = cefpython.g_applicationSettings["string_encoding"]
    except:
        appEncoding = "utf-8"
    if type(errorMsg) == bytes:
        errorMsg = errorMsg.decode(encoding=appEncoding, errors="replace")
    try:
        with codecs.open(errorFile, mode="a", encoding=appEncoding) as fp:
            fp.write("\n[%s] %s\n" % (
                time.strftime("%Y-%m-%d %H:%M:%S"), errorMsg))
    except:
        print("cefpython: WARNING: failed writing to error file: %s" % (
            errorFile))
    # Convert error message to ascii before printing, otherwise
    # you may get error like this:
    # | UnicodeEncodeError: 'charmap' codec can't encode characters
    errorMsg = errorMsg.encode("ascii", errors="replace")
    errorMsg = errorMsg.decode("ascii", errors="replace")
    print("\n"+errorMsg+"\n")
    cefpython.QuitMessageLoop()
    cefpython.Shutdown()
    os._exit(1)

def CefAdvanced():
    sys.excepthook = ExceptHook
    appSettings = dict()
    if DEBUG:
        # cefpython debug messages in console and in log_file
        appSettings["debug"] = True
        cefwindow.g_debug = True
    appSettings["log_file"] = GetApplicationPath("debug.log")
    appSettings["log_severity"] = cefpython.LOGSEVERITY_INFO
    appSettings["persist_session_cookies"] = True
    appSettings["cache_path"] = SB_CACHE_PATH
    appSettings["release_dcheck_enabled"] = True # Enable only when debugging
    appSettings["browser_subprocess_path"] = "%s/%s" % (
        cefpython.GetModuleDirectory(), "subprocess")
    cefpython.Initialize(appSettings)

    wndproc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
    }

    browserSettings = dict()
    browserSettings["universal_access_from_file_urls_allowed"] = True
    browserSettings["file_access_from_file_urls_allowed"] = True

    windowHandle = cefwindow.CreateWindow(title="StormBot",
                                          className="stormbot", width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                                          icon="icon.ico", windowProc=wndproc)
    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowHandle)
    browser = cefpython.CreateBrowserSync(windowInfo, browserSettings, navigateUrl=GetApplicationPath("index.html"))


    bindings = cefpython.JavascriptBindings(bindToFrames=True, bindToPopups=True)
    JSBindings(bindings)
    browser.SetJavascriptBindings(bindings)

    cefpython.MessageLoop()
    cefpython.Shutdown()

def CloseWindow(windowHandle, message, wparam, lparam):
    # NOW_PLAYING_THREAD.stop()
    browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()
    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)

def QuitApplication(windowHandle, message, wparam, lparam):
    win32gui.PostQuitMessage(0)
    return 0

if __name__ == "__main__":
    # create the StormBot dir if it doesn't exist
    if not os.path.exists(SB_CACHE_PATH):
        os.makedirs(SB_CACHE_PATH)
    NowPlaying.STORM_BOT_HOME = STORM_BOT_HOME
    CefAdvanced()
