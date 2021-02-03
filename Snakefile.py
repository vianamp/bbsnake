import os
import numpy as np
from skimage import io as skio

# Image path
img_urls = {
    'sample1': 'http://www.siumed.edu/~dking2/intro/images/SC1.jpg',
}

def get_address(wildcards):
    return img_urls[wildcards.sample]

def prepare_image(wildcards):
    # Get filename based on URL
    filename = img_urls[wildcards.sample].split('/')[-1]
    # Load image
    img = skio.imread('data/'+filename)
    print(img.shape,img.dtype)
    # Convert from RGB to grayscale and adjust contrast
    img = img.max(axis=-1)
    pinf, psup = np.percentile(img.flatten(),[5,95])
    img = np.clip(img,pinf,psup)
    img = (255*(img-pinf)/(psup-pinf)).astype(np.uint8)
    # Save with standard name and format
    skio.imsave('data/%s.png'%wildcards.sample, img)
    return 'data/%s.png'%wildcards.sample

rule targets:
    input:
        expand("data/{sample}.png", sample=img_urls.keys())
        
rule download_images:
    output:
        "data/{sample}.done"
    params:
        address=get_address
    shell:
        '''
        wget {params.address} --directory data/
        touch data/{wildcards.sample}.done
        '''
        
rule prepare_images:
    input:
        "data/{sample}.done",
        prepare_image
    output:
        "data/{sample}.png"
