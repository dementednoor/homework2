import os
from termcolor import colored


Error_dict = {
    'WO': 'Wrong actions order for a single task',  # WO for wrong order
    'PA': "Parallel activity on single core"  # PA for parallel activity
}
Error_list = []
State_sequence = ['activate', 'start', 'terminate']
Existing_tasks = {}  # task:state
Cores = {}  # core: list of tasks


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


def sync_checker(core_name, curr_task):
    for task_name in Existing_tasks:
        if (task_name and curr_task in Cores[core_name]) and task_name != curr_task \
                and Existing_tasks[task_name] != 'terminate':  # checking all tasks but current
            res = '{}. {}'.format(Error_dict['PA'], 'Referring to {} while {} is not terminated'
                                 .format(curr_task, task_name))
            #  print(colored(res, 'red')) - uncomment if you want to see errors in console too
            return res
        else:
            return None


if __name__ == '__main__':
    os.chdir('/home/noor/luxoft_hw/')
    path_init('Your current working directory is {}.'
              ' Would you like to change it? (y/n)'.format(colored(os.getcwd(), 'green')))
    with open('Demo_Exercise_Trace.btf', 'r') as f:
        data = f.read()
    strings = data.split('\n')
    strings.pop(0)  # deleting the 1st item because it's a comment
    strings.pop(-1)  # deleting the last item because it's empty
    core_tasks = []
    with open('/home/noor/PycharmProjects/luxoft-hw/error_report.txt', 'w') as er:
        for s in strings[1:30]:
            #  print(s)
            task_info = s.split(',')
            task_id = task_info[4]
            core = task_info[1]
            if task_id not in core_tasks:
                core_tasks.append(task_id)
            Cores[core] = core_tasks
            task = Task(task_id, task_info[-1])  # -1 as the last one parameter (state)
            if task.order_error_check(Existing_tasks.get(task.name)) is not None:
                Error_list.append('{}. {}'.format(s, task.order_error_check(Existing_tasks.get(task.name))))
                er.write('{}. {}'.format(s, task.order_error_check(Existing_tasks.get(task.name))))
            if sync_checker(core, task_id) is not None:
                Error_list.append('{}. {}'.format(s, sync_checker(core, task_id)))
                er.write('{}. {}'.format(s, sync_checker(core, task_id)))
            task.state_update()
        print('-'*30)
        for e in Error_list:
            print(e)
