# TexPlotPDF

## How to
*Input*: folder with .pdf files containing plots   
*Output*: single pdf file of all the plots
```
cd TexPlotPDF/src
python pdf_maker.py -path ~/Downloads/plots -subplots 33
```

## Help
```
python pdf_maker.py --help                                                                                                
usage: pdf_maker.py [-h] [-path path] [-subplots subplots [subplots ...]] [-title title [title ...]]

Combines pdf plots into a tex file and makes a joint pdf.

options:
  -h, --help            show this help message and exit
  -path path            path to plots folder
  -subplots subplots [subplots ...]
                        subplot layout per page
  -title title [title ...]
                        title of the pdf
```
