import cv2
import pytesseract
import time
from PIL import Image, ImageTk
from tkinter import Tk, Label, Entry, Button


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def checker(im, x, y):
    return im.getpixel((x, y)) == (240, 240, 240)


def get_range(im):
    width, height = im.size
    i = 83
    for j in range(169, height):
        pixel = im.getpixel((i, j))
        if not checker(im, i, j):
            continue
        if not checker(im, i, j + 17):
            continue
        if not checker(im, i + 20, j):
            continue
        if not checker(im, i + 20, j + 17):
            continue
        k = i
        while checker(im, k, j):
            k += 1

        return (i, j, k - 1)
        break
    else:
        return None


def crop():
    im = Image.open("..\\..\\tmp\\dump.png")

    range = get_range(im)

    if range:
        i, j, k = range
        cropped = im.crop((i, j, k, j + 17))
        cropped.save("..\\..\\tmp\\cropped.png")
        return cropped
    else:
        print("Not found")
        im.show()
        return None


input_value = []


def show(image):
    master = Tk()
    master.geometry("400x200")
    tkimage = ImageTk.PhotoImage(image)
    label = Label(master, image=tkimage)
    label.pack()

    def enter():
        input_value.append(input(" > "))
        master.destroy()

    master.after(0, enter)
    print(dir(master.mainloop))
    master.mainloop()


def process(image):
    img = cv2.imread("..\\..\\tmp\\cropped.png")
    text = pytesseract.image_to_string(img)
    if not text:
        try:
            show(image)
            print(input_value)
            text = input_value[0]
        except:
            import traceback

            print(traceback.format_exc())
    with open("..\\..\\tmp\\item_name.txt", "w") as f:
        f.write(text.strip())


def main():
    image = crop()
    process(image)


if __name__ == "__main__":
    main()
