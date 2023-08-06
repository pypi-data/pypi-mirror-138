
# ----------------------------------------------------------------------------------------
from nettoolkit import *
from collections import OrderedDict
from copy import deepcopy

from .member import *
from .entity import *
from .static import *
from .fwObj import *

# ----------------------------------------------------------------------------------------
# Local Functions
# ----------------------------------------------------------------------------------------

def _object_group_list(config_list):
	"""extracts obect groups from provided configuration list ie.config_list 
	returns object groups (OBJ)s in a list

	Args:
		config_list (list): full configuration list

	Returns:
		list: object-groups list
	"""
	obj_grp_list = []
	obj_group_started = False
	for line in config_list:
		spaces = STR.indention(line)
		if line.startswith("object-group"): 
			obj_group_started = True
			obj_grp_list.append(line.rstrip())
			continue
		if obj_group_started and spaces > 0:
			obj_grp_list.append(line.rstrip())
			continue
		if obj_group_started:
			break
	return obj_grp_list


def get_member_obj(member_type, member, objs):
	"""convert and provided string member to member object aka: Network, OBJ, Ports based on its member-type provided.
	objs: requires for recursive lookup for OBJ (if any)

	Args:
		member_type (str): type of member
		member (str): string repr of Network, OBJ, Ports etc
		objs (OBJS): collection of Object-groups (OBJS object)

	Raises:
		Exception: InvalidMemberType

	Returns:
		[Network, Ports, None]: Based on member type returns member object
	"""
	member_type_map = {
		'port-object': port_member,
		'network-object': network_member,
		'icmp-object': None,		# TBD
		'group-object': None,		# TBD
		'protocol-object': None,	# TBD
		# ... add more as need
	}
	if member_type not in member_type_map: 
		raise Exception(f"InvalidMemberTypeDefined-{member_type} for member-{member}")
	return member_type_map[member_type](member, objs)



# ----------------------------------------------------------------------------------------
# Collection of Object Group(s) objects
# ----------------------------------------------------------------------------------------
class OBJS(Plurals):
	"""collection of object groups

	Args:
		Plurals (Plurals): Inherits - group of items properties definitions
	"""
	def __init__(self, config_list):
		super().__init__()
		self.what = "object-groups"
		self.obj_grps_list = _object_group_list(config_list)
		self._set_obj_grp_basics()
		self.set_objects()

	def changes(self, change): 
		"""collate the delta changes recorded in all object-groups and provide delta for that change ( "ADDS", "REMOVALS")

		Args:
			change (str): type of change for which change output requested (  "ADDS", "REMOVALS" )

		Returns:
			str: delta changes
		"""
		return super().changes('object-group', change)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def get_matching_obj_grps(self, requests):
		"""matches provided (request members) in all object-groups available on device and 
		returns dictionary of object-group names, where object-group matches same members in it.

		Args:
			requests (tuple, list, set): list/set/tuple with members of dict, containing 
				'source', 'destination', 'ports' as keys.

		Raises:
			Exception: Invalid Request type

		Returns:
			dict: include all three, src, dest, port
		"""
		candidates = {'source': [], 'destination': [], 'ports': []}
		group_names = {}
		if not isinstance(requests, (tuple, list, set)):
			raise Exception(f"NotValidRequestProvided-{requests}")
		for request in requests:
			for loc, member in candidates.items():
				if request[loc] in ANY: continue
				member.append(request[loc])
		for loc, member in candidates.items():
			obj_grps_list = self.matching_obj_grps(member)
			if obj_grps_list:
				group_names[loc] = obj_grps_list
		return group_names

	def matching_obj_grps(self, member):
		"""matches provided [members] in all object-groups available on device and 
		returns list of object-group names, where object-group matches same members in it.

		Args:
			member (list, set, tuple): list/set/tuple with members

		Returns:
			list: singular object
		"""
		if isinstance(member, str):
			return [obj for name, obj in self if member in obj]
		elif isinstance(member, (tuple, list, set)):
			g = []
			for name, obj in self:
				match = False
				for m in member:
					match = m in obj
					if not match: break
				if match and len(obj) == len(member): g.append(obj)
			return g

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS ~~~~~~~~~~~~~~~~~~~

	def _set_obj_grp_basics(self):
		"""set basic information of each object-group.

		Returns:
			dict: representation dictionary of self.
		"""
		obj_grp_name = None
		for obj_grps_line in self.obj_grps_list:
			spaces = STR.indention(obj_grps_line)
			if spaces == 0:
				spl_obj_grps_line = obj_grps_line.split()
				obj_grp_type = spl_obj_grps_line[1]
				obj_grp_name = spl_obj_grps_line[2]
				if obj_grp_name not in self._repr_dic: self._repr_dic[obj_grp_name] = {}
				self._repr_dic[obj_grp_name]['type'] = obj_grp_type
				self._repr_dic[obj_grp_name]['candiates_list'] = []
				try:
					obj_grp_svc_filter = spl_obj_grps_line[3]
					self._repr_dic[obj_grp_name]['svc_filter'] = obj_grp_svc_filter
				except:
					self._repr_dic[obj_grp_name]['svc_filter'] = ""
			else:
				self._repr_dic[obj_grp_name]['candiates_list'].append(obj_grps_line)
		return self._repr_dic

	def set_objects(self):
		"""set extended information of each object-group.
		"""
		h = 0
		for obj_grp_name, obj_grp_details in self._repr_dic.items():
			obj_grp = OBJ(obj_grp_name, h)
			obj_grp.set_instance_primary_details(obj_grp_details)
			obj_grp.parent = self
			obj_grp.parse()
			self._repr_dic[obj_grp_name] = obj_grp
			h += 1

# ----------------------------------------------------------------------------------------
# Object Group Detail
# ----------------------------------------------------------------------------------------
class OBJ(Singulars):
	"""Individual group object

	Args:
		Singulars (Singulars): Inherits - individual object properties definitions

	Raises:
		Exception: IncorrectIteminItemType
		Exception: InvalidGroupMemberType
		Exception: NoValidCandidate

	Returns:
		OBJ: a single object-group object
	"""

	def __init__(self, obj_grp_name, _hash):
		"""Individual object-group object initialization

		Args:
			obj_grp_name (str): name of an object-group
			_hash (int): hashes for object-group
		"""
		super().__init__(obj_grp_name)
		self.name = obj_grp_name
		self.description = ""
		self.removals = {}
		self.adds = {}
		self._hash = _hash
	def __eq__(self, obj): 
		return (((self>obj) is None) 
			and ((obj>self) is None) 
			# and (self.description == obj.description)		# tantative
			)
	def __len__(self): return self._len_of_members()
	def __contains__(self, member): return self._contains(member)
	def __iadd__(self, n): 
		self._add(n)
		return self
	def __isub__(self, n): 
		self._delete(n)
		return self
	def __gt__(self, obj):
		diffs = self._missing(obj)
		obj_grp = self._blank_copy_of_self()
		obj_grp._repr_dic = diffs
		if diffs: return obj_grp
	def __lt__(self, obj):
		diffs = obj._missing(self)
		obj_grp = self._blank_copy_of_self()
		obj_grp._repr_dic = diffs
		if diffs: return obj_grp
	def __add__(self, attribs):
		newobj = deepcopy(self)
		newobj += attribs
		return newobj
	def __sub__(self, attribs): 
		newobj = deepcopy(self)
		newobj._delete(attribs)
		return newobj

	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~

	def str(self):
		"""String representation of full object-group

		Returns:
			str: object-group
		"""
		s = self._group_head()
		s += self._group_description()
		s += self._to_str(self._repr_dic, header=False)
		return s

	# object-group additions / removals
	def add(self, *arg): return self._add(*arg)
	def delete(self, *arg): return self._delete(*arg)

	# String representation of object-group additions / removals
	def add_str(self, header=True): return self._to_str(self.adds)
	def del_str(self, header=False): return self._to_str(self.removals)


	def over(self, acls):
		""" returns dictionary of acls with acl/line/attribute if object group present in any acls

		Args:
			acls (ACLS): dictionary of all acls (ACLS)

		Returns:
			dict: dictionary of acls with acl/line/attribute 
		"""
		d = {}
		for i, acl in acls:
			d.update(self._within(acl))
		return d

	def has(self, obj):
		"""returns object group if self contains provided object-group.

		Args:
			obj (OBJ): object-group object to check within

		Returns:
			(OBJ, None, False): object-group object if self within it else None
		"""
		if 'group-object' not in self.keys():
			return None
		for sgrp in self['group-object']:			
			if obj is self.parent[sgrp]:
				return self
			else:
				return self.parent[sgrp].has(obj)
		return False


	# ---------------- Operate on a Copy --------------- 	

	def _blank_copy_of_self(self):
		"""create and return a copy of original instance

		Returns:
			OBJ: copy of self
		"""
		obj_grp = OBJ(self._name, self._hash*1)
		obj_grp.set_instance_primary_details(self.grp_details)
		return obj_grp


	# ~~~~~~~~~~~~~~~~~~~ INTERNALS / SUPPORTIVE ~~~~~~~~~~~~~~~~~~~

	def _within(self, acl):
		"""if self object group is within an acl, provides line number and  attributes details 
		with matching object group name

		Args:
			acl (ACL): access-list object to check within

		Returns:
			dict: dictionary of acls with line/attributes for matching self.
		"""
		d = {}
		acl_name = acl.name
		for i, line in acl:
			for attr in GROUP_VALID_FIELDS:
				if isinstance(line, ACL_REMARK): continue
				if not isinstance(line[attr], OBJ): continue
				selfmatch = line[attr] is self
				parentmatch = line[attr].has(self)
				if not (selfmatch or parentmatch): continue
				if not d.get(acl_name): d[acl_name] = {}
				if not d[acl_name].get(i): d[acl_name][i] = {}
				d[acl_name][i][attr] = self if selfmatch else parentmatch
		return d

	def _len_of_members(self):
		"""supporting len() : count of total members

		Returns:
			int: count of total members
		"""
		l = 0
		for v in self._repr_dic.values():
			l += len(v)
		return l

	def _contains(self, member):
		"""supporting - [x in, not in instance]:

		Args:
			member (str, int, list, set, tuple, Network, Ports): member(s) to check in self

		Returns:
			Bool: boolean return if matches member in self.
		"""
		if isinstance(member, (str, int, Network, Ports)):
			member_type = self._get_member_type(member)
			member_obj = get_member_obj(member_type, member, self.parent)
			if not self._repr_dic.get(member_type): return None
			for _ in self[member_type]:
				if isinstance(_, OBJ) and _._contains(member):
					return _
				else: pass
				if member_obj == _:  return _
		elif isinstance(member, (list,set,tuple)):
			for m in member:
				if m not in self: return False
			return True
		else:
			# print(type(member))
			return None

	def _add(self, item):
		"""supporting inst.add(member) : method for setting key/value for instance

		Args:
			item (str, int, list, set, tuple): item/attribute to be added to object-group

		Raises:
			Exception: IncorrectIteminItemType

		Returns:
			str: Delta of addition
		"""
		if isinstance(item, (tuple, set, list)):
			s = ''
			for _ in item:  
				s += self._add(_)
			return s
		elif isinstance(item, (str, int)):
			item_type = self._get_member_type(item)
			updated_item = self._get_item_object(item_type, item)
			return self._obj_add(item_type, updated_item)
		else:
			item_type = self._get_member_type(item)
			raise Exception(f"IncorrectIteminItemType-{item_type}/{item}")

	def _delete(self, item):
		"""supporting inst.delete(member) : method for removing key/value for instance

		Args:
			item (str, int, list, set, tuple): item/attribute to be removed from object-group

		Raises:
			Exception: IncorrectIteminItemType

		Returns:
			str: Delta of deletion
		"""
		if isinstance(item, (tuple, set, list)):
			s = ''
			for _ in item: 
				s += str(self._delete(_))
			return s
		elif isinstance(item, (str, int)):
			item_type = self._get_member_type(item)
			updated_item = self._get_item_object(item_type, item)
			return self._obj_delete(item_type, updated_item)
		else:
			item_type = self._get_member_type(item)
			raise Exception(f"IncorrectIteminItemType-{item_type}/{item}")

	def _missing(self, obj):
		"""supporting in comparision between to instances (a > b, a < b):
		compare and return differences in dictionary.

		Args:
			obj (OBJ): another object of an object-group to match with

		Returns:
			dict: differences dictionary
		"""
		diffs = {}
		if not isinstance(obj, OBJ): return self
		t = self.obj_grp_type == obj.obj_grp_type
		s = self.obj_grp_svc_filter == obj.obj_grp_svc_filter
		if not t or not s:
			return diffs

		for self_k, self_v in self._repr_dic.items():
			if not obj._repr_dic.get(self_k):
				obj._repr_dic[self_k] = None
			obj_v = obj[self_k]
			if obj_v is None:
				diffs[self_k] = self_v
			else:
				found = self_v == obj_v
				if found: continue
				diffs[self_k] = self_v.difference(obj_v)
		return diffs

	# ----------------- String repr / supportive --------------- #

	def _group_head(self):
		"""return String representation of object-group header/name line

		Returns:
			str: object-group header/name
		"""
		return (f"object-group {self.obj_grp_type} {self._name} {self.obj_grp_svc_filter}\n")

	def _group_description(self):
		"""return String representation of object-group description line

		Returns:
			str: object-group description
		"""
		return (f" description {self.description}\n")

	def _to_str(self, dic, header=True):
		"""return String representation of object-group ( add/remove actions )

		Args:
			dic (dict): Delta dictionary generated during add/remove action
			header (bool, optional): add header line or not. Defaults to True

		Returns:
			str: object-group
		"""
		s = self._group_head() if header else ""		
		m = ''
		negate = 'no ' if dic is self.removals else ''
		for _type, candidates in dic.items():
			for c in candidates:
				# _c = self._get_candidate_str(c)
				m += f" {negate}{_type} {c}\n"
		s += m
		return s if m else m


	## ----------- Other Supportive to Supportives --------- ##

	def _get_candidate_str(self, c):
		"""supporting method to get the OBJ object name

		Args:
			c (OBJ): object-group object

		Returns:
			str: object-group name
		"""
		return c.name if isinstance(c, OBJ) else c

	def _get_item_object(self, item_type, item):
		"""supporting method for retriving member-type/member pair for for a member

		Args:
			item_type (str): string of item type
			item (str): string of item

		Returns:
			various: item object( Network, Ports, etc. )
		"""
		spl_line = [item_type]
		spl_line.extend(item.split())
		updated_item = self._get_member(item_type, spl_line)
		return updated_item

	def _get_member(self, obj_type, spl_line):
		"""supporting method for retriving member object for provided object-type 

		Args:
			obj_type (str): string of item type
			spl_line (list): object group member splitted line

		Raises:
			Exception: InvalidGroupMemberType

		Returns:
			various: item object( Network, Ports, etc. )
		"""
		if obj_type == 'network-object':
			member = network_group_member(spl_line, 1, self.parent)
		elif obj_type == 'port-object':
			member = port_group_member(spl_line, 1, self.parent)
		elif obj_type == 'icmp-object':
			member = icmp_group_member(spl_line)
		elif obj_type == 'protocol-object':
			member = protocol_group_member(spl_line)
		elif obj_type == 'group-object':
			member = group_object_member(spl_line, self.parent)
		else:
			raise Exception(f"InvalidGroupMemberType-Noticed-[{obj_type}]\n{spl_line}")
		return member

	def _obj_add(self, item_type, item):
		"""supporting method for setting key/value for instance

		Args:
			item_type (str): string of item type
			item (str): item object( Network, Ports, etc. )

		Returns:
			str: string of delta changes for item addition
		"""
		if not self.adds.get(item_type): self.adds[item_type] = set()
		if not self._repr_dic.get(item_type): self._repr_dic[item_type] = set()
		self._repr_dic[item_type].add(item)
		self.adds[item_type].add(item)
		return f" {item_type} {item}\n"

	# supporting method for removing key/value for instance
	def _obj_delete(self, item_type, item):
		"""	# supporting method for removing key/value for instance

		Args:
			item_type (str): string of item type
			item (str): item object( Network, Ports, etc. )

		Raises:
			Exception: NoValidCandidate

		Returns:
			str: string of delta changes for item deletion
		"""
		if not self.removals.get(item_type): self.removals[item_type] = set()
		try:
			self._repr_dic[item_type].remove(item)
			self.removals[item_type].add(item)
			if len(self._repr_dic[item_type]) == 0:
				del(self._repr_dic[item_type])
			return f" no {item_type} {item}\n"
		except:
			print(f"NoValidCandidateFoundToRemove/OrAlreadyRemoved-\n{item_type}: {item}")			

	def _get_member_type(self, member):
		"""dynamic detection of member-type for given member

		Args:
			member (str): string representation of member

		Raises:
			Exception: InvalidMember

		Returns:
			str: string representation of member-type for provided member
		"""
		for k, v in MEMBERS_MEMBERTYPES.items():
			if member in k: return v
		try:
			network_member(member, self.parent)
			return 'network-object'
		except:
			pass
		try:
			port_member(member, self.parent)
			return 'port-object'
		except:
			pass
		if isinstance(member, str) and member in self.parent:
			return 'group-object'
		raise Exception(f"InvalidMemberFound:{member}, unable to generate member type for it.")



	# ~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~~
	# USED WHILE INITIATLIZING / PARSER
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def set_instance_primary_details(self, obj_grp_details):
		"""set primary variable details of instance

		Args:
			obj_grp_details (dict): object-group primary/basic details (candidates-list, type, service-filter)
		"""
		self.obj_grp_lines_list = obj_grp_details['candiates_list']
		self.obj_grp_type = obj_grp_details['type']
		self.obj_grp_svc_filter = obj_grp_details['svc_filter']

	def parse(self):
		"""starts parsing object-group-config-lines-list and set extended variables of instance
		"""
		for line in self.obj_grp_lines_list:
			spl_line = line.lstrip().split()
			sub_obj_type = spl_line[0]
			if sub_obj_type == 'description':
				self.description = line[13:]
				continue
			member = self._get_member(spl_line[0], spl_line)
			if not self._repr_dic.get(spl_line[0]): 
				self._repr_dic[spl_line[0]] = set()
			member = self._get_candidate_str(member)
			self._repr_dic[spl_line[0]].add(member)

	# ~~~~~~~~~~~~~~~~~~~ PROPERTIES ~~~~~~~~~~~~~~~~~~~

	@property
	def grp_details(self):
		"""object group details in dictionary (helpful in generating copy)

		Returns:
			dict: object-group primary/basic details
		"""
		_grp_details = {
			'type': self.obj_grp_type,
			'svc_filter': self.obj_grp_svc_filter,
			'candiates_list': [],
		}
		return _grp_details
	


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
