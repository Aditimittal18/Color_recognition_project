import cv2 as cv          #To read image
import argparse           #To take image as input
import pandas as pd       #To read csv file

#To take custom image as input
arg = argparse.ArgumentParser()
arg.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(arg.parse_args())
img = cv.imread(args["image"])

#To get height and width of the image
(h, w, c) = img.shape[:3]

#To resize the image and fit into the window
def rescale_frame(frame, scale):
    # works for images, videos and live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimentions = (width,height)
    return cv.resize(frame, dimentions, interpolation = cv.INTER_AREA)

if w<800 and h<800:
    img = rescale_frame(img,1.55)

elif w>1000 and w<2000 or h>1000 and h<2000:
    img = rescale_frame(img,0.55)

elif w>2000 and h>2000:
    img = rescale_frame(img,0.25)

#To give name to all the columns in csv file and read the csv file
fieldnames = ["color_name", "R", "G", "B"]

#Color dataset reference https://en.wikipedia.org/wiki/Web_colors
csv = pd.read_csv('dataset.csv', names=fieldnames, header=None)

#To find the color name
def get_colorname(R,G,B):
    min = 1000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=min):
            min = d
            cname = csv.loc[i,"color_name"]
    return cname

click = False
r = g = b = 0
#r = red color, g = green color, b = blue color

#To bind the function to mouse event 
def positionRGB(event, x, y, flags, param):
    #LBUTTONDOWN = left mouse click
    if event == cv.EVENT_LBUTTONDOWN:
        global b, g, r, click
        click = True
        b,g,r = img[y,x]
        r = int(r)
        g = int(g)
        b = int(b)

#New window would open       
cv.namedWindow('Color Recognition')

#If clicked then find the values of r,g,b
cv.setMouseCallback('Color Recognition',positionRGB)

output=[]

#infite loop
while(1):
    #Showing the resized image
    cv.imshow("Color Recognition",img)
    if(click):
        #reference https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html

        #To display color and color names
        cv.rectangle(img,(20,20), (400,80), (255,255,255),-1)
        cv.circle(img,(60,50), 20, (b,g,r), -1)
        cv.circle(img,(60,50), 20, (0,0,0), 1)
        text = get_colorname(r,g,b)
        cv.putText(img, text,(90,60),2,0.8,(0,0,0),2,cv.LINE_AA)
        output.append(text)
 
        click=False
        

    #Break the loop when user hits 'esc or d' key    
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

#To save the selected colors in a text file
f=open('output_color.txt','w')
f.write('Colors selected in image:\n')
for i in output:
    f.write(i)
    f.write('\n')

f.close()

#To destroy the 'Color Recognition' window
cv.destroyAllWindows()
