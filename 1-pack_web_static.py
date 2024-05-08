#!/usr/bin/python3
'''Fabric script that generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo.'''

from fabric.api import local
from datetime import datetime


def do_pack():
    '''Create the versions folder if it doesn't exist'''
    local('sudo mkdir -p versions')

    # Generate the timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the archive name
    archive_name = "web_static_{}.tgz".format(timestamp)

    # Compress the web_static folder into a .tgz archive
    result = local(
            "sudo tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        archive_path = "versions/{}".format(archive_name)
        return archive_path
    else:
        return None
