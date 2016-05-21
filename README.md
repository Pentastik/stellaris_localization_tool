
# Stellaris Localization Parser & Browser

Hello!

This is a simple parser for stellaris.

Please just see source code in stellaris.py.

There is some method to help your work.

I will not explain source code, sorry!


## Prerequisities

* python 2.7+ [download](https://www.python.org/downloads/)
* pymongo (python mongodb client library)

### (optionals for work with mongodb & browser)

* mongodb 3.2+ [download](https://www.mongodb.com/download-center?jmp=nav#community)
* restheart 2.0+ [download](https://github.com/SoftInstigate/RESTHeart/releases) (provide rest interface of mongodb)
* **restheart-20000.jar** (included in files folder)


# Installation & Usage

### simple
  - setup python & pymongo
  - run main.py

### mongos
  1. setup mongodb with default configuration
  2. setup restheart
  3. replace restheart.jar with restheart-2000.jar (because default jar limited fetch size to 1000)
  4. run mongodb & restheart

### browser
  1. open browser/browser.html
  2. change HOST, CHECKSUM value in javascript
  3. open browser.html


# Build Font

* bmfont [download](http://www.angelcode.com/products/bmfont/)
* bmfont configuration for Korean [stellaris_font_setup.bmfc](files/stellaris_font_setup.bmfc)
* DO NOT INCLUDE LF(10), RF(13) IN CHARACTER RANGE

## Font information

check [ods file sheet](files/some_localization_info.ods)


# Other Links

* [Korean Translation Community](http://cafe.daum.net/Europa)
* [Korean Translation Workspace](http://team-waldo.xyz/zanata/project/view/StellarisKR)
* [Japanese Translation Workspace](https://docs.google.com/spreadsheets/d/1k1kwkF45TMvxDZZguuSaVME0lYwNPGLMkjjjUwU3BC8/edit#gid=0)


# License

* [LICENSE.md](LICENSE.md)


# Screenshots

![run main.py](https://github.com/Pentastik/stellaris_localization_tool/raw/master/files/output-example.PNG)

![browser](https://github.com/Pentastik/stellaris_localization_tool/raw/master/files/browser-example.PNG)
