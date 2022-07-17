import requests

from helpers.map_requests import MapSnapshotRequest

API_URL = "https://api.mapbox.com/styles/v1/{0}/static/{1}/auto/{2}x{3}?access_token={4}"



def get_mapbox_snapshot(args:MapSnapshotRequest, token:str):
    """
    This functions makes a call to MapBox's statics api and 
    saves the result image in the indicated path.
    """
    request_url = API_URL.format(
          args.style_id,
          args.get_mapbox_polyline(),
          args.width,
          args.height,
          token)

    response = requests.get(request_url)

    if (response.status_code != 200):
        print(response.text)
        return None
    try:
      newFile = args.generate_filename()
      open(newFile, 'wb').write(response.content)
      
      return newFile.split('/')[-1]
    except Exception as e:
      print(e)
      return None

