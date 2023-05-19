

try:
    help
except NameError:
    print("SKIP")
    raise SystemExit

help() 
help(help) 
help(int) 
help(1) 
import micropython
help(micropython) 
help('modules') 

print('done') 
