import PyPDF2
import json
import os
import re
import webbrowser


def create_html(bookmarks, books):
    return """
<html>

<head>
    <title>Invisible Sun Index</title>
    <style>
        @font-face {
            font-family: "duvall-font";
            src: url(data:font/woff;base64,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 ) format('woff');
        }
    </style>
    <style>
        body {
            font-family: Palatino Linotype;
            color: floralwhite;
            background-color: black;
        }

        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: black;
        }

        .title {
            font-family: duvall-font;
            float: left;
            padding-left: 2%;
        }

        #bookmarks {
            float: none;
            clear: both;
            margin-top: 80px;
        }

        ul {
            columns: 500px;
        }

        li {
            list-style: none;
            border-right: 1px solid #671C19;
        }

        .the_key a {
            color: #671C19;
            font-weight: bold;
            float: right;
            padding-right: 10px;
        }

        .the_path a {
            color: #212950;
            font-weight: bold;
            float: right;
            padding-right: 10px;
        }

        .the_way a {
            color: #A5622A;
            font-weight: bold;
            float: right;
            padding-right: 10px;
        }

        .the_gate a {
            color: #4D2E6D;
            font-weight: bold;
            float: right;
            padding-right: 10px;
        }

        .ih {
            display: none;
        }

        .search {
            text-align: right;
            padding-top: 20px;
            padding-right: 8%;
            float: right;
        }

        .search input {
            font-size: larger;
        }

        .subject {
            display: inline-block;
            max-width: 75%;
        }
    </style>
    <script>
        bookmarks = BOOKMARKS_GO_HERE
    </script>
    <script>
        function loaded() {
            // Relative links to the user's Invisible Sun book PDFs
            booklink = BOOK_PATHS_GO_HERE

            var ul = document.createElement('ul');
            for (const [key, value] of Object.entries(bookmarks)) {
                if (key == 'null') continue;
                var li = document.createElement('li');
                li.innerHTML = `<span class="subject">${key}</span>`
                for (const [book, pages] of Object.entries(value)) {
                    var span = document.createElement('span');
                    for (page of pages) {
                        span.innerHTML += `<span class="${book.replace(/ /g, '_').toLowerCase()}">
                                    <a href="${booklink[book.replace(/ /g, '-')]}#page=${Number(page) + 2}" target="_blank">${book}(${page})</a>
                                </span>`
                        li.appendChild(span)
                    }
                }

                ul.appendChild(li)
            }
            var div = document.getElementById('bookmarks');
            div.appendChild(ul)

            let cards = document.getElementsByClassName('subject')
            window.globalCards = Array.from(cards)

            // create a dictionary of words/tokens to cards for searching
            var dict = {};
            for (var i = 0; i < cards.length; i++) {
                let card = cards[i]
                let tokens = card.innerText.toLowerCase().replace(/(\(|\)|,)/g, "").replace(/-/g, " ").split(' ')
                for (token of tokens) {
                    var list = generateTokenGroups(token)
                    for (var item of list) {
                        if (item in dict) {
                            dict[item].push(card)
                        } else {
                            dict[item] = [card]
                        }
                    }
                }
            }
            console.log(Object.keys(dict).length)
            window.globalDict = dict
        }

        // Take a string and return all possible substrings
        function generateTokenGroups(inputString) {
            const tokens = [];

            for (let i = 0; i < inputString.length; i++) {
                for (let j = i + 1; j <= inputString.length; j++) {
                    tokens.push(inputString.slice(i, j));
                }
            }

            return tokens;
        }

        function liveSearch() {

            // get the search query from the input field
            let search_query = document.getElementById("searchbox").value.toLowerCase();

            // If the search query is empty, remove the class from all elements
            if (search_query.length == 0) {
                for (item of window.globalCards) {
                    item.parentElement.classList.remove("ih");
                }
                return
            }

            // Add the class to remove visibility of the element
            for (item of window.globalCards) {
                item.parentElement.classList.add("ih");
            }

            // Split the search query into tokens
            search_query = search_query.split(" ").filter(e => e);

            var found = [];

            // Loop through each token
            for (query of search_query) {
                var search = [];
                // Is the search query found in the dictionary?
                if (query in window.globalDict) {

                    // Make found items visible
                    for (item of window.globalDict[query]) {
                        // item.classList.remove("ih");
                        search.push(item)
                    }
                }
                // Add the found items to the found array
                found.push(search)
            }

            // Find the intersection of the found items
            var intersection = found[0];
            for (var i = 1; i < found.length; i++) {
                intersection = intersection.filter(element => found[i].includes(element));
                console.log(intersection)
            }

            // Make the intersection visible
            for (item of intersection) {
                item.parentElement.classList.remove("ih");
            }

        }

    </script>
</head>

<body onload="loaded()">
    <header>
        <h1 class="title">Invisible Sun Index</h1>
        <div class="search">
            <label for="searchbox">Search:</label>
            <input type="search" oninput="liveSearch()" id="searchbox">
        </div>
    </header>
    <div id="bookmarks">
    </div>
</body>

</html>
    """.replace(
        "BOOKMARKS_GO_HERE", json.dumps(bookmarks)
    ).replace(
        "BOOK_PATHS_GO_HERE", json.dumps(books)
    )


def extract_index_data(file):
    # Open the PDF file
    print(f"Opening {file} to extract index data...")
    with open(file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract the index data from pages 147 to 153
        index_data = {}
        ln = 0
        for page_num in range(146, 153):
            print(f"Extracting index data from page {page_num + 1}...")
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            text = re.sub(r"(\d)([A-Za-z])", r"\1\n\2", text)  # Add missing newlines
            lines = text.splitlines()

            # Specific fix for middle column of page 151
            for i in range(len(lines)):
                if lines[i].find("vertula kada (advancement) The Key 205") != -1:
                    lines[i] = "vertula kada (advancement) The Key 205"
                    lines[i + 1] = (
                        "very far (range) The Way , The Gate, " + lines[i + 1]
                    )

            hold = ""
            for line in lines:
                # Fix for Anguish
                if "Anguish" not in hold:
                    line = re.sub(r"^The Gate(.)", r"\1", line)
                else:
                    line = hold + line
                    hold = ""
                # Replace apostrophes with single quotes
                line = re.sub(r"\u2019", "'", line)
                if (
                    re.search(r"^\d{3}$", line) != None
                    or re.search(r"^Glossary$", line) != None
                ):
                    continue
                if re.search(r"^.+\s\d", line) != None:
                    page_numbers = re.findall(r"\d+", line)
                    books = re.findall(r"(The Key|The Path|The Way|The Gate)", line)
                    # subject = re.search(r'([A-Za-z ,\'\(\)\-]+)(?=The Key|The Path|The Way|The Gate)', line)
                    subject = re.search(
                        r"([A-Za-z ,\'\(\)\-]+?)(?=The (Key|Path|Way|Gate))", line
                    )
                    if subject != None:
                        subject = subject.group(1)
                        subject = hold + " " + subject
                        subject = subject.strip()

                    # clear held over line
                    hold = ""

                    # Fix for Squad 57B
                    if subject == "B of the Thah":
                        subject = "Squad 57B of the Thah"
                    # Add subject, books, and pages to index_data
                    if subject not in index_data:
                        index_data[subject] = {}
                    if len(books) == 1:
                        if books[0] not in index_data[subject]:
                            index_data[subject][books[0]] = page_numbers
                    else:
                        for n in range(len(books)):
                            if books[n] not in index_data[subject]:
                                index_data[subject][books[n]] = []
                            index_data[subject][books[n]].append(page_numbers[n])
                else:
                    hold = line

        return index_data


if __name__ == "__main__":
    # Get path to Invisible Sun PDF files
    path = input("Enter full path to Invisible Sun PDF files: ")
    files = os.listdir(path)

    # Create dictionary of book paths
    books = {"The-Key": "", "The-Path": "", "The-Way": "", "The-Gate": ""}

    # Search for book paths in provided directory and add them to the books dictionary
    for file in files:
        for book in books:
            search = re.search(
                r"^" + book + r"-Hyperlinked-and-Bookmarked-\d{4}-\d{2}-\d{2}_.+\.pdf",
                file,
            )
            if search != None:
                books[book] = path + "\\" + search.group(0)
                print(f"Found {books[book]}")

    # Check if all book paths were found
    for book in books:
        if books[book] == "":
            print(f"Could not find {book}")
            exit()

    # Extract index data from The Gate PDF
    index_data = extract_index_data(books["The-Gate"])

    # Create HTML file with index data
    f = open("invisible_sun_index.html", "w")
    f.write(create_html(index_data, books))
    f.close()

    print("Done!\nOpening invisible_sun_index.html in default browser...")

    # Get the path to the HTML file
    is_file = (
        "file://"
        + os.path.dirname(os.path.realpath(__file__))
        + "\\invisible_sun_index.html"
    )

    # Open the HTML file in the default browser
    webbrowser.open(is_file, 2)
