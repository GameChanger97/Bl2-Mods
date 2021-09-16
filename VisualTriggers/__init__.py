from typing import List
import os
import json
import threading
import math
import unrealsdk
from unrealsdk import *
from ..ModMenu import EnabledSaveType, ModTypes, SDKMod, OptionManager, KeybindManager, RegisterMod, Game


#Storing triggers and waypoints
WAYPOINT_CLASSES = ["WillowWaypoint"]
TRIGGER_CLASSES = [ "WillowTrigger"]
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
COLORS_SIZE = len(COLORS)



class VisualTriggers(SDKMod):
    #Basic info
    Name = "Visual Triggers"
    Version = "1.0"
    SupportedGames = Game.BL2
    Types = ModTypes.Utility
    Description = "Visualizes trigger and waypoint zones with a key press."
    Author = "GameChanger97"

    #Feel free to uncomment the line below to auto-enable the mod on start up
    #SaveEnabledState = EnabledSaveType.LoadWithSettings

    waypointsActive = False
    triggersActive = False

    #turns on and off waypoints with a keypress by rendering or flushing debug cylinders for each waypoint object
    def _show_waypoints(self) -> None:
        #on
        if self.waypointsActive == False:
            for waypoint_class in WAYPOINT_CLASSES:
                for color_index, trigger in enumerate(unrealsdk.FindAll(waypoint_class)):
                    cylinder = trigger.CylinderComponent

                    if not cylinder:
                        continue

                    #Values for the debug cylinders
                    bounds = cylinder.Bounds
                    origin = bounds.Origin
                    extent = bounds.BoxExtent
                    radius = cylinder.CollisionRadius
                    height = cylinder.CollisionHeight

                    #setting min values for triggers gearbox left with 0 radius or height so they still render
                    if height == 0:
                        height = 25
                
                    #calculates the height of the cylinder in order to provide the debug cylinder with start and end vecotors
                    z1 = origin.Z - height
                    z2 = origin.Z + height

                    if radius == 0:
                        radius = 25

                    #rendering the debug cylinders
                    trigger.DrawDebugCylinder((origin.X, origin.Y, z1),
                                      (origin.X, origin.Y, z2),
                                      radius,
                                      self.NumOfLines.CurrentValue,
                                      *COLORS[color_index % COLORS_SIZE],
                                      True,
                                      1800)

                self.waypointsActive = True
        #off
        else:
            for waypoint_class in WAYPOINT_CLASSES:
                for trigger in unrealsdk.FindAll(waypoint_class):

                    #This function removes all debug lines so we have to reset both keybind booleans
                    trigger.FlushPersistentDebugLines()

            self.waypointsActive = False
            self.triggersActive = False

    #turns on and off triggers with a keypress by rendering or flushing debug cylinders for each waypoint object
    def _show_triggers(self) -> None:
        #on
        if self.triggersActive == False:
            for trigger_class in TRIGGER_CLASSES:
                for color_index, trigger in enumerate(unrealsdk.FindAll(trigger_class)):
                    cylinder = trigger.CylinderComponent
                    if not cylinder:
                        continue
                # optional bool bPersistentLines, optional float Lifetime);
                    bounds = cylinder.Bounds
                    origin = bounds.Origin
                    extent = bounds.BoxExtent
                    radius = cylinder.CollisionRadius
                    height = cylinder.CollisionHeight
                    if height == 0:
                        height = 25
                
                    z1 = origin.Z - height
                    z2 = origin.Z + height

                    if radius == 0:
                        radius = 25
                  
                    trigger.DrawDebugCylinder((origin.X, origin.Y, z1),
                                      (origin.X, origin.Y, z2),
                                      radius,
                                      self.NumOfLines.CurrentValue,
                                      *COLORS[color_index % COLORS_SIZE],
                                      True,
                                      1800)
                    
                self.triggersActive = True

        #off
        else:
            for trigger_class in TRIGGER_CLASSES:
                for trigger in unrealsdk.FindAll(trigger_class):
                    trigger.FlushPersistentDebugLines()
            self.triggersActive = False
            self.waypointsActive = False

    #Clear the cylinders for previous maps when you enter a new map
    def ClearCylinders(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) ->bool:
        for trigger_class in TRIGGER_CLASSES:
            for trigger in unrealsdk.FindAll(trigger_class):
                trigger.FlushPersistentDebugLines()
        return True

    #Option for how many lines to render with
    def __init__(self) -> None:

        self.NumOfLines = OptionManager.Options.Slider(
            Caption="Number of lines",
            Description="The number of lines you want to be used for drawing the debug cylinders",
            StartingValue=12,
            MinValue=6,
            MaxValue=50,
            Increment=1

        )

        self.Options = [
            self.NumOfLines
        ]

        #keybinds
        VISUALIZE_WAYPOINTS: KeybindManager.Keybind = KeybindManager.Keybind(
            "Visualize Waypoints", "8", True, OnPress=self._show_waypoints
        )

        VISUALIZE_TRIGGERS: KeybindManager.Keybind = KeybindManager.Keybind(
            "Visualize Triggers", "9", True, OnPress=self._show_triggers
        )

        self.Keybinds = [VISUALIZE_TRIGGERS, VISUALIZE_WAYPOINTS]

    #change the number of lines used to render the cylinders when the user updates the slider
    def ModOptionChanged(self, option: OptionManager.Options.Base, new_value) -> None:
        
        if option == self.NumOfLines:
            self.NumOfLines.CurrentValue = new_value

    def Enable(self) -> None:
        super().Enable()
        unrealsdk.RunHook("WillowGame.WillowPlayerController.WillowClientDisableLoadingMovie", "BoolResetter", ResetHook)

    def Disable(self) -> None:
        unrealsdk.RemoveHook("WillowGame.WillowPlayerController.WillowClientDisableLoadingMovie", "BoolResetter")
        super().Disable()


VTInstance = VisualTriggers()

#The hook passes through this before going to ClearCylinders
def ResetHook(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) ->bool:
    VTInstance.ClearCylinders(caller, function, params)
    return True


INSTANCE: VisualTriggers = VisualTriggers()

RegisterMod(INSTANCE)
