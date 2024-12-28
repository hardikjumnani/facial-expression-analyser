# initial json format of compliments.json
# {str, List[str]}

# final json format of compliments_formatted.json
# {str, List[List[str]]}
# all words of the compliments are split.
import json
from typing import Dict, List

with open('compliments.json', 'r') as compliments:
    data: Dict[str, List[str]] = json.load(compliments)

for emotion, compliments in data.items():
    for i, compliment in enumerate(compliments):
        data[emotion][i] = compliment.split(' ')

with open('compliments_formatted.json', 'w+') as compliments_formatted:
    json.dump(data, compliments_formatted, indent=4)