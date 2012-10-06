import codecs
import random
import math

output = codecs.open('test.svg', 'r', encoding='utf-8').read()

output = output.replace("WIND_DEGREES", str(random.randrange(0, 360)))

codecs.open('test-output.svg', 'w', encoding='utf-8').write(output)
