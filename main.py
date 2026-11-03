import easygui
import pdfplumber
import re

file_path = easygui.fileopenbox(title="Select the Audi PDF to Convert", filetypes=["*.pdf"])
file_name = file_path.split("\\")[-1]
whole_text = ""
if file_path:
    #open file and extract text from each page
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            whole_text += text


    model_pattern = re.compile(r"\w{6}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    dfrt_pattern = re.compile(r"(?<=Destination Charge \(subject to change, add to all orders\):\s)\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    metallic_paint = re.compile(r"(?<=Metallic or pearl effect paint:\s)\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    #includes options with no price
    option_with_price = re.compile(r"\b\w{3}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}|\b\w{3}\s\$0\s\$0")
    #uses multi line RegEx - Keep in mind to use flags=re.MULTILINE
    paint_pattern = re.compile(r"^(?:\w+\s)+\w+\n?\r?^(?:X\s|-\s){1,5}^\b\d[A-Z]\d[A-Z]|^(?:\w+\s)+\w+\n?\r?^(?:X\s|-\s){1,5}^\b[A-Z]\d[A-Z]\d")

    regex_text = re.compile(f"{model_pattern.pattern}|{dfrt_pattern.pattern}|{metallic_paint.pattern}|{option_with_price.pattern}|{paint_pattern.pattern}", flags=re.MULTILINE)
    regex_text = regex_text.findall(whole_text)

    for each_match in regex_text:
        print(each_match)
        
