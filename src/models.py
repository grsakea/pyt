class Tweet():
    def __init__(self, status):
        self.status = status
        self.tid = status.id
        self.user = status.user
        self._list_ressource()

    def _list_ressource(self):
        self.ent = {}
        self.ent['vid'] = []
        self.ent['pic'] = []
        self.ent['url'] = []

        if hasattr(self.status, 'extended_entities'):
            for i in self.status.extended_entities['media']:
                if (i['type'] == 'animated_gif' or i['type'] == 'video'):
                    self.ent['vid'].append((i['url'], self.choose_video(i)))
                else:
                    self.ent['pic'].append((i['url'], i['media_url_https']))
        if 'urls' in self.status.entities:
            for i in self.status.entities['urls']:
                self.ent['url'].append((i['url'], i['display_url'],
                                       i['expanded_url']))

    def __lt__(self, other):
        return self.tid < other.tid

    def choose_video(vids):
        chosen = vids['expanded_url']
        max_br = -1
        for i in vids['video_info']['variants']:
            try:
                if i['bitrate'] > max_br:
                    max_br = i['bitrate']
                    chosen = i['url']
            except:
                pass
        return(chosen)
