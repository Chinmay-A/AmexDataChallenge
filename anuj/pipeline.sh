#!/bin/bash

# This script is used to run the entire ML pipeline
# To install dependencies: run `bash pipeline.sh -i`
# To preprocess data (data files generated in out/ directory): run `bash pipeline.sh -p`
# To train model (models saved in out/): run `bash pipeline.sh -t`
# To make predictions based on trained models and generate output csv(s): run `bash pipeline.sh -o`

while getopts "ipto" option; do
    case $option in
        i)
            # Install dependencies
            echo "Installing dependencies..."
            # Add your installation commands here
            pip3 install -r requirements.txt
            ;;
        p)
            # Pre-process data
            echo "Generating data..."
            # Add your preprocess.py execution command here
            python3 preprocessing.py
            ;;
        t)
            # Train model
            echo "Training model..."
            # Add your train_model.py execution command here
            python3 training.py
            ;;
        o) 
            # Generate output
            echo "Generating Output Files using predictions from model..."
            # Add your make_predictions.py execution command here
            python3 predict.py
            ;;
        *)
            # Invalid option
            echo "Invalid option: -$OPTARG"
            ;;
    esac
done
