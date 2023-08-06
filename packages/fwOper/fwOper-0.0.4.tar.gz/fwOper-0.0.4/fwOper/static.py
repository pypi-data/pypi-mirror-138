
# ----------------------------------------------------------------------------------------
# Static / Universal Variables
# ----------------------------------------------------------------------------------------
ADD = 'add'			# request types
DEL = 'del'

ANY = ('any', 'any4', 'any6')
any4 = ('0.0.0.0 0.0.0.0', '0/0', '0.0.0.0/0')
any6 = ('::/0',)

DEFAULT_ROUTE = ("0.0.0.0", "0.0.0.0")

ICMP = ('echo', 'echo-reply')
VALID_PROTOCOLS = ('tcp', 'udp', 'icmp', 'ip', 'scp')
VALID_PORT_MATCHES = ('eq', 'range', 'echo', 'echo-reply', 'object-group')
PORT_MAPPINGS = {
	7: 'echo', 
	22: 'ssh', 
	23: 'telnet', 
	80: 'www', 
	443: 'https', 
}
VALID_MEMBER_TYPES = ('network-object', 'port-object', 
	'icmp-object', 'protocol-object', 'group-object', )

MEMBERS_MEMBERTYPES = {
	ICMP: 'icmp-object',
	VALID_PROTOCOLS: 'protocol-object',
}

GROUP_VALID_FIELDS = {'source', 'destination', 'ports', 'protocol'}

# ----------------------------------------------------------------------------------------

LINE_SNG = f'!{"-"*80}!\n'

# ----------------------------------------------------------------------------------------
