"""
Loader script.

Takes as input a directory containing JSON objects created by the processing
script. For each JSON object, post it to BuildingOS.

On a successful post, moves the object to a designated archive directory.
"""

import requests

from utils import defaults
from utils import utils

def post_json_files(root):
    """
    Post json objects in a designated directory to BuildingOS.

    Params:
        root string
    """
    json_dir = defaults.json_dir(root)
    archive = defaults.json_archive(root)
    post_url = defaults.BOS_URL

    json_files = utils.get_files_in_dir(json_dir)
    if not json_files:
        utils.warn('No JSON files to process. Terminating')
        exit()

    utils.print_time('LOADER START')
    for json_file in json_files:
        print('Posting file: %s ...' % (json_file)),
        with open(json_file, 'rb') as jf:
            payload = {'data': jf}
            response = requests.post(post_url, files=payload)
            print('done')

            print('Server response: %s' % (response.text))

        utils.move(json_file, archive)

    utils.print_time('LOADER END')

