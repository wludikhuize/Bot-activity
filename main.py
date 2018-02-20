from data import dataCollection, returnAllValues
import config

name = config.name
pwd = config.pwd

name, type_, primary, secondary = returnAllValues()

dataCollection(name, pwd)

