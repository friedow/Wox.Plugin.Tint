#encoding=utf8

import requests
import webbrowser
from wox import Wox,WoxAPI
import json
import os.path

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

    def query(self, key):
        self.initializeLibrary()

        results = []

        if key.startswith("add"):
            if key == "add":
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
            
            paletteName = key.lstrip("add ")
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
        
        elif key.startswith("palette"):
            # TODO: list colors and add new ones
            pass
        
        for palette in self.library['palettes']:
            results.append({
                "Title": palette['name'],
                "SubTitle": "",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method":"navigate",
                    "parameters": ["tint palette '" + palette['name'] + "'"],
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
        WoxAPI.change_query("tint palette '" + name + "'")

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Tint()
