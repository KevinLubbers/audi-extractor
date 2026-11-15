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


    each_model_text_pattern = re.compile(r"\w{6}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}\n(?:(?!\w{6}\s\$\d+,?\d+\s\$\d+,?\d+\n|INTERIOR COMPONENT OPTIONS\n).*\n)*(?:INTERIOR COMPONENT OPTIONS\n|\$\d+,?\d+\s\$\d+,?\d+\n)", flags=re.MULTILINE)
    each_model_text = each_model_text_pattern.findall(whole_text)

    model_pattern = re.compile(r"\w{6}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    dfrt_pattern = re.compile(r"(?<=Destination Charge \(subject to change, add to all orders\):\s\$)\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    #new pattern accounts for paints with NO PRICE aka - -     keep in mind need to convert - - to $0
    #ALSO Keep in mind CRYSTAL EFFECT paint present in MY27, think if it will be an issue for MY28
    metallic_paint_pattern = re.compile(r"(?<=Metallic or pearl effect paint:\s\$)\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}|(?<=Metallic or pearl effect paint:\s)-\s-")
    #includes options with no price
    option_with_price_pattern = re.compile(r"\b\w{3}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}|\b\w{3}\s\$0\s\$0")
    #uses multi line RegEx - Keep in mind to use flags=re.MULTILINE
    paint_pattern = re.compile(r"^(?:\w+\s)+\w+\n?\r?^(?:X\s|-\s)*^\b\d[A-Z]\d[A-Z]|^(?:\w+\s)+\w+\n?\r?^(?:X\s|-\s)*^\b[A-Z]\d[A-Z]\d", flags=re.MULTILINE)

    #simplified creating our data structure by looping over regex matches instead of needing to parse each model out of each line
    model_list = []
    for each_match in each_model_text:
        temp_model_list = []
        temp_option_list = []
        #creating and OEM model code *MDL pricing 
        raw_model_text = model_pattern.findall(each_match)[0].replace(",", "").split(" ")
        model_code = raw_model_text[0]
        model_msrp = raw_model_text[1]
        model_invoice = raw_model_text[2]

        temp_option_list.append({"option": "*MDL", "name": "Base Price", "invoice": int(model_invoice), "msrp": model_msrp, "type": "Price"})
        dfrt = dfrt_pattern.findall(each_match)
        metallic_paint = metallic_paint_pattern.findall(each_match)
        option_with_price = option_with_price_pattern.findall(each_match)
        paints = paint_pattern.findall(each_match)
        temp_model_list.append({"model": model_code, "options": temp_option_list})
        print(f"Model: {model} \nDfrt: {dfrt} \nMetallic Paint Price: {metallic_paint} \nOptions: {option_with_price} \nPaint: {paint}")
