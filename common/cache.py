import requests
import pickle


class Cache:
    def __init__(self):
        self.r = {}
        self.queue = set()

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

    def queue_ressource(self, url):
        if url not in self.r:
            self.queue.add(url)

    def fetch_queue(self):
        out = list(self.queue)
        r = requests.post('http://127.0.0.2:8080/multiple_content',
                          json=out)
        self.queue = set()
        temp = pickle.loads(r.content)
        print(type(temp))
        for i in temp:
            self.r[i] = temp[i]
