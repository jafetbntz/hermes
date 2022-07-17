import os
from flask import Flask, abort, request
from helpers.get_map_with_mapbox import get_mapbox_snapshot

from helpers.map_requests import MapSnapshotRequest

MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')

app = Flask(__name__)


@app.route("/info")
def info():

    return {
        "service": "Hermes | Map Snapshots Service",
        "powered_by": "Carbono 14"
    }


@app.post("/snaphot")
def new_snapshot():
    result = {
        "success": False
    }

    snap_request = request.json
    
    if not snap_request['coordinates']:
        result['message'] = 'INVALID_PARAMETERS'
        abort(400, result)

    points = [(p['lat'], p['lng'])  for p in snap_request['coordinates']]
    snapshot = MapSnapshotRequest(
        points=points,
        base_folder=os.environ.get('PICTURES_FOLDER_PATH', '/var/www/html/pictures')
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
        abort(400, result)


    try:
        snap_url = get_mapbox_snapshot(snapshot, MAPBOX_TOKEN)
        result['snapshot_url'] = snap_url
        result["success"] = True
    except Exception as e:
        print(e)
        result['message'] = 'INTERNAL_ERROR'
        abort(500, result)


    return result