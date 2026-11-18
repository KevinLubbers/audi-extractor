import easygui
import pymupdf
import pdfplumber

#basic file selection and text extraction
file_path = easygui.fileopenbox(title="Select the Audi PDF to Troubleshoot", filetypes=["*.pdf"])
file_name = file_path.split("\\")[-1]
whole_text = ""
'''
if file_path:
    #open file and extract text from each page
    with pymupdf.open(file_path) as pdf:
    # Loop through each page
        for page_number in range(pdf.page_count):
            page = pdf.load_page(page_number)
            # Extract text from the page
            page_text = page.get_text("text")
            whole_text += page_text
'''
#pdfplumber test - move comment to test pymupdf

if file_path:
    #open file and extract text from each page
    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            whole_text += text
            progress = (page_num / total_pages)
            bar_length = 30
            filled = int(bar_length * progress)
            bar = "█" * filled + "-" * (bar_length - filled)
            print(f"\rProgress: |{bar}| {progress:.0%} ({page_num}/{total_pages})", end="", flush=True)
        #moves cursor to next line after progress bar finishes
        print()
    print(whole_text)
#used for troubleshooting RegEx pattern issues
#we can pull the text for the PDF and test different RegEx Patterns in an interactive environment