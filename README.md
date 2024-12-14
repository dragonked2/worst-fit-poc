# worst-fit-poc

This repo contains a PoC of exploiting Worst Fit (props to Orange Tsai and Splitline who presented this research at Black Hat EMEA 2024)

Exploitation payload example: `＂ --use-askpass=calc ＂` (uses the fullwidth quotation mark which worst fit converts to a normal double quote; however, at this point the built-in double quote escaping from `subprocess` won't trigger anymore)
