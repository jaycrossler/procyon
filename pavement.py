from paver.easy import *
from paver.setuputils import setup
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

setup(
    name="procyon",
    packages=['procyon'],
    version='0.0.0.1',
    url="",
    author="Jay Crossler",
    author_email="jay.crossler@gmail.com"
)

@task
def install_dependencies():
    """ Installs dependencies."""
    sh('pip install --upgrade -r requirements.txt')

@task

@task
def install_dev_fixtures():
    """ Installs development fixtures in the correct order """
    fixtures = [
        'fixtures/initial_data.json',  # Users and site-wide data
        ]

    for fixture in fixtures:
        sh("python manage.py loaddata {fixture}".format(fixture=fixture))




def sync():
    """ Runs the syncdb process with migrations """
    sh("python manage.py syncdb --noinput")
    sh("python manage.py migrate --all")


@cmdopts([
    ('bind=', 'b', 'Bind server to provided IP address and port number.'),
])
@task
def start_django(options):
    """ Starts the Django application. """
    bind = options.get('bind', '')
    sh('python manage.py runserver %s &' % bind)

@task
def stop():
    """
    Stop the GeoNode Django application
    """
    kill('python', 'runserver')

@task
def start():
    """ Syncs the database and then starts the development server. """
    sync()
    start_django()
    info("The Procyon Pages are now available.")


@cmdopts([
    ('template=', 'T', 'Database template to use when creating new database, defaults to "template_postgis"'),
])
@task
def createdb(options):
    """ Creates the database in postgres. """
    from procyon import settings
    template = options.get('template', 'template1')
    database = settings.DATABASES.get('default').get('NAME')
    sh('createdb {database} -T {template}'.format(database=database, template=template))


@task
def create_db_user():
    """ Creates the database in postgres. """
    from procyon import settings
    database = settings.DATABASES.get('default').get('NAME')
    user = settings.DATABASES.get('default').get('USER')
    password = settings.DATABASES.get('default').get('PASSWORD')

    sh('psql -d {database} -c {sql}'.format(database=database,
            sql='"CREATE USER {user} WITH PASSWORD \'{password}\';"'.format(user=user, password=password)))



def kill(arg1, arg2):
    """Stops a proces that contains arg1 and is filtered by arg2
    """
    from subprocess import Popen, PIPE

    # Wait until ready
    t0 = time.time()
    # Wait no more than these many seconds
    time_out = 30
    running = True

    while running and time.time() - t0 < time_out:
        p = Popen('ps aux | grep %s' % arg1, shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

        lines = p.stdout.readlines()

        running = False
        for line in lines:

            if '%s' % arg2 in line:
                running = True

                # Get pid
                fields = line.strip().split()

                info('Stopping %s (process number %s)' % (arg1, fields[1]))
                kill = 'kill -9 %s 2> /dev/null' % fields[1]
                os.system(kill)

        # Give it a little more time
        time.sleep(1)
    else:
        pass

    if running:
        raise Exception('Could not stop %s: '
                        'Running processes are\n%s'
                        % (arg1, '\n'.join([l.strip() for l in lines])))

