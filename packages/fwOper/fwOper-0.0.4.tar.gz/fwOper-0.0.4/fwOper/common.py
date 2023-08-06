
from .static import *

def heading(what, name, change):
	"""used to get the Banner heading

	Args:
		what (str): banner require for what? (valid options = acl, object-group)
		name (str): filter on valid options ( acl/object-group name )
		change (str): filter on change type ( valid options = adds, removals)

	Returns:
		str: banner for the provided requirements
	"""
	matter = f'! {change} - for the {what}: {name}\n'
	return LINE_SNG+matter+LINE_SNG