#!/usr/bin/python3
'''
Deletes out-of-date archives using the function do_clean
'''
import os
from fabric.api import cd, env, local, run

env.hosts = ['100.26.133.151', '100.25.168.188']


def do_clean(number=0):
    '''Deletes out-of-date archives'''
    n = int(number)
    if n <= 1:
        n = 1  # Keep at least one version
    # Local Archive Cleanup
    local_archives = os.listdir('./versions')
    local_archives.sort(reverse=True)
    for local_archive in local_archives[n:]:
        local("sudo rm -f versions/{}".format(local_archive))

    # Remote Archive Cleanup
    with cd("/data/web_static/releases/"):
        remote_archives = run(
                "ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'").split()
        remote_archives.sort(reverse=True)
        for remote_archive in remote_archives[n:]:
            run("sudo rm -rf {}".format(remote_archive))
