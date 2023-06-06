# version:1.0.1905.9051
import gxipy as gx
from PIL import Image as img,ImageFont, ImageDraw
import cv2
import io
import time
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import ttk, Tk, Label, Button, Text, Radiobutton
from tkinter import filedialog
import numba as nb

# using datetime module
import datetime
ct = datetime.datetime.now()
ts = ct.timestamp()
print("timestamp:-", ts)
from datetime import datetime
date_time = datetime.fromtimestamp(ts)
str_date_time = date_time.strftime("%Y-%m-%d_%H_%M_%S")
filename = str_date_time + ".png"
print(filename)

# ct stores current time

# print("Current timestamp", str_date_time)

def selectOutputDir():
    text1.delete(1.0, END)
    outputDir = filedialog.askdirectory(parent=window)
    text1.insert(INSERT, outputDir)

# @nb.njit
def sum_gt_nb(arr):
    arr = arr.ravel()
    result = 0
    for x in arr:
        result += x
    return result

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
    cam.ExposureTime.set(40000)

    # set gain
    cam.Gain.set(5.0)

    # start data acquisition
    cam.stream_on()

    # acquire image: num is the image number
    num = 10
    # for i in range(num):

    cursorWidth = 5
    ROIwidth = 100
    ROIwidthHalf = int(20/2)
    frameWidth = 1440
    frameHalfWidth = int(frameWidth/2)
    frameHeight = 1080
    frameHalfHeight = int(frameHeight/2)
    print (frameHalfWidth)
    print(frameHalfHeight)

    start_point = ((frameHalfWidth)-(cursorWidth+1), (frameHalfWidth)-(cursorWidth+1))
    end_point = ((frameHalfWidth)+(cursorWidth+1), (frameHalfWidth)+(cursorWidth+1))
    color = 255
    thickness = 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 50)
    fontScale = 2
    fontColor = (255, 255, 255)
    thickness = 2
    lineType = 2



    while (True):
        # get raw image
        raw_image1 = cam.data_stream[0].get_image()
        frame1 = raw_image1.get_numpy_array()
        cursor1 = np.sum(frame1[(frameHalfWidth-cursorWidth):(frameHalfWidth+cursorWidth), (frameHalfWidth-cursorWidth):(frameHalfWidth+cursorWidth)])
        raw_image2 = cam.data_stream[0].get_image()
        frame2 = raw_image2.get_numpy_array()
        cursor2 = np.sum(frame2[(frameHalfWidth - cursorWidth):(frameHalfWidth + cursorWidth), (frameHalfWidth - cursorWidth):(frameHalfWidth + cursorWidth)])
        # if raw_image is None:
        #     print("Getting image failed.")
        #     continue

        # create numpy array with data from raw image
        # numpy_image = raw_image.get_numpy_array()
        # if numpy_image is None:
        #     continue

        # sum1 = sum_gt_nb(frame1[1:100])
        # sum2 = sum_gt_nb(frame2[1:100])

        sum1 = np.sum(frame1[(frameHalfWidth-ROIwidthHalf):(frameHalfWidth+ROIwidthHalf), (frameHalfWidth-ROIwidthHalf):(frameHalfWidth+ROIwidthHalf)])
        sum2 = np.sum(frame2[(frameHalfWidth - ROIwidthHalf):(frameHalfWidth + ROIwidthHalf), (frameHalfWidth - ROIwidthHalf):(frameHalfWidth + ROIwidthHalf)])
        #
        if sum1 > sum2:
            # difframe = frame1 - frame2
            difframe = cv2.subtract(np.uint8(frame1), np.uint8(frame2))
            FI = cursor1/cursor2
        else:
            # difframe = frame2 - frame1
            difframe = cv2.subtract(np.uint8(frame2), np.uint8(frame1))
            FI = cursor2 / cursor1

        # show acquired image
        pillow_im = img.fromarray(difframe, 'L')
        cv_im = np.array(pillow_im)
        plt.cla()


        if cv2.waitKey(1) & 0xFF == ord('s'):
            import datetime
            ct = datetime.datetime.now()
            ts = ct.timestamp()
            print("timestamp:-", ts)
            from datetime import datetime
            date_time = datetime.fromtimestamp(ts)
            str_date_time = date_time.strftime("%Y-%m-%d_%H_%M_%S")
            filename = text1.get("1.0", 'end-1c') + '/' + str_date_time + ".png"
            print(filename)
            cv2.rectangle(cv_im, start_point, end_point, color, thickness)
            cv2.putText(cv_im, str(FI)[0:4],
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        thickness,
                        lineType)
            cv2.imwrite(filename, cv_im)
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px
        cv2.rectangle(cv_im, start_point, end_point, color, thickness)
        cv2.putText(cv_im, str(FI)[0:4],
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
        cv2.imshow('Preview', cv_im)
        # img.show()

        # print height, width, and frame ID of the acquisition image
        # print("Frame ID: %d   Height: %d   Width: %d"
        #       % (raw_image1.get_frame_id(), raw_image1.get_height(), raw_image1.get_width()))
        print("Frame #: %d   FI: %d"
              % (raw_image1.get_frame_id(), FI))

    # stop data acquisition
    cam.stream_off()

    # close device
    cam.close_device()

if __name__ == "__main__":
    window = Tk()
    window.geometry('1350x250')
    window.title("imageLinePlotter")

    lbl1 = Label(window, text="Press q to stop video")
    lbl1.grid(column=8, row=0)
    lbl2 = Label(window, text="Press s to save image")
    lbl2.grid(column=8, row=1)

    text1 = Text(width=70, height=1)  # Output DIR
    text1.grid(column=1, row=0, sticky=W)

    # text0.pack()

    btn1 = Button(window, text="Select Output Dir", command=selectOutputDir)
    btn1.grid(column=0, row=0, sticky=W)
    btn2 = Button(window, text="Start video preview", command=main)
    btn2.grid(column=0, row=1, sticky=W)
    btn3 = Button(window, text="Norma")
    btn3.grid(column=0, row=2, sticky=W)
    btn4 = Button(window, text="Save")
    btn4.grid(column=0, row=4, sticky=W)

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
