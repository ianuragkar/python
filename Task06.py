org_img = "https://upload.wikimedia.org/wikipedia/commons/5/50/Vd-Orig.png"     #Image file
kernel_number = 6       #Select kernel number

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

img = mpimg.imread(org_img)
w = np.shape(img)[0]
h = np.shape(img)[1]
edge = len(kernel)//2
fil_img = np.zeros((w,h,3))

#copy edge pixels
for j in range(0,edge):
    for k in range(0,w):
        fil_img[j,k] = img[j,k]
        fil_img[k,j] = img[k,j]
        fil_img[w-1,k] = img[w-1,k]
        fil_img[k,h-1] = img[k,h-1]

for x in range(edge,np.shape(img)[0]-edge):
    for y in range(edge,np.shape(img)[1]-edge):
        acc = [0,0,0]
        kernel_total = 0    #sum of kernel elements for normalization
        for kx in range(0,np.shape(kernel)[0]):     #Convolute the pixel with the kernel
            for ky in range(0,np.shape(kernel)[1]):
                kernel_total += kernel[kx][ky]
                nx = x + kx - edge      #evaluate corresponding position in image for convolution
                ny = y + ky - edge
                pixel = img[nx,ny]
                for i in range(0,3):
                    acc[i] += pixel[i] * kernel[kx,ky]
            
        #check if normalisation required
        if kernel_total == 0:
            fil_img[x,y] = acc
        else:
            fil_img[x,y] = acc/kernel_total
        
fig = plt.figure()
plt.suptitle(kernel_name + ' Convolution', fontsize=40)
fig.add_subplot(1,2,1)
plt.imshow(img)
plt.xlabel('Before', fontsize=20)
fig.add_subplot(1,2,2)
plt.imshow(fil_img)
plt.xlabel('After', fontsize=20)
plt.savefig('Vd-Conv.png')
plt.show()
