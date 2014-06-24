from distutils.core import setup
import os
import py2exe


def get_cefpython_path():
    import cefpython3 as cefpython

    path = os.path.dirname(cefpython.__file__)
    return "%s%s" % (path, os.sep)


def get_setup_path():
    return os.path.dirname(__file__)


def get_data_files():
    cefp = get_cefpython_path()
    sp = get_setup_path()
    data_files = [('', ['%s/icudt.dll' % cefp,
                        '%s/d3dcompiler_43.dll' % cefp,
                        '%s/devtools_resources.pak' % cefp,
                        '%s/ffmpegsumo.dll' % cefp,
                        '%s/libEGL.dll' % cefp,
                        '%s/libGLESv2.dll' % cefp,
                        '%s/Microsoft.VC90.CRT.manifest' % cefp,
                        '%s/msvcm90.dll' % cefp,
                        '%s/msvcp90.dll' % cefp,
                        '%s/msvcr90.dll' % cefp,
                        '%s/subprocess.exe' % cefp,
                        'index.html',
                        'icon.ico']),
                  ('locales', ['%s/locales/en-US.pak' % cefp]),
                  ]
    for src_dir in "css", "js", "fonts":
        for root, dirs, files in os.walk(src_dir):
            data_files.append((root, map(lambda f:root + "/" + f, files)))

    return data_files

setup(
    data_files=get_data_files(),
    windows=['StormBot.py']
)
