# Caesar Cipher Decryptor
- - -
## Overview
This command line script automatically 
decrypts any text file encrypted using 
caesar cipher by analyzing every possible 
cipher shift and finding the candidate with 
most recognizable English words.
## How it works
1. The script reads the encrypted text file.
2. It generates a candidate decryption for each of the 25 possible Caesar cipher shifts.
3. Each candidate is analyzed by counting how many of its words appear in an English dictionary.
4. The candidate with the highest number of recognizable words is selected as the most likely decryption.
5. The decrypted text is written to a new output file.

Capitalization, punctuation, and formatting are preserved during decryption.

## How to use
1. Install the nltk library

`pip install nltk`

2. Run the following code to get the necessary resources

```
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('words')
```

3. Run the script from a command line prompt

```python decrypt.py sample.txt```

4. Assuming the file was encrypted using 
   Caesar cipher, an output file named
   `decrypted_sample.txt` should be generated
   containing the decrypted text


5. Open the output file and read the 
   deciphered message!

### Requirements
* Python 3.x
* NLTK
* NLTK words corpus