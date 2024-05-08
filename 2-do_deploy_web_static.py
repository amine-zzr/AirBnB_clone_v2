#!/usr/bin/python3
'''The function do_deploy, distributes an archive to your web servers'''
from fabric.api import env, put, run
import os

env.hosts = ['100.26.133.151', '100.25.168.188']


def do_deploy(archive_path):
    '''Check if the archive file exists'''
    if not os.path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, '/tmp')

    # Extract the archive to /data/web_static/releases/
    archive_filename = os.path.basename(archive_path)
    release_folder = '/data/web_static/releases/' + os.path.splitext(
            archive_filename)[0]
    run(f'mkdir -p {release_folder}')
    run(f'tar -xzf /tmp/{archive_filename} -C {release_folder}')

    # Delete the archive from the web server
    run(f'rm /tmp/{archive_filename}')

    # Move the contents of the release folder to the parent folder
    run(f'mv {release_folder}/web_static/* {release_folder}')

    # Remove the now empty web_static folder
    run(f'rm -rf {release_folder}/web_static')

    # Remove the current symbolic link
    run('rm -rf /data/web_static/current')

    # Create a new symbolic link linked to the new version of the code
    run(f'ln -s {release_folder} /data/web_static/current')

    return True
