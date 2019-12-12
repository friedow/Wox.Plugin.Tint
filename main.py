#encoding=utf8

import requests
import webbrowser
from wox import Wox,WoxAPI
import json
import os.path
import re
import sys
import subprocess
from PIL import Image, ImageDraw
from colour import Color

class Tint(Wox):

    def initializeLibrary(self):
        self.libraryPath = 'data.json'
        self.library = {}
        self.library['palettes'] = []

        if os.path.isfile(self.libraryPath):
            self.openLibrary()
        else:
            self.createLibrary()

    def createLibrary(self):
        self.library = {}
        self.library['palettes'] = []
        self.saveLibrary()
    
    def openLibrary(self):
        with open(self.libraryPath, 'r') as libraryFile:
            self.library = json.load(libraryFile)

    def saveLibrary(self):
        with open(self.libraryPath, 'w+') as libraryFile:
            json.dump(self.library, libraryFile)

    def context_menu(self, result):
        return [{
            "Title": "Name your new palette",
            "SubTitle": "Just start typing to name your new color palette!",
            "IcoPath": "Images/app.png",
            "JsonRPCAction": {
                "method":"",
                "parameters": "",
                "dontHideAfterAction": True
            }
        }]

    def query(self, key):
        self.initializeLibrary()

        results = []

        addingPaletteWithoutName = re.search('^add$', key)
        if addingPaletteWithoutName:
            results.append({
                "Title": "Name your new palette",
                "SubTitle": "Just start typing to name your new color palette!",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method":"navigate",
                    "parameters": ["tint add "],
                    "dontHideAfterAction": True
                }
            })
            return results
        
        addingPaletteWithName = re.search('^add (?P<paletteName>[a-zA-Z0-9]+)$', key)
        if addingPaletteWithName:
            paletteName = addingPaletteWithName.group('paletteName')
            results.append({
                "Title": "Create palette: " + paletteName,
                "SubTitle": "Creates a new color palette.",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method":"createPalette",
                    "parameters": [paletteName],
                    "dontHideAfterAction": True
                }
            })
            return results
        
        elif key.startswith("add "):
            results.append({
                "Title": "Invalid Palette Name",
                "SubTitle": "Please use only A-Z and 0-9 for palette names.",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method":"",
                    "parameters": "",
                    "dontHideAfterAction": True
                }
            })
            return results
        
        browsingPalettes = re.search('^palette (?P<paletteName>[a-zA-Z0-9]+)$', key)
        if browsingPalettes:
            paletteName = browsingPalettes.group('paletteName')
            palette = self.findPalette(paletteName)
            if palette:
                for color in palette['colors']:
                    previewImagePath = self.createColorPreviewImage(hexColor)
                    results.append({
                        "Title": color['hex'],
                        "SubTitle": "",
                        "IcoPath": previewImagePath,
                        "JsonRPCAction": {
                            "method":"copyToClipboard",
                            "parameters": [color['hex']],
                            "dontHideAfterAction": False
                        }
                    })
                results.append({
                    "Title": "Add color",
                    "SubTitle": "Adds a new color to the palette.",
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method":"navigate",
                        "parameters": ["tint palette " + paletteName + " add "],
                        "dontHideAfterAction": True
                    }
                })
                return results


        addingColor = re.search('^palette (?P<paletteName>[a-zA-Z0-9]+) add #?(?P<hexColor>([abcdefABCDEF0-9]{3}|[abcdefABCDEF0-9]{6}))$', key)
        if addingColor:
            paletteName = addingColor.group('paletteName')
            hexColor = '#' + addingColor.group('hexColor')
            previewImagePath = self.createColorPreviewImage(hexColor)
            results.append({
                "Title": "Add color: " + hexColor,
                "SubTitle": "Adds a new color to the selected palette.",
                "IcoPath": previewImagePath,
                "JsonRPCAction": {
                    "method":"addColor",
                    "parameters": [paletteName, hexColor],
                    "dontHideAfterAction": True
                }
            })
            return results
        
        elif re.search('^palette (?P<paletteName>[a-zA-Z0-9]+) add .+$', key):
            results.append({
                "Title": "Invalid Color Format",
                "SubTitle": "Please provide the color in hex format.",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method":"",
                    "parameters": "",
                    "dontHideAfterAction": True
                }
            })
            return results
            
        searchingPalette = re.search('^(palette )?(?P<paletteName>[a-zA-Z0-9]*)$', key)
        if searchingPalette:
            paletteName = searchingPalette.group('paletteName')
            palettes = self.findPalettes(paletteName)
            for palette in palettes:
                results.append({
                    "Title": palette['name'],
                    "SubTitle": "",
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method":"navigate",
                        "parameters": ["tint palette " + palette['name']],
                        "dontHideAfterAction": True
                    }
                })
            results.append({
                "Title": "Create color palette",
                "SubTitle": "Adds a new color palette to the library.",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method":"navigate",
                    "parameters": ["tint add "],
                    "dontHideAfterAction": True
                }
            })
            return results
    
    def navigate(self, command):
        WoxAPI.change_query(command)

    def createPalette(self, name):
        self.initializeLibrary()

        self.library['palettes'].append({
            "name": name,
            "colors": []
        })
        self.saveLibrary()
        WoxAPI.change_query("tint palette " + name)

    def findPalette(self, name):
        palettes = [palette for palette in self.library['palettes'] if palette['name'] == name]
        if len(palettes):
            return palettes[0]

    def findPalettes(self, name):
        return [palette for palette in self.library['palettes'] if palette['name'].lower().startswith(name.lower())]

    def addColor(self, paletteName, hexColor):
        self.initializeLibrary()

        palette = self.findPalette(paletteName)
        if palette:
            palette['colors'].append({
                'hex': hexColor
            })
            self.saveLibrary()
        WoxAPI.change_query("tint palette " + paletteName)

    def createColorPreviewImage(self, color):
        previewColor = Color(color)
        previewImage = Image.new('RGB', (100, 100), (int(previewColor.red * 255), int(previewColor.green * 255), int(previewColor.blue * 255)))
        previewImagePath = 'colors/' + color + '.jpg'
        previewImage.save(previewImagePath)
        return previewImagePath

    def copyToClipboard(self, text):
        subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(str.encode(text))

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Tint()
