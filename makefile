main:
	@ echo "Run main script"
	@ python3 ./main.py

clean:
	@ echo "Clean __pycache__"
	@ rm -f -r ./scripts/__pycache__/
	@ rm -f -r ./scripts/frontend/__pycache__/
	@ rm -f -r ./scripts/frontend/visualization/__pycache__/
	@ rm -f -r ./scripts/backend/__pycache__/
	@ rm -f -r ./scripts/backend/config/__pycache__/
	@ rm -f -r ./scripts/backend/models/__pycache__/
	@ rm -f -r ./scripts/backend/preprocessing/__pycache__/
	@ rm -f -r ./scripts/backend/utils/__pycache__/

test:
	@ echo "Run tests"
	@ python3 ./main.py -test

split:
	@ echo "Splitting Datasets and Saving"
	@ python3 ./main.py --split

train_DNN:
	@ echo "Training Multilayer Perceptron"
	@ python3 ./main.py --train_DNN

reset: clean
	@ echo "Removing all saved data and generated directories"
	@ rm -f -r ~/Documents/MasterThesis/results/
	@ rm -f -r ~/Documents/MasterThesis/data/split_bins/
	@ rm -f -r ~/Documents/MasterThesis/data/DNN_models_relpath/

push: clean
	@ echo "Updating master branch"
	@ git add .
	@ git commit -m "Auto-Backup"
	@ git push
