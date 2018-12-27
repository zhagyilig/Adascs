import toml
import os
import sys
import docker
import commands
import time
from functools import wraps
import logging

reload(sys)
sys.setdefaultencoding('utf8')

def setup_logger():
    formatter = logging.Formatter('[%(asctime)s] %(funcName)s(%(lineno)d) %(levelname)s %(message)s')
    handler = logging.FileHandler('jenkins_build.log')
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

def run_timer(func):
        @wraps(func)
        def func_timer(*args,**kwargs):
                start = time.time()
                result = func(*args,**kwargs)
                end = time.time()
                print ("Total time running %s: %s seconds" %
                        (func.func_name, end-start)
                      )
                return result
        return func_timer

@run_timer
def auto_build(project, workspace='none',consul_ip='192.168.199.64:8500',uat_env='1'):
    supervisor_file = '/home/mico/docker/auto_jenkins_build/' + project + '.ini'
    supervisor_ini = project + '.ini'
    ports = []
    ports_dict = {}

    logger.info('=== auto_build ===')
    logger.info(project)
    logger.info(workspace)
    logger.info(consul_ip)
    logger.info(uat_env)

    result = os.system('CONSUL=%s /srv/goProjects/goflow/bin/goflowx conf -service %s /home/mico/docker/auto_jenkins_build/conf.ctmpl /home/mico/docker/auto_jenkins_build/%s_conf.toml' % (consul_ip, project, project))

    logger.info(result)

    if result != 0:
        print "consul: %s" % consul_ip
	exit(1)

    if consul_ip == '13.228.224.35:8500':
	consul_ip = '172.31.28.159:8500'

    with open("%s_conf.toml" % project) as f:
        config = toml.loads(f.read())

    if os.path.exists(supervisor_file):
        os.remove(supervisor_file)

    if os.path.exists('Dockerfile'):
        os.remove('Dockerfile')
    for command,port in config['listen_addrs'].items():
        if type(port) == list:
            for p in port:
                p = p.split(':')
                ports.append(p[1])
                ports_dict[p[1]] = p[1]
        else:
            port = port.split(':')
            print '-----777----',port
            if port.count('') == 1 and len(port) == 2:
                ports.append(port[1])
                ports_dict[port[1]] = port[1]
            elif port[0] != '':
                ports.append(port[0])
                ports_dict[port[0]] = port[0]
            else:
                #print 'The toml file format is error..'
                #return 0
                pass

        print '2222'
        if command in ['root_port','no_port']:
            instance = '''
[program:%s]
command=/project/%s -c /project/conf.ctmpl
numprocs=1
numprocs_start=0
priority=999
autostart=true
autorestart=unexpected
startsecs=3
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=20
directory=/project
stopasgroup=false
killasgroup=false
redirect_stderr=true
stdout_logfile=/logs/%s.access.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stderr_logfile=/logs/%s.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
environment=PYTHONPATH='/project'
environment=UATENV='%s',CONSUL='%s'
            ''' % (project, project, project, project,uat_env,consul_ip)
        else:
            instance = '''
[program:%s_%s]
command=/project/%s %s -c /project/conf.ctmpl
numprocs=1
numprocs_start=0
priority=999
autostart=true
autorestart=unexpected
startsecs=3
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=20
directory=/project
stopasgroup=false
killasgroup=false
redirect_stderr=true
stdout_logfile=/logs/%s.%s.access.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stderr_logfile=/logs/%s.%s.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
environment=PYTHONPATH='/project'
environment=UATENV='%s',CONSUL='%s'
#environment=CONSUL=consulip:8500
            ''' % (project,command.replace(" ", "_"),project,command,project,command.replace(" ", "_"),project,command.replace(" ", "_"),uat_env,consul_ip)
        ini = open(supervisor_file,'a+')
        ini.write(instance)
        print instance
    if project == 'ugm':
        instance_jobs = '''
[program:ugm_job_expirer]
command=/project/ugm job expirer -c /project/conf.ctmpl
numprocs=1
numprocs_start=0
priority=999
autostart=true
autorestart=unexpected
startsecs=3
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=20
directory=/project
stopasgroup=false
killasgroup=false
redirect_stderr=true
stdout_logfile=/logs/ugm.job.expirer.access.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stderr_logfile=/logs/ugm.job.expirer.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
environment=PYTHONPATH='/project'
environment=UATENV='%s',CONSUL='%s'
#environment=CONSUL=consulip:8500

[program:ugm_job_mautic]
command=/project/ugm job mautic -c /project/conf.ctmpl
numprocs=1
numprocs_start=0
priority=999
autostart=true
autorestart=unexpected
startsecs=3
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=20
directory=/project
stopasgroup=false
killasgroup=false
redirect_stderr=true
stdout_logfile=/logs/ugm.job.mautic.access.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stderr_logfile=/logs/ugm.job.mautic.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
environment=PYTHONPATH='/project'
environment=UATENV='%s',CONSUL='%s'
#environment=CONSUL=consulip:8500

[program:ugm_job_syncer]
command=/project/ugm job syncer -c /project/conf.ctmpl
numprocs=1
numprocs_start=0
priority=999
autostart=true
autorestart=unexpected
startsecs=3
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=20
directory=/project
stopasgroup=false
killasgroup=false
redirect_stderr=true
stdout_logfile=/logs/ugm.job.syncer.access.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stderr_logfile=/logs/ugm.job.syncer.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
environment=PYTHONPATH='/project'
environment=UATENV='%s',CONSUL='%s'
#environment=CONSUL=consulip:8500
        ''' % (uat_env,consul_ip,uat_env,consul_ip,uat_env,consul_ip)
        ini.write(instance_jobs)
        print instance_jobs
    ini.close()

    file_resource = ''
    if config.has_key('file_resource'):
        for k,v in config['file_resource'].items():
            file_resource = file_resource + 'copy %s /project/%s\n' %(k,v)
        os.system('cp -r %s/%s /home/mico/docker/auto_jenkins_build/'%(workspace,k))
    if len(ports) == 0:
        dockerfile_file = '''
From hub.ezbuy.me/goservices/goservices
ADD %s /project
ADD conf.ctmpl /project
ADD %s /app
%s
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
VOLUME ["/app","/logs","/project","/srv/feedshare"]
WORKDIR /app
ENV JAEGER_AGENT_HOST="192.168.199.70"
#CMD  ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]
       ''' % (project,supervisor_ini,file_resource)
    else:
         dockerfile_file = '''
From hub.ezbuy.me/goservices/goservices
ADD %s /project
ADD conf.ctmpl /project
ADD %s /app
%s
VOLUME ["/app","/logs","/project","/srv/feedshare"]
WORKDIR /app
ENV JAEGER_AGENT_HOST="192.168.199.70"
EXPOSE %s
#CMD  ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]
        ''' % (project,supervisor_ini,file_resource," ".join(ports))

    with open('/home/mico/docker/auto_jenkins_build/Dockerfile','w') as f:
        f.write(dockerfile_file)
    print dockerfile_file
    print ports
    print ports_dict
    return ports_dict

@run_timer
def start_container(project,docker_url='192.168.199.56:2375',**kwargs):
    ports = kwargs
    print ports
    project = project.lower()
    client = docker.DockerClient(base_url='tcp://%s' % docker_url,version='1.21')
    client.login(username='admin', password='Ezbuy123456', registry='hub.ezbuy.me')
    client.images.pull('hub.ezbuy.me/goservices/%s:latest' % project)
    try:
        if client.containers.get(project):
            client.containers.get(project).remove(force='true')
    except Exception,e:
        print 'no container!'
        print e
    client.containers.run('hub.ezbuy.me/goservices/%s:latest' % project,detach=True,mem_limit="2G",name=project,restart_policy={"Name":"always"},ports=ports['ports'],volumes={"/logs":{"bind":"/logs","mode":"rw"}, "/srv/feedshare":{"bind":"/srv/feedshare","mode":"rw"}},environment=["consul_ip=192.168.199.64:8500"])


@run_timer
def docker_push_image(project,build_number):
    """push image"""
    project = project.lower()
    print '## docker_push_image: ',project
    try:
        client = docker.DockerClient(base_url='tcp://192.168.199.56:2375', version='1.39')
        print 1
        client.login(username='admin', password='Ezbuy123456', registry='hub.ezbuy.me')
        print 2
        client.images.build(path='/home/mico/docker/auto_jenkins_build/', tag='%s:%s' % (project,build_number), dockerfile='Dockerfile')
        print 3
        img = client.images.get('%s:%s' %(project,build_number))
        print 4
        img.tag(repository='hub.ezbuy.me/goservices/%s' % (project), tag='latest', force='true')
        print 5
        client.images.push('hub.ezbuy.me/goservices/%s:latest' %(project))
        print 6
    except Exception,e:
        print '## function(docker_push_image) is failed, detail error: %s' % e
        sys.exit()
    print 'docker_push_image is success'

if __name__ == '__main__':
    print '---------create_supervisor_file-------------'
    logger.info('---------create_supervisor_file-------------')
    try:
        if len(sys.argv) == 3:
            ports_dict = auto_build(sys.argv[1])
        elif len(sys.argv) == 4:
            ports_dict = auto_build(sys.argv[1],sys.argv[3])
        elif len(sys.argv) == 6:
            ports_dict = auto_build(sys.argv[1],sys.argv[3],sys.argv[4])
        elif len(sys.argv) == 7:
            ports_dict = auto_build(sys.argv[1],sys.argv[3],sys.argv[4],sys.argv[6])
    except Exception,e:
        print  'auto_build is fiald'
        print e
        sys.exit()
    print  '## auto_build is success'

    if type(ports_dict) == dict:
        print '---------docker_push_image-------------'
        docker_push_image(sys.argv[1],sys.argv[2]) # $projectName $BUILD_NUMBER
        print '---------start_docker_container-------------'
        print("## len(sys.argv): ", len(sys.argv))
        print(sys.argv[1],sys.argv[5])

        if len(sys.argv) in [6,7]:
            start_container(sys.argv[1],sys.argv[5],ports=ports_dict)
	else:
            start_container(sys.argv[1],ports=ports_dict)
