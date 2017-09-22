# -*- coding: utf-8 -*-
# quick update, restart remote server
from fabric.api import run, env, local, cd, roles
from fabric.contrib import project
import os

# define sets of servers as roles
env.roledefs = {
    'app': ['160.16.242.199']
}
env.user = 'ec2-user'


def host_type():
    run('uname -s')


src_dir = {
    'production': '/var/opt/comic/prod',
    'dev': '/var/opt/comic/dev',
    'lpdev': '/var/opt/LP_dev/',
    'lppro': '/var/opt/LP_deploy/',
}


@roles('app')
def update(target='dev'):
    work_dir = src_dir.get(target, 'dev')
    script = 'restart'
    ping = 'curl 127.0.0.1/api/stat/'
    if target == 'production':
        script = 'restart_product'
        ping = 'curl 127.0.0.1/api/stat/'

    run('cd %s && git fetch' % work_dir)
    last_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (work_dir, last_commit))
    run('cd %s && git status' % work_dir)
    run('cd %s && source env/bin/activate && pip install -U pip' % work_dir)
    run('cd %s && source env/bin/activate && pip install -r requirements.txt' % work_dir)
    run('cd %s && cd bin && sh %s' % (work_dir, script))
    run(ping)


@roles('app')
def tail(target='dev'):
    work_dir = src_dir.get(target, 'dev')
    script = 'tail'
    if target == 'production':
        script = 'tail_p'
    run('cd %s && cd bin && sh %s' % (work_dir, script))


@roles('app')
def sync(target='dev'):
    work_dir = src_dir.get(target, 'dev')
    dirname = os.path.dirname
    local_path = dirname(os.path.abspath(__file__))
    sync_path = os.path.join(local_path, 'runtime')
    with cd(work_dir):
        exclude = ['*.pyc', '*~', '.DS*', '*.swp']
        project.rsync_project(work_dir, local_dir=sync_path, exclude=exclude)
