import os


# Image path
img_paths = {
    'sample1': 'http://www.siumed.edu/~dking2/intro/images/SC1.jpg',
}

def get_address(wildcards):
    return img_paths[wildcards.sample]

rule targets:
    input:
        expand("data/{sample}.done", sample=img_paths.keys())
        
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