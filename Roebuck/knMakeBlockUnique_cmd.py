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

"""
@name:          MakeUnique
@description:   Takes one or many blocks and creates a unique copy with own block definitions.
@version:       1.4
@link:          https://github.com/ejnaren/rhinotools
@notes:         Works with Rhino 5.








@Installation: Copy to the Rhino script folder. ie.: C:\Users\"USER"\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts
                Options to use the function:
                1. Recommended: Import the bundled "Block Tools" toolbar with readymade buttons to call the functions.
                2. Add a new button with the following macro: ( _NoEcho !-_RunPythonScript "MakeUnique.py" _Echo )
                3. Add an alias with the above command
                3. Call the script directly by using this command: "-RunPythonScript MakeUnique.py"

@Changelog:
    1.1: Make script into a command to be included in the BlockTools part of RhinoTools.
    1.2: Fix scaling bug and retain properties from the original block. lso simplifies the script a lot making it faster by removing a lot of redundant code. Must have been drunk when I wrote the first version...
    1.3: Unify version numbers and small redraw optimization.
    1.4: Fix bug where "bad objects" would break the script if present in blocks.
"""

#******* Imports ********************
#************************************

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as G
import re

#******* Main function ********************
#******************************************

def RunCommand( is_interactive ):
    if sc.escape_test(False):
        print "script cancelled" #do something

    print "Making unique..."

    #******* Get blocks *****************
    #************************************

    objectIds = rs.GetObjects("Pick some blocks", 4096, preselect=True)
    if not objectIds:
        print "No objects"
        return False

    #pause viewport redraw
    rs.EnableRedraw(False)

    #******* Sort blocks by type ********
    #************************************
    blockTypes = {}
    for id in objectIds:
        blockName = rs.BlockInstanceName(id)
        if blockName not in blockTypes:
            blockTypes[blockName] = []
        blockTypes[blockName].append(id)


    #***** Define new block and add *****
    #************************************

    #Get block names
    blockNames = rs.BlockNames()

    #gather all new objects when done
    finalObjs = []

    for blockType in blockTypes:
        for id in blockTypes[blockType]:
            #Get the block transformation matrix and name
            blockXForm = rs.BlockInstanceXform(id)
            blockName = rs.BlockInstanceName(id)

            #Get objects in the block            
            exObjs = rs.BlockObjects(blockName)

            #create new block name

            # if the string ends in digits m will be a Match object, or None otherwise.
            strippedName = re.sub(r'#[0-9]+$', '', blockName)

            #test if block name exist and add to the end number if true.
            x = 0
            tryAgain = True
            while tryAgain:
                x += 1
                newerBlockName = strippedName+"#"+str(x)
                if newerBlockName not in blockNames:
                    tryAgain = False
                    break

            #insert exObjs as new block
            rs.AddBlock(exObjs, [0,0,0], newerBlockName, delete_input = True)
            newerBlock = rs.InsertBlock(newerBlockName, [0,0,0])

            #match properties from original
            rs.MatchObjectAttributes(newerBlock, id)

            #transform new block
            rs.TransformObject(newerBlock, blockXForm)

            #append for final selection
            finalObjs.append(newerBlock)

        #add name to list of used blocknames.
        blockNames.append(newerBlockName)


    #Delete original block
    rs.DeleteObjects(objectIds)

    #Select all new objects
    rs.SelectObjects(finalObjs)

    rs.EnableRedraw(True)

    print "...aaand its done."
    #End RunCommand()

    #end sane
    return 0

RunCommand(True) #Run script

#END MakeUnique