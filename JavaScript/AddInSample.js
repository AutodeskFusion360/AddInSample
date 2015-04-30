//Author-Autodesk Inc.
//Description-This is sample addin.

var commandIdOnQAT = 'demoCommandOnQATJS';
var commandIdOnPanel = 'demoCommandOnPanelJS';

var errorDescription = function(e) {
    return (e.description ? e.description : e);
};

var commandDefinitionById = function(id) {
    var app = adsk.core.Application.get();
    var ui = app.userInterface;
    if (!id) {
        ui.messageBox('commandDefinition id is not specified');
        return null;
    }
    var commandDefinitions_ = ui.commandDefinitions;
    var commandDefinition_ = commandDefinitions_.itemById(id);
    return commandDefinition_;
};

var commandControlByIdForQAT = function(id) {
    var app = adsk.core.Application.get();
    var ui = app.userInterface;
    if (!id) {
        ui.messageBox('commandControl id is not specified');
        return null;
    }
    var toolbars_ = ui.toolbars;
    var toolbarQAT_ = toolbars_.itemById('QAT');
    var toolbarControls_ = toolbarQAT_.controls;
    var toolbarControl_ = toolbarControls_.itemById(id);
    return toolbarControl_;
};

var commandControlByIdForPanel = function(id) {
    var app = adsk.core.Application.get();
    var ui = app.userInterface;
    if (!id) {
        ui.messageBox('commandControl id is not specified');
        return null;
    }
    var workspaces_ = ui.workspaces;
    var modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment');
    var toolbarPanels_ = modelingWorkspace_.toolbarPanels;
    var toolbarPanel_ = toolbarPanels_.item(0);
    var toolbarControls_ = toolbarPanel_.controls;
    var toolbarControl_ = toolbarControls_.itemById(id);
    return toolbarControl_;
};

var destroyObject = function(uiObj, tobeDeleteObj) {
    if (uiObj && tobeDeleteObj) {
        if (tobeDeleteObj.isValid) {
            tobeDeleteObj.deleteMe();
        } else {
            uiObj.messageBox('tobeDeleteObj is not a valid object');
        }
    }
};

function run(context) {

    "use strict";
    if (adsk.debug === true) {
        /*jslint debug: true*/
        debugger;
        /*jslint debug: false*/
    }

    var ui;
    try {
        var commandName = 'Demo';
        var commandDescription = 'Demo Command';
        var commandResources = './resources';
        
        var app = adsk.core.Application.get();
        ui = app.userInterface;

        var onInputChanged = function(args) {
            try
            {
                var command = adsk.core.Command(args.firingEvent.sender);
                ui.messageBox('Input: ' + command.parentCommandDefinition.id + ' changed event triggered');
            } catch (e) {
                ui.messageBox('Input changed event failed: ' + errorDescription(e));
            }
        };

        var onCommandExecuted = function(args) {
            try {
                var command = adsk.core.Command(args.firingEvent.sender);
                ui.messageBox('command: ' + command.parentCommandDefinition.id + ' executed successfully');

            } catch (e) {
                ui.messageBox('command executed failed: ' + errorDescription(e));
            }
        };

        var onCommandCreatedOnQAT = function(args) {
            try {
                var command = args.command;
                command.execute.add(onCommandExecuted);
                ui.messageBox('QAT command created successfully');

            } catch (e) {
                ui.messageBox('QAT command created failed: ' + errorDescription(e));
            }
        };

        var onCommandCreatedOnPanel = function(args) {
            try {
                var command = args.command;
                command.execute.add(onCommandExecuted);
                command.inputChanged.add(onInputChanged);

                var commandInputs_ = command.commandInputs;
                commandInputs_.addValueInput('valueInput_', 'Value', 'cm', adsk.core.ValueInput.createByString('0.0 cm'));
                commandInputs_.addBoolValueInput('boolvalueInput_', 'Checked', true);
                commandInputs_.addStringValueInput('stringValueInput_', 'String Value', 'Default value');
                commandInputs_.addSelectionInput('selectionInput', 'Selection', 'Select one');
                var dropDownCommandInput_ = commandInputs_.addDropDownCommandInput('dropdownCommandInput', 'Drop Down', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
                var dropDownItems_ = dropDownCommandInput_.listItems;
                dropDownItems_.add('ListItem 1', true);
                dropDownItems_.add('ListItem 2', false);
                dropDownItems_.add('ListItem 3', false);
                var multiSelectionCommandInput_ = commandInputs_.addMultiSelectCommandInput('multiSelectionCommandInput', 'Multi Selection');
                var multiSelectionCommandInputListItems_ = multiSelectionCommandInput_.listItems;
                multiSelectionCommandInputListItems_.add('ListItem 1', true);
                multiSelectionCommandInputListItems_.add('ListItem 2', true);
                multiSelectionCommandInputListItems_.add('ListItem 3', false);
                commandInputs_.addRangeCommandFloatInput('rangeCommandFloatInput', 'Range', 'cm', 0.0, 10.0, true);

                ui.messageBox('Panel command created successfully');

            } catch (e) {
                ui.messageBox('Panel command created failed: ' + errorDescription(e));
            }
        };

        var commandDefinitions_ = ui.commandDefinitions;

        // add a command button on Quick Access Toolbar
        var toolbars_ = ui.toolbars;
        var toolbarQAT_ = toolbars_.itemById('QAT');
        var toolbarControlsQAT_ = toolbarQAT_.controls;
        var toolbarControlQAT_ = toolbarControlsQAT_.itemById(commandIdOnQAT);
        if (!toolbarControlQAT_) {
            var commandDefinitionQAT_ = commandDefinitions_.itemById(commandIdOnQAT);
            if (!commandDefinitionQAT_) {
                commandDefinitionQAT_ = commandDefinitions_.addButtonDefinition(commandIdOnQAT, commandName, commandDescription, commandResources);
            }
            commandDefinitionQAT_.commandCreated.add(onCommandCreatedOnQAT);
            toolbarControlQAT_ = toolbarControlsQAT_.addCommand(commandDefinitionQAT_, commandIdOnQAT);
            toolbarControlQAT_.isVisible = true;
            ui.messageBox('A demo command button is successfully added to the Quick Access Toolbar');
        }

        // add a command on create panel in modeling workspace
        var workspaces_ = ui.workspaces;
        var modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment');
        var toolbarPanels_ = modelingWorkspace_.toolbarPanels;
        var toolbarPanel_ = toolbarPanels_.item(0); // add the new command under the first panel
        var toolbarControlsPanel_ = toolbarPanel_.controls;
        var toolbarControlPanel_ = toolbarControlsPanel_.itemById(commandIdOnPanel);
        if (!toolbarControlPanel_) {
            var commandDefinitionPanel_ = commandDefinitions_.itemById(commandIdOnPanel);
            if (!commandDefinitionPanel_) {
                commandDefinitionPanel_ = commandDefinitions_.addButtonDefinition(commandIdOnPanel, commandName, commandDescription, commandResources);
            }
            commandDefinitionPanel_.commandCreated.add(onCommandCreatedOnPanel);
            toolbarControlPanel_ = toolbarControlsPanel_.addCommand(commandDefinitionPanel_, commandIdOnPanel);
            toolbarControlPanel_.isVisible = true;
            ui.messageBox('A demo command is successfully added to the create panel in modeling workspace');
        }
    }
    catch (e) {
        if (ui) {
            ui.messageBox('AddIn Start Failed : ' + errorDescription(e));
        }
    }
}

function stop(context) {
    var ui;
    try {
        var app = adsk.core.Application.get();
        ui = app.userInterface;
        var objArrayQAT = [];
        var objArrayPanel = [];

        var commandControlQAT_ = commandControlByIdForQAT(commandIdOnQAT);
        if (commandControlQAT_) {
            objArrayQAT.push(commandControlQAT_);
        }
        var commandDefinitionQAT_ = commandDefinitionById(commandIdOnQAT);
        if (commandDefinitionQAT_) {
            objArrayQAT.push(commandDefinitionQAT_);
        }

        var commandControlPanel_ = commandControlByIdForPanel(commandIdOnPanel);
        if (commandControlPanel_) {
            objArrayPanel.push(commandControlPanel_);
        }
        var commandDefinitionPanel_ = commandDefinitionById(commandIdOnPanel);
        if (commandDefinitionPanel_) {
            objArrayPanel.push(commandDefinitionPanel_);
        }

        objArrayQAT.forEach(function(obj){
            destroyObject(ui, obj);
        });

        objArrayPanel.forEach(function(obj){
            destroyObject(ui, obj);
        });

    } catch (e) {
        if (ui) {
            ui.messageBox('AddIn Stop Failed : ' + errorDescription(e));
        }
    }
}