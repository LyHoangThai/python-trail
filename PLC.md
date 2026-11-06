# Interactive PLC learning lab

Open http://localhost:8765/learn and choose **PLC** in the subject dropdown. Its eight introductory lessons have separate **Ladder Logic** and **Structured Text** tabs. Python has its own five learning paths and separate progress counts. It uses virtual switches and a lamp; no PLC, wiring, industrial software license or connection to equipment is needed.

## Ladder Logic (lessons 46–49)

Build one lamp rung with up to four parallel paths and four series contacts per path:

- Choose SW1 or SW2 in the toolbox, then drag a contact to the new parallel path box.
- Drop another contact on a + gap to make a series path. Drag existing contacts to reorder them or move between paths.
- Drag the LAMP coil to the output box. An unconnected coil stays OFF and cannot pass a turn-in.
- Drag existing components to the bin to remove them. Undo/Redo restores diagram edits.
- For touch or keyboard, select a toolbox item or existing component, then tap a drop zone or press Enter.
- Choose normally open (NO, passes when its bit is true) or normally closed (NC, passes when its bit is false).
- Toggle the switches and watch contacts/path highlights and the lamp update immediately.
- Click a row in the switch-combination table to set that input combination.
- Use Run scan to check the current diagram through the worker, or Turn in assignment to check all four combinations and save a graded version.

Contacts on one path combine with AND. Parallel paths combine with OR and join before the one LAMP coil. A bare-wire path has no conditions and always passes; no paths or an unconnected coil means the output is OFF. Removing a path’s last contact removes that path. Contact symbols describe tests of BOOL bits, not the physical wiring of a switch.

## Structured Text (lessons 50–53)

Edit the program, toggle inputs and click Run scan. Alternatively, click Run case in the results table. Each scanned case records its lamp result in the table; changing the program clears those results. The lamp and output show the executed case. Editing source or changing inputs during a scan does not apply stale results to a different program/input state.

This teaching interpreter supports a deliberately small Boolean subset:

- Predefined BOOL inputs SW1 and SW2 and output LAMP.
- Assignment with `:=` and terminating `;`.
- TRUE/FALSE, AND, OR, NOT and parentheses.
- IF / THEN / ELSE / END_IF; blocks.
- Case-insensitive names/keywords, `//` line comments and `(* ... *)` comments.

Example:

```text
IF NOT SW1 THEN
    LAMP := TRUE;
ELSE
    LAMP := FALSE;
END_IF;
```

Each Run represents one fresh scan, with LAMP initially FALSE. The lab does not implement retained state, latches, timers, counters, numeric types, declarations, loops, functions, vendor libraries, I/O addresses or full IEC 61131-3 conformance. It is not an industrial PLC compiler/runtime or a hardware control system.

## Shared learning features

PLC lessons use the same Description/History tabs, saved drafts, turn-in IDs, result banners, completion tracking, parent review and source differences as Python lessons. The Helper changes to PLC-specific categories and examples. Worked solutions and saved ladder answers are shown as contact/path summaries in the student view.

Optional source files live in each matching lesson folder: assignment.ladder.json for diagrams, assignment.st for Structured Text, plus lesson.json and README.md. The browser is the main interactive environment. The Python Run command is not an ST or Ladder interpreter. Optional VS Code turn-in submits the saved source to the same simulator grader.

The grader tests every SW1/SW2 combination, so a constant ON or OFF answer cannot pass a switch-dependent assignment. ST lessons also require their named construct, such as AND, OR, or IF with NOT.

Concepts and syntax were checked against [CODESYS Ladder circuit documentation](https://content.helpme-codesys.com/en/CODESYS%204/_c4ld_connect_elements_to_a_circuit.html) and [CODESYS Structured Text IF documentation](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_st_instruction_if.html). The teaching examples and simulator are original; CODESYS is not required.
