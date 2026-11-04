# Story and companion save state

All values use existing save slots. Save size and layout are unchanged.

| Flag | Meaning |
| --- | --- |
| B50 | New Bark introduction actors hidden/completed |
| B51 | Sister's explained Eevee acquisition |
| B52 | Sabrina partner victory at Slowpoke Well |
| B53 | Sabrina partner victory against Radio Tower Petrel |
| B54 | Optional Saffron student practice won |
| B55/B56/B57 | Violet/Ecruteak/Blackthorn optional sister battles won |
| B5D | Disable added sister story NPCs on the female player route |
| B5E | Companion status explicitly initialized |
| B5F | Sabrina joined |

The former unused daily-tail bits are now protected by ClearDailyFlags. B58-B5C
still reset with other native daily bits. See RTC-PERSISTENCE.md for legacy-save
compatibility and actual elapsed-day testing.

VAR 416F records introduction completion and repairs its hide flag for older saves.
VAR 416E transports the selected companion message to common script 2072. Neither
adds a save variable. Select conversations require standing on foot with Sabrina
present; native A interactions and original field controls retain priority.

Future event scripts can activate Sabrina with SetFlag B5E and SetFlag B5F, or
deactivate her with SetFlag B5E and ClearFlag B5F. Use the named constants in
include/constants/flags.h. The C API SabrinaCompanion_SetJoined does the same.
Initialization is kept set when disabled, preventing the legacy starter fallback
from undoing the choice. Joined status remains saved during Gym suppression,
cycling, surfing, cutscenes, ordinary battles and AI partner battles.

Sabrina is independent human object 252 (sprite 369, script FFFF). Native Pokemon
object 253 and its identity are preserved. Human positions are not serialized as
ordinary NPCs; one companion is safely recreated from the native Pokemon's fresh
walking trail after loading or leaving a suppressed action.
