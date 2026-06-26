# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan


def DataStoreToCSV(tabl):
    string = ""
    if tabl.settings.showHeaders:
        allHeadings = tabl.VisibleHeadingsList()
        for heading in allHeadings:
            string += str(heading) + ","
        string += "\n"

    allData = tabl.VisibleDataList()

    for row in allData:
        for item in row:
            if str(item) == "None":
                string += ","
            else:
                string += '"' + str(item) + '",'
        string += "\n"
    return string
