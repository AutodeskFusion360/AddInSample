#Author-Autodesk Inc.
#Description-This is sample addin.

import adsk.core, adsk.fusion, traceback

commandIdOnQAT = 'demoCommandOnQAT'
commandIdOnPanel = 'demoCommandOnPanel'

# global set of event handlers to keep them referenced for the duration of the command
handlers = []

def commandDefinitionById(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandDefinition id is not specified')
        return None
    commandDefinitions_ = ui.commandDefinitions
    commandDefinition_ = commandDefinitions_.itemById(id)
    return commandDefinition_

def commandControlByIdForQAT(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandControl id is not specified')
        return None
    toolbars_ = ui.toolbars
    toolbarQAT_ = toolbars_.itemById('QAT')
    toolbarControls_ = toolbarQAT_.controls
    toolbarControl_ = toolbarControls_.itemById(id)
    return toolbarControl_

def commandControlByIdForPanel(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandControl id is not specified')
        return None
    workspaces_ = ui.workspaces
    modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment')
    toolbarPanels_ = modelingWorkspace_.toolbarPanels
    toolbarPanel_ = toolbarPanels_.item(0)
    toolbarControls_ = toolbarPanel_.controls
    toolbarControl_ = toolbarControls_.itemById(id)
    return toolbarControl_

def destroyObject(uiObj, tobeDeleteObj):
    if uiObj and tobeDeleteObj:
        if tobeDeleteObj.isValid:
            tobeDeleteObj.deleteMe()
        else:
            uiObj.messageBox('tobeDeleteObj is not a valid object')

def run(context):
    ui = None
    try:
        commandName = 'Demo'
        commandDescription = 'Demo Command'
        commandResources = './resources'

        app = adsk.core.Application.get()
        ui = app.userInterface

        class InputChangedHandler(adsk.core.InputChangedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.firingEvent.sender
                    ui.messageBox('Input: ' + command.parentCommandDefinition.id + ' changed event triggered')
                except:
                    if ui:
                        ui.messageBox('Input changed event failed:\n{}'.format(traceback.format_exc()))

        class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.firingEvent.sender
                    ui.messageBox('command: ' + command.parentCommandDefinition.id + ' executed successfully')
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'.format(traceback.format_exc()))

        class CommandCreatedEventHandlerPanel(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = CommandExecuteHandler()
                    cmd.execute.add(onExecute)

                    onInputChanged = InputChangedHandler()
                    cmd.inputChanged.add(onInputChanged)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    handlers.append(onInputChanged)

                    commandInputs_ = cmd.commandInputs
                    commandInputs_.addValueInput('valueInput_', 'Value', 'cm', adsk.core.ValueInput.createByString('0.0 cm'))
                    commandInputs_.addBoolValueInput('boolvalueInput_', 'Checked', True)
                    commandInputs_.addStringValueInput('stringValueInput_', 'String Value', 'Default value')
                    commandInputs_.addSelectionInput('selectionInput', 'Selection', 'Select one')
                    dropDownCommandInput_ = commandInputs_.addDropDownCommandInput('dropdownCommandInput', 'Drop Down', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
                    dropDownItems_ = dropDownCommandInput_.listItems
                    dropDownItems_.add('ListItem 1', True)
                    dropDownItems_.add('ListItem 2', False)
                    dropDownItems_.add('ListItem 3', False)
                    multiSelectionCommandInput_ = commandInputs_.addMultiSelectCommandInput('multiSelectionCommandInput', 'Multi Selection')
                    multiSelectionCommandInputListItems_ = multiSelectionCommandInput_.listItems
                    multiSelectionCommandInputListItems_.add('ListItem 1', True)
                    multiSelectionCommandInputListItems_.add('ListItem 2', True)
                    multiSelectionCommandInputListItems_.add('ListItem 3', False)
                    commandInputs_.addRangeCommandFloatInput('rangeCommandFloatInput', 'Range', 'cm', 0.0, 10.0, True)

                    ui.messageBox('Panel command created successfully')
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'.format(traceback.format_exc()))

        class CommandCreatedEventHandlerQAT(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.command
                    onExecute = CommandExecuteHandler()
                    command.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    ui.messageBox('QAT command created successfully')
                except:
                    ui.messageBox('QAT command created failed:\n{}'.format(traceback.format_exc()))

        commandDefinitions_ = ui.commandDefinitions

        # add a command button on Quick Access Toolbar
        toolbars_ = ui.toolbars
        toolbarQAT_ = toolbars_.itemById('QAT')
        toolbarControlsQAT_ = toolbarQAT_.controls
        toolbarControlQAT_ = toolbarControlsQAT_.itemById(commandIdOnQAT)
        if not toolbarControlQAT_:
            commandDefinitionQAT_ = commandDefinitions_.itemById(commandIdOnQAT)
            if not commandDefinitionQAT_:
                commandDefinitionQAT_ = commandDefinitions_.addButtonDefinition(commandIdOnQAT, commandName, commandDescription, commandResources)
            onCommandCreated = CommandCreatedEventHandlerQAT()
            commandDefinitionQAT_.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            toolbarControlQAT_ = toolbarControlsQAT_.addCommand(commandDefinitionQAT_, commandIdOnQAT)
            toolbarControlQAT_.isVisible = True
            ui.messageBox('A demo command button is successfully added to the Quick Access Toolbar')

        # add a command on create panel in modeling workspace
        workspaces_ = ui.workspaces
        modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment')
        toolbarPanels_ = modelingWorkspace_.toolbarPanels
        toolbarPanel_ = toolbarPanels_.item(0) # add the new command under the first panel
        toolbarControlsPanel_ = toolbarPanel_.controls
        toolbarControlPanel_ = toolbarControlsPanel_.itemById(commandIdOnPanel)
        if not toolbarControlPanel_:
            commandDefinitionPanel_ = commandDefinitions_.itemById(commandIdOnPanel)
            if not commandDefinitionPanel_:
                commandDefinitionPanel_ = commandDefinitions_.addButtonDefinition(commandIdOnPanel, commandName, commandDescription, commandResources)
            onCommandCreated = CommandCreatedEventHandlerPanel()
            commandDefinitionPanel_.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            toolbarControlPanel_ = toolbarControlsPanel_.addCommand(commandDefinitionPanel_, commandIdOnPanel)
            toolbarControlPanel_.isVisible = True
            ui.messageBox('A demo command is successfully added to the create panel in modeling workspace')

    except:
        if ui:
            ui.messageBox('AddIn Start Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        objArrayQAT = []
        objArrayPanel = []

        commandControlQAT_ = commandControlByIdForQAT(commandIdOnQAT)
        if commandControlQAT_:
            objArrayQAT.append(commandControlQAT_)

        commandDefinitionQAT_ = commandDefinitionById(commandIdOnQAT)
        if commandDefinitionQAT_:
            objArrayQAT.append(commandDefinitionQAT_)

        commandControlPanel_ = commandControlByIdForPanel(commandIdOnPanel)
        if commandControlPanel_:
            objArrayPanel.append(commandControlPanel_)

        commandDefinitionPanel_ = commandDefinitionById(commandIdOnPanel)
        if commandDefinitionPanel_:
            objArrayPanel.append(commandDefinitionPanel_)

        for obj in objArrayQAT:
            destroyObject(ui, obj)

        for obj in objArrayPanel:
            destroyObject(ui, obj)

    except:
        if ui:
            ui.messageBox('AddIn Stop Failed:\n{}'.format(traceback.format_exc()))
