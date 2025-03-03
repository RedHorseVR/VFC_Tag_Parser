# VFC_Tag_Parser
A generalized parser for any language code structured tagging with mapping for VFC tools usage 


#BASIC FUNCITON - WORK IN PROGRESS

The languages dir contians a set of _lang files that are used to do language specific parsing

The core parser is the VFCtagger.py - it uses the _lang file definitions to indents the code to show structured
It then applies a generalized tagging {tagA, tagB, tag X} to the code.
After that it uses the _lang file again to map the generalized tags into language specific structure using th VFC patterns
Finally - new work now - it generates a full VFC file from then tagged code.

#More information:

A VFTOOL -  to be open sourced soon - will enalbe full visualization and editing of the VFC code.
You might try the Java VFC_Viewer here to see what these look like

You may email me at luis.droid.phone@gmail.com if you would like to learn more and support this work.

 
