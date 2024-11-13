import csv
import json

# Define CSV and JSON
csvPath = 'fineTune/Dataset for Llama - FAQ Additional Prompts.csv'
jsonPath = 'fineTune/data.json'

with open(csvPath, mode ='r', encoding ='utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)
    data = list(csvReader) # convert to list of dictionary

# write the dictionaries to JSON
with open(jsonPath, mode='w', encoding='utf-8') as jsonFile:
    json.dump(data, jsonFile, indent=4)

print("CSV has been converted.")