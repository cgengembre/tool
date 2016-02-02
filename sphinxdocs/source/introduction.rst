################################################################################
Introduction
################################################################################
********************************************************************************
Goal
********************************************************************************

The goal of the *tool* python package is to generate easily data :

* which define a machining tool as a list of python dictionaries defined in <link>,
* usable as data input for nessy2m simulations.

********************************************************************************
Defining a machining tool
********************************************************************************

* A Tool is a set of Toolsteps
* A Toolstep is a set of Teeth
* A Tooth is a list of Elementary teeth 

********************************************************************************
General python script defining a machining tool
********************************************************************************

:: 

    # File Test_tool.py
    # Create the tool:
    myTool = tool.Tool(name = 'Name')
    # Create the toolsteps:
    toolStep1 = toolstep.ToolstepModel(name = 'Etage1')
    toolStep2 = toolstep.ToolstepModel(name = 'Etage2')
    # Create teeth:
    toothHelico = tooth.Tooth_toroidal_mill(…) 
    toothInsert = tooth.Tooth_insert(…)
    toothHelico.draw()
    # Put a tooth in a toolstep:
    # -- First create a frame to position a tooth in a toolstep
    # -- Then add the tooth
    frame1 = toolStep1.foref.create_frame(…)
    toolStep1.addTooth(toothHelico, frame1 )
    frame1 = toolStep1.foref.create_frame(…)
    toolStep1.addTooth(toothInsert, frame1 )
    …
    # Put a toolstep in the tool: 
    # -- First create a frame to position a toolstep in the tool
    # -- Then add the toolstep to the tool
    frame=myTool.foref.create_frame(…)
    myTool.addToolstep(toolStep1, frame)
    frame=myTool.foref.create_frame(…)
    myTool.addToolstep(toolStep2, frame)
    # Draw to control
    myTool.draw()
    # write the data that will be input to nessy2m
    myTool.write(’file_name’)

Every three dots (...) will be detailed below.

This script must be launched by an other one called tool_maker.py whose path must be added to your PATH.

So, to generate your tool, your must launch your scrip like this :

::
    
    [your prompt]$ tool_maker.py Test_tool.py
    
The script tool_maker.py will import all the python modules needed by your script (tool, toolpath, tooth, FoR), and launch the scrip passed as argument.
