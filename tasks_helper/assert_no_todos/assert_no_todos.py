import os


def assert_no_todos():
    has_todo_been_found = False
    for root, directories, files in os.walk(os.curdir):
        for filename in files:
            filepath = os.path.join(root, filename)

            if root.startswith('./.git') or root.startswith('./.idea'):
                continue
            if filename == 'assert_no_todos.py':
                continue

            try:
                with open(filepath, 'r') as file:
                    if 'TODO' in file.read():
                        has_todo_been_found = True
                        print(f'TODO found in {filepath}')
            except BaseException:
                # ignore error
                pass

    if has_todo_been_found:
        exit(1)
