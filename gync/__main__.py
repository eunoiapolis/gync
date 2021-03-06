# imports
import os, os.path, sys, subprocess

# functions
def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def check_args(args_list):
    if len(args_list) == 2 and args_list[1] in args_actions:
        pwd_dir = subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        if is_git_directory(pwd_dir.strip() + '/'):
            repo_args.append(pwd_dir.strip() + '/')
            modify_sync()
            print(pwd_dir.strip() + '/' + " successfully added as a git repository.")
        else:
            print(pwd_dir.strip() + '/' + " is not a git repository.")
    elif len(args_list) > 2 and args_list[1] in args_actions:
        for i in range(2, len(args_list)):
            if is_git_directory(args_list[i]):
                repo_args.append(args_list[i])
                print(args_list[i] + " successfully added as a git repository.")
            else:
                print(args_list[i] + " is not a git repository.")
        modify_sync()
    elif len(args_list) >= 2:
        print("Invalid args.")
        sys.exit()

def is_git_directory(path = '.'):
        return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0

def modify_sync():
    with safe_open_w(config_file) as config:
        if args_list[1] == '-a':
            for i in repo_args:
                if i not in repo_list:
                    repo_list.append(i)
        elif args_list[1] == '-r':
            for i in repo_args:
                if i in repo_list:
                    repo_list.remove(i)
        repo_list.sort()
        for path in repo_list:
            if is_git_directory(path):
                config.write(path)
                config.write('\n')
            else:
                print(path + " is not a git repository.")

def repo_check(path):
    std_output = subprocess.run(['git', '-C', path, 'status', '--porcelain'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if std_output == '':
        return True
    return False

def sync_repo(repo_list):
    for i in repo_list:
        if repo_check(i):
            print(i + " is up-to-date.")
        else:
            print("Syncing " + i)
            subprocess.run(["git","-C", i, "pull"])
            subprocess.run(["git","-C", i, "add", "."])
            subprocess.run(["git","-C", i, "commit", "-m", "autocommit"])
            subprocess.run(["git","-C", i, "push"])

# main function
config_file = str(os.environ.get('HOME'))+'/.config/gync/gync.conf'
args_list = sys.argv
args_actions = ['-a', '-r']

repo_list = []
repo_args = []

if os.path.exists(config_file):
    with open(config_file, 'r') as config:
        repo_list = config.read().splitlines()

check_args(args_list)
sync_repo(repo_list)
