import unittest
import os
import sys
import trace_error_checker


class MyTestCase(unittest.TestCase):
    def test_path_init(self):  # checking btf path
        file_path = trace_error_checker.path_init(('Your current working directory is {}. '
                                                   'Would you like to change it? (y/n)'
                                                   .format(os.getcwd())))
        self.assertEqual(os.getcwd(), file_path)

    def test_empty_file_checker(self):  # checking if trace file is not empty
        try:
            path = sys.argv[1]
            os.chdir(path)
            self.assertFalse(os.path.getsize('Demo_Exercise_Trace.btf') == 0)
        except IndexError:
            #  print("You didn't specify path to the btf file. Please, try again")
            self.skipTest('No path parameter')

    def test_order_error_checker1(self):  # checking activate -> start sequence
        t = trace_error_checker.Task('T1', 'start')
        trace_error_checker.State_sequence = ['activate', 'start', 'terminate']
        trace_error_checker.Full_state_sequence = ['activate', 'start', 'preempt', 'resume', 'terminate']
        order = t.order_error_check('activate')
        self.assertEqual(order, None)

    def test_order_error_checker2(self):  # checking terminate -> activate sequence
        t = trace_error_checker.Task('T2', 'activate')
        trace_error_checker.State_sequence = ['activate', 'start', 'terminate']
        trace_error_checker.Full_state_sequence = ['activate', 'start', 'preempt', 'resume', 'terminate']
        order = t.order_error_check('terminate')
        self.assertEqual(order, None)

    def test_order_error_checker3(self):  # checking terminate -> start sequence (wrong one)
        trace_error_checker.Error_dict = {
            'WO': 'Wrong actions order for a single task',  # WO for wrong order
            'PA': "Parallel activity on single core"  # PA for parallel activity
        }
        t = trace_error_checker.Task('T1', 'start')
        order = t.order_error_check('terminate')
        self.assertEqual(order, '{}. {} follows {}'.format(trace_error_checker.Error_dict['WO'], t.state, 'terminate'))

    def test_sync_checker1(self):  # checking synchronous activity with another working task
        trace_error_checker.Existing_tasks = {'T1': 'start', 'T2': 'start'}
        trace_error_checker.Error_dict = {
            'WO': 'Wrong actions order for a single task',  # WO for wrong order
            'PA': "Parallel activity on single core"  # PA for parallel activity
        }
        core = trace_error_checker.Core('Core1')
        core.tasks = ['T1', 'T2']
        sync = core.sync_checker('T2')
        self.assertNotEqual(sync, None)

    def test_sync_checker2(self):  # checking synchronous activity when only one task is working
        trace_error_checker.Existing_tasks = {'T1': 'active', 'T2': 'terminate'}
        core = trace_error_checker.Core('Core1')
        core.tasks = ['T1', 'T2']
        sync = core.sync_checker('T1')
        self.assertEqual(sync, None)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
