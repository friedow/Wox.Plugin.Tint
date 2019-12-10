#encoding=utf8

import requests
import webbrowser
from wox import Wox,WoxAPI
import json
import os

class Tint(Wox):

    def __init__(self) {
        self.dataFilePath = 'data.json'

        if not os.path.exists(dataFilePath):
            self.data = {}
            self.data['palettes'] = []
            self.saveData()
        
        else:    
            with open(dataFilePath, 'r') as dataFile:
                self.data = json.load(dataFile)
    }

    def saveData():
        with open('data.txt', 'w+') as dataFile:
            json.dump(self.data, dataFile)

    def query(self, key):
        results = []
        results.append({
            "Title": "'" + key + "'",
            "SubTitle": "Key Debugger",
            "IcoPath": "Images/app.png",
            "JsonRPCAction": {
                "method":"navigate",
                "parameters": [""],
                "dontHideAfterAction": True
            }
        })

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
        
        results.append({
            "Title": "Create color palette",
            "SubTitle": "Adds a new color palette to the library.",
            "IcoPath": "Images/app.png",
            "JsonRPCAction": {
                "method":"navigate",
                "parameters": ["tint add "],
                "dontHideAfterAction":True
            }
        })

        return results
    
    def navigate(self, command):
        WoxAPI.change_query(command)

    def createPalette(self, name):
        # fsd
        pass

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Tint()
