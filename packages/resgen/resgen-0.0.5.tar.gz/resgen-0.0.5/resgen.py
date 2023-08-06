from app import application
import click
import os

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option(
    '-i',
    '--input_folder',
    type=str, 
    help='The name of the input folder where the image(s) are located us required.')
@click.option(
    '-o',
    '--output_folder',
    type=str,
    default='output',
    help='The name of the output folder you want to place the saved images is required.')
def main(output_folder, input_folder):
    if not input_folder:
        print('The name of the input folder where the image(s) are located us required. Type respon --help to see usage ')
        return
    if not output_folder:
        print('The name of the output folder you want to place the saved images is required. Type respon --help to  see usage ')
        return
    current_directory = os.getcwd()
    try:
        input_directory = os.path.join(current_directory, input_folder)
        output_directory = os.path.join(current_directory, output_folder)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        application.initialize(input_directory, output_directory)
    except OSError as e:
        print(e.message)
    except KeyboardInterrupt:
        print('[-] Detected CTRL +C. Exiting....')
        sys.exit(1)