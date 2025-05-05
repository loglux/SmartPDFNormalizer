# SmartPDFNormalizer

**SmartPDFNormalizer** is a command-line utility that normalises PDF page sizes to a unified format and optionally inserts a blank page at a specific position.  
It is useful for ensuring consistent display, layout uniformity, or preparing documents for print or automated processing.

## Features

- Detects the most common page dimensions across the document (mode).
- Calculates the average of similar page sizes (within a tolerance).
- Rescales all pages to the average dimensions.
- Optionally inserts a blank page at a given position.
- Generates a report of all page transformations in both `.txt` and `.json` formats.

## Requirements

- Python 3.7+
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (`pip install pymupdf`)

## Installation

Clone the repository and install the required dependency:

```bash
git clone https://github.com/yourusername/SmartPDFNormalizer.git
cd SmartPDFNormalizer
pip install -r requirements.txt
```

`requirements.txt`:
```
pymupdf
```

## Usage

```bash
python pdf2norm.py input.pdf output.pdf [--insert_blank 3] [--report_txt my_report.txt] [--report_json my_report.json]
```

### Arguments

| Argument           | Description                                                                          |
|--------------------|--------------------------------------------------------------------------------------|
| `input`            | Path to the input PDF file.                                                         |
| `output`           | Path to the output PDF file (after normalisation).                                  |
| `--insert_blank`   | (Optional) 1-based index of where to insert a blank page.                           |
| `--report_txt`     | (Optional) Path to save the human-readable `.txt` report. Default: `report.txt`.    |
| `--report_json`    | (Optional) Path to save the machine-readable `.json` report. Default: `report.json`.|

## Example

```bash
python pdf_norm.py input.pdf output.pdf --insert_blank 3 --report_txt summary.txt --report_json summary.json
```

This command will:
- Calculate the most frequent page size in the input PDF.
- Average the dimensions of similar pages (within 0.15 pt tolerance).
- Resize all pages to that average size.
- Insert a blank page as the new third page.
- Save transformation details to `summary.txt` and `summary.json`.

## Output

- `output.pdf`: The normalised PDF file.
- `report.txt`: A plain-text summary of page changes.
- `report.json`: A structured report with details for each page.

## Limitations

- The tool currently assumes that most pages are of the desired size and filters out outliers like covers or inserts based on similarity to the mode.
- Pages with drastically different sizes (e.g. scanned covers or inserts) will be forcefully rescaled unless filtered beforehand.

## License

This project is licensed under the MIT Licence. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions, issues and suggestions are welcome!  
Please fork the repository and open a pull request.
