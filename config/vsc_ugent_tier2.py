# the reframe command needs to contain the following in order to help ReFrame with selecting the system since it uses hostname as the selection parameter and it is the same for all clusters.
# `--system $SLURM_CLUSTERS`

from reframe.core.backends import register_launcher
from reframe.core.launchers import JobLauncher
import os

account = ""

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
            'name': 'doduo',
            'descr': 'doduo cpu only',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'doduo',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/doduo'],
                    'access': ['--clusters=doduo'],
                    'environs': ['default'],
                    'descr': 'GPU nodes (AMD Rome, 250GiB RAM)',
                    'max_jobs': 128,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 96,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 48,
                        'arch': 'zen2',
                    },
                    'features': [
                        'cpu',                     
                    ],
                }
            ]   
        },
        {
            'name': 'swalot',
            'descr': 'swalot cpu only',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'swalot',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/swalot'],
                    'access': ['--clusters=swalot'],
                    'environs': ['default'],
                    'descr': 'CPU nodes (intel-haswell, 116GiB RAM)',
                    'max_jobs': 128,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 20,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 10,
                        'arch': 'haswell',
                    },
                    'features': [
                        'cpu',
                    ],
                }
            ]
        },
        {
            'name': 'skitty',
            'descr': 'skitty cpu only',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'skitty',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/skitty'],
                    'access': ['--clusters=skitty'],
                    'environs': ['default'],
                    'descr': 'CPU nodes (intel-skylake, 177GiB RAM)',
                    'max_jobs': 72,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 36,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 18,
                        'arch': 'skylake',
                    },
                    'features': [
                        'cpu',
                    ],
                }
            ]
        },
        {
            'name': 'victini',
            'descr': 'victini cpu only',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'victini',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/victini'],
                    'access': ['--clusters=victini'],
                    'environs': ['default'],
                    'descr': 'CPU nodes (intel-skylake, 88GiB RAM)',
                    'max_jobs': 96,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 36,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 18,
                        'arch': 'skylake',
                    },
                    'features': [
                        'cpu',
                    ],
                }
            ]
        },
        { 
            'name': 'gallade',
            'descr': 'gallade cpu only',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'gallade',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/gallade'],
                    'access': ['--clusters=gallade'],
                    'environs': ['default'],
                    'descr': 'cpu nodes (AMD Milan, 940GiB RAM)',
                    'max_jobs': 16,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 128,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 64,
                        'arch': 'zen3',
                    },
                    'features': [
                        'cpu',
                    ],
                }
            ]
        },
        { 
            'name': 'donphan',
            'descr': 'donphan cpu only',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'donphan',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/donphan'],
                    'access': ['--clusters=donphan'],
                    'environs': ['default'],
                    'descr': 'cpu nodes (Intel Cascade Lake, 738GiB RAM)',
                    'max_jobs': 16,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 36,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 18,
                    },
                    'features': [
                        'cpu',
                    ],
                }
            ]
        },
        {
            'name': 'accelgor',
            'descr': 'accelgor gpu cluster',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'accelgor',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/accelgor'],
                    'access': ['--clusters=accelgor'],
                    'environs': ['default'],
                    'descr': 'gpu nodes',
                    'max_jobs': 9,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 48,
                        'num_sockets': 2,                        
                        'num_cpus_per_socket': 24,
                    },
                    'features': [
                        'gpu',
                    ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node={num_gpus_per_node}'],
                        }
                    ],
                    'devices': [
                        {
                            'type': 'gpu',
                            'num_devices': 4,
                        }
                    ],
                }
            ]
        },
        {
            'name': 'joltik',
            'descr': 'joltik',
            'hostnames': ['gligar.*.gastly.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'joltik',
                    'scheduler': 'slurm',
                    'prepare_cmds': ['module swap cluster/joltik'],
                    'access': ['--clusters=joltik'],
                    'environs': ['default'],
                    'descr': 'gpu nodes',
                    'max_jobs': 10,
                    'launcher': 'mympirun',
                    'modules': ['vsc-mympirun'],
                    'processor': {
                        'num_cpus': 32,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 16,
                    },
                    'features': [
                        'gpu',
                    ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node={num_gpus_per_node}'],
                        }
                    ],
                    'devices': [
                        {
                            'type': 'gpu',
                            'num_devices': 4,
                        }
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
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_name)s: %(message)s',  # noqa: E501
                    'append': False,
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
