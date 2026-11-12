# Audi Order Guide Extractor
## Extract the text from your PDF
1. Navigate to the project folder and run ```python main.py```
2. Select the proper Order Guide when prompted
3. The data will be saved in a SQLite file or JSON format for your archives
## Insert the data into PCS Maintenance
1. Open PCS Maintenance and manually set your effective date
2. Run ```python input-json-to-pcs.py```
3. Select one or more models from the menu
4. Press "Start"
## Troubleshooting
RegEx Patterns can start failing if the Manufacturer starts changing the format of the Order Guide. This rarely if ever happens, but anything is possible.

You can manually check each RegEx Pattern in an interactive environment (we recommend [RegExr](https://regexr.com))

1. Run ```python debug_text.py``` and select the Order Guide you need to troubleshoot
2. Select the generated text and paste it into your interactive RegEx environment
3. Test your heart out