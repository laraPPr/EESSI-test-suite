"""
This module tests the binary 'lmp' in available modules containing substring 'LAMMPS'.
The tests come from the lammps github repository (https://github.com/lammps/lammps/)
"""

import reframe as rfm
import reframe.utility.sanity as sn

from eessi.testsuite import hooks, utils
from eessi.testsuite.constants import *  # noqa

@rfm.simple_test
class EESSI_LAMMPS(rfm.RunOnlyRegressionTest):
    scale = parameter(SCALES.keys())
    valid_prog_environs = ['default']
    valid_systems = ['*']
    time_limit = '30m'
    tags = {TAGS['CI']}
    device_type = parameter([DEVICE_TYPES[CPU], DEVICE_TYPES[GPU]])

    # Parameterize over all modules that start with LAMMPS
    module_name = parameter(utils.find_modules('LAMMPS'))
    executable = 'lmp -in in.lj'

    # Set sanity step
    @deferrable
    def assert_lammps_openmp_treads(self):
        '''Assert that OpenMP thread(s) per MPI task is set'''
        n_threads = sn.extractsingle(
            '^  using (?P<threads>[0-9]+) OpenMP thread\(s\) per MPI task', self.stdout, 'threads', int)

        return sn.assert_eq(n_threads, self.num_cpus_per_task)

    @deferrable
    def assert_lammps_processor_grid(self):
        '''Assert that the processor grid is set correctly'''
        grid = list(sn.extractall(
            '^  (?P<x>[0-9]+) by (?P<y>[0-9]+) by (?P<z>[0-9]+) MPI processor grid', self.stdout, tag=['x', 'y', 'z']))
        n_cpus = int(grid[0][0]) * int(grid[0][1]) * int(grid[0][2])

        return sn.assert_eq(n_cpus, self.num_tasks)

    @deferrable
    def assert_total_nr_neigbors(self):
        '''Assert that the test calulated the right number of neighbours'''
        n_neighbours = sn.extractsingle(
            '^Total \# of neighbors \= (?P<neighbours>\S+)', self.stdout, 'neighbours', int)
        
        return sn.assert_eq(n_neighbours, 1202833)


    @sanity_function
    def assert_sanity(self):
        '''Check all sanity criteria'''
        return sn.all([
            self.assert_lammps_openmp_treads(),
            self.assert_lammps_processor_grid(),
            self.assert_total_nr_neigbors(),
        ])


    @performance_function('img/s')
    def perf(self):
        return sn.extractsingle(r'^(?P<perf>[.0-9]+)% CPU use with [0-9]+ MPI tasks x [0-9]+ OpenMP threads', self.stdout, 'perf', float)

    @run_after('init')
    def run_after_init(self):
        """hooks to run after init phase"""

        # Filter on which scales are supported by the partitions defined in the ReFrame configuration
        hooks.filter_supported_scales(self)

        hooks.filter_valid_systems_by_device_type(self, required_device_type=self.device_type)

        hooks.set_modules(self)

        # Set scales as tags
        hooks.set_tag_scale(self)

    @run_after('setup')
    def run_after_setup(self):
        """hooks to run after the setup phase"""
        # TODO: implement
        # It should bind to socket, but different MPIs may have different arguments to do that...
        # We should at very least prevent that it binds to single core per process,
        # as that results in many threads being scheduled to one core.
        # binding may also differ per launcher used. It'll be hard to support a wide range and still get proper binding
        if self.device_type == 'cpu':
            hooks.assign_tasks_per_compute_unit(test=self, compute_unit=COMPUTE_UNIT['CPU_SOCKET'])
        elif self.device_type == 'gpu':
            hooks.assign_tasks_per_compute_unit(test=self, compute_unit=COMPUTE_UNIT['GPU'])
        else:
            raise NotImplementedError(f'Failed to set number of tasks and cpus per task for device {self.device_type}')

    @run_after('setup')
    def set_omp_num_threads(self):
        """
        Set number of OpenMP threads.
        Set OMP_NUM_THREADS.
        Set default number of OpenMP threads equal to number of CPUs per task.
        """

        omp_num_threads = self.num_cpus_per_task
        self.env_vars['OMP_NUM_THREADS'] = omp_num_threads
        utils.log(f'env_vars set to {self.env_vars}')