import pickle
from bottle import Bottle, run, abort

app = Bottle()
store = None


@app.route('/status/from_id/<sid:int>')
def status_from_id(sid):
    tweets = store.tweets
    if tweets[-1].tid <= sid:
        abort(204)
    else:
        to_send = []

        i = len(tweets) - 1
        while True:
            cur = tweets[i]
            if cur.tid <= sid or i <= 0:
                break
            to_send.append(cur)
            i -= 1

        return pickle.dumps(to_send)

    abort(400)


def launch_server(main_store):
    global store
    store = main_store
    run(app, host='localhost', port=8080)
