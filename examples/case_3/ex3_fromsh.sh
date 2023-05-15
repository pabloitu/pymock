#!/bin/bash

# Function to replace the variables in args.txt
replace_variables() {
    sed -i "s/start_date = .*/start_date = $1/g" $5
    sed -i "s/end_date = .*/end_date = $2/g" $5
    sed -i "s/mag_min = .*/mag_min = $3/g" $5
    sed -i "s/seed = .*/seed = $4/g" $5
}

# Forecast date range
start_forecast="2009-03-01"
end_forecast="2009-06-09"

# Iterate through the range of dates
current_date="$start_forecast"
# Set random seed
RANDOM=640
while [[ "$current_date" != "$end_forecast" ]]; do

    # Replace the variables with the current date, seed and mag_min
    end_date=$(date -d "$current_date + 1 day" +"%Y-%m-%d")
    replace_variables "$current_date" "$end_date" "3.5" "$RANDOM" "input/args.txt"

    # Run the model
    pymock input/args.txt

    # Increment the current date by 1 day
    current_date=$(date -d "$current_date + 1 day" +"%Y-%m-%d")
done


