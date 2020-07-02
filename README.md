# replace_text
usage: reg_ex_sub.py [-h] -f FILE -o FILE -p STR -r STR or FILE

```
Performs regular expression substition via pattern searching and matching. The
text is then replaced with input either an input string, or strings read from
an existing file. The command line options specified here are repeatable, and
also must be matched (i.e. the first input must match the first pattern
specified).

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -f FILE, -file FILE, --file FILE
                        Input file to be searched.
  -o FILE, -out FILE, --output-file FILE
                        Output file to be written.
  -p STR, --pattern STR
                        String/pattern to be searched for in the input file.
                        NOTE: does not work well for non-isolated strings. Use
                        bash's sed for such cases.
  -r STR or FILE, --replace STR or FILE
                        String or file containing strings used to replace
                        matched pattern in the input file.
```
