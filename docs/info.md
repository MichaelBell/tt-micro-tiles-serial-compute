<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

A 16-bit shift register that is clocked in from ui_in[0].  The low and high byte can be output on uo_out.

Additionally the result of certain computations of the low and high byte of the shift register can be latched and displayed:

- When ui_in[4] is high the result of ADDing the low and high bytes of the shift regsiter is latched
- When ui_in[5] is high the result of ANDing the low and high bytes of the shift regsiter is latched

## How to test

Clock data in on ui_in[0].

ui_in[2:1] select the output, as follows

| ui_in[2:1] | Output |
| ---------- | ------ |
| 0          | Low byte of shift register |
| 1          | High byte of shift register |
| 2          | Latched ADD result |
| 3          | Latched AND result |

Finally, if rst_n is high the outputs mirror the inputs.  Reset is otherwise unused.
