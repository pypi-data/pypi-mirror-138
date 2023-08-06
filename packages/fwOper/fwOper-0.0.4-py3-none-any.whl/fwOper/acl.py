
# ----------------------------------------------------------------------------------------
from nettoolkit import *
from collections import OrderedDict
from copy import deepcopy

from .acg import OBJ
from .member import *
from .entity import *
from .static import *
from .fwObj import *

# ----------------------------------------------------------------------------------------
# Local Functions
# ----------------------------------------------------------------------------------------

def access_list_list(config_list):
	"""extracts access-lists from provided configuration list ie.config_list.

	Args:
		config_list (list): configuration list

	Returns:
		list: access-lists lines in a list
	"""
	return [line.rstrip() for line in config_list if line.startswith("access-list ")]


def update_obj_grp_str(item, what):
	"""update the object group and host string in acl

	Args:
		item (dict): acl line item
		what (str): acl line attribte name ('source', 'destination', 'ports', 'protocol')

	Returns:
		str: string represenation of object group or host object in acl
	"""
	if isinstance(item[what], OBJ):
		return 'object-group ' + item[what].name
	if isinstance(item[what], Network) and item[what].host:
		return 'host ' +  item[what].network
	else:
		return item[what]


def dummy_group(source_grp, item, values):
	"""create a dummy object-group with provided items, by taking template as source group

	Args:
		source_grp (OBJ): source group (will be a template to create new dummy group)
		item (str): acl line attribte name ('source', 'destination', 'ports', 'protocol')
		values (str, set, tuple, list): set of value(s)

	Returns:
		OBJ: object-group object with provided item: values
	"""
	v = values if isinstance(values, (set, tuple, list)) else {values,}
	dg = OBJ('temporary', 1)
	if item in ('protocol',):rdk = 'protocol-object'
	if item in ('ports',):rdk = 'port-object'
	if item in ('source', 'destination'): rdk = 'network-object'
	ogd = {}
	ogd['candiates_list'] = ''
	ogd['type'] = source_grp.obj_grp_type
	ogd['svc_filter'] = source_grp.obj_grp_svc_filter
	dg.set_instance_primary_details(ogd)
	dg._repr_dic[rdk] = v
	return dg

# ----------------------------------------------------------------------------------------
# Access Lists Entries
# ----------------------------------------------------------------------------------------

class ACLS(Plurals):
	"""collection of ACL objects

	Args:
		Plurals (Plurals): Inherits - group of items properties definitions
	"""

	def __init__(self, config_list, objs=None):
		super().__init__()
		self.what = "access-lists"
		self.acls_list = access_list_list(config_list)
		self.set_acl_names()
		self.set_objects(objs)

	def changes(self, change): 
		"""collate the delta changes recorded in all access-lists and provide delta for that change ( "ADDS", "REMOVALS")

		Args:
			change (str): type of change for which change output requested (  "ADDS", "REMOVALS" )

		Returns:
			str: delta changes
		"""
		return super().changes('acl', change)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def set_acl_names(self):
		"""sets available access-lists names in _repr_dic (key)

		Returns:
			dict: _repr_dict
		"""
		for acl_line in self.acls_list:
			spl_acl_line = acl_line.split()
			acl_name = spl_acl_line[1]
			if acl_name not in self._repr_dic: self._repr_dic[acl_name] = []
			self._repr_dic[acl_name].append(acl_line)
		return self._repr_dic

	def set_objects(self, objs):
		"""sets access-lists (ACL)s in _repr_dic (value)

		Args:
			objs (OBJS): object of dictionary of object-groups
		"""
		for acl_name, acl_lines_list in self._repr_dic.items():
			acl =  ACL(acl_name, acl_lines_list, objs)
			acl.parse(objs)
			self._repr_dic[acl_name] = acl

# ----------------------------------------------------------------------------------------
# Access List detail
# ----------------------------------------------------------------------------------------

class ACL(Singulars):
	"""Individual access-list object

	Args:
		Singulars (Singulars): Inherits - individual object properties definitions

	Raises:
		Exception: MissingMandatoryParameter
		Exception: exact match process error

	Returns:
		ACL: a single access-list object

	Yields:
		tuple: tuple of (line-number, line-attributes) 
	"""

	end_point_identifiers_pos = {	# static index points 
		0: 5,						# src
		1: 7,						# dst
		2: 9,						# port
	}
	mandatory_item_values_for_str = ('acl_type', 'action', 'protocol',
		'source', 'destination', 'ports', 'log_warning' )

	def __init__(self, acl_name, acl_lines_list, objs):
		super().__init__(acl_name)
		self.name = acl_name
		self.acl_lines_list = acl_lines_list
		self.objs = objs
		self.adds = ''
		self.removals = ''
		self._sequence = False
		self._repr_dic = OrderedDict()
	@property
	def max(self): return max(self._repr_dic.keys())
	@property
	def min(self): return min(self._repr_dic.keys())
	@property 	             ## Boolean: sequence number visibility
	def sequence(self): return self._sequence
	@sequence.setter
	def sequence(self, seq): self._sequence = seq
	def __iter__(self):
		for k, v in sorted(self._repr_dic.items()):
			yield (k, v)
	def __getitem__(self, item):
		if isinstance(item, slice):
			return ''.join([self[i] for i in range(*item.indices(len(self)))])
		else:
			try:
				return self._to_str(item)
			except KeyError:
				return None
	def __delitem__(self, item): self.delete(item)
	def __add__(self, attribs):  return self.copy_and_append(attribs)
	def __sub__(self, n): return self.copy_and_delete(n)
	def __iadd__(self, attribs): 
		self.append(attribs)
		return self
	def __isub__(self, n): 
		self.delete(n)
		return self
	def __eq__(self, obj): return self._is_equal(obj)
	def __gt__(self, obj): return self._compare(obj)
	def __lt__(self, obj): return obj._compare(self)
	def __contains__(self, item): return self.contains(item)
		
	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~

	def str(self):
		"""String representation of full acl

		Returns:
			str: full acl
		"""
		s = ''
		for k, v in self:
			s += self[k]
		return s

	def add_str(self): 
		"""String representation of acl recoded additions

		Returns:
			str: recorded acl changes (adds)
		"""
		return str(self.adds)
	def del_str(self): 
		"""String representation of acl recoded deletions

		Returns:
			str: recorded acl changes (removals)
		"""
		return str(self.removals)

	# //////// OPERATIONS /////////

	def delete(self, attribs, stop=None, step=1): 
		"""delete a line in acl:  can be use with standard delete command as well,
		del(acl_name[n])

		Args:
			attribs (int, dict): int->deletes an entry by line number, dict->delete entry which matches attribute
			stop (int, optional): to delete a range of lines provide end sequence. Defaults to None.
			step (int, optional): to delete line numbers in multiple of. Defaults to 1.

		Returns:
			str: delta change(s) for the deletion of entry
		"""
		if isinstance(attribs, int):
			if stop and isinstance(stop, int):
				s = ''
				for i in reversed(range(attribs, stop, step)):
					s += self.delete(i)
				return s
			else:
				return self._delete_by_line(attribs)
		elif isinstance(attribs, dict):
			return self._delete_by_attribs(attribs)
		elif isinstance(attribs, slice):
			for i in reversed(range(*attribs.indices(len(self)))):
				self.delete(i)
		else:
			print(f"Incorrect input to delete {attribs}")
			return None

	def insert(self, line_no, attribs):
		"""insert a line in acl:  can be use with standard way as well,
		aclname[line_no] = attribs
		display warning message - MatchingEntryAlreadyexistAtLine, if a match already exist in acl

		Args:
			line_no (int): line number at which entry to be inserted
			attribs (dict): line attributes

		Returns:
			str: delta change(s) for the insertion of entry
		"""
		mv = self.contains(attribs)
		if not mv:
			self._key_extend(line_no)
			return self._add(line_no, attribs)
		else:
			print(f"MatchingEntryAlreadyexistAtLine-{mv}")

	def append(self, attribs):
		"""append a line to acl
		display warning message - MatchingEntryAlreadyexistAtLine, if a match already exist in acl

		Args:
			attribs (dict): line attributes

		Returns:
			str: delta change(s) for the append of entry
		"""
		mv = self.contains(attribs)
		if not mv:
			return self._add(self.max+1, attribs)
		else:
			print(f"MatchingEntryAlreadyexistAtLine-{mv}")

	def contains(self, item):
		"""check matching attributes in acl object, and return set of matching 
		acl line numbers for containing item (sparse match)

		Args:
			item (dict): line attributes

		Returns:
			set: set of matching acl line numbers (sparse match)
		"""
		matching_lines = set()
		item = self._update_group_members(item)
		for line_no, acl_details in  self:
			if isinstance(acl_details, dict):
				for item_k, item_v in item.items():
					if item_k == 'log_warning': continue
					if isinstance(acl_details[item_k], OBJ):
						if item_v not in acl_details[item_k]: break
						continue
					if item_v != acl_details[item_k]: break
				else:
					matching_lines.add(line_no)
		return matching_lines

	def exact(self, item):
		"""check matching attributes in acl object, and return set of matching 
		acl line numbers for exact matches item only

		Args:
			item (dict): line attributes

		Raises:
			Exception: exact match process error

		Returns:
			set: set of matching acl line numbers (exact match)
		"""
		matching_lines = set()
		item = self._update_group_members(item)
		for line_no, acl_details in  self:
			if isinstance(acl_details, dict):
				for item_k, item_v in item.items():
					if item_k == 'log_warning': continue
					if isinstance(acl_details[item_k], OBJ):
						dg_rdk = dummy_group(acl_details[item_k], item_k, item_v)
						try:
							if dg_rdk != acl_details[item_k]: 
								break
						except:
							raise Exception("exact match process error..")
						continue
					if item_v != acl_details[item_k]: break
				else:
					matching_lines.add(line_no)
		return matching_lines

	def difference(self, obj):
		"""difference between self and another ACL object elements

		Args:
			obj (ACL): another ACL object to compare differences

		Returns:
			dict: difference between self and another ACL object elements
		"""
		diffacl = ACL(self._name, None, self.grp)
		for self_k, self_v in self._repr_dic.items():
			if isinstance(self_v, ACL_REMARK): continue
			_self_v = {k:v for k,v in self_v.items() if k != 'remark'}
			for obj_k, obj_v in obj._repr_dic.items():
				if isinstance(obj_v, ACL_REMARK): continue
				_obj_v = {k:v for k,v in obj_v.items() if k != 'remark'}
				found = _self_v == _obj_v
				if found: break
			if not found:
				diffacl[self_k] = self_v
		return diffacl

	def same_elements(self, obj):
		"""compare self for similar elements with provided another ACL object.

		Args:
			obj (ACL): another ACL object to compare elements

		Returns:
			bool: if self and provided ACL has same elements or not
		"""
		return ( not self.difference(obj) and not obj.difference(self) )


	# ---------------- Operate on a Copy --------------- 	

	def copy_and_append(self, attribs):
		"""create duplicate of self, append a new acl line in new object with provided attributes 

		Args:
			attribs (dict): line attributes

		Returns:
			ACL: copy of ACL with attributes appended
		"""
		newobj = deepcopy(self)
		newobj.append(attribs)
		return newobj

	def copy_and_delete(self, attribs):
		"""create duplicate of self, delete a line in new acl for given line number/attributes

		Args:
			attribs (dict): line attributes

		Returns:
			ACL: copy of ACL with attributes/line removed
		"""
		newobj = deepcopy(self)
		newobj -= attribs
		return newobj

	def copy_and_insert(self, line_no, attribs):
		"""create duplicate of self, insert a new acl line in new acl object,
		with provided attributes at given line number and return new updated object.
		existing object remains untouched.

		Args:
			line_no (int): line number at which entry to be inserted
			attribs (dict): line attributes

		Returns:
			ACL: copy of ACL with attributes/line insert
		"""
		newacl = deepcopy(self)
		newacl.insert(line_no, attribs)
		return newacl

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS / SUPPORTIVE ~~~~~~~~~~~~~~~~~~~

	def _delete_by_line(self, line_no):
		"""Supportive : delete a line in acl

		Args:
			line_no (int): line number at which entry to be deleted

		Returns:
			str: delta change(s) for the deletion of entry
		"""
		removals = self._del_str(line_no)
		self.removals += removals
		self._key_delete(line_no)
		if self.max > line_no: self._key_deflate(line_no)

		return removals

	def _delete_by_attribs(self, attribs):
		"""Supportive : delete a line in acl by attrib

		Args:
			attribs (dict): line attributes

		Returns:
			str: delta change(s) for the addition of entry
		"""
		mv = self.contains(attribs)
		s = ''
		for i in reversed(sorted(mv)):
			s += self._delete_by_line(i)
		return s

	def _is_equal(self, obj):
		"""supportive: for standard way of comparing two ACL objects self and obj

		Args:
			obj (ACL): another ACL object to be compared with self

		Returns:
			bool: if both ACL objects (self and obj) are equal or not
		"""
		for k, v in obj:
			if k in self._repr_dic and self._repr_dic[k] == v: continue
			else: return False
		return True

	def _compare(self, obj):
		"""supportive: compare and get difference between self and obj/ACL object

		Args:
			obj (ACL): another ACL object to be compared with self

		Returns:
			ACL: an ACL with differences between self and provided obj(ACL) object
		"""
		diffacl = ACL(self._name, None, self.grp)
		for self_k, self_v in self._repr_dic.items():
			found = False
			for obj_k, obj_v in obj._repr_dic.items():
				found = self_v == obj_v
				if found: break
			if not found: diffacl[self_k] = self_v
		return diffacl

	def _key_extend(self, n):
		"""supportive: insert a new line at position n

		Args:
			n (int): sequence line number of an acl from where keys to be extended to insert a new line
		"""
		rvs_keys = list(reversed(self._repr_dic.keys()))
		for key in rvs_keys:
			if key >= n: self[key+1] = self._repr_dic[key]
			else: break

	def _key_delete(self, n):
		"""supportive: deletes a line in ACL

		Args:
			n (int): sequence line number of an acl to be removed
		"""
		try:
			del(self._repr_dic[n])
		except:
			print(f"NoDeletableEntryFoundForLine-{n}-orAlreadyRemoved")

	def _key_deflate(self, n):
		"""supportive: rearranges next lines

		Args:
			n (int): sequence line number of an acl from where keys to be deflated
		"""
		last_used_key = self.max
		for key in range(n, last_used_key):
			self[key] = self._repr_dic[key+1]
		del(self._repr_dic[last_used_key])

	def _add(self, line_no, attribs):
		"""supportive : update member per std and insert entry to acl

		Args:
			line_no (int): line number
			attribs (dict): attributes to be set on line

		Returns:
			str: delta change of modification
		"""
		attribs = self._update_members(attribs)
		attribs = self._update_remarks(line_no, attribs)
		self[line_no] = attribs
		adds = self._to_str(line_no)
		self.adds += adds
		return adds

	def _update_members(self, attribs):
		"""supportive : attributes update as per std source/destination/port/protocol

		Args:
			attribs (dict): attributes to be modified with members if any

		Returns:
			dict: updated attributes
		"""
		attribs = self._update_group_members(attribs)
		return attribs

	def _update_remarks(self, n, attribs):
		"""supportive : remark attributes update, if not provided use previous line remark

		Args:
			n (int): line number
			attribs (dict): remark attributes to be modified if need any

		Returns:
			dict: updated attributes
		"""
		if not attribs.get('remark') :
			try:
				attribs['remark'] = self._repr_dic[n-1]['remark']
			except:
				attribs['remark'] = str(self._repr_dic[n-1])
		return attribs

	def _update_group_members(self, attribs):
		"""supportive : source/destination/port attributes update as per std 

		Args:
			attribs (dict): attributes

		Returns:
			dict: updated attributes
		"""
		sdps = {'source', 'destination', 'ports'}
		for sdp in sdps:
			self._update_an_attrib(attribs, sdp)
		return attribs

	def _update_an_attrib(self, attribs, sdp):
		"""supportive : an attribute update as per std ( one of source/destination/port )

		Args:
			attribs (dict): attributes
			sdp (str): attribute name ('source', 'destination' etc..)
		"""
		f = port_group_member if sdp == 'ports' else network_group_member
		if isinstance(attribs[sdp], (set, tuple, list)):
    		# iterable attribute update
			self._update_set_attribs(attribs, sdp, f)
		else:
    		# normal attribute update
			attribs[sdp] = f(str(attribs[sdp]).split(), idx=0, objectGroups=self.objs)

	def _update_set_attribs(self, attribs, sdp, f):
		"""supportive : an attribute update per std (iterable attribute)

		Args:
			attribs (dict): attributes
			sdp (str): attribute name ('source', 'destination' etc..)
			f (function): function on which the action to carried up on
		"""
		s = set()
		for _sdp in attribs[sdp]:
			s.add(f(str(_sdp).split(), idx=0, objectGroups=self.objs))
		attribs[sdp] = s

	# ----------------- String repr / supportive --------------- #

	def _to_str(self, n, sequence=True):
		"""String representation of an acl-line (n)

		Args:
			n (int): line number
			sequence (bool, optional): require sequence number in output. Defaults to True.

		Returns:
			str: an acl line
		"""
		seq = self.sequence and sequence
		seq_no = f"line {n} " if seq else ""
		item = self._repr_dic[n]
		if isinstance(item, dict):
			for v in self.mandatory_item_values_for_str:
				if v not in item:
					item[v] = self._normalize(v)
			log_warning = " log warning" if item['log_warning'] else ""
			src = update_obj_grp_str(item, 'source')
			dst = update_obj_grp_str(item, 'destination')
			pt  = update_obj_grp_str(item, 'ports')
			prt = update_obj_grp_str(item, 'protocol')
			s = (f"access-list {self._name} {seq_no}"
				 f"{item['acl_type']} {item['action']} {prt} "
				 f"{src} {dst} {pt}{log_warning}\n")
		else:
			s = f"access-list {self._name} {seq_no}{item}"
		return s


	def _del_str(self, n=0):
		"""negating string of an acl-line (n), can be use with standard way as well
		usage: del(acl[n:n+x:step]) to delete acl entry(ies).
		get/find deleted entries using property acl.removals
		[remove full acl if n is not provided]

		Args:
			n (int, optional): line number. Defaults to 0.

		Returns:
			str: delta for negating acl line(s)
		"""
		s = ''
		if n and isinstance(n, int): 
			return "no " + self._to_str(n, False)
		elif n and isinstance(n, (list, tuple, set)):
			for i in n: s += self._del_str(i)
		elif not n:
			for n, v in self: s += self._del_str(n)
		return s 

	## ----------- Other Supportive to Supportives --------- ##

	def _normalize(self, item):
		"""return default attributes for the require item/attribute.

		Args:
			item (str): attribute name

		Raises:
			Exception: MissingMadatoryParameter

		Returns:
			various: standard value for item, defined in normalize_item_values
		"""
		normalize_item_values = {
			'acl_type': 'extended', 
			# 'action': 'permit', 
			# 'protocol': 'tcp', 
			# 'source': , 
			# 'destination': , 
			# 'ports': , 
			'log_warning': True,
			}
		if normalize_item_values.get(item):
			return normalize_item_values[item]
		else:
			raise Exception(f"MissingMandatoryParameter-{item}, NormalizationNotAvailableForMandatoryField")


	# ~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~~
	# USED WHILE INITIATLIZING / PARSER
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def parse(self, objs):
		"""parse access-list-lines-list and set _repr_dic
		objs requires for acl lines having object-group-names

		Args:
			objs (OBJS): object of object-groups (OBJS)
		"""
		remark = None
		for line_no, line in enumerate(self.acl_lines_list):
			test = line.startswith("access-list al_from_blue extended deny tcp any4 any4 object-group INET-TCP-DROP")
			spl_line = line.split()
			# remarks line
			if spl_line[2] == 'remark':
				remark = " ".join(spl_line[3:])
				self._repr_dic[line_no] = ACL_REMARK(remark)
				continue
			# src /dst / ports
			idx_variance = 0
			protocol_variance = 1 if spl_line[4] == "object-group" else 0
			for k, v in self.end_point_identifiers_pos.items():
				pv = v+protocol_variance+idx_variance
				if k == 0: source      = network_group_member(spl_line, idx=pv, objectGroups=objs)
				if k == 1: destination = network_group_member(spl_line, idx=pv, objectGroups=objs)
				if k == 2: ports       = port_group_member(spl_line, idx=pv, objectGroups=objs)
				try:
					if spl_line[pv] in ANY: idx_variance -= 1
				except:
					pass
			self._repr_dic[line_no] = {
				'remark': remark,
				'acl_type': spl_line[2],
				'action': spl_line[3],
				'protocol': spl_line[4+protocol_variance],
				'source': source,
				'destination': destination,
				'ports': ports,
				'log_warning': STR.found(line, 'log warnings'),
			}


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
