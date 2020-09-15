To run .m file from command line:

matlab -nodisplay -nosplash -nodesktop -r "run('./readfile.m');"


.bashrc function:

# MATLAB Shortcut Function
function mat {
  matlab -nodisplay -nosplash -nodesktop -r "run('./$1');"
}
