# JHIM Funds Mapper
The purpose of this code is to scrape data from the investments overview website and then allow users to input relevant keywords that will result in actual JHIM products being displayed.

## Necessary package installations
All required packages to run the code is in the <strong>requirements.txt</strong> file.
Simply run `pip install -r requirements.txt` to have all packages installed.

## scraper.py
This script collects data from the JHIM investments overview website and results in a "funds_data.json" file being produced.
There is no need to run this file unless you desire to update the "funds_data.json" file. 
Please be aware of potential HTML element changes on the JHIM investments overview website, as that will require re-configuring the paths in the scraper.py file.
The code to overwrite the current "funds_data.json" file is commented out.

## match.py
The code in this file is responsible for producing the top funds that closest match an inputted string. 
A fund's name, values, and captions are all considered when matching on the inputted string.
Currently, the script is set to output the top funds based on name, but this can easily be changed in the main function.