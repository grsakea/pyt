from datetime import timezone


class Tweet():
    def __init__(self, status):
        # self.status = status
        self.rt = hasattr(status, 'retweeted_status')

        self.tid = status.id
        o_status = None
        if self.rt:
            o_status = status
            status = o_status.retweeted_status

        self.time = status.created_at.replace(tzinfo=timezone.utc)\
            .astimezone(tz=None)

        self.username = status.user.name
        self.screen_name = status.user.screen_name

        if status.truncated:
            status.text = status.extended_tweet['full_text']
            if "entities" in status.extended_tweet:
                status.extended_entities = \
                    status.extended_tweet['entities']
            status.entities = {}

        if not hasattr(status, "extended_entities"):
            status.extended_entities = {}

        self.entities = {"url": [], "media": []}
        if 'urls' in status.entities:
            self.entities['url'] = status.entities['urls']
        if 'urls' in status.extended_entities:
            self.entities['url'] = status.extended_entities['urls']
        if 'media' in status.extended_entities:
            self.entities['media'] = status.extended_entities['media']

        if hasattr(status, 'full_text'):
            self.text = status.full_text
        else:
            self.text = status.text
        self.user = status.user
        self._list_ressource(status, o_status)

    def _list_ressource(self, status, o_status):
        self.ent = {}
        self.ent['vid'] = []
        self.ent['gif'] = []
        self.ent['pic'] = []
        self.ent['url'] = []
        self.ent['profile'] = [status.user.profile_image_url_https.
                               replace('normal', 'bigger')]
        if self.rt:
            self.ent['profile'].\
                    append(o_status.user.profile_image_url_https.
                           replace('normal', 'bigger'))

        for i in self.entities['media']:
            if (i['type'] == 'animated_gif'):
                self.ent['gif'].append((i['url'], self.choose_video(i)))
            elif (i['type'] == 'video'):
                self.ent['vid'].append((i['url'], self.choose_video(i)))
            else:
                self.ent['pic'].append((i['url'],
                                        i['media_url_https']+':orig'))
        for i in self.entities['url']:
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
