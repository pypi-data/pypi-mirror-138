import websocket
import _thread
import time
import weakref
import queue


master_dict = {}
master_queues = []
master_lock =  _thread.allocate_lock()


def config(field):
    def f(field=field):
        try:
            master_lock.acquire()
            return master_dict.get(field)
        finally:
            master_lock.release()
    return f

def destroy_queue(proxy):
    master_lock.acquire()
    master_queues.remove(proxy)
    master_lock.release()

def get_queue():
    que = queue.Queue()
    master_lock.acquire()
    master_queues.append(weakref.proxy(que, destroy_queue))
    for k, v in master_dict.items():
        que.put((k, v))
    master_lock.release()
    return que

def on_message(ws, message):
    try:
        master_lock.acquire()
        if '\t' in message:
            k, v = message.split('\t', 1)
            master_dict[k] = v
            for queue in master_queues:
                queue.put((k, v))
        else:
            for queue in master_queues:
                queue.put((message, None))
            del(master_dict[message])
    finally:
        master_lock.release()

        
def on_error(ws, error):
    print("ERROR:", error)
    pass

def on_close(ws, close_status_code, close_msg):
    pass

def on_open(ws):
    ws.send(ws.key)

def startup(key, url="wss://stream.realtimeconfig.com:1443/"):
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.key = key
    
    _thread.start_new_thread(ws.run_forever, ())



