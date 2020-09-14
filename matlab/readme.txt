To run .m file from command line:

matlab -nodisplay -nosplash -nodesktop -r "run('path/to/your/script.m');exit;" | tail -n +11
https://stackoverflow.com/questions/38723138/matlab-execute-script-from-command-linux-line


matlab -nodisplay -nosplash -nodesktop -r "run('./readfile.m');exit;" | tail -n +11
