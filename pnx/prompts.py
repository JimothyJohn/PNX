CLASSIFY_PROMPT = """
If this image contains a cardboard box answer 'yes' otherwise reply with 'no'. Answer yes or no as quickly and shortly as possible, latency is a key so your response must be only yes or no. No explanation or additional detail, just that one word. The environment is supposed to be a warehouse where a yellow tunnel is visible  above a powered roller conveyor that should be empty.
"""

DETECT_PROMPT = """
Tell me the rough location of the center of the box in x and y where x is the location from 0 to 1 where the center is from top (0) to bottom (1) and y is the left to right. This is the schema of your response that I expect: {"x": 0.20, "y": 0.31, confidence_level: 0.41}. Do not elaborate or add any additional detail besides the basic output I just described.
"""
