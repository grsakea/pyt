class Tweet():
    def __init__(self, status):
        self.status = status
        self.rt = hasattr(self.status, 'retweeted_status')

        self.tid = status.id
        if self.rt:
            self.o_status = status
            self.status = self.o_status.retweeted_status

        self.text = self.status.text
        self.user = status.user
        self._list_ressource()

    def _list_ressource(self):
        self.ent = {}
        self.ent['vid'] = []
        self.ent['gif'] = []
        self.ent['pic'] = []
        self.ent['url'] = []
        self.ent['profile'] = [self.status.user.profile_image_url_https.
                               replace('normal', 'bigger')]
        if self.rt:
            self.ent['profile'].\
                    append(self.o_status.user.profile_image_url_https.
                           replace('normal', 'bigger'))

        if hasattr(self.status, 'extended_entities'):
            for i in self.status.extended_entities['media']:
                if (i['type'] == 'animated_gif'):
                    self.ent['gif'].append((i['url'], self.choose_video(i)))
                elif (i['type'] == 'video'):
                    self.ent['vid'].append((i['url'], self.choose_video(i)))
                else:
                    self.ent['pic'].append((i['url'],
                                            i['media_url_https']+':orig'))
        if 'urls' in self.status.entities:
            for i in self.status.entities['urls']:
                self.ent['url'].append((i['indices'], i['display_url'],
                                       i['expanded_url']))

    def __lt__(self, other):
        return self.tid < other.tid

    def choose_video(self, vids):
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