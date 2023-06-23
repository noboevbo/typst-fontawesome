# typst-fontawesome

A Typst library for Font Awesome icons through the desktop fonts.

## Usage

### Install the fonts

You can download the fonts from the official website: https://fontawesome.com/download

Or you can use the helper script to download the fonts and metadata:

`python helper.py -dd -v {version}`

Here `-dd` means to download and extract the zip file. You can use `-d` to only download the zip file.

After downloading the zip file, you can install the fonts depending on your OS.

### Install the library

Put the `fontawesome.typ` file in your project directory, and import it:

`#import "fontawesome.typ": *`

### Use the icons

You can use the `fa-icon` function to create an icon with its name:

`fa-icon("chess-queen")()`

Or you can use the `fa-` prefix to create an icon with its name:

`fa-chess-queen()`

#### Customization

The `fa-icon` function is a curried `text`, so you can customize the icon by passing parameters to it:

`#fa-icon("chess-queen")(fill: blue)`

## Example

See the `example.typ` file for a complete example. (TODO: add a gallery for all icons)

## Contribution

Feel free to open an issue or a pull request if you find any problems or have any suggestions.

### Python helper

The `helper.py` script is used to download fonts and generate typst code. I aim only to use standard python libraries, so running it on any platform with python installed should be easy.

## License

This library is licensed under the MIT license. Feel free to use it in your project.