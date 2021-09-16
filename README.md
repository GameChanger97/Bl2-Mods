# Bl2-Mods
A repository for my bl2 mods, currently just visual triggers but maybe I'll make more.
## [Visual Triggers](VisualTriggers/)
![Visual Triggers](https://github.com/GameChanger97/Bl2-Mods/blob/main/Borderlands%202%20(32-bit,%20DX9)%209_15_2021%204_17_58%20PM%20(2).png?raw=true)
Special thanks to ShadowEvil, Mopiod, Apple1417, FromDarkHell, and Juso for all the help with questions.  And an additional thanks to Juso for providing an early working proof of concept.
- Turn on skeletal outlines of triggers or waypoints with a keybind (default 8 and 9)

### Installation 
Like any python sdk mod, you will need the python sdk which can be downloaded [here](https://github.com/bl-sdk/PythonSDK).
Next simply click the Visual Triggers folder in this repo and download the zip file.  Then extract the folder into your mods folder which can be found at Steam\steamapps\common\Borderlands 2\Binaries\Win32\Mods

### Mod Options
- By default triggers are bound to 8 and waypoints are bound to 9, but feel free to rebind them to whatever you like.  They will appear in the keybind menu [here](https://imgur.com/a/HxIVmRU)
- The mods tab in options will also allow you to set the number of lines for the polygon representing the cylinder hitbox to have.  You can use the slider to set it anywhere from 6 to 50.  The more lines, the more accurate to the hitbox so I recommend setting it at or near the max unless you experience performance issues. [Here](https://imgur.com/a/00rg4Yi) is a picture of the menu.
- - [Here](https://imgur.com/a/QMP2kzu) is an example of a hitbox using the minimum 6 lines.
- - [Here](https://imgur.com/a/bhRm0Kp) is an example of the same hitbox using 50 lines.

### Known Issues
- Because of the way the clear function works, if you have both waypoints and triggers shown, turning one of them off by pressing the keybind again will turn both off.  Both get reset to a ready state though, so you can simply repress the key of the one you didn't want turned off.
- Unfortunately, leaving the game or switching maps with the the debug shapes still shown will not reset the keybind to its' ready state.  The side-effect of this is that you will need to press either keybind twice to show the cylinders.  The first time will reset the state and allow the mod to continue to work properly.

If anyone finds a solution to either issue, or finds any additional issues, feel free to let me know on discord at gamechanger97#4552

### Additional Info
##### Here I'm just going to post some examples and stuff I've learned during testing that may be useful for glitch hunters.
#### Gearbox Inconsistencies
The first thing I should mention is, gearbox never does the same thing the same way 100% of the time.  I'm sure a lot of you already know that.  There are some triggers/waypoints that don't have a set collision radius or height, sometimes they have neither.  For some of them, it is because they are likely unused.  For others, they work as intended but must use some other way to function.  Unfortunately, the only way to fix this would be to compile a list of all triggers that are not working properly, individually reference each case, and try to guestimate the true hitbox.  It is usually safe to assume that ones floating in the air probably extend to the ground. In order to allow triggers with a 0 radius or height to still render, I gave them each a minumum.  [Here](https://imgur.com/a/FJkkjm7) is an example of one with a 0 collision height. [Here](https://imgur.com/a/c8O4sX4) is an example of one with both 0 radius and 0 height... I'm sure you are wondering about that last part...

#### Boss Arenas
Boss arenas seem to have numberous small triggers in them.  I really haven't looked too much into if they are used or what they might do yet, but the bunker arena has by far the most I found.  [Example 1](https://imgur.com/a/TB4SmVs) [Example 2](https://imgur.com/a/19XX1Fr)  
You may have also noticed the floating green one in the clip of the 0 radius trigger, I am pretty sure it is just the defualt position for the waypoint associated with bunker.

#### Small trigger under the map
[Here](https://imgur.com/a/rZlqksJ) is an example at Bunker.  I've also seen them in Sanctuary before it is in the air and in 3 horns divide.  I assume it is some defualt that is in all maps, but I just figured I'd mention it.

#### Final Thoughts
Some of you may have seen earlier builds of this mod that used spheres.  The spheres were initially good for testing, but they fail to take height into consideration so the top and bottom of the spheres did not reflect the true hitbox. [Here](https://imgur.com/a/gsC0WD6) is an example of how the height is useful for precision.  You may find a waypoint on the map that doesn't correspond to any waypoints or triggers, it isn't very common but gearbox did do this a bit.  If you are curious what a debug cylinder corresponds to and can't find anything in any of the missions associated with it, I recommend opening blcmm and searching getall WillowTrigger in object explorer.  This will show you all the triggers and waypoints and if you can find the map, you can go through them looking for fields affiliated with missions or other in game actions.
