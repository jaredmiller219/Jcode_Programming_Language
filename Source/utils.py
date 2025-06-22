from tokens import *

def string_with_arrows(text, position_start, position_end):
	result = ''

	# Calculate indices
	index_start = max(text.rfind('\n', 0, position_start.index), 0)
	index_end = text.find('\n', index_start + 1)
	if index_end < 0: index_end = len(text)

	# Generate each line
	line_count = position_end.line_number - position_start.line_number + 1
	for i in range(line_count):
		# Calculate line columns
		line = text[index_start:index_end]
		column_start = position_start.column if i == 0 else 0
		column_end = position_end.column if i == line_count - 1 else len(line) - 1

		# Append to result
		result += line + '\n'
		result += ' ' * column_start + '^' * (column_end - column_start)

		# Re-calculate indices
		index_start = index_end
		index_end = text.find('\n', index_start + 1)
		if index_end < 0: index_end = len(text)

	return result.replace('\t', '')

def suggest_keyword(identifier):
	# Simple suggestion: return the first keyword with distance 1
	for keyword in KEYWORDS:
		if len(identifier) == len(keyword) and sum(a != b for a, b in zip(identifier, keyword)) == 1:
			return keyword
	return None
