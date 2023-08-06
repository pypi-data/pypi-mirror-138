
# ----------------------------------------------------------------------------------------
from nettoolkit import *

from .entity import *
from .static import *

# ----------------------------------------------------------------------------------------
# Control Functions
# ----------------------------------------------------------------------------------------
def network_group_member(spl_line, idx, objectGroups=None):
	"""returns Network group member object from given splitted line

	Args:
		spl_line (list): splitted line of an acl entry
		idx (int): index position to start looking for network
		objectGroups (OBJS, optional): object-groups object. Defaults to None.

	Raises:
		Exception: UndefinedEndPointType

	Returns:
		(Network, OBJ, None): Network group member object
	"""
	if spl_line[idx] == 'object-group':
		try:
			return objectGroups[spl_line[idx+1]]		# <- OBJ
		except:
			return None
	elif spl_line[idx] in ANY:
		return Network(*DEFAULT_ROUTE)
	else:
		address = spl_line[idx+1] if spl_line[idx] == 'host' else spl_line[idx]
		ao = addressing(address)
		if type(ao) == IPv6:
			return Network(address)
		if type(ao) == IPv4:
			try:
				return Network(address, spl_line[idx+1])
			except:
				return Network(address)
	raise Exception(f"UndefinedEndPointType: {spl_line}\n{idx}")

def port_group_member(spl_line, idx, objectGroups=None):
	"""returns Port group member object from given splitted line

	Args:
		spl_line (list): splitted line of an acl entry
		idx (int): index position to start looking for port(s)
		objectGroups (OBJS, optional): object-groups object. Defaults to None.

	Raises:
		Exception: UndefinedPort/PortType

	Returns:
		(Ports, OBJ, None): Network group member object
	"""
	try: spl_line[idx]
	except: return ''
	if 4 < len(spl_line) <= 8:
		pts = Ports("", "")
	elif spl_line[idx] == 'eq':
		pts = Ports(spl_line[idx], spl_line[idx+1])
	elif spl_line[idx] =='range':
		pts = Ports(spl_line[idx], spl_line[idx+1], spl_line[idx+2])
	elif spl_line[idx] == 'object-group':
		try:
			pts = objectGroups[spl_line[idx+1]]
		except:
			pts = None
			pass													### bypassed temporily
	elif spl_line[idx] in ICMP:
		pts = Ports(spl_line[idx], "")
	elif spl_line[4] == 'icmp':				### Exceptional match for missing icmp ports
		pts = Ports("", 'echo')				  # define port as echo in this case
	elif spl_line[idx] == 'log':
		return ''
	else:
		raise Exception(f"UndefinedPort/PortType: {spl_line} at index {idx}")
	return pts

def icmp_group_member(spl_line):
	"""returns icmp port group member object from given splitted line

	Args:
		spl_line (list): splitted line of an acl entry

	Returns:
		IcmpProtocol: IcmpProtocol member object
	"""
	pts = IcmpProtocol(spl_line[-1])
	return pts

def protocol_group_member(spl_line):
	"""returns protocol group member object from given splitted line

	Args:
		spl_line (list): splitted line of an acl entry

	Returns:
		NetworkProtocol: NetworkProtocol member object
	"""
	pts = NetworkProtocol(spl_line[-1])
	return pts

def group_object_member(spl_line, objectGroups=None):
	"""returns object-group object from given splitted line

	Args:
		spl_line ([type]): [description]
		objectGroups ([type], optional): [description]. Defaults to None.

	Returns:
		OBJ: object-group OBJ member object
	"""
	try:
		return objectGroups[spl_line[-1]]
	except:
		return None	


def network_member(network, objs=None):
	"""returns Network group member object for given network, objs will require if network has object-group.

	Args:
		network (str): ip-network string
		objs (OBJS, optional): object-groups object. Defaults to None.

	Raises:
		Exception: InvalidNetwork

	Returns:
		Network: Network group member object
	"""
	if not isinstance(network, str): return network	
	# ----------------------------------------------------
	network = network.strip()
	# ----------------------------------------------------
	if network in ANY: return Network(*DEFAULT_ROUTE)
	# ----------------------------------------------------
	spl_network = network.split("/")
	net_obj = None
	if len(spl_network) == 2:
		net_obj = addressing(network)
		if net_obj:
			mask = int(spl_network[1]) 
			return Network(spl_network[0], bin_mask(mask))
	# ----------------------------------------------------
	spl_network = network.split(" ")
	if len(spl_network) == 2:
		if spl_network[0] == 'object-group': 
			return objs[spl_network[1]]
		mask = to_dec_mask(spl_network[1])
		net = spl_network[0] +"/"+ str(mask)
		net_obj = addressing(net)
		if net_obj: 
			return Network(spl_network[0], spl_network[1])
	# ----------------------------------------------------
	else:
		subnet = network + "/32"
		net_obj = addressing(network)
		if net_obj:
			return Network(network, '255.255.255.255')
	# ----------------------------------------------------
	raise Exception(f"InvalidNetwork")


def port_member(port, objs):
	"""returns Port group member object for given port, objs will require if port has object-group

	Args:
		port (str): port string
		objs (OBJS): object-groups object

	Raises:
		Exception: InvalidPort

	Returns:
		Ports: Ports member object
	"""
	port = str(port).strip()
	if port.startswith('eq '): port = port[3:].lstrip()
	if port.startswith('range '): port = port[6:].lstrip()
	if port in ICMP: return Ports("", port)
	# ----------------------------------------------------
	spl_port = port.split(" ")
	if len(spl_port) == 2: 
		if spl_port[0] == 'object-group': 
			return objs[spl_port[1]]
		return Ports('range', spl_port[0], spl_port[1])
	dspl_port = port.split("-")
	if len(dspl_port) == 2: return Ports('range', dspl_port[0], dspl_port[1])
	elif len(dspl_port) == 1 and len(spl_port) == 1: return Ports('eq', port)
	# ----------------------------------------------------
	raise Exception(f"InvalidPort")

# ----------------------------------------------------------------------------------------

def get_match_dict(request_parameters, objs):
	"""search for request parameters and return matching parameters dictionary.
	(dictionary with attributes require to match in ACL)

	Args:
		request_parameters (dict): request paramters in dictionary
		objs (OBJS): object-groups object

	Returns:
		dict: with filtered parameters only
	"""
	matching_parameters = ('remark', 'acl_type', 'action', 'protocol', 'source',
		'destination', 'ports',)
	network_member_parameters = ('source', 'destination')
	port_member_parameters = ('ports',)
	matching_dict = {}
	for item in matching_parameters:
		if item in network_member_parameters and item in request_parameters:
			matching_dict[item] = network_member(request_parameters[item], objs)
		elif item in port_member_parameters and item in request_parameters:
			matching_dict[item] = port_member(request_parameters[item], objs)
		elif item in request_parameters:
			matching_dict[item] = request_parameters[item]
	return matching_dict


# ----------------------------------------------------------------------------------------
# Other Functions
# ----------------------------------------------------------------------------------------

def get_port_name(n):
	"""update and return well known port number for port name

	Args:
		n (int): port number

	Returns:
		str: well-known port name else port number
	"""
	return PORT_MAPPINGS[n] if PORT_MAPPINGS.get(n) else n

def update_ports_name(requests):
	"""update and return well known port number for port name in given request port

	Args:
		requests (dict): acl attributes in request dictionary

	Returns:
		dict: updated request attributes
	"""
	for request in requests: 
		request['ports'] = get_port_name(request['ports'])
	return requests

# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------
