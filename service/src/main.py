import json
import os
from flask import Flask, Response, abort, request
from redis import Redis

from map_requests import MapSnapshotRequest
    
redis_client = Redis(host='redis', port=6379)

PICTURES_FOLDER_PATH = '/var/www/html/pictures'
SNAPSHOTS_QUEUE_KEY = 'queue:snapshot_reques'

app = Flask(__name__)


@app.route("/info")
def info():

    return {
        "service": "Hermes | Map Snapshots Service",
        "powered_by": "Carbono 14",
        "queue": redis_client.llen(SNAPSHOTS_QUEUE_KEY)
    }


@app.get("/snaphots")
def get_snapshots():
    arr = os.listdir(PICTURES_FOLDER_PATH)

    return json.dumps({
        "result": arr
    })


@app.post("/snaphots")
def new_snapshot():
    result = {
        "success": False
    }

    snap_request = request.json
    
    if not snap_request['coordinates']:
        result['message'] = 'INVALID_PARAMETERS'
        abort(400, Response(result))

    points = [(p['lat'], p['lng'])  for p in snap_request['coordinates']]
    snapshot = MapSnapshotRequest(
        points=points,
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


    if not snapshot.is_valid():
        result['message'] = 'INVALID_PARAMETERS'
        abort(400, Response(result))


    try:

        
        redis_client.lpush(SNAPSHOTS_QUEUE_KEY,snapshot.json())
        result['success'] = True

    except Exception as e:
        print('[ERROR] - ', e)
        result['message'] = 'INTERNAL_ERROR'
        abort(500, Response(result))


    return result