import websocket, rel
import json
import queue
import csv

BASELINE_SAMPLES = 10
REALTIME_SAMPLES = 10

LIVE_DATA = queue.Queue(maxsize=REALTIME_SAMPLES)

# Write the baseline data to the "baseline_data folder"
def write_baseline(ws, message):
    global acc_count
    global gyr_count

    values = json.loads(message)['values']
    row = (values[0], values[1], values[2])

    if acc_count < BASELINE_SAMPLES:
        if (ws.url.split('.')[-1] == 'accelerometer'):
            writer = csv.writer(f_acc, lineterminator='\n')
            writer.writerow(row)
            acc_count += 1
    if gyr_count < BASELINE_SAMPLES:
        if (ws.url.split('.')[-1] == 'gyroscope'):
            writer = csv.writer(f_gyr, lineterminator='\n')
            writer.writerow(row)
            gyr_count += 1

    if acc_count==BASELINE_SAMPLES and gyr_count==BASELINE_SAMPLES:
        rel.abort()
        f_acc.close()
        f_gyr.close()
        print("Baseline recorded")

# Push data to queue        
def queue_on_message(ws, message):
    values = json.loads(message)['values']
    row = (values[0], values[1], values[2])
    if LIVE_DATA.full():
        popped = LIVE_DATA.get()
    LIVE_DATA.put(row)

def on_error(ws, error):
    print("error occurred")
    print(error)

def on_close(ws, close_code, reason):
    print("connection close")
    print("close code : ", close_code)
    print("reason : ", reason  )

def on_open(ws):
    print("connection open")
    
def record(addr):
    EXT = "sensor/connect?type=android.sensor.%s"
    addr = f'{addr}/{EXT}'

    symbol="accelerometer"
    ws = websocket.WebSocketApp(addr % (symbol,),
                        on_open=on_open,
                        on_message=queue_on_message,
                        on_error=on_error,
                        on_close=on_close)
    ws.run_forever()  

def record_baseline(addr):

    EXT = "sensor/connect?type=android.sensor.%s"
    addr = f'{addr}/{EXT}'

    global f_acc
    global f_gyr
    f_acc = open("baseline_data/baseline_acc.csv", 'w')
    f_gyr = open("baseline_data/baseline_gyr.csv", 'w')

    global acc_count
    global gyr_count
    acc_count = 0
    gyr_count = 0

    symbol="accelerometer"
    fn = "{BASELINE_DATA_PATH}baseline_{}.csv"
    ws = websocket.WebSocketApp(addr % (symbol,),
                        on_open=on_open,
                        on_message=write_baseline,
                        on_error=on_error,
                        on_close=on_close)
    ws.run_forever(dispatcher=rel)  

    symbol="gyroscope"
    ws = websocket.WebSocketApp(addr % (symbol,),
                        on_open=on_open,
                        on_message=write_baseline,
                        on_error=on_error,
                        on_close=on_close)
    ws.run_forever(dispatcher=rel)

    rel.signal(2, rel.abort)  # Keyboard Interrupt  
    rel.dispatch()  
