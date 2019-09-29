import unittest
import os
from termcolor import colored
from btf_tracer import trace_error_checker


class MyTestCase(unittest.TestCase):
    def test_path_init(self):  # checking btf path
        file_path = trace_error_checker.path_init(('Your current working directory is {}. '
                                                   'Would you like to change it? (y/n)'
                                                   .format(colored(os.getcwd(), 'green'))))
        self.assertEqual(os.getcwd(), file_path)

    def test_empty_file_checker(self):  # checking if trace file is not empty
        os.chdir('/home/noor/luxoft_hw/')
        self.assertFalse(os.path.getsize('Demo_Exercise_Trace.btf') == 0)

    def test_order_error_checker1(self):  # checking activate -> start sequence
        t = trace_error_checker.Task('T1', 'start')
        order = t.order_error_check('activate')
        self.assertEqual(order, None)

    def test_order_error_checker2(self):  # checking terminate -> activate sequence
        t = trace_error_checker.Task('T2', 'activate')
        order = t.order_error_check('terminate')
        self.assertEqual(order, None)

    def test_order_error_checker3(self):  # checking terminate -> start sequence (wrong one)
        t = trace_error_checker.Task('T1', 'start')
        order = t.order_error_check('terminate')
        self.assertEqual(order, '{}. {} follows {}'.format(trace_error_checker.Error_dict['WO'], t.state, 'terminate'))

    def test_sync_checker1(self):  # checking synchronous activity with another working task
        trace_error_checker.Existing_tasks = {'T1': 'activate', 'T2': 'start'}
        trace_error_checker.Cores = {'Core1': ['T1', 'T2']}
        sync = trace_error_checker.sync_checker('Core1', 'T2')
        self.assertNotEqual(sync, None)

    def test_sync_checker2(self):  # checking synchronous activity when only one task is working
        trace_error_checker.Existing_tasks = {'T1': 'active', 'T2': 'terminate'}
        trace_error_checker.Cores = {'Core1': ['T1', 'T2']}
        sync = trace_error_checker.sync_checker('Core1', 'T1')
        self.assertEqual(sync, None)


if __name__ == '__main__':
    unittest.main()
