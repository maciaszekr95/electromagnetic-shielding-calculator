# Electromagnetic shielding effectiveness (EMSE)

Video Demo:

<https://drive.google.com/file/d/1eGRshmRuMpeAI-Rh5FmwbgkDfOzgtYt4/view?usp=sharing>

#### Description:

This project is a simple look at the problem of choosing the proper material for electromagnetic shielding. It is run in the terminal based on a user-provided frequency. It chooses the material from the CSV file and calculates absorption losses, reflection losses, and total shielding effectiveness.

## How to run

In order for it will run correctly, two files are requested, ‘project.py’ and ‘materials.csv’. With them in one folder, the program is started by the command:

    python project.py

Next, the program asks for frequency, for example ‘50Hz’, ‘1kHz’, or ‘2.5MHz’. It works with the following SI units: mHz, Hz, kHz, MHz, GHz. The space between value and unit is not requested but code allows to use it as well.

## project.py

This file consists of ‘main’ and three additional functions responsible for correct calculation and the presented output.

‘main’ controls data intake and summons other functions. Also, here the results are printed. In case of unwanted behavior of other functions, it prompts error messages.

‘frequency_checker’ uses regular expressions in order to determine unit and value. It separates them and converts them to a float and Hz. The last thing handled here is determining whether the user prefers millihertz (mHz) or megahertz MHz. Wrong value or unproper or missing unit cause ‘ValueError’ return.

‘get_material’ reads ‘materials.csv’ and searches for the material corresponding to the provided frequency. It returns the list of all matching materials and their parameters needed for calculations. If the frequency does not match any material, it returns an error.

‘calculate_shielding’ calculates absorption and reflection losses. It uses frequency, thickness, relative permeability mu_r, and relative conductivity sigma_r. In order to simplify the calculations, the distance from the source of radiation is constant at 0.3 m. Both results are summed and returned as a float.

## materials.csv

The file contains the data from three materials: mu-metal, Si-steel, and copper. For all, I have copied or calculated the name, frequencies, relative permeability, relative conductivity, and usual thickness used in applications. The frequency ranges are as follows: mu-metal 0 Hz to 10 kHz, Si-steel 10 kHz - 1 MHz, and copper 100 kHz - 1 GHz.

## Implementation decisions

File ‘materials.csv’ was created in order to separate data from code. First, I wanted to get data directly from the source website, but it is presented there in the form of a graphic, so I have decided to make my own file.

The result of material selection is in the form of a list, as frequencies may be covered by more materials than just one. The user needs to distinguish which one he wants to use, as there are other parameters that may indicate that, such as complexity of implementation or costs, not only shielding effectiveness.

## test_project.py

File contains tests of all three functions using ‘pytest’. Tests check for unit recalculation, rejection of incorrect data, usage of one or more materials, out-of-range frequency, or missing CSV file. They also check the structure of calculation results.

Library and tests are run by commands:

    pip install pytest
    pytest test_project.py

## Assumptions and source

Program uses predefined material parameters and thickness to use. I want to make it more complicated in the future, but being aware of the CS50P requirements, I stopped myself from doing that. The presented calculation model is a general engineering idea, not an overcomplicated physical model. Currently, the user has no impact on the thickness of the material; the program is also not suggesting it. The same applies to the distance from the source.

As a source of knowledge, I have used: <https://www.academyofemc.com/shielding>

English was checked with Grammarly

eDx: RobertM95

GitHub: maciaszekr95
