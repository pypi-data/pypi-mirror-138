import os
import subprocess 

def convert(file_name):
    file_name = file_name.split('.')[0]
    if f'{file_name}.ipynb' not in os.listdir():  
        print('Save .py file as .ipynb because no such file already exists.')            
        command = f'jupytext --to notebook {file_name}.py'
    else:
        print('Save .ipynb file as .py with interactive syntax') 
        command = f'jupytext --to py:percent {file_name}.ipynb'
        
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT) 
    except Exception as e:
        print(f'Converstion failed! Terminal output:')
        [print(line) for line in e.stdout.decode('utf-8').split('\r\n')]
    