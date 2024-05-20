This software was used to prepare the manuscript on the tracking of chlorophyll fluorescence development in the leaves of sunflower plants under the influence of bentazone herbicide.

IMAGE CAPTURE

The original software for the MUSES9-HS hyperspectral camera does not allow for the creation of a time series of images.
The mouse_player.py program was used to automatically capture fluorescence images using the MUSES9-HS software on a Windows PC by performing mouse clicks and keyboard inputs.

At first start, the program will attempt to install any necessary libraries.
Most likely, adjustments will need to be made to the code in order to run it on another PC.
Please carefully read all of the comments in the code and make any necessary changes.

The scripts are located in three text files:
mouse_begin.txt - is played once at the start;
mouse_loop.txt - is repeated multiple times in the middle with a specified interval until the end time specified in settings.txt;
mouse_end.txt - plays once at the end.

Each script file contains the following information:
- The type of action (0 = left mouse click; 1 = symbol input; 2 = special keypress; 3 = screenshot);
- X coordinate of the mouse click or text to input, or a special key to press;
- Y coordinate of the mouse click (or nothing if it is not a click);
- Time in seconds to wait before the operation;
- Text comment.

To record a script for other purposes, you can use mouse_recorder.py. 
It records only left mouse clicks and keyboard input.
To exit recording, make a right mouse click and press ESC.


IMAGE PROCESSING

BIMP-F.py is a batch image measurement program that was used to measure the area of increased fluorescence in plant leaves caused by droplets of bentazone herbicide.
To use BIMP-F, place the BIMP-F.py file in a folder containing the images you want to process and then run it. 
At the first run, it will prompt you to install any necessary Python libraries.
