# Fleaux
(as in like, control flow.. I dont know, I couldn't think of a name and came up with this)

## Installation
```bash
python -m pip install fleaux
```
## Usage
```bash
fleaux  [filename] [filetype (h, cpp, py)]
```
or 
```bash
python3 -m fleaux [filename] [filetype]
```
and you can also always call '-h' if you need to see this again!
```bash
fleaux -h
How to Fleaux
fleaux [filename] [filetype (h, cpp, py)]
or
--update (to update fleauxData)
```

When you first use this program in a given directory
you will be prompted to enter your Name and email.
```bash
your name: Oliver
your email: hello@wave.com
```
This data will be stored in a file in the directory, 
so whenever you call it the author and email sections of 
header comments will be prefilled with that data instead of
having to prompt you everytime.
However, if you want to update any of this info you can
with
```bash
fleaux --update
```