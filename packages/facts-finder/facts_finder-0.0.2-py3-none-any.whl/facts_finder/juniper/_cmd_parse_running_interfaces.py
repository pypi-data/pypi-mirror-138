"""juniper interface from config command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC, JSet

from facts_finder.juniper._cmd_parse_running import Running
from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.juniper.statics import JUNIPER_IFS_IDENTIFIERS
from facts_finder.juniper.common import get_subnet
from facts_finder.juniper.common import get_v6_subnet
from facts_finder.juniper.common import get_vlans_juniper

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningInterfaces(Running):
	"""object for interface level config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output

		Args:
			cmd_op (list, str): config output, either list of multiline string
		"""    		    		
		super().__init__(cmd_op)
		self.interface_dict = OrderedDict()

	def interface_read(self, func):
		"""directive function to get the various interface level output

		Args:
			func (method): method to be executed on interface config line

		Returns:
			dict: parsed output dictionary
		"""    		
		ports_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if l.startswith("set interfaces interface-range"): continue
			if not l.startswith("set interfaces"): continue
			spl = l.split()
			int_type = None
			for k, v in JUNIPER_IFS_IDENTIFIERS.items():
				if spl[2].startswith(v):
					int_type = k
					break
			if not int_type: 
				print(f"UndefinedInterface(Type)-{spl[2]}")
				continue
			p = _juniper_port(int_type, spl)
			if not p: continue
			if not ports_dict.get(p): ports_dict[p] = {}
			port_dict = ports_dict[p]
			func(port_dict, l, spl)
		return ports_dict


	def interface_ips(self):
		"""update the interface ipv4 ip address details
		"""    		
		func = self.get_ip_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_ip_details(port_dict, l, spl):
		"""parser function to update interface ipv4 ip address details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		subnet = _get_v4_subnet(spl, l)
		if not subnet: return		
		port_dict['v4'] = {}
		port_dict['v4']['address'] = _get_v4_address(spl, l)
		port_dict['v4']['ip'] = _get_v4_ip(spl, l)
		port_dict['v4']['mask'] = _get_v4_mask(spl, l)
		port_dict['v4']['subnet'] = subnet

	def interface_v6_ips(self):
		"""update the interface ipv6 ip address details
		"""    		
		func = self.get_ipv6_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_ipv6_details(port_dict, l, spl):
		"""parser function to update interface ipv6 ip address details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		address = _get_v6_address(spl, l)
		if not address: return
		link_local = _is_link_local(address)
		if not port_dict.get('v6'): port_dict['v6'] = {}
		v6_port_dic = port_dict['v6']
		if link_local :
			if v6_port_dic.get("link-local"): return None
			v6_port_dic['link-local'] = {}
			v6_pd = v6_port_dic['link-local']
		else:
			if v6_port_dic.get("address"): return None
			v6_pd = v6_port_dic
		v6_pd['address'] = address
		v6_pd['ip'] = _get_v6_ip(address)
		v6_pd['mask'] = _get_v6_mask(address)
		v6_pd['subnet'] = get_v6_subnet(address)


	def interface_vlans(self):
		"""update the interface vlan details
		"""   
		func = self.get_int_vlan_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_vlan_details(port_dict, l, spl):
		"""parser function to update interface vlan details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		vlans = get_vlans_juniper(spl)
		if not vlans: return None
		if not port_dict.get('vlan'): port_dict['vlan'] = []
		port_dict['vlan'].extend(vlans)


	def interface_mode(self):
		"""update the interface port mode trunk/access details
		"""   
		func = self.get_interface_mode
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_interface_mode(port_dict, l, spl):
		"""parser function to update interface port mode trunk/access details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		mode = 'interface-mode' in spl
		if not mode: return None
		if not port_dict.get('port_mode'): port_dict['port_mode'] = spl[-1]


	def interface_description(self):
		"""update the interface description details
		"""   
		func = self.get_int_description
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_description(port_dict, l, spl):
		"""parser function to update interface description details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		description = ""
		if l.startswith("set interfaces ") and "description" in spl:
			desc_idx = spl.index("description")
			description = " ".join(spl[desc_idx+1:])
		if description and not port_dict.get('description'):
			port_dict['description'] = description
		return port_dict

	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------


def get_interfaces_running(cmd_op, *args):
	"""defines set of methods executions. to get various inteface parameters.
	uses RunningInterfaces in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningInterfaces(cmd_op)
	R.interface_ips()
	R.interface_v6_ips()
	R.interface_vlans()
	R.interface_mode()
	R.interface_description()
	# # update more interface related methods as needed.

	return R.interface_dict



# ------------------------------------------------------------------------------

def _juniper_port(int_type, spl):
	"""get port/interface number based on interface type for split line
	"""    	
	if spl[3] == 'unit':
		if spl[2] in ('irb', 'vlan'):
			return spl[4]
		return spl[2]+"."+spl[4]
	else:
		return spl[2]

def _get_v4_subnet(spl, line):
	if not _is_v4_addressline(line): return None
	return get_subnet(spl[spl.index("address") + 1])

def _get_v4_ip(spl, line):
	if not _is_v4_addressline(line): return None
	return spl[spl.index("address") + 1].split("/")[0]

def _get_v4_address(spl, line):
	if not _is_v4_addressline(line): return None
	return spl[spl.index("address") + 1]

def _get_v4_mask(spl, line):
	if not _is_v4_addressline(line): return None
	return spl[spl.index("address") + 1].split("/")[1]

def _is_v4_addressline(line):	
	if line.find("family inet") == -1: return None
	if line.find("address") == -1: return None
	return True
# ------------------------------------------------------------------------------


def _get_v6_address(spl, line):
	v6ip = _is_v6_addressline(spl, line)
	if not v6ip : return None
	return v6ip

def _get_v6_ip(v6ip):
	return v6ip.split("/")[0]

def _get_v6_mask(v6ip):
	return v6ip.split("/")[1]

def _is_v6_addressline(spl, line):
	if line.find("family inet6") == -1: return None
	try:
		if spl[spl.index('inet6')+1] != 'address': return None
	except: return None
	return spl[spl.index('inet6')+2]

def _is_link_local(v6_ip):
	return v6_ip.lower().startswith("fe80:")

# ------------------------------------------------------------------------------
