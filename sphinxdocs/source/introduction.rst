################################################################################
Introduction
################################################################################
********************************************************************************
Goal
********************************************************************************

The goal of the **tool** python package is to generate easily data :

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
    toolStep1 = toolstep.ToolstepModel(name = 'Toolstep1')
    toolStep2 = toolstep.ToolstepModel(name = 'Toolstep2')
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
    
The script tool_maker.py will import all the python modules needed by your script (tool, toolstep, tooth, FoR), and launch the scrip passed as argument.

********************************************************************************
Explanation of the general scrip above
********************************************************************************

The **tool** python package consist of tree python modules :
    * the ``tooth`` module where every tooth type is defined
    * the ``toolstep`` module manages the toolsteps of the tools.
    * the ``tool`` module allows to create the tools.

The **tool** module need an other module called **FoR** (short for "frame of reference") manages positioning of the teeth in the toolsteps or the toolsteps in the tools. 

--------------------------------------------------------------------------------
Object-oriented programming
--------------------------------------------------------------------------------

The **tool** pyhton package has been thought in *Object-oriented programming*. 

For example in the script above, ``toothInsert = tooth.Tooth_insert(…)`` create a new *object* that is an *instance* of the *class* ``Toot_insert`` defined in the module ``tooth``, and assign the variable ``toothInsert`` with the *object* newly created.

--------------------------------------------------------------------------------
Python classes defining different types of teeth
--------------------------------------------------------------------------------

The module ``tooth`` offers 5 Python classes to create teeth :
    * ``Tooth_insert``
    * ``Tooth_toroidal_mill``
    * ``Tooth_cylindrical_mill``
    * ``Tooth_ball_mill``
    * ``Tooth_sliced``

The class inheritance system well-known in Object-oriented programming, offers here 2 things : 
    * each ``Tooth_*`` class above have in common 2 *methodes* : 
        * ``my_tooth.draw()`` draw the tooth ``my_tooth`` in a 3D window.
        * ``my_tooth.torsion_transformation()`` applies a tortion transfomation to the tooth ``my_tooth``
    * every object that is an instance of a class ``Tooth_*`` can be added to a toolstep or a tool.