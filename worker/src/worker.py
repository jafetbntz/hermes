import json
import os
from pathlib import Path
from redis import Redis
from helpers.get_map_with_mapbox import get_mapbox_snapshot
from helpers.map_requests import MapSnapshotRequest


PICTURES_FOLDER_PATH = '/var/www/html/pictures'
MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')
SNAPSHOTS_QUEUE_KEY = 'queue:snapshot_reques'

def _handle_queue(conn):
    snap_request = conn.rpop(SNAPSHOTS_QUEUE_KEY)
    if snap_request == None:
        return
        
    snap_request = json.loads(snap_request)
    print('🚀 ~ file: worker.py ~ line 22 ~ snap_request', snap_request)


    snapshot = MapSnapshotRequest(
        points=snap_request.get('coordinates_list'),
        base_folder=PICTURES_FOLDER_PATH
    )

    if snap_request.get('width') != None:
        snapshot.width = snap_request['width']

    if snap_request.get('height') != None:
        snapshot.height = snap_request['height']

    if snap_request.get('stroke_width') != None:
        snapshot.stroke_width = snap_request['stroke_width']

    if snap_request.get('style_id') != None:
        snapshot.style_id = snap_request['style_id']

    if snap_request.get('fill_color') != None:
        snapshot.fill_color = snap_request['fill_color']

    if snap_request.get('fill_opacity') != None:
        snapshot.fill_opacity = snap_request['fill_opacity']
        
    map_url = get_mapbox_snapshot(snapshot, MAPBOX_TOKEN)
    print('🚀 ~ file: worker.py ~ line 48 ~ map_url', map_url)
    if map_url != None:
        ## TODO: Notify the generation of the snapshot through some push notification service and/or some WebSocket channel 
        pass
    else:
        ## Notify failure to internal Team
        pass


if __name__ == "__main__":
    print("Starting Hermes worker...")
    redis_client = Redis(host='redis', port=6379)
    print("Creating pictures folder...")
    try:
        path = Path(PICTURES_FOLDER_PATH)
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print("[ERROR] - ", '🚀 ~ file: worker.py ~ line 60 ~ e', e)


    while True:

        try:
            _handle_queue(redis_client)
        except Exception as e:
            print("[ERROR] - ", '🚀 ~ file: worker.py ~ line 69 ~ e', e)
