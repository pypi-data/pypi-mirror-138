
# ----------------------------------------------------------------------------------------
from nettoolkit import *

from .static import *

# ----------------------------------------------------------------------------------------
# Parents Classes
# ----------------------------------------------------------------------------------------
class EntiryProperties():
	"""Common properties/methods for individual entities
	"""
	def __str__(self): return self._str
	def __repr__(self): return self._str
	def __hash__(self): return self._hash
	def __eq__(self, obj): return str(obj) == str(self)

class Singular(EntiryProperties):
	"""a common class template to create an IcmpProtocol or NetworkProtocol object instance 

	Args:
		EntiryProperties (EntiryProperties): Common properties/methods for individual entities
	"""
	def __init__(self, _type):
		self._type = _type
		self._str = f'icmp-object {self._type}'.strip()
		self._hash = hash(self._type)
IcmpProtocol = Singular
NetworkProtocol = Singular

# ----------------------------------------------------------------------------------------
# Control Classes
# ----------------------------------------------------------------------------------------

class Network(EntiryProperties):
	"""a network/subnet object

	Args:
		EntiryProperties (EntiryProperties): Common properties/methods for individual entities
	"""
	def __init__(self, network, dotted_mask=None): 
		if dotted_mask:
			self.mask = to_dec_mask(dotted_mask)
			self.network = network + "/" + str(self.mask)
		else:
			self.network = network
			self.mask = None
		self.host = False
		self.address_it()

	def address_it(self):
		"""set addressing object and a few basic variables.
		"""
		self._network = addressing(self.network)
		self._hash = hash(self._network)
		self.version = self._network.version
		if self.version == 4 and (not self.mask or self.mask == 32):  
			self.mask = 32
			self.host = True
		if self.version == 6 and (not self.mask or self.mask == 128):
			self.mask = 128
			self.host = True

	@property
	def _str(self):
		"""string property for the self object

		Returns:
			str: string representation of self
		"""
		if self.version == 4: net = self._network.ipbinmask()
		if self.version == 6: net = self._network.network + "/" + str(self.mask)
		if net in any4: return 'any4'
		if net in any6: return 'any6'
		if self.host: net = net.split(" ")[0].split("/")[0]
		return net

# ----------------------------------------------------------------------------------------
class Ports(EntiryProperties):
	"""a port/range-of-ports object

	Args:
		EntiryProperties (EntiryProperties): Common properties/methods for individual entities
	"""
	def __init__(self, port_type, port, port_range_end='', objectGroups=None): 
		self._set_porttype(port_type)
		self._set_ports(port, port_range_end, objectGroups)
		self._hash = hash(port)

	def split(self):
		"""split the port string to a list

		Returns:
			list: port string splitted
		"""
		return str(self).split()

	def _set_porttype(self, port_type):
		"""port type validations

		Args:
			port_type (str): various port types (ex: eq, range, ...)

		Raises:
			Exception: InvalidPortType
		"""
		if port_type in VALID_PORT_MATCHES:
			self.port_type = port_type
			if port_type in ICMP:
				self.port_type = ''
				self.start = port_type				
				self.end = ''
				self._set_mapped_port_numbers(self.start, self.end)
		elif port_type == 'log' or port_type == '':
			self.port_type = ''
			self.start = ''
			self.end = ''
		else:
			raise Exception(f"InvalidPortType{port_type}, Valid options are {VALID_PORT_MATCHES}")

	def _set_mapped_port_numbers(self, start, end):
		"""port numbers (start, end) validations

		Args:
			start (str): range start number/ or port number
			end (str): range end number
		"""
		for k, v in PORT_MAPPINGS.items():
			if v == start: 
				self.start = int(k)
			if v == end: 
				self.end = int(k)
		try: self.end
		except: self.end = ''
		try: self.start
		except: self.start = ''

	def _set_ports(self, start, end, objectGroups):
		"""port number validations including object groups

		Args:
			start (str, int): start number of range of ports
			end (str, int): end number of range of ports
			objectGroups (str): object-group name

		Returns:
			None: None
		"""
		if not self.port_type: return None
		if start in PORT_MAPPINGS.values() or end in PORT_MAPPINGS.values():
			self._set_mapped_port_numbers(start, end)
			return
		if self.port_type == 'object-group':
			self.end = ''
			self.start = objectGroups(start)
			return
		try:
			self.start = int(start)
		except:
			self.start = start
		try:
			self.end = int(end) if self.port_type == 'range' else ''
		except:
			self.end = end if self.port_type == 'range' else ''

	@property
	def _str(self):
		"""string representation of self

		Returns:
			str: string representation of self
		"""
		port = PORT_MAPPINGS[self.start] if self.start in PORT_MAPPINGS else self.start
		port_end = PORT_MAPPINGS[self.end] if self.end in PORT_MAPPINGS else self.end
		port_end = f' {port_end}' if port_end else ''
		port_type = f'{self.port_type} ' if self.port_type else ''
		return f'{port_type}{port}{port_end}'.strip()

	def __contains__(self, port):
		"""validates if provided port is part of port members

		Args:
			port (int): port number

		Returns:
			bool: if port is within port members
		"""
		end = self.start if not self.end else self.end
		for k, v in PORT_MAPPINGS.items():
			if v == port: port = k
		try:
			return self.start <= port <= end
		except:
			print(f"Invalid Port to check within [{self.start} <= {port} <= {end}]")

# ----------------------------------------------------------------------------------------

class ACL_REMARK():
	"""ACL remark entity object
	"""
	def __init__(self, remark): self.remark = remark
	def __str__(self): return self.str()
	def __repr__(self): return self.remark
	def __eq__(self, obj): return str(obj) == str(self)
	def str(self): return self.remark + "\n"


# ----------------------------------------------------------------------------------------
#  DUMMY BLANK OBJECT GOUPs
# ----------------------------------------------------------------------------------------

class NetworkObject():
	obj_grp_type = 'network'
	obj_grp_svc_filter = ''

class UDPPortObject(Singular):
	obj_grp_type = 'service'
	obj_grp_svc_filter = 'udp'

class TCPPortObject(Singular):
	obj_grp_type = 'service'
	obj_grp_svc_filter = 'tcp'

class ProtocolObject(Singular):
	obj_grp_type = 'protocol'
	obj_grp_svc_filter = ''

class ICMPPortObject(Singular):
	obj_grp_type = 'icmp-type'
	obj_grp_svc_filter = ''

# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
