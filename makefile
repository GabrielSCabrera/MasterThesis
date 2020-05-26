main:
	@ echo "Running Main Script"
	@ python3 ./main.py

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

test:
	@ echo "Running Test Script"
	@ python3 ./main.py --test

unit_tests:
	@ echo "Running Unit Tests"
	@ python3 ./main.py --unit_tests

split:
	@ echo "Splitting Datasets and Saving"
	@ python3 ./main.py --split

train_DNN:
	@ echo "Training Multilayer Perceptron"
	@ python3 ./main.py --train_DNN

score_DNN:
	@ echo "Scoring Saved Model"
	@ python3 ./main.py --score_DNN

cluster:
	@ echo "Extracting Clusters"
	@ python3 ./main.py --cluster

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
