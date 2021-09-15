from typing import List
import os
import json
import threading
import math
import unrealsdk
from unrealsdk import *
from ..ModMenu import EnabledSaveType, ModTypes, SDKMod, OptionManager, KeybindManager, RegisterMod, Game



WAYPOINT_CLASSES = ["WillowWaypoint"]
TRIGGER_CLASSES = [ "WillowTrigger"]
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
COLORS_SIZE = len(COLORS)



class VisualTriggers(SDKMod):
    Name = "Visual Triggers"
    Version = "1.0"
    SupportedGames = Game.BL2
    Types = ModTypes.Utility
    Description = "Visualizes trigger and waypoint zones with a key press."
    Author = "GameChanger97"
    #SaveEnabledState = EnabledSaveType.LoadWithSettings

    waypointsActive = False
    triggersActive = False


    def _show_waypoints(self) -> None:
        if self.waypointsActive == False:
            for waypoint_class in WAYPOINT_CLASSES:
                for color_index, trigger in enumerate(unrealsdk.FindAll(waypoint_class)):
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

                self.waypointsActive = True
        else:
            for waypoint_class in WAYPOINT_CLASSES:
                for trigger in unrealsdk.FindAll(waypoint_class):
                    trigger.FlushPersistentDebugLines()
            self.waypointsActive = False
            self.triggersActive = False

    def _show_triggers(self) -> None:
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

        else:
            for trigger_class in TRIGGER_CLASSES:
                for trigger in unrealsdk.FindAll(trigger_class):
                    trigger.FlushPersistentDebugLines()
            self.triggersActive = False
            self.waypointsActive = False

    def ResetBools(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) ->bool:
        for trigger_class in TRIGGER_CLASSES:
            for trigger in unrealsdk.FindAll(trigger_class):
                trigger.FlushPersistentDebugLines()
        return True

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

        VISUALIZE_WAYPOINTS: KeybindManager.Keybind = KeybindManager.Keybind(
            "Visualize Waypoints", "8", True, OnPress=self._show_waypoints
        )

        VISUALIZE_TRIGGERS: KeybindManager.Keybind = KeybindManager.Keybind(
            "Visualize Triggers", "9", True, OnPress=self._show_triggers
        )

        self.Keybinds = [VISUALIZE_TRIGGERS, VISUALIZE_WAYPOINTS]

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

def ResetHook(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) ->bool:
    VTInstance.ResetBools(caller, function, params)
    return True


INSTANCE: VisualTriggers = VisualTriggers()

RegisterMod(INSTANCE)
