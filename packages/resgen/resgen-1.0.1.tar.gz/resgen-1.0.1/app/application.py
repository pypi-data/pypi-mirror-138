import os
from PIL import Image

sizes = [
    1920,
    1600,
    1366,
    1024,
    768,
    640
]


def initialize(input_directory: str, output_directory: str):
    """The function initializes the process
       ----------
       input_directory : string, required
           The full path to the images
       output_directory : string, required
           The full path to the output directory
       Returns null
       """
    counter = 1
    folder_name = f'image_{counter}'
    try:
        print('[+] Creating responsive images.... ')
        for file in os.listdir(input_directory):
            f_image = os.path.join(input_directory, file)
            img = Image.open(f_image)
            save_image(img, folder_name, output_directory)
            folder_name = f'image_{counter + 1}'
        print(f'[+] Responsive Images created. Saved in {output_directory}')
    except OSError as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)


def save_image(image: Image, name: str, output_directory: str):
    """Function to loop through the image sizes and save each one per fie
       Parameters
       ----------
       image : object, required
           The Image object from the file
       name : string, required
           The name we would be giving the file
       output_directory : str, required
            The location where the files would be saved
       Returns null
       -------

       """
    try:
        for size in sizes:
            resized_image = image.resize((size, size))
            if not os.path.exists(os.path.join(output_directory, name)):
                os.mkdir(os.path.join(output_directory, name))
            current_file_name = os.path.join(output_directory, name, f'{name}_{size}_.jpeg')
            resized_image.save(current_file_name)
    except Exception as e:
        raise Exception(e)




