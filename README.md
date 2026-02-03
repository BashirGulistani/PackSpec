# PackSpec

PackSpec turns messy “packaging spec” strings from supplier feeds into a clean schema:
case pack qty, inner pack qty, carton dimensions, carton weight, and a rough packaging type.


If you’ve ever worked with vendor catalogs, you know the situation:
- one supplier gives “24 pcs/ctn”
- another gives “Carton Qty: 24”
- some give dimensions like “18x12x10 in”
- others use “40*30*20 cm”
- weight might be in lb or kg
- sometimes it’s half missing, sometimes it’s all jammed into one sentence

PackSpec is meant to be an ETL helper: normalize the easy 70–90%, and surface the messy cases clearly.

---

## Install

```bash
pip install -e .
