#!/bin/bash

# Function to replace the variables in args.txt
replace_variables() {
    sed -i "s/start_date = .*/start_date = $1/g" $4
    sed -i "s/end_date = .*/end_date = $2/g" $4
    sed -i "s/seed = .*/seed = $3/g" $4
}

# Forecast date range
start_forecast="2010-01-01"
end_forecast="2010-01-20"

# Iterate through the range of dates
current_date="$start_forecast"
# Set random seed
RANDOM=640
while [[ "$current_date" != "$end_forecast" ]]; do

    # Replace the variables with the current date and seed
    end_date=$(date -d "$current_date + 1 day" +"%Y-%m-%d")
    replace_variables "$current_date" "$end_date" "$RANDOM" "input/args.txt"

    # Run the model as desired (python+run.py or binary)
    python ../../run.py input/args.txt
#    pymock input/args.txt

    # Increment the current date by 1 day
    current_date=$(date -d "$current_date + 1 day" +"%Y-%m-%d")
done


