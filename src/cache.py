import requests


class Cache:
    def __init__(self):
        self.r = {}

    def get_resource(self, url):
        if url in self.r:
            print("Cache hit", url)
            return self.r[url]
        else:
            print("Cache miss", url)
            r = requests.post('http://127.0.0.2:8080/content',
                              {'resource': url})
            data = r.content
            self.r[url] = data
            return data
