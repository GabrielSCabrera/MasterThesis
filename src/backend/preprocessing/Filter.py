from numba import njit
import numpy as np
import os

class Filter:

    def __init__(self, kernel, label):
        '''
            PURPOSE
            Superclass for various image editing filters

            PARAMETERS
            kernel          <ndarray> of shape (m,N,N), where N%2 == 1
        '''
        # Checking that the kernel is a 3-D NxN (N%2==1) numerical ndarray
        if not isinstance(kernel, np.ndarray):
            msg = 'Parameter \'kernel\' must be a numpy <ndarray>'
            raise TypeError(msg)
        elif kernel.ndim != 4:
            msg = 'Parameter \'kernel\' must be four-dimensional'
            raise ValueError(msg)
        elif kernel.shape[1] != kernel.shape[2] != kernel.shape[3]:
            msg = 'Parameter \'kernel\' must have equal sized axes 1, 2, and 3'
            raise ValueError(msg)
        elif kernel.shape[1] % 2 != 1:
            msg = 'Parameter \'kernel\' must have odd-sized dimensions'
            raise ValueError(msg)
        elif kernel.shape[1] < 3:
            msg = 'Parameter \'kernel\' axes 1, 2, and 3 must be size 3 or greater'
            raise ValueError(msg)

        # Checking that 'label' is a <str>
        if not isinstance(label, str):
            msg = 'Parameter \'label\' expects a <str>'
            raise TypeError(msg)

        self.label = label
        self.kernel_data = kernel
        self.pad = (kernel.shape[1]-1)//2

    @property
    def kernel(self):
        '''
            PURPOSE
            Return the filter data array

            RETURNS
            self.kernel_data        3-D numerical <ndarray>
        '''
        return self.kernel_data

    def __call__(self, *args, **kwargs):
        '''
            PURPOSE
            Create an instance of Edited_Video on which the Filter subclass has
            been applied

            PARAMETERS
            arr         3-D np.ndarray

            RETURNS
            filtered    3-D np.ndarray
        '''
        msg = 'Method __call__(arr) must be implemented in a Filter subclass'
        raise NotImplementedError(msg)

    @staticmethod
    @njit(cache = True)
    def convolve(filter, pad, img, stride):
        '''
            PURPOSE
            To convolve a 3-D padded image (y,x,z) and series of 3-D filters
            (filters,z,y,x)

            PARAMETERS
            filter          4-D <ndarray>
            pad             <int> (N-1)//2
            image           3-D <ndarray>
            stride          <int> greater than zero

            WARNINGS
            No type, shape, or value checking.
            'image' should be pre-padded with zeros!

            RETURNS
            filtered_img    ndarray of <np.float64>
        '''
        img_shape = (filter.shape[0], img.shape[0]-2*pad, img.shape[1]-2*pad,
                     img.shape[2]-2*pad)

        img_shape_stride = (img_shape[0], img_shape[1]//stride,
                            img_shape[2]//stride, img_shape[3]//stride)

        filtered_img = np.zeros(img_shape_stride, dtype = np.float64)
        for f in range(img_shape[0]):
            for l,x in enumerate(range(0, img_shape[1], stride)):
                for m,y in enumerate(range(0, img_shape[2], stride)):
                    for n,z in enumerate(range(0, img_shape[3], stride)):
                        for i in range(filter.shape[1]):
                            for j in range(filter.shape[2]):
                                for k in range(filter.shape[3]):
                                    filtered_img[f,l,m,n] += \
                                    img[x+i,y+j,z+k]*filter[f,i,j,k]
        return filtered_img

    def to_binary(arr):
        '''
            PURPOSE
            Collapses an array into binary values by performing unit
            normalization and rounding
        '''
        arr_max = np.max(arr)
        arr_min = np.min(arr)
        arr_mid = (arr_max - arr_min)/2
        arr[arr <= arr_mid] = 0
        arr[arr > arr_mid] = 1
        return arr

class Sobel(Filter):

    def __init__(self, directions = None, intensity = 1):
        '''
            PURPOSE
            Create a Sobel filter, which extracts image gradients

            PARAMETERS
            directions      <nonetype> or <dict> of <bool> values
            intensity       <int> or <float>

            NOTES
            Parameter 'directions' may only contain one or a combination of the
            keys that follow: 'N', 'S', 'E', 'W', 'NE', 'NW', 'SE', and/or 'SW'.
            Their values should be of type <bool>.
        '''

        label = 'Sobel'

        # Gradient filters in cardinal & primary intercardinal directions
        filters = {}
        # North Gradient
        filters['N'] = np.array([[[-1.0,0,1],[-2,0,2],[-1,0,1]]])
        # South Gradient
        filters['S'] = np.array([[[1.0,0,-1],[2,0,-2],[1,0,-1]]])
        # East Gradient
        filters['E'] = np.array([[[1.0,2,1],[0,0,0],[-1,-2,-1]]])
        # West Gradient
        filters['W'] = np.array([[[-1.0,-2,-1],[0,0,0],[1,2,1]]])
        # Northeast Gradient
        filters['NE'] = np.array([[[0.0,-1,-2],[1,0,-1],[2,1,0]]])
        # Northwest Gradient
        filters['NW'] = np.array([[[-2.0,-1,0],[-1,0,1],[0,1,2]]])
        # Southeast Gradient
        filters['SE'] = np.array([[[2.0,1,0],[1,0,-1],[0,-1,-2]]])
        # Southwest Gradient
        filters['SW'] = np.array([[[0.0,1,2],[-1,0,1],[-2,-1,0]]])

        # Setting default 'directions': create keys 'N' and 'W' and set to True
        if directions is None:
            directions = {'S':True, 'W':True}

        # Filters that will be used
        sel_filters = []

        # Checking validity of 'directions'
        for key, value in directions.items():
            valid_keys = ['N','S','E','W','NE','NW','SE','SW']
            join_keys = ", ".join(valid_keys)

            if key not in valid_keys:
                msg = ( 'Parameter \'directions\' may only contain keys with '
                       f'the following case-sensitive values: {join_keys}.')
                raise ValueError(msg)

            elif not isinstance(value, bool):
                msg = ('Parameter \'directions\' may only contain values of '
                       'type <bool>.')
                raise TypeError(msg)

            elif value is True:
                sel_filters.append(filters[key])

        # Creating the multidimensional kernel
        kernel = intensity*np.concatenate(sel_filters, axis = 0)
        # Initializing the superclass constructor
        super().__init__(kernel, label = label)

    def __call__(self, arr, stride = 1):
        '''
            See superclass 'Filter' method '__call__'
        '''
        new_data = super().convolve(self.kernel, self.pad, arr, stride)
        new_data = np.sum(new_data**2, axis = 1)
        return np.mean(np.sqrt(new_data), axis = -1).astype(np.uint8)

class Mean_Blur(Filter):

    def __init__(self, size = 3):
        '''
            PURPOSE
            Create an arithmetic mean blur filter, which blurs an image

            PARAMETERS
            size        odd-valued <int> greater than 2
        '''
        label = 'Mean Blur'
        # Checking that 'size' fulfills required conditions
        msg = 'Parameter \'size\' must be an odd-valued <int> greater than two.'
        if not isinstance(size, int):
            raise TypeError(msg)
        elif size % 2 != 1 or size < 3:
            raise ValueError(msg)
        # Mean blur filter
        kernel = np.ones((1,size,size,size), dtype = np.float64)/(size**2)
        # Initializing the superclass constructor
        super().__init__(kernel, label)

    def __call__(self, arr, stride = 1):
        '''
            See superclass 'Filter' method '__call__'
        '''
        new_data = super().convolve(self.kernel, self.pad, arr, stride)
        shape = new_data.shape
        return new_data.reshape((shape[0],shape[2],shape[3],shape[4]))

class Gaussian_Blur(Filter):

    def __init__(self, size = 3, sigma = 1):
        '''
            PURPOSE
            Create a Gaussian blur filter, which blurs an image

            PARAMETERS
            size        odd-valued <int> greater than 2
            sigma       <float> greater than zero
        '''
        label = 'Gaussian Blur'
        # Checking that 'size' fulfills required conditions
        msg = 'Parameter \'size\' must be an odd-valued <int> greater than two.'
        if not isinstance(size, int):
            raise TypeError(msg)
        elif size % 2 != 1 or size < 3:
            raise ValueError(msg)

        # Checking that 'sigma' fulfills required conditions
        msg = 'Parameter \'sigma\' must be a <float> greater than zero.'
        if not isinstance(sigma, (int, float)):
            raise TypeError(msg)
        elif sigma <= 0:
            raise ValueError(msg)

        # Mean blur filter
        kernel = self.normal_distribution(size, sigma)[None,:,:,:]
        # Initializing the superclass constructor
        super().__init__(kernel, label)

    @staticmethod
    def normal_distribution(size, sigma):
        '''
            PURPOSE
            Creates a Gaussian kernel for a 2-D square array of shape
            (size, size) using the normal distribution.

            PARAMETERS
            size        odd-valued <int> greater than 2
            sigma       <float> greater than zero

            RETURNS
            kernel      <ndarray> of shape (size, size)
        '''
        # Creating the empty kernel coordinates
        coords = np.arange(1, size+1)
        X,Y,Z = np.meshgrid(coords, coords, coords)
        # Coordinates for the center of the kernel
        center = (size-1)//2 + 1
        # Centering values around the kernel center
        X = X - center
        Y = Y - center
        Z = Z - center
        # Getting distances from center
        D = X**2 + Y**2 + Z**2
        # Applying Gaussian function to distances
        kernel = np.exp(-D/(2*sigma**2))/(2*np.pi*sigma**2)
        # Normalizing
        kernel = kernel/np.sum(kernel)
        return kernel

    def __call__(self, arr, stride = 1):
        '''
            See superclass 'Filter' method '__call__'
        '''
        new_data = super().convolve(self.kernel, self.pad, arr, stride)
        shape = new_data.shape
        return new_data.reshape((shape[1],shape[2],shape[3]))

class Edge_Detect(Filter):

    def __init__(self, axes = None, intensity = 1):
        '''
            PURPOSE
            Create an edge detection filter, which extracts image outlines

            PARAMETERS
            axes            <nonetype> or <dict> of <bool> values
            intensity       <int> or <float>

            NOTES
            Parameter 'directions' may only contain one or a combination of the
            keys that follow: 'H', 'V', 'LD', and/or 'RD'.
            Their values should be of type <bool>.
        '''
        label = 'Edge Detection'
        # Edge detection over four axes
        filters = {}
        # Horizontal Edges
        filters['H'] = np.array([[[-1.0,-1,-1],[2,2,2],[-1,-1,-1]]])
        # Vertical Edges
        filters['V'] = np.array([[[-1.0,2,-1],[-1,2,-1],[-1,2,-1]]])
        # Left Diagonal Edges
        filters['LD'] = np.array([[[2.0,-1,-1],[-1,2,-1],[-1,-1,2]]])
        # Right Diagonal Edges
        filters['RD'] = np.array([[[-1.0,-1,2],[-1,2,-1],[2,-1,-1]]])

        # Setting default 'directions': create keys 'H' and 'V' and set to True
        if axes is None:
            axes = {'H':True, 'V':True}

        # Filters that will be used
        sel_filters = []

        # Checking validity of 'directions'
        for key, value in axes.items():
            valid_keys = ['H','V','LD','RD']
            join_keys = ", ".join(valid_keys)

            if key not in valid_keys:
                msg = ( 'Parameter \'directions\' may only contain keys with '
                       f'the following case-sensitive values: {join_keys}.')
                raise ValueError(msg)

            elif not isinstance(value, bool):
                msg = ('Parameter \'directions\' may only contain values of '
                       'type <bool>.')
                raise TypeError(msg)

            elif value is True:
                sel_filters.append(filters[key])

        # Creating the multidimensional kernel
        kernel = intensity*np.concatenate(sel_filters, axis = 0)
        # Initializing the superclass constructor
        super().__init__(kernel, label)

    def __call__(self, arr, stride = 1):
        '''
            See superclass 'Filter' method '__call__'
        '''
        new_data = super().convolve(self.kernel, self.pad, arr, stride)
        new_data = np.sum(new_data**2, axis = 1)
        return np.mean(np.sqrt(new_data), axis = -1).astype(np.uint8)

class Laplacian(Filter):

    def __init__(self, size = 3, sigma = 1, intensity = 1, negative = False):
        '''
            PURPOSE
            Create a Laplace of Gaussian filter, which sharpens an image

            PARAMETERS
            size        odd-valued <int> greater than 2
            sigma       <float> greater than zero
            intensity   <float> greater than zero
            negative    <bool> represents the sign of the filter
        '''
        label = 'Laplace Sharpen'
        # Checking that 'size' fulfills required conditions
        msg = 'Parameter \'size\' must be an odd-valued <int> greater than two.'
        if not isinstance(size, int):
            raise TypeError(msg)
        elif size % 2 != 1 or size < 3:
            raise ValueError(msg)

        # Checking that 'sigma' fulfills required conditions
        msg = 'Parameter \'sigma\' must be a <float> greater than zero.'
        if not isinstance(sigma, (int, float)):
            raise TypeError(msg)
        elif sigma <= 0:
            raise ValueError(msg)

        # Checking that 'intensity' fulfills required conditions
        msg = 'Parameter \'intensity\' must be a <float> greater than zero.'
        if not isinstance(intensity, (int, float)):
            raise TypeError(msg)
        elif intensity <= 0:
            raise ValueError(msg)

        # Checking that 'negative' fulfills required conditions
        msg = 'Parameter \'negative\' must be a <bool>.'
        if not isinstance(negative, bool):
            raise TypeError(msg)

        # Mean blur filter
        kernel = self.laplacian_of_gaussian(size, sigma, intensity, negative)
        # Initializing the superclass constructor
        super().__init__(kernel[None,:,:,:], label)

    @staticmethod
    def laplacian_of_gaussian(size, sigma, intensity = 1, negative = False):
        '''
            PURPOSE
            Creates a Laplace of Gaussian kernel for a 2-D square array of shape
            (size, size) using the normal distribution.

            PARAMETERS
            size        odd-valued <int> greater than 2
            sigma       <float> greater than zero
            intensity   <float> greater than zero
            negative    <bool> represents the sign of the filter

            RETURNS
            kernel      <ndarray> of shape (size, size)
        '''
        # Creating the empty kernel coordinates
        coords = np.arange(1, size+1)
        X,Y,Z = np.meshgrid(coords, coords)
        # Coordinates for the center of the kernel
        center = (size-1)//2 + 1
        # Centering values around the kernel center
        X = X - center
        Y = Y - center
        Z = Z - center
        # Getting distances from center
        D = X**2 + Y**2 + Z**2
        # Applying Laplacian of Gaussian function to distances
        kernel = -D/(2*sigma**2)
        kernel = -np.exp(kernel)*(1+kernel)/(np.pi*sigma**4)
        # Normalizing to Corners
        kernel = kernel-kernel[0,0,0]
        if negative:
            kernel = -kernel
        return kernel*intensity

    def __call__(self, arr, stride = 1):
        '''
            See superclass 'Filter' method '__call__'
        '''
        new_data = super().convolve(arr, stride)
        new_data = super().convolve(self.kernel, self.pad, arr, stride)
        shape = new_data.shape
        return new_data.reshape((shape[0],shape[2],shape[3],shape[4]))

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x = np.linspace(0, 0.01, 100)
    X,Y,Z = np.meshgrid(x,x,x)
    arr = X**2 - Y**3 + Z**2
    plt.imshow(arr[:,:,0])
    plt.show()
    gauss = Gaussian_Blur()
    out = gauss(arr, 2)
    plt.imshow(out[:,:,0])
    plt.show()
