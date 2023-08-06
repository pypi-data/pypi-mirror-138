## LOTR SDK

This SDK provides an easy way to integrate the API endpoints of The One API. More information about the API can be found here: https://the-one-api.dev/documentation

## Notice

This current version of the SDK does not currently support additional options like pagination, filtering, or sorting

## Usage

Download the sdk using pip

`pip install lotr-one`

Import the SDK client into your project

`from lotr-one import client`

Create a LOTR client and assign it to a variable

`lotr = LOTR()`

Start making calls

`lotr.get_book()`


## Supported Functions

Some routes on the API provide the ability to get second-level data. For example, all the chapters from a specific book. This second-level data can be accessed by passing `True` along with the ID of the requested record. The functions to which this applies are outlined below.

| Function | (Parameter=default) |
| ----------- | ----------- |
| get_book | (id=None, chapter=False) |
| get_movie() | (id=None, quote=False) |
| get_character | (id=None, quote=False)
| get_quote | (id=None, quote=False)
| get_character | (id=None)