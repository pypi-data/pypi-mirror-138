import os
import subprocess 

def convert(file_prefix, is_py):
    '''
    Save .ipynb as .py and vice-versa
    '''
    
    ## Remove any file extensions/suffixes if user wrongly submitted a full file name
    file_prefix = 'test'
    file_prefix = file_prefix.split('.')[0]
    ipynb_file = f'{file_prefix}.ipynb'    
    py_file = f'{file_prefix}.py'  
    
    '''
    Save .py as .ipynb and vice-versa. Delete any opposing file first if it already 
    exists before the conversion to force VS-Code to render the changes properly 
    if both files happen to be open.
    '''    
    if is_py:
        if ipynb_file in os.listdir():
            #print(f'deleting {ipynb_file}')
            os.remove(ipynb_file)
        #print(f'Saving {py_file} as {ipynb_file}')
        command = f'jupytext --to notebook {file_prefix}.py'
    else:
        if py_file in os.listdir():
            #print(f'deleting {py_file}')
            os.remove(py_file)
        #print(f'Saving {ipynb_file} as {py_file} with interactive syntax') 
        command = f'jupytext --to py:percent {file_prefix}.ipynb'
        
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT) 
    except Exception as e:
        print(f'Converstion failed! Terminal output:')
        [print(line) for line in e.stdout.decode('utf-8').split('\r\n')]