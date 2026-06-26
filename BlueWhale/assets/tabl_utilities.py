# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
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
                    string +=  '"' + str(item) + '",'
            string += "\n"
        return string