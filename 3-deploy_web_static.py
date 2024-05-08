#!/usr/bin/python3
'''Orchestrates the archive creation and deployment process.'''
from fabric.api import env, run, local, put
from datetime import datetime

env.hosts = ['100.26.133.151', '100.25.168.188']
env.user = 'ubuntu'


def do_pack():
    '''Creates a .tgz archive from the contents of the web_static folder.
    Return Value: Returns the path of the created archive if successful
        otherwise returns None.
    '''
    now = datetime.now()
    archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
    local("mkdir -p versions")
    local(f" sudo tar -czvf versions/{archive_name} web_static")
    return f"versions/{archive_name}"


def do_deploy(archive_path):
    '''Distributes an archive to the web servers, unpacks it, and updates
       the symbolic link to the new version.
    Parameters:
    archive_path: Path to the archive file to deploy.
    Return Value: Returns True if deployment is successful,
        otherwise returns False.'''
    if not archive_path:
        return False

    put(archive_path, '/tmp/')
    release_folder = f"/data/web_static/releases/{archive_path.split('/')[1]}"
    run(f"mkdir -p {release_folder}")
    run(f"tar -xzf {archive_path} -C {release_folder}")
    run(f"rm {archive_path}")
    run(f"mv {release_folder}/web_static/* {release_folder}")
    run(f"rm -rf {release_folder}/web_static")
    run(f"rm -rf /data/web_static/current")
    run(f"ln -s {release_folder} /data/web_static/current")
    return True


def deploy():
    '''Orchestrates the archive creation and deployment process.'''
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
