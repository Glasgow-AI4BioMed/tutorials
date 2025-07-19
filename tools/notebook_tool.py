import argparse
import json
import os
from nbconvert import HTMLExporter
import nbformat

def remove_code_cells(notebook):
    # Filter out code cells
    notebook['cells'] = [cell for cell in notebook.get('cells', []) if cell.get('cell_type') != 'code']
	
def normalize_sources(notebook_dict):
    for cell in notebook_dict.get("cells", []):
        if isinstance(cell.get("source"), list):
            cell["source"] = "".join(cell["source"])
    return notebook_dict

def convert_to_html(notebook, output_path):
    nb = nbformat.from_dict(normalize_sources(notebook))

    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(nb)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(body)

    print(f"Notebook converted to HTML at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Tool for cleaning and exporting a notebook for checking.")
    parser.add_argument("--in_notebook", type=str, required=True, help="Path to the input .ipynb file")
    parser.add_argument("--out_html", type=str, required=True, help="Path to the output HTML page")

    args = parser.parse_args()

    # Load the notebook
    with open(args.in_notebook, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
        
    remove_code_cells(notebook)
    
    convert_to_html(notebook, args.out_html)

if __name__ == "__main__":
    main()
