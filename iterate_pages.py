import pdf2image
from tqdm import tqdm
import os
import pytesseract
from PyPDF2 import PdfFileWriter, PdfFileReader 
try:
    from PIL import Image
except ImportError:
    import Image




def pdf_to_string_list(pdf='DOC021.PDF',footer=150) -> list:
    # 
    inputpdf = PdfFileReader(open(pdf, "rb"))
    maxPages = inputpdf.numPages
    chunkSize = 10
    st_lst = [] # list of strings
    for page in tqdm(range(1, maxPages, chunkSize)):
        pil_images = pdf2image.convert_from_path(pdf, dpi=200, first_page=page,
                                                     last_page=min(page + chunkSize - 1, maxPages), fmt= 'jpg',
                                                     thread_count=10, userpw=None,
                                                     use_cropbox=False, strict=False)
        for img in pil_images:
            width, height = img.size
            tmp_img = img.crop((0, height-footer, width, height))
            st_lst.append(pytesseract.image_to_string(tmp_img))
            # tmp_img = tmp_img.save("output/"+str(page)+".jpg") # to save images
    return st_lst

def get_page_name(st: str) -> str:
    for i in st[:-2].split("\n"):
        if "CHANGE" in i.upper():
            if i.upper().startswith("CHANGE"):
                return i[9:] # len("CHANGE 1 ") = 9
            else:
                return i[:-9]

def squeeze(txt: dict) -> list:
    """
    This function will return list of tuples in format: (name,start_id,seq,version)
    """
    lst = []
    print(list(txt.keys()))
    print(list(ranges(list(txt.keys()))))
    for seq in list(ranges(list(txt.keys()))):
        if seq[0] == seq[1]: # if a single page
            lst.append([
                txt[seq[0]][0],
                seq[0],
                seq,
                txt[seq[0]][1]
            ])
        else: # if it's a range of pages
            lst.append([
                txt[seq[0]][0] + " - " + txt[seq[1]][0],
                seq[0],
                seq,
                txt[seq[0]][1]
            ])
            
    return lst
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def iterate(path='./output'):
    """
    This function will iterate a over directory and preform ocr on each image
    """
    for entry in os.scandir(path):
        if entry.path.endswith(".jpg") and entry.is_file():
            page = entry.path.split("/")[-1].split('.')[0]
            text = ocr_core(entry.path)
            if "CHANGE" in text.upper():
                print("%s: %s"%(page,text))


def ranges(seq):
    start, end = seq[0], seq[0]
    count = start
    for item in seq:
        if not count == item:
            yield start, end
            start, end = item, item
            count = item
        end = item
        count += 1
    yield start, end

def generate_change_lst(path):
    d = {}
    bad = {}
    txt = {}
    st_lst = pdf_to_string_list(pdf=path)
    for i in range(len(st_lst)):
        if "CHANGE" in st_lst[i].upper():
            version = st_lst[i].upper().split("CHANGE ")[-1][0] #potential bug with double digit version
            txt[i+1] = get_page_name(st_lst[i]),version
            if version in d:
                d[version].append(i+1)
            else:
                d[version] = [i+1]
        else:
            bad[st_lst[i]] = i+1
    return txt

if __name__ == "__main__":

    txt = generate_change_lst('DOC021.PDF') # replace with your pdf's name
    print(squeeze(txt))
    
    