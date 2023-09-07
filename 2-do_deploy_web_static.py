#!/usr/bin/python3
"""
fabric script that generates a .tgz archive from
the contents of web_static
distributes archive to web servers
"""
from fabric import task
from fabric.exceptions import NetworkError
import os


"""Define the user and hosts for the web servers"""
env.user = 'ubuntu'
env.hosts = ['54.209.59.161', '52.3.246.242']

@task
def do_deploy(archive_path):
    """
    Distribute and deploy an archive to web servers.
    """
    if not os.path.isfile(archive_path):
        return False

    try:
        """Get the base name of the archive (without extension)"""
        base_name = os.path.basename(archive_path).split('.')[0]

        """Upload the archive to the /tmp/ directory on the web servers"""
        put(archive_path, '/tmp/')

        """Create the release directory"""
        run('mkdir -p /data/web_static/releases/{}'.format(base_name))

        """Uncompress the archive to the release directory"""
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(os.path.basename(archive_path), base_name))

        """Remove the uploaded archive"""
        run('rm /tmp/{}'.format(os.path.basename(archive_path)))

        """Create a symbolic link to the new release"""
        run('rm -f /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(base_name))

        return True

    except NetworkError:
        return False
