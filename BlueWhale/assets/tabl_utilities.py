


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