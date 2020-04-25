org_img = "https://upload.wikimedia.org/wikipedia/commons/5/50/Vd-Orig.png"     #Image file
kernel_number = 8       #Select kernel number

kernel_name_dict = {1:'Identity',
2:'Edge Enhance',
3:'Edge Detect',
4:'Emboss',
5:'Sharpen',
6:'Box Blur',
7:'Gaussian Blur',
8:'Gaussian Blur 5x5',
9:'Edge Detect',
10:'Edge Detect 3'}

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import threading

kernel_dict = {'Identity':np.array([[0,0,0],[0,1,0],[0,0,0]]),
'Edge Enhance':np.array([[0,0,0],[-1,1,0],[0,0,0]]),
'Edge Detect':np.array([[0,1,0],[1,-4,1],[0,1,0]]),
'Emboss':np.array([[-2,-1,0],[-1,1,1],[0,1,2]]),
'Sharpen':np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),
'Box Blur':np.array([[1,1,1],[1,1,1],[1,1,1]]),
'Gaussian Blur':np.array([[1,2,1],[2,4,2],[1,2,1]]),
'Gaussian Blur 5x5':np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]]),
'Edge Detect':np.array([[1,0,-1],[0,0,0],[-1,0,1]]),
'Edge Detect 3':np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])}

kernel_name = kernel_name_dict.get(kernel_number)
kernel = kernel_dict.get(kernel_name)
start = time.time()

img = mpimg.imread(org_img)
w = np.shape(img)[0]
h = np.shape(img)[1]
edge = len(kernel)//2
filImg = np.zeros((w,h,3))
convImg = filImg

RGBmax = np.amax(np.amax(img, axis=2))  # Check if RGB values are in range(0,1) or (0,255)
if RGBmax > 1:  # Convert RGB255 to RGB1
    img = np.dot(img,1/255)

kernel_total = 0    #sum of kernel elements for normalization
for kx in range(0,np.shape(kernel)[0]):     #Convolute the pixel with the kernel
    for ky in range(0,np.shape(kernel)[1]):
        kernel_total += kernel[kx,ky]
kernel_total = 1 if kernel_total > 1 else kernel_total

def convPixels(channel):
    for j in range(0,edge):     #copy edge pixels
        for k in range(0,w):
            filImg[j,k][channel] = img[j,k][channel]
            filImg[k,j][channel] = img[k,j][channel]
            filImg[w-j-1,k][channel] = img[w-j-1,k][channel]
            filImg[k,h-j-1][channel] = img[k,h-j-1][channel]

    for x in range(edge,np.shape(img)[0]-edge):
        for y in range(edge,np.shape(img)[1]-edge):
            acc = [0,0,0]
            for kx in range(0,np.shape(kernel)[0]):     #Convolute the pixel with the kernel
                for ky in range(0,np.shape(kernel)[1]):
                    nx = x + kx - edge      #evaluate corresponding position in image for convolution
                    ny = y + ky - edge
                    pixel = img[nx,ny]
            acc[channel] += pixel[channel] * kernel[kx,ky]
            filImg[x,y][channel] = acc[channel]/kernel_total
    return filImg[channel]

for channel in range(np.shape(img)[2]):     # Sequential operation
    convImg[channel] = convPixels(channel)
    
seqEnd = time.time()
seqTime = round((seqEnd - start),2)
print(f'Sequential operation End in {seqTime} seconds')
    
threads = []
for ch in range(np.shape(img)[2]):
    t = threading.Thread(target=convPixels, args=[ch])
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()

mulTime = round((time.time() - seqEnd),2)
print(f'Multi-threaded operation End in {mulTime} seconds')
print(f'Time gained: {round((seqTime - mulTime),2)} seconds, {round(((seqTime-mulTime)*100/seqTime),2)}% improvement')

fig = plt.figure()
plt.suptitle(kernel_name + ' Convolution', fontsize=40)
fig.add_subplot(1,2,1)
plt.imshow(img)
plt.xlabel('Before', fontsize=20)
fig.add_subplot(1,2,2)
plt.imshow(filImg)
plt.xlabel('After', fontsize=20)
plt.show()
