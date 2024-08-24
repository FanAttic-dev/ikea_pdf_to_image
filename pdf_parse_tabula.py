import pandas as pd
import tabula

file = "assets/request.pdf"

# Read pdf into list of DataFrame
dfs = tabula.read_pdf(file, pages='all')

...
# convert PDF into CSV file
# tabula.convert_into("test.pdf", "output.csv", output_format="csv", pages='all')

# convert all PDFs in a directory
# tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')

