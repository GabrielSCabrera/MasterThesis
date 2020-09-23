main:
	@ echo "Running Main Script"
	@ python3.8 ./main.py

clean:
	@ echo "Removing '_pycache__' Directories"
	@ rm -f -r ./src/__pycache__/
	@ rm -f -r ./src/frontend/__pycache__/
	@ rm -f -r ./src/frontend/visualization/__pycache__/
	@ rm -f -r ./src/backend/__pycache__/
	@ rm -f -r ./src/backend/config/__pycache__/
	@ rm -f -r ./src/backend/models/__pycache__/
	@ rm -f -r ./src/backend/preprocessing/__pycache__/
	@ rm -f -r ./src/backend/utils/__pycache__/

install:
	@ echo "Running Test Script"
	@ python3.8 ./main.py --sync

reset: clean
	@ echo "Removing All Saved Data and Generated Directories"
	@ rm -f -r ~/Documents/MasterThesis/results/
	@ rm -f -r ~/Documents/MasterThesis/data/split_bins/
	@ rm -f -r ~/Documents/MasterThesis/data/DNN_models_relpath/

push: clean
	@ echo "Updating Master Branch"
	@ git add .
	@ git commit -m "Auto-Backup"
	@ git push

pull: clean
	@ echo "Pulling from Master Branch"
	@ git pull
