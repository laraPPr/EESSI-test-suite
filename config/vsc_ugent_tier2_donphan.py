from reframe.core.backends import register_launcher
from reframe.core.launchers import JobLauncher
import os

account = "gentall"

# use 'info' to log to syslog
syslog_level = 'warning'

perf_logging_format = 'reframe: ' + '|'.join([
    'username=%(osuser)s',
    'version=%(version)s',
    'name=%(check_name)s',
    'system=%(check_system)s',
    'partition=%(check_partition)s',
    'environ=%(check_environ)s',
    'num_tasks=%(check_num_tasks)s',
    'num_cpus_per_task=%(check_num_cpus_per_task)s',
    'num_tasks_per_node=%(check_num_tasks_per_node)s',
    'modules=%(check_modules)s',
    'jobid=%(check_jobid)s',
    '%(check_perfvalues)s',
])

format_perfvars = '|'.join([
    'perf_var=%(check_perf_var)s',
    'perf_value=%(check_perf_value)s',
    'unit=%(check_perf_unit)s',
]) + '|'


@register_launcher('mympirun')
class MyMpirunLauncher(JobLauncher):
    def command(self, job):
        return ['mympirun', '--hybrid', str(job.num_tasks)]


site_configuration = {
    'systems': [
        {
            'name': 'donphan',
            'descr': 'donphan',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'donphan',
                    'scheduler': 'slurm',
                    'prepare_cmds': [
                        'source /cvmfs/pilot.eessi-hpc.org/latest/init/bash',
                        'export SLURM_EXPORT_ENV=ALL',
                        'export OMPI_MCA_pml=ucx',
                    ],
                    'environs': ['default'],
                    'access':  ['-p cpu', '--export=None'],
                    'descr': 'cpu nodes',
                    'max_jobs': 1,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 8,
                    },
                    'features': [
                        'cpu',
                    ],
                },
            ]
        },
    ],
    'environments': [
        {
            'name': 'default',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
        },
        {
            'name': 'foss-2021a',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpif90',
            'modules': ['foss/2021a']
        },
        {
            'name': 'intel-2021a',
            'modules': ['intel'],
            'cc': 'mpiicc',
            'cxx': 'mpiicpc',
            'ftn': 'mpiifort',
        },
        {
            'name': 'CUDA',
            'modules': ['CUDA'],
            'cc': 'nvcc',
            'cxx': 'nvcc',
        },
        {
            'name': 'foss-2020b',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpif90',
            'modules': ['foss/2020b']
        },
    ],
    'general': [
        {
            'purge_environment': True,
            'resolve_module_conflicts': False,  # avoid loading the module before submitting the job
            'keep_stage_files': True,
        }
    ],
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'file',
                    'name': os.path.join(os.getenv('RFM_OUTPUT_DIR', os.curdir), 'logs', 'reframe.log'),
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_name)s: %(message)s',  # noqa: E501
                    'append': False,
                    'timestamp': "%Y%m%d_%H%M%S",
                },
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s',
                },
                {
                    'type': 'file',
                    'name': 'reframe.out',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': False,
                },
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': '%(check_job_completion_time)s ' + perf_logging_format,
                    'format_perfvars': format_perfvars,
                    'append': True,
                },
                {
                    'type': 'syslog',
                    'address': '/dev/log',
                    'level': syslog_level,
                    'format': perf_logging_format,
                    'format_perfvars': format_perfvars,
                    'append': True,
                },
            ],
        }
    ],
}
