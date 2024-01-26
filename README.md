# Invisible Sun tools
Some files to help play the Invisible Sun RPG

## Invisible Sun index
A Python script that scrapes The Gate pdf for index references and presents them as a standalone HTML file. The links open the appropriate PDF to the referenced page.

Video: https://www.youtube.com/watch?v=v3uuBQ3dGsE

**NOTE**: The script specifically looks for files that use the [Monte Cook Games](https://www.montecookgames.com/) naming convention for downloaded files. If you have renamed the files, the script will not work.

### Prerequisites
 - Python 3.6+
 - Locally saved versions of the main four Invisible Sun PDFs (The Key, The Path, The Way, The Gate) in a single folder.

### Usage
1. Save or clone the repositiory to your computer.

2. Install the dependencies:

    ```pip install -r requirements.txt```

3. Run the script:

    ```python create-index.py```

4. Enter the path to the folder containing your saved PDFs.

5. The script will create a file called invisible_sun_index.html in the same folder as the script. Open the file in your browser to view the index.

### Using the HTML file
Once loaded in your browser, the links will open the PDFs in your browser.

There is a search function to make it easier to find a specific topic.

## Get Cards
Python script to extract card data from Invisible Sun card PDF files and create a JSON file for use in other applications.

### Prerequisites
 - Python 3.6+
 - Locally saved versions of the Invisible Sun card PDFs.

 ### Usage
 1. Save or clone the repositiory to your computer.

 2. Install the dependencies:
    
    ```pip install -r requirements.txt```

3. Run the script:
    
    ```python get-cards.py "C:\path\to\folder\with\pdfs\cardfile.pdf"```

4. The script will create a file in the same folder as the script.