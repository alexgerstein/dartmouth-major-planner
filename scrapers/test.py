import re

number = "14-334.4"
split = re.match('[0-9]*\.?([0-9]+$)?', number)
print split.group(0)