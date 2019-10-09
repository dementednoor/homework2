import os
from termcolor import colored
import sys


Error_dict = {
    'WO': 'Wrong actions order for a single task',  # WO for wrong order
    'PA': "Parallel activity on single core"  # PA for parallel activity
}
Error_list = []
State_sequence = ['activate', 'start', 'terminate']
Existing_tasks = {}  # task:state
# core: list of tasks


class Core:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_tasks(self, task):
        self.tasks.append(task)

    def sync_checker(self, curr_task):
        for tsk in Existing_tasks:
            # checking if two tasks are different and if they both are running at the same core
            if tsk and curr_task in self.tasks and curr_task != tsk:
                try:
                    if Existing_tasks[tsk] != 'terminate' and Existing_tasks[curr_task] in ['active', 'start']:
                        res = '{}. ({}:{}, {}:{})'.format(Error_dict['PA'], curr_task, Existing_tasks[curr_task],
                                                          tsk, Existing_tasks[tsk])
                        return res
                    elif Existing_tasks[curr_task] != 'terminate' and Existing_tasks[tsk] in ['active', 'start']:
                        res = '{}. ({}:{}, {}:{})'.format(Error_dict['PA'], curr_task, Existing_tasks[curr_task],
                                                          tsk, Existing_tasks[tsk])
                        return res
                except KeyError:  # raises if the task is not among existing ones yet
                    if Existing_tasks[tsk] in ['active', 'start']:
                        res = '{}. {}'.format(Error_dict['PA'], 'Starting one task while another is not terminated')
                        return res


class Task:
    def __init__(self, name, state):
        self.name = name
        self.state = state

    def state_update(self):
        Existing_tasks[self.name] = self.state

    def order_error_check(self, prev_state):
        try:
            prev_idx = State_sequence.index(prev_state)  # previous state index
            if State_sequence[prev_idx+1] != self.state:
                res = '{}. {} follows {}'.format(Error_dict['WO'], self.state, prev_state)
                #  print(colored(res, 'red')) - uncomment if you want to see errors in console too
                return res
            else:
                return None
        except IndexError:  # raises when prev_state = 'terminate' and it's the last element of the list
            if State_sequence[0] != self.state:
                res = '{}. {} follows {}'.format(Error_dict['WO'], self.state, prev_state)
                #  print(colored(res, 'red'))  uncomment if you want to see errors in console too
                return res
            else:
                return None
        except ValueError:  # raises in the very beginning when states in Existing_tasks are None
            if self.state != 'activate':
                res = "{}. {} is not activated".format(Error_dict['WO'], self.name)
                #  print(colored("{}. {} is not activated".format(Error_dict['WO'], self.name), 'red')) -
                #  uncomment if you want to see errors in console too
                return res
            else:
                return None


def path_init(start_message):
    print(start_message)
    answer = input()
    if answer == 'y':
        path = input('Enter working directory path:\n')
        try:
            os.chdir(path)
            print("Current path is {} now.".format(colored(os.getcwd(), 'green')))
        except FileNotFoundError:
            print("This path doesn't exist. Please, try again.")
            path_init('Your current working directory is {}. '
                      'Would you like to change it? (y/n)'.format(colored(os.getcwd(), 'green')))
    elif answer == 'n':
        print('Working directory remains the same.\n')
    else:
        path_init("Please answer 'y' or 'n'")
    return os.getcwd()


if __name__ == '__main__':
    try:
        os.chdir(sys.argv[1])  # path to dir with btf file
        path_init('Your current working directory is {}.'
                  ' Would you like to change it? (y/n)'.format(colored(os.getcwd(), 'green')))
        with open('Demo_Exercise_Trace.btf', 'r') as f:
            data = f.read()
        strings = data.split('\n')
        strings.pop(0)  # deleting the 1st item because it's a comment
        strings.pop(-1)  # deleting the last item because it's empty
        with open(sys.argv[2], 'w') as er:
            for s in strings:
                #  print(s)
                task_info = s.split(',')
                task_id = task_info[4]
                core = Core(task_info[1])
                if task_id not in core.tasks:
                    core.tasks.append(task_id)
                task = Task(task_id, task_info[-1])  # -1 as the last one parameter (state)
                if task.order_error_check(Existing_tasks.get(task.name)) is not None:
                    Error_list.append('{}. {}'.format(s, task.order_error_check(Existing_tasks.get(task.name))))
                    er.write('{} {} {}\n'.format(task_info[0], strings.index(s) + 2,
                                                 task.order_error_check(Existing_tasks.get(task.name))))
                task.state_update()
                if core.sync_checker(task_id) is not None:
                    Error_list.append('{}. {}'.format(s, core.sync_checker(task_id)))
                    er.write('{} {} {}\n'.format(task_info[0], strings.index(s)+2, core.sync_checker(task_id)))
    except IndexError:
        print("You didn't specify paths to the btf directory and output file. Please, try again")
