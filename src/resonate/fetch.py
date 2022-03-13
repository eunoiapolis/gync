# imports
import os, os.path, sys, subprocess, csv

# functions
def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def check_args(args_list):
    if len(args_list) == 2 and args_list[1] in args_remote:
        for i in remote_list:
            if not is_git_repository(i[0]):


    if len(args_list) == 2 and args_list[1] in args_actions:
        pwd_dir = (subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')).strip() + '/'
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

def modify_fetch():
    with safe_open_w(fetch_file) as fetch:
        if args_list[1] == '-f':
            for i in repo_args:
                if i not in remote_list:
                    remote_list.append(i)
        remote_list.sort()
        pwd_dir = (subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')).strip() + '/'
        for remote in remote_list:
            if is_git_directory(path):
                config.write(path)
                config.write('\n')
            else:
                print(path + " is not a git repository.")

def fetch_repo(remote_list):
    for i in remote_list:
        if is_git_directory(i[0]):
            print(i[0] + " repository is present.")
        else:
            print("Fetching "+i[1]+ "to " + i[0])
            if not os.path.exists(i[0]):
                subprocess.run(["mkdir", "-p", i[0])
            subprocess.run(["git", "clone", i[1], i[0]])

fetch_file = str(os.environ.get('HOME'))+'/.config/resonate/fetch.txt'
args_list = sys.argv
args_remote = ['-f']

pwd_dir = (subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')).strip() + '/'
remote_list = []
repo_args = []

if os.path.exists(fetch_file):
    with open(fetch_file, 'r') as fetch:
        csv_file = csv.reader(fetch_file)
        for row in csv_file:
            remote_list.append(row)

check_args(args_list)
fetch_repo(remote_list)
