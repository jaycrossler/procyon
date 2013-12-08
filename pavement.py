from paver.easy import *
from paver.setuputils import setup
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

setup(
    name="procyon",
    packages=['procyon'],
    version='0.0.0.2',
    url="",
    author="Jay Crossler",
    author_email="jay.crossler@gmail.com"
)


@task
def install_dependencies():
    """ Installs dependencies."""
    sh('pip install --upgrade -r requirements.txt')


@task
def shell():
    sh('python manage.py shell')


@task
def install_dev_fixtures():
    """ Installs development fixtures in the correct order """
    fixtures = [
        'procyon/fixtures/initial_data.json',  # Users and site-wide data
        'procyon/fixtures/star_type.json',
        'procyon/fixtures/starcatalog.planet.json',
        'procyon/fixtures/starcatalog.starpossiblyhabitable.json',
    ]

    for fixture in fixtures:
        sh("python manage.py loaddata {fixture}".format(fixture=fixture))

    fixture = lambda file_name: os.path.join(os.path.dirname(os.path.abspath(__file__)), 'procyon/fixtures', file_name)
    db = 'procyon'

    #NOTE - we're importing these from a data file because: a)They can be updated, and
    #       b)It's so much data (55Mb when exported)
    filename='hygxyz.csv'
    num_lines = sum(1 for line in open(fixture(filename)))
    sh('psql -d {db} -c "COPY starcatalog_star FROM \'{file}\' DELIMITER \',\' CSV header;"'.format(db=db, file=fixture(filename)))
    sh('psql -d {db} -c "alter sequence starcatalog_star_id_seq restart with {linecount};"'.format(db=db, linecount=num_lines+1))
    sh('psql -d {db} -c "insert into starsystemmaker_starmodel (star_id, location) select id, ST_SetSRID(ST_MakePoint("X", "Y", "Z"),900913) from starcatalog_star;"')


@task
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
def stop_django():
    """
    Stop the GeoNode Django application
    """
    kill('python', 'runserver')


@task
def stop():
    """ Syncs the database and then starts the development server. """
    stop_django()


@task
def start():
    """ Syncs the database and then starts the development server. """
    stop()
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

    # Presuming you have the latest version of postgres/postgis, otherwise, have to run:
    #   https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/
    sh('psql -d {database} -c "CREATE EXTENSION postgis;"'.format(database=database))
    sh('psql -d {database} -c "CREATE EXTENSION postgis_topology;"'.format(database=database))


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
                killcmd = 'kill -9 %s 2> /dev/null' % fields[1]
                os.system(killcmd)

        # Give it a little more time
        time.sleep(1)
    else:
        pass

    if running:
        raise Exception('Could not stop %s: '
                        'Running processes are\n%s'
                        % (arg1, '\n'.join([l.strip() for l in lines])))