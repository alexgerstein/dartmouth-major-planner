import re

number = "334."
split = re.match('[0-9]*(\.[0-9]+$)?', number)
print split.group(0)