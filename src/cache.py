import requests


class Cache:
    def __init__(self):
        self.r = {}

    def get_resource(self, url):
        if url in self.r:
            return self.r[url]
        else:
            r = requests.post('http://127.0.0.2:8080/content',
                              {'resource': url})
            data = r.content
            self.r[url] = data
            return data
