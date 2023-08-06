import glob
import os
import sys
import subprocess


def get_platform():
    '''
        input:  None
        output: (str) OS name 
    '''

    platform = sys.platform

    if platform == "linux" or platform == "linux2":
        return "LINUX"
    elif platform == "darwin":
        return "MAC"
    elif platform == "win32":
        return "WIN"
    else: 
        None


def get_shell():
    '''
        input:  None
        output: (str) shell name 
    '''

    if get_platform() == "MAC":
        return os.environ["SHELL"]
    
    return os.readlink('/proc/%d/exe' % os.getppid())


def get_rc_path():
    '''
        input:  None
        output: path of shell config file
    '''

    rc_path = "~/.bashrc"
    if "zsh" in get_shell():
        rc_path = "~/.zshrc"
    
    return rc_path


def set_unix_var(key, value):
    '''
        input:  (str) env_key , (str) env_value
        output: None
    '''

    rc_path = get_rc_path()
    VAR_EXISTS = False
     
    # with is like your try .. finally block in this case
    with open(os.path.expanduser(rc_path), 'r') as file:
        data = file.readlines()
        for i, line in enumerate(data):
            pattern = f"export {key}="
            if pattern in line:
                data[i] =  f"export {key}='{value}';\n"
                VAR_EXISTS = True

        
        if not VAR_EXISTS:
            data.append(f"export {key}='{value}';\n")

    # # and write everything back
    with open(os.path.expanduser(rc_path), 'w') as file:
        file.writelines( data )


def set_win_var(key, value):
    '''
        input:  (str) env_key , (str) env_value
        output: None
    '''
    subprocess.run("SETX {0} {1} /M".format(key, value))



def set_env_var(key, value):
    '''
        input:  (str) env_key , (str) env_value
        output: None
    '''

    platform = get_platform()

    if platform == "WIN":
        set_win_var(key,value)
    
    else:
       set_unix_var(key,value)


def get_env_dict():
    '''
        input:  None
        output: list of env key value pairs (dict)
    '''
    rc_path = get_rc_path()
     
    # with is like your try .. finally block in this case
    env_list = []
    env_dict = {}
    with open(os.path.expanduser(rc_path), 'r') as file:
        data = file.readlines()
        for i, line in enumerate(data):
            pattern = f"export"
            if pattern in line and "#" not in line:
                env_list.append(line)
        
        for i in range(len(env_list)):
            # replace certain char
            line = env_list[i]
            line = line.replace(";","").replace("export","").replace(" ","")
            key, value = line.split("=")
            value = value.replace("'",'').replace("\n","")

            env_dict[key] = value

    return env_dict        

def get_env_var(key):
    try:
        env_dict = get_env_dict()
        return env_dict[key]
    except:
        raise Exception("ENV Variable Doesn't Exist")

