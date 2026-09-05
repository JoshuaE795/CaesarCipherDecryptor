# Import
# --------------------------------------------------------------------------------
import sys, os, io
from time import perf_counter
from nltk.corpus import words
# --------------------------------------------------------------------------------

'''
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('words')
'''

# Functions
# --------------------------------------------------------------------------------
# read substring excluding non-caesar characters like punctuation
def strip_special(string:str):
    stripped_str:str = ""
    for char in string:
        if char.lower() in alph:
            stripped_str += char
    return stripped_str
# --------------------------------------------------------------------------------

# Setup
# --------------------------------------------------------------------------------
start:float = perf_counter()

e_filename = sys.argv[1]
all_words:set[str] = set(words.words())
alph:str = "abcdefghijklmnopqrstuvwxyz"
# temp file for each possible encryption
candidates:list[io.StringIO] = [io.StringIO() for i in range(25)]
# count the sensible words in each decryption
candidate_sensible_words:list[int] = [0 for i in range(25)]
# --------------------------------------------------------------------------------


# Go through each number shift, writing each decryption to a new temporary file
# --------------------------------------------------------------------------------
with open(e_filename, 'r') as file:
    for shift in range(1, 26):

        lower_map:dict[str, str] = {
            item:alph[(index + shift)%26]
            for index, item in enumerate(alph)
        }
        upper_map:dict[str, str] = {
            item:alph.upper()[(index + shift)%26]
            for index, item in enumerate(alph.upper())
        }

        file.seek(0) # reset line
        
        for line in file:
            if line.strip() == "": # directly copy the line over if its just a blank
                d_line:str = line
            else:

                d_line:str = ""
                for char in line:
                    if char.lower() not in alph: # directly copy over special characters
                        d_line += char
                    elif char == char.lower():
                        '''
                        decrypt lower case characters by compiling a dictionary of lowercase 
                        letter keys to their corresponding caesar'd letter values by adding 
                        the shift to the index of the letter and using the modulo operator to 
                        make the values wrap around upon exceeding the length of the alphabet
                        '''
                        d_line += lower_map[char]
                    else:
                        '''
                        in the case of uppercase letters, do the same but with an uppercase
                        alphabet
                        '''
                        d_line += upper_map[char]
            candidates[shift-1].write(d_line) # subtract 1 from the shift to determine the index of the file

# --------------------------------------------------------------------------------

# Record the number of sensible words contained for each number shift
# --------------------------------------------------------------------------------
for index, tempfile in enumerate(candidates):
    tempfile.seek(0) # reset line
    for word in tempfile.getvalue().split():
        # if a sensible word is found, increment the counter for that file
        if(strip_special(word).lower() in all_words):
            candidate_sensible_words[index] += 1
# --------------------------------------------------------------------------------

# Determine the most sensible decryption based on the amount of sensible words
# --------------------------------------------------------------------------------
candidates.insert(0, e_filename)
candidate_sensible_words.insert(0, 0)
most_sensible = open(e_filename, 'r') # initialize most_sensible as the original file
most_sensibility:int = 0

# set the most sensibility as the sensibiilty of the original file in case it is already decrypted
with open(e_filename, 'r') as original:
    original.seek(0)
    for word in original.read().split():
        if(strip_special(word).lower() in all_words):
            most_sensibility += 1

for i in range(len(candidates)):
    if candidate_sensible_words[i] > most_sensibility:
        most_sensibility = candidate_sensible_words[i]
        most_sensible = candidates[i]
# --------------------------------------------------------------------------------

# Name appropriately
# --------------------------------------------------------------------------------
ext:str = ""
num:int = 1

# continuously increase the number of the decrypted file until the name is available
while os.path.exists(f"decrypted_{e_filename[:e_filename.index('.')]}{ext}.txt"):
    num+=1
    ext=f"_{num}"

# create the new decrypted file using the validated name
with open(f"decrypted_{e_filename[:e_filename.index('.')]}{ext}.txt", 'x') as d_file:
    for line in (
            most_sensible.getvalue()
            if type(most_sensible) == io.StringIO
            else most_sensible.read()
    ):
        d_file.write(line)
# --------------------------------------------------------------------------------

end:float = perf_counter()
print(f"Elapsed Time: {end - start}") # display the time taken to execute this process