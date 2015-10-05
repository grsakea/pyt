import subprocess
import tempfile
import time


class MediaWidget():
    def __init__(self, media, m_type, cache):
        with tempfile.NamedTemporaryFile() as t:
            t.write(cache.get_resource(media))
            if m_type == "pic":
                subprocess.run(['sxiv', t.name])
            if m_type == "gif":
                subprocess.run(['mpv', '--loop=inf', t.name])
            if m_type == "vid":
                subprocess.run(['mpv', t.name])
            time.sleep(1)
