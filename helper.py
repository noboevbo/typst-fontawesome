import argparse
import json
import zipfile
import urllib.request
import shutil
import os
import glob
import textwrap

parser = argparse.ArgumentParser(description="typst-fontawesome helper script")

parser.add_argument(
    "-d",
    "--download",
    help="Download FontAwesome fonts and metadata (occur two times to extract the zip file)",
    action="count",
    default=0,
)
parser.add_argument("-v", "--version", help="FontAwesome version", required=True)
parser.add_argument(
    "-o", "--output", help="Output dir (default: current dir .)", default="."
)
parser.add_argument(
    "-g",
    "--generate",
    help="Generate typst files (can be `lib`, `doc`)",
    default=["lib", "doc"],
)


def download(version, output, extract=False):
    ZIP_LINK_TEMPLATE = (
        "https://use.fontawesome.com/releases/v{}/fontawesome-free-{}-desktop.zip"
    )
    zip_link = ZIP_LINK_TEMPLATE.format(version, version)

    print(f"Downloading FontAwesome {version} metadata from {zip_link}")

    zip_file = os.path.join(output, "fontawesome.zip")

    # Download the zip file to the output directory
    req = urllib.request.Request(zip_link, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        with open(zip_file, "wb") as f:
            shutil.copyfileobj(response, f)

    if extract:
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(output)


def generate_lib(version, output):
    print(f"Generating typst lib for FontAwesome {version}")

    LIB_PREAMBLE_TEMPLATE = """\
    /*

    typst-fontawesome

    https://github.com/duskmoon314/typst-fontawesome

    generated by typst-fontawesome helper python script

    */

    #let fa-icon(
      name,
      fa-version: "Font Awesome {}",
      fa-set: "Free"
    ) = text.with(
      font: fa-version + " " + fa-set,
      name
    )

    """

    # split the version to get the major version
    major_version = version.split(".")[0]

    lib_preamble = textwrap.dedent(LIB_PREAMBLE_TEMPLATE).format(major_version)

    lib_file = os.path.join(output, "fontawesome.typ")

    with open(lib_file, "w") as f:
        f.write(lib_preamble)

        # Find the metadata/icons.json file with glob
        icons_file = glob.glob(
            os.path.join(output, "**/metadata/icons.json"), recursive=True
        )
        if len(icons_file) == 0:
            raise Exception("Cannot find metadata/icons.json")
        icons_file = icons_file[0]

        with open(icons_file, "r") as icons_f:
            icons_data = json.load(icons_f)

            for icon_name, icon_data in icons_data.items():
                # Generate the icon line
                f.write(
                    f"#let fa-{icon_name} = fa-icon(\"\\u{{{icon_data['unicode']}}}\")\n"
                )

                # Generate the alias lines
                if "aliases" in icon_data:
                    if "names" in icon_data["aliases"]:
                        for alias_name in icon_data["aliases"]["names"]:
                            f.write(
                                f"#let fa-{alias_name} = fa-icon(\"\\u{{{icon_data['unicode']}}}\")\n"
                            )


def generate_doc(version, output):
    print(f"Generating typst doc for FontAwesome {version}")

    DOC_TEMPLATE = """\
    #import "fontawesome.typ": *

    = typst-fontawesome

    duskmoon314

    https://github.com/duskmoon314/typst-fontawesome

    A Typst library for Font Awesome {version} icons through the desktop fonts.

    == Usage

    === Install the fonts

    You can download the fonts from the official website: https://fontawesome.com/download

    Or you can use the helper script to download the fonts and metadata:

    `python helper.py -dd -v {version}`

    Here `-dd` means download and extract the zip file. You can use `-d` to only download the zip file.

    After downloading the zip file, you can install the fonts depending on your OS.

    === Import the library

    Put the `fontawesome.typ` file in your project directory, and import it:

    `#import "fontawesome.typ": *`

    === Use the icons

    You can use the `fa-icon` function to create an icon with its name:

    `fa-icon("chess-queen")()` #fa-icon("chess-queen")()

    Or you can use the `fa-` prefix to create an icon with its name:

    `fa-chess-queen()` #fa-chess-queen()

    ==== Customization

    The `fa-icon` function is a curried `text`, so you can customize the icon by passing parameters to it:

    `#fa-icon("chess-queen")(fill: blue)` #fa-icon("chess-queen")(fill: blue)

    == Gallery

    TODO
    """

    doc_file = os.path.join(output, "example.typ")

    with open(doc_file, "w") as f:
        f.write(textwrap.dedent(DOC_TEMPLATE).format(version=version))


def main():
    args = parser.parse_args()

    if args.download > 0:
        download(args.version, args.output, args.download > 1)

    if "lib" in args.generate:
        generate_lib(args.version, args.output)

    if "doc" in args.generate:
        generate_doc(args.version, args.output)


if __name__ == "__main__":
    main()
