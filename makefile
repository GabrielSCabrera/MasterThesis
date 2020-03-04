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
	@ rm -f -r ./scripts/backend/preprocessing/__pycache__/
	@ rm -f -r ./scripts/backend/prototypes/__pycache__/

test: clean
	@ echo "Run tests"
	@ python3 ./main.py -test

reset: clean
	@ echo "Removing all saved data and generated directories"
	@ rm -f -r ~/Documents/MasterThesis/results/
	@ rm -f -r ~/Documents/MasterThesis/data/split_bins
