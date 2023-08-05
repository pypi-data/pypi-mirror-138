
# String to Date Time Format

If You importing your data from a .csv file ,might be some time you can get the error as improper format for date time library then you can use this library to convert to a suitable format for your data.

## installation
- command Prompt -pip install string_dtm
- Jp notebook >! pip install string_dtm


## Use
- import string_dtm
- from string_dtm import convert
- convert.to_fmt(string,format)
 EX :-
- string='14-11-2005 00:00'
- format='%Y-%m-%d %H:%M:%S' 
convert.to_fmt(string,format)
- Result > 2005-11-14 00:00:00
## Authors

- [@ranjit Maity](https://www.github.com/RanjitM007)

