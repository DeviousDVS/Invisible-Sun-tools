from contextlib import suppress
import json
import platform
import PyPDF2
import re
import sys


def remove_extra_spaces(text):
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\n ", "\n", text)
    text = re.sub(r" \n", "\n", text)
    return text


def extract_index_data(file, start_page=3):
    # Open the PDF file
    with open(file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract the text data from pages
        spell_dict = {}
        count = 0

        # Process a single page if one is specified
        end_page = len(pdf_reader.pages)
        if start_page != 3:
            end_page = start_page + 1

        # Loop through the pages
        for page_num in range(start_page, end_page):
            # Print progress to the console
            sys.stdout.write("\rExtracting from page: %i " % page_num)
            sys.stdout.flush()

            # Extract the text from the page
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Basic text cleanning
            replacements = {
                r"(THE KEY|THE PATH|THE WAY|THE GATE)": lambda m: m.group(0).lower(),
                r"(TM and ©2019 Monte Cook Games,)": "",
                r"(TM and ©2018 Monte Cook Games, LLC)": "",
                r"(TM and ©2020 Monte Cook Games,)": "",
                r"(LLC. Invisible Sun and its logo are trademarks of Monte Cook Games,)": "",
                r"(LLC in the United States and other countries. Permission granted to duplicate for personal use.)": "",
                r"(’)": "'",
                r"(–)": "-",
                r"(“|”)": '"',
                r"r*(“|”)": '"',  # r* is to make key different. It has no effect on the replacement (HACK)
                r"(✦)": "",
                r"(,)": ",",
            }

            for pattern, replacement in replacements.items():
                text = re.sub(pattern, replacement, text, re.DOTALL)

            # Problem page
            # if page_num == start_page != 3:
            #     print(text)

            # Determine where the spells start and divide into individual items
            # spell_names = re.findall(r"Color: [A-Z]{1}[a-z]+([A-Z]+\s*[A-Z]*)\nLevel:", text)
            # text = re.sub(r"([A-Z'-]{4,}\s*[A-Z'-]*\s*[A-Z'-]*\s*[A-Z'-]*\s*[A-Z'-]*)", r"###\1", text).strip()
            text = re.sub(
                r"(([A-Z',-]+\s+)+)(?=Level\:\s+\d+)", r"###\1", text, re.MULTILINE
            ).strip()

            # Problem page
            # if page_num == start_page != 3:
            #     print(text)

            # print(text)
            spells = re.split(r"###", text)

            # Remove blanks
            remove_list = []
            for spell_num in range(len(spells)):
                if (re.search(r".+", spells[spell_num])) == None:
                    remove_list.append(spell_num)

            for i in sorted(remove_list, reverse=True):
                # print(f"Removing blank spell '{spells[i]}' of length {len(spells[i])}")
                del spells[i]

            # Extract the data from each spell
            for spell_num in range(len(spells)):
                count += 1
                try:
                    # name = re.search(r"([A-Z]{3,}\s*[A-Z]*\s*[A-Z]*)", spells[spell_num]).group(0).replace("\nL", "").replace("\n", "").strip()
                    name = (
                        re.search(
                            r"(([A-Z',-]+\s+)+)(?=Level\:\s+\d+)",
                            spells[spell_num],
                            re.MULTILINE,
                        )
                        .group(0)
                        .replace("\n", "")
                        .strip()
                    )
                    name = remove_extra_spaces(name)
                    # print(f"{count}. " + name)

                    level = remove_extra_spaces(
                        re.search(r"Level:\s+(\d+)", spells[spell_num]).group(1)
                    )

                    dice = re.search(r"\((\+\d+ di[c]*e[a-z\s']*)\)", spells[spell_num])
                    if dice != None:
                        dice = remove_extra_spaces(
                            dice.group(1).replace("\n", "").strip()
                        )
                    else:
                        dice = ""

                    lookahead = r"(?=Color:)"
                    if spells[spell_num].find("Depletion:") > -1:
                        lookahead = r"(?=Depletion:)"

                    # description = re.search(r"Level: \d+(?: \(\+\d+ di[c]*e\))?([\nA-Za-z0-9_,ö';—−\"\+\-\(\)\. ]+)([^A-Za-z+\:])", spells[spell_num]).group(1).replace("\n", "").strip()
                    description = (
                        re.search(
                            r"Level:\s+\d+(?: \(\+\d+ di[c]*e[a-z\s']*\))?([\nA-Za-z0-9_,ö';:—−/?\[\]\"\+\-\(\)\. ]+)"
                            + lookahead,
                            spells[spell_num],
                        )
                        .group(1)
                        .replace("\n", "")
                        .strip()
                    )
                    description = remove_extra_spaces(
                        re.sub(r"([a-z])(\.|:)([A-Z])", r"\1\2\n\3", description)
                    )

                    color = remove_extra_spaces(
                        re.search(r"Color:\s+([A-Z][a-z]+)", spells[spell_num]).group(1)
                    )

                    depletion = re.search(
                        r"Depletion:\s+([\w\s\d\(\)\-]+)[^A-Za-z+\:]", spells[spell_num]
                    )
                    if depletion != None:
                        depletion = remove_extra_spaces(
                            depletion.group(1).replace("\n", "").strip()
                        )
                    else:
                        depletion = ""

                    facets = re.search(
                        r"Facet(?:s)?: ([ \w\d\(\)\-,]+)", spells[spell_num]
                    )
                    if facets != None:
                        facets = remove_extra_spaces(facets.group(1).strip())
                    else:
                        facets = ""

                    spell_dict[name] = {
                        "level": level,
                        "dice": dice,
                        "description": description,
                        "depletion": depletion,
                        "color": color,
                        "facets": facets,
                    }

                except Exception as e:
                    print(text)
                    print(f"Error extracting spell data from {name}: {e}")
                    print(f"Spell text: {spells[spell_num]}")
                    spell_dict[name] = {
                        "level": level,
                        "dice": dice,
                        "description": description,
                        "depletion": depletion,
                        "color": color,
                        "facets": facets,
                    }
                    print(spell_dict[name])

        return spell_dict


if __name__ == "__main__":
    file = ""
    start_page = 3
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if platform.system() == "Windows" and "\\" in file:
            output = file.replace(".pdf", ".json").split("\\")[-1]
        elif "/" in file:
            output = file.replace(".pdf", ".json").split("/")[-1]
    else:
        print(
            """Usage: Python get-cards.py [FILE] [OUTPUT FILE] [START_PAGE]
Example: Python .\\get-cards.py "C:\\Users\\User\\Desktop\\Cards\\Cards.pdf" "C:\\Users\\User\\Desktop\\Cards\\Cards.json" 3"""
        )
        exit()

    if len(sys.argv) > 3 and sys.argv[3].isnumeric():
        print(sys.argv[3])
        start_page = int(sys.argv[3])

    index_data = extract_index_data(file, start_page)

    # Sort the data alphabetically by name
    index_data = dict(sorted(index_data.items()))

    if len(sys.argv) > 2 and sys.argv[2] != "":
        output = sys.argv[2]

    f = open(output, "w")
    f.write(json.dumps(index_data))
    f.close()

    # print(index_data[0])
