#!/usr/bin/python3
"""
Create a .tgz archive from the contents of the web_static folder.
Distribute this archive to multiple web servers, effectively
 deploying your web application.
"""
from fabric.api import env, put, run, local
from os import path
from datetime import datetime


env.hosts = ['54.209.59.161', '52.3.246.242']

def do_pack():
    """
    This function is responsible for creating a timestamped
    .tgz archive of the web_static folder.
    """
    current_date = datetime.utcnow()
    file = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(
        current_date.year,
        current_date.month,
        current_date.day,
        current_date.hour,
        current_date.minute,
        current_date.second)

    if path.isdir('versions') is False:
        if local('mkdir -p versions').failed is True:
            return None
    if local('tar -cvzf {} web_static'.format(file)).failed is True:
        return None
    return file

def do_deploy(archive_path):
    """
    This function is responsible for deploying the archive to the web
    servers and setting up the symbolic link.
    """
    file = archive_path.split('/')[-1]
    name = archive_path.split('.')[0]
    if path.isfile(archive_path):
        if put(archive_path, '/tmp/{}'.format(file)).failed is True:
            return False
        if run('rm -rf /data/web_static/releases/{}/'.
               format(name)).failed is True:
            return False
        if run('mkdir -p /data/web_static/releases/{}/'.
               format(name)).failed is True:
            return False
        if run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
                file, name)).failed is True:
            return False
        if run('rm /tmp/{}'.format(file)).failed is True:
            return False
        if run("mv /data/web_static/releases/{}/web_static/* "
               "/data/web_static/releases/{}/".format(
                       name,
                       name)).failed is True:
            return False
        if run("rm -rf /data/web_static/releases/{}/web_static".
               format(name)).failed is True:
            return False
        if run('rm /data/web_static/current').failed is True:
            return False
        if run('ln -s /data/web_static/releases/{} /data/web_static/current'
               .format(name)).failed is True:
            return False
        return True
    return False

def deploy():
    """
    higher-level function that calls do_pack and then do_deploy. It's a
    convenient way to trigger both packaging and deployment with a single command
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
