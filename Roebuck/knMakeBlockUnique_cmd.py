# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan




import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as G
import re


def RunCommand( is_interactive ):
    if sc.escape_test(False):
        print "script cancelled"

    print "Making unique..."


    objectIds = rs.GetObjects("Pick some blocks", 4096, preselect=True)
    if not objectIds:
        print "No objects"
        return False

    rs.EnableRedraw(False)

    blockTypes = {}
    for id in objectIds:
        blockName = rs.BlockInstanceName(id)
        if blockName not in blockTypes:
            blockTypes[blockName] = []
        blockTypes[blockName].append(id)



    blockNames = rs.BlockNames()

    finalObjs = []

    for blockType in blockTypes:
        for id in blockTypes[blockType]:
            blockXForm = rs.BlockInstanceXform(id)
            blockName = rs.BlockInstanceName(id)

            exObjs = rs.BlockObjects(blockName)


            strippedName = re.sub(r'

            x = 0
            tryAgain = True
            while tryAgain:
                x += 1
                newerBlockName = strippedName+"
                if newerBlockName not in blockNames:
                    tryAgain = False
                    break

            rs.AddBlock(exObjs, [0,0,0], newerBlockName, delete_input = True)
            newerBlock = rs.InsertBlock(newerBlockName, [0,0,0])

            rs.MatchObjectAttributes(newerBlock, id)

            rs.TransformObject(newerBlock, blockXForm)

            finalObjs.append(newerBlock)

        blockNames.append(newerBlockName)


    rs.DeleteObjects(objectIds)

    rs.SelectObjects(finalObjs)

    rs.EnableRedraw(True)

    print "...aaand its done."

    return 0

RunCommand(True)

