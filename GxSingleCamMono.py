# version:1.0.1905.9051
import gxipy as gx
from PIL import Image as img
import cv2
import io
import time
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import ttk, Tk, Label, Button, Text, Radiobutton
from tkinter import filedialog
from tkinter.filedialog import *

def selectOutputDir():
    text1.delete(1.0, END)
    outputDir = filedialog.askdirectory(parent=window)
    text1.insert(INSERT, outputDir)

def main():
    # print the demo information
    print("")
    print("-------------------------------------------------------------")
    print("Sample to show how to acquire mono image continuously and show acquired image.")
    print("-------------------------------------------------------------")
    print("")
    print("Initializing......")
    print("")

    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return

    # open the first device
    cam = device_manager.open_device_by_index(1)

    # exit when the camera is a color camera
    if cam.PixelColorFilter.is_implemented() is True:
        print("This sample does not support color camera.")
        cam.close_device()
        return

    # set continuous acquisition
    cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

    # set exposure
    cam.ExposureTime.set(40)

    # set gain
    cam.Gain.set(24.0)

    # start data acquisition
    cam.stream_on()

    # acquire image: num is the image number
    num = 10
    # for i in range(num):
    while (True):
        # get raw image
        raw_image = cam.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue

        # create numpy array with data from raw image
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue

        # show acquired image
        pillow_im = img.fromarray(numpy_image, 'L')
        cv_im = np.array(pillow_im)
        plt.cla()
        cv2.imshow('Preview', cv_im)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # img.show()

        # print height, width, and frame ID of the acquisition image
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))

    # stop data acquisition
    cam.stream_off()

    # close device
    cam.close_device()

if __name__ == "__main__":
    window = Tk()
    window.geometry('1350x250')
    window.title("imageLinePlotter")

    # lbl0 = Label(window, text="Выбор директории выходного файла")
    # lbl0.grid(column=0, row=0)
    # lbl1 = Label(window, text="Output Dir")
    # lbl1.grid(column=0, row=0)
    # lbl2 = Label(window, text="Y_line")
    # lbl2.grid(column=0, row=1)
    lbl3 = Label(window, text="Press q to stop video")
    lbl3.grid(column=8, row=0)

    text1 = Text(width=70, height=1)  # Output DIR
    text1.grid(column=1, row=0, sticky=W)
    # text2 = Text(width=70, height=1)  # Background
    # text2.grid(column=1, row=1, sticky=W)
    # text3 = Text(width=70, height=1)  # Base (white field)
    # text3.grid(column=1, row=2, sticky=W)
    # text4 = Text(width=70, height=1)  # Output DIR
    # text4.grid(column=1, row=4, sticky=W)
    # text5 = Text(width=6, height=1)  # Coordinate
    # text5.grid(column=5, row=0, sticky=W)
    # text6 = Text(width=6, height=1)
    # text6.grid(column=7, row=0, sticky=W)  # Status
    # text7 = Text(width=70, height=1)  # Output DIR
    # text7.grid(column=1, row=3, sticky=W)
    # text8 = Text(width=70, height=1)  # Output DIR
    # text8.grid(column=1, row=5, sticky=W)
    # text0.pack()

    btn1 = Button(window, text="Select Output Dir", command=selectOutputDir)
    btn1.grid(column=0, row=0, sticky=W)
    btn2 = Button(window, text="Start video preview", command=main)
    btn2.grid(column=0, row=1, sticky=W)
    btn3 = Button(window, text="Norma")
    btn3.grid(column=0, row=2, sticky=W)
    btn4 = Button(window, text="Save")
    btn4.grid(column=0, row=4, sticky=W)
    # btn5 = Button(window, text="Plot easy!", command=plotEasy)
    # btn5.grid(column=6, row=0, sticky=W)
    # btn6 = Button(window, text="[(im/base)adjusted - (BG/baseBG)adjusted] + (BG/baseBG)adjusted",
    #               command=plot_normalized_adjusted_4_overlay)
    # btn6.grid(column=2, row=2, sticky=W)
    # btn7 = Button(window, text="(im - BG) + (BG)green", command=plot_like_Eimar)
    # btn7.grid(column=2, row=3, sticky=W)
    # btn8 = Button(window, text="[(im/base)adjusted - (BG/baseBG)adjusted]adjusted",
    #               command=plot_normalized_adjusted)
    # btn8.grid(column=2, row=4, sticky=W)
    # btn9 = Button(window, text="Select Base BG", command=WhiteFieldOpen_BG)
    # btn9.grid(column=0, row=3, sticky=W)
    # btn10 = Button(window, text="Select multiple", command=plotMultiple)
    # btn10.grid(column=0, row=5, sticky=W)
    # btn11 = Button(window, text="imadjust", command=im_adjust)
    # btn11.grid(column=2, row=5, sticky=W)
    # btn12 = Button(window, text="R/G", command=R2G)
    # btn12.grid(column=2, row=6, sticky=W)
    # btn13 = Button(window, text="R-G", command=R_G)
    # btn13.grid(column=2, row=7, sticky=W)
    # btn14 = Button(window, text="R/G vs R-G", command=comparison)
    # btn14.grid(column=2, row=8, sticky=W)

    LED = BooleanVar()
    rb0 = Radiobutton(text="Violet", variable=LED, value=0)
    rb0.grid(column=2, row=0, sticky=W)
    rb1 = Radiobutton(text="Red", variable=LED, value=1)
    rb1.grid(column=2, row=1, sticky=W)

    Mode = BooleanVar()
    rb2 = Radiobutton(text="Mode1", variable=Mode, value=0)
    rb2.grid(column=4, row=1, sticky=W)
    rb3 = Radiobutton(text="Mode2", variable=Mode, value=1)
    rb3.grid(column=5, row=1, sticky=W)
    rb4 = Radiobutton(text="Mode3", variable=Mode, value=2)
    rb4.grid(column=6, row=1, sticky=W)

    window.mainloop()
    main()
