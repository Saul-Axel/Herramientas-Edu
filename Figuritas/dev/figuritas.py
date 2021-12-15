from tkinter import *
import random
from typing import final
from PIL import ImageTk, Image
from io import BytesIO
import win32clipboard as clip
import win32con

root = Tk()
root.title('Figuritas')
# root.geometry('800x600')

# Configure grid
for i in range(7):
    root.rowconfigure(i, weight=1)
for i in range(6):
    root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=2)

# Configure images
img1 = Image.open('img/1.png')
img2 = Image.open('img/2.png')
img3 = Image.open('img/3.png')
img4 = Image.open('img/4.png')
img5 = Image.open('img/5.png')
img6 = Image.open('img/6.png')
listImg = [img1, img2, img3,
           img4, img5, img6]
listVal = [1, 10, 100]
copyImage = Image.open('img/1.png')
finalImage = None


def generarNum(cant):
    num = 0
    for i in range(cant):
        if i == 0:
            num += random.randrange(1, 9)
        else:
            num += random.randrange(0, 9)
        if i != cant-1:
            num *= 10
    return num


def generarPatron(digit, img):
    for i in range(img):
        # Elegir patron
        rng = random.randrange(0, 6)
        # Aplicar transformación
        if rng < 3:
            digit += listVal[rng % 3]
        else:
            digit -= listVal[rng % 3]
        # Imagenes
        if i == 0:
            im1 = listImg[rng]
        else:
            im2 = listImg[rng]
            dst = Image.new('RGB', (im1.width + im2.width, im1.height))
            dst.paste(im1, (0, 0))
            dst.paste(im2, (im1.width, 0))
            im1 = dst
    global copyImage
    copyImage = im1
    finalImage = ImageTk.PhotoImage(im1)
    # change image
    patronImagen.configure(image=finalImage)
    patronImagen.photo_ref = finalImage
    return digit


def generar(digit, img):
    # Generar primer número
    if int(digit) < 0:
        digit = 1
    digit = generarNum(int(digit))
    numInicio.delete(0, END)
    numInicio.insert(0, digit)

    if int(img) < 0:
        img = 1
    digit = generarPatron(int(digit), int(img))
    numFiguras.delete(0, END)
    numFiguras.insert(0, digit)


def copiar():
    output = BytesIO()
    copyImage.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_DIB, data)
    clip.CloseClipboard()


labelcantDigitos = Label(root, text="Número de Digitos", justify='right').grid(
    row=1, column=1, sticky=EW)
cantDigitos = Spinbox(root, from_=1, to=10)
cantDigitos.grid(
    row=1, column=2, sticky=EW)

labelnumImg = Label(root, text="Número de Figuras", justify='right').grid(
    row=1, column=4, sticky=EW)
numImg = Spinbox(root, from_=1, to=10)
numImg.grid(
    row=1, column=5, sticky=EW)

butonGenerar = Button(root, text="Generar", width=10, height=1, command=lambda: generar(
    cantDigitos.get(), numImg.get())).grid(
        row=2, column=3, sticky=N+S+W+E)

numInicio = Entry(root, width=10, justify='right')
numInicio.grid(
    row=4, column=1, sticky=EW)
numFiguras = Entry(root, width=10, justify='right')
numFiguras.grid(
    row=4, column=5, sticky=EW)

patronImagen = Label(image=finalImage)
patronImagen.grid(row=5, column=1, columnspan=7, sticky=N+S+W+E)

butonDescargar = Button(root, text="Copiar", width=10, height=1, command=lambda: copiar()).grid(
    row=6, column=3, sticky=N+S+W+E)

root.mainloop()
