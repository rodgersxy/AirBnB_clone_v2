#!/usr/bin/python3
"""
fabric script that generates a .tgz archive from
the contents of web_static
distributes archive to web servers
"""
from fabric.api import local, put, run, env
from datetime import datetime


"""Define the user and hosts for the web servers"""
env.user = 'ubuntu'
env.hosts = ['54.209.59.161', '52.3.246.242']

def do_pack():
    """distribute and deploy an archive to web servers"""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local('sudo mkdir -p ./versions')
    path = './versions/web_static_{}'.format(now)
    local('sudo tar -czvf {}.tgz web_static'.format(path))
    name = '{}.tgz'.format(path)
    if name:
        return name
    else:
        return None


def do_deploy(archive_path):
    """
    Distribute and deploy an archive to web servers.
    Upload the archive to the /tmp/ directory on the web servers
    Create a symbolic link to the new release
    """
    try:
        archive = archive_path.split('/')[-1]
        path = '/data/web_static/releases/' + archive.strip('.tgz')
        current = '/data/web_static/current'
        put(archive_path, '/tmp')
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(archive, path))
        run('rm /tmp/{}'.format(archive))
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf {}'.format(current))
        run('ln -s {} {}'.format(path, current))
        print('New version deployed!')
        return True
    except:
        return False
