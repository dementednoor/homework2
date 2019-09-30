Running script command should look like this:

python   trace_error_checker.py   path_to_dir_with_btf_file    path_to_output_error_file  
# (spaces are for better visibility)

for example:
python   trace_error_checker.py /home/user/luxoft_hw/ /home/user/luxoft-hw/error_report.txt
# luxoft_hw directory holds the Demo_Exercise_Trace.btf (script doesn't ask to include the filename to the path, cause we consider the name of the file is always the same). Output file's name is up to user, so he can specify it by himself.

Running tests is similair:

python   test.py    path_to_dir_with_btf_file

for example:
python   test.py    /home/user/luxoft_hw/  

# User only has to specify path to the btf file directory, because output file isn't tested.