
# ----------------------------------------------------------------------------------------
from copy import deepcopy
from abc import abstractclassmethod

from .common import *

# ----------------------------------------------------------------------------------------
# SHARED Functions
# ----------------------------------------------------------------------------------------
def get_object(obj, file=None, conf_list=None, **kwargs):
	"""Pre-defined set of steps to get objects.  ( either input require file/conf_list ;  preferred conf_list )

	Args:
		obj (OBJS, ACLS, ROUTES,INSTANCES): various objects type
		file (str, optional): file name with path. Defaults to None.
		conf_list (list, optional): configuration content in list format. Defaults to None.

	Raises:
		Exception: MissingMandatoryInput

	Returns:
		object: object
	"""
	if file is not None:
		with open(file, 'r') as f:
			conf_list = f.readlines()
	objs = obj(conf_list, **kwargs)
	if conf_list: return objs
	raise Exception("MissingMandatoryInput(AtleastOneRequire {file/conf_list})")


# ----------------------------------------------------------------------------------------
# SHARED Classes
# ----------------------------------------------------------------------------------------
class Common():
	"""Commons properties/methods for Singular/Plural objects
	"""
	def __init__(self): self._repr_dic = {}
	def __iter__(self):
		for k, v in self._repr_dic.items():
			yield (k, v)
	def __getitem__(self, item): 
		return self._repr_dic[item]# if self._repr_dic.get(item) else None
	def __getattr__(self, attr): 
		try:
			return self[attr]
		except KeyError:
			raise AttributeError(attr)
	def __repr__(self): return f'{self.__class__.__name__}[{self._name}]'
	def keys(self): return self._repr_dic.keys()
	def values(self): return self._repr_dic.values()
	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result

# ----------------------------------------------------------------------------------------
class Plurals(Common):
	"""collection of objects 

	Args:
		Common (Common): Inherits Commons properties/methods for Singular/Plural objects
	"""
	def __repr__(self):
		setofobjs = ",\n".join(set(self._repr_dic.keys()))
		return f'{"-"*40}\n# Dict of {self.what} listed below:  #\n{"-"*40}\n{setofobjs}\n{"-"*40}'

	@abstractclassmethod
	def set_objects(cls): pass

	def changes(self, what, change):
		"""collate the recorded delta changes and provide delta for that change ( "ADDS", "REMOVALS" )

		Args:
			what (str): where to look for the change ('acl', 'object-group')
			change (str): type of change for which change output requested ( "ADDS", "REMOVALS" )

		Raises:
			Exception: INCORRECTCHANGE

		Returns:
			str: delta changes
		"""
		if change.upper() not in ("ADDS", "REMOVALS"): 
			raise Exception('INCORRECTCHANGE: Valid options are "ADDS/REMOVALS"')
		s = ''
		for name, obj in self:
			if not obj.__dict__[change.lower()]: continue
			s += heading(what, name, change)
			f = obj.add_str if change.lower() == 'adds' else obj.del_str
			s += f()
		return s	

# ----------------------------------------------------------------------------------------
class Singulars(Common):
	"""a single object

	Args:
		Common (Common): Inherits Commons properties/methods for Singular/Plural objects
	"""
	def __init__(self, name=''):
		super().__init__()
		self._name = name
	def __setitem__(self, key, value):  self._repr_dic[key] = value
	def __len__(self):  return len(self._repr_dic.keys())
	def __str__(self): return self.str()
	@abstractclassmethod
	def parse(cls): pass

# ----------------------------------------------------------------------------------------
