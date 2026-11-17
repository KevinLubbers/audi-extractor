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

    #pattern that selects the text from *MDL pricing to just after exterior paints
    #this allows us to loop through each chunk of text, knowing it is one model
    each_model_text_pattern = re.compile(r"\w{6}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}\n(?:(?!\w{6}\s\$\d+,?\d+\s\$\d+,?\d+\n|INTERIOR COMPONENT OPTIONS\n).*\n)*(?:INTERIOR COMPONENT OPTIONS\n|\$\d+,?\d+\s\$\d+,?\d+\n)", flags=re.MULTILINE)
    each_model_text = each_model_text_pattern.findall(whole_text)

    model_pattern = re.compile(r"\w{6}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    dfrt_pattern = re.compile(r"(?<=Destination Charge \(subject to change, add to all orders\):\s\$)\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}")
    #new pattern accounts for paints with NO PRICE aka - -     keep in mind need to convert - - to $0
    #ALSO Keep in mind CRYSTAL EFFECT paint present in MY27, think if it will be an issue for MY28
    metallic_paint_pattern = re.compile(r"(?<=Metallic or pearl effect paint:\s\$)\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}|(?<=Metallic or pearl effect paint:\s)-\s-")
    #includes options with no price
    option_pattern = re.compile(r"\b\w{3}\s\$\d{1,3},?\d{1,3}\s\$\d{1,3},?\d{1,3}|\b\w{3}\s\$0\s\$0")
    #uses multi line RegEx - Keep in mind to use flags=re.MULTILINE
    paint_pattern = re.compile(r"^.*\n^(?:X\s?|-\s?|x\s?)+\n^[A-Z0-9]{4}\b", flags=re.MULTILINE)
    #paint_pattern = re.compile(r"^(?:\w+\s)+\w+\n?\r?^(?:X\s|-\s)*^\b\d[A-Z]\d[A-Z]|^(?:\w+\s)+\w+\n?\r?^(?:X\s|-\s)*^\b[A-Z]\d[A-Z]\d", flags=re.MULTILINE)
    interior_pattern = re.compile(r"\b(?:(?!\n|IN)\(?[A-Z]{2}\)?\s.*){1,8}(?=EXTERIOR COLOR \/)")

    #simplified creating our data structure by looping over regex matches instead of needing to parse each model out of each line
    model_list = []
    for each_match in each_model_text:
        temp_model_list = []
        temp_option_list = []
        #creating and OEM model code *MDL pricing 
        raw_model_text = model_pattern.findall(each_match)[0].replace(",", "").replace("$", "").split(" ")
        model_code = raw_model_text[0]
        model_msrp = raw_model_text[1]
        model_invoice = raw_model_text[2]
        temp_option_list.append({"option": "*MDL", "name": "Base Price", "invoice": int(model_invoice), "msrp": model_msrp, "type": "Price"})

        dfrt_raw = dfrt_pattern.findall(each_match)[0].replace(",", "").replace("$", "").split(" ")
        dfrt_msrp = dfrt_raw[0]
        dfrt_invoice = dfrt_raw[1]
        temp_option_list.append({"option": "DFRT", "name": "Destination Charge", "invoice": int(dfrt_invoice), "msrp": dfrt_msrp, "type": "Price"})

        #replace - for $0
        metallic_paint_raw = metallic_paint_pattern.findall(each_match)[0].replace(",", "").replace("$", "").replace("-", "0").split(" ")
        metallic_paint_msrp = metallic_paint_raw[0]
        metallic_paint_invoice = metallic_paint_raw[1]

        options_raw = option_pattern.findall(each_match)
        for each_option in options_raw:
            option = each_option.replace(",", "").replace("$", "").split(" ")
            option_code = option[0]
            option_msrp = option[1]
            option_invoice = option[2]
            temp_option_list.append({"option": option_code, "invoice": int(option_invoice), "msrp": option_msrp, "type": "IND"})

        interiors_raw = interior_pattern.findall(each_match)[0].replace("(", "").replace(")", "")
        only_interiors = re.compile(r"\b[A-Z]{2}\b").findall(interiors_raw)
        for each_interior in only_interiors:
            option_code = each_interior
            temp_option_list.append({"option": option_code, "invoice": 0, "msrp": 0, "type": "INT"})
        
        paints = paint_pattern.findall(each_match)
        for each_paint in paints:
            split_text = each_paint.split("\n")
            option_name = re.sub(r"\s*\([^)]*\)", "",split_text[0]).strip()
            option_code = split_text[2]
            if "metallic" in option_name.lower() or "pearl" in option_name.lower():
                paint_msrp = metallic_paint_msrp
                paint_invoice = metallic_paint_invoice
            else:
                paint_msrp = "0"
                paint_invoice = "0"
            temp_option_list.append({"option": option_code, "name": option_name, "invoice": int(paint_invoice), "msrp": int(paint_msrp), "type": "Color"})

        temp_model_list.append({"model": model_code, "options": temp_option_list})
        model_list.append(temp_model_list)
        #end each model loop
    print(model_list)
