import re
pattern = r'(?<!\$)\\(sqrt|frac|times|div)(?:\{|\s)'
s = r"$\sqrt{12}$ = $\sqrt{4 \cdot 3}$ = $\sqrt{4} \cdot \sqrt{3}$ = $2$$\sqrt{3}$"
for m in re.finditer(pattern, s):
    print(m.start(), m.group(), repr(s[max(0, m.start()-5):m.end()+5]))
