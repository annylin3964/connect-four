# connect-four

## Files in connect-four
It contains two txt files(dataset) and three python files. `constants.py` contains all the configuration of the scripts, `functions.py` stores the functions we need for executing the match, analyses the results and Google Cloud related setup. `run.py` is the main script you need to run, it calles the functions and composed them in the correct order to implement the assessment.

## Execute the script
Execute the following command to

`python connect-four/run.py`
  1. Play the match
  2. Analyses the matches result
  3. Write the result to database
  
Note: The current Google Cloud User is hardcoded in `constant.py` file, if you want to use another account, please change the google cloud related configuration in the file.
