""" static variables used for Cisco defined here.

"""
# ------------------------------------------------------------------------------
# Standard number of characters for identifing interface short-hand
# ------------------------------------------------------------------------------
CISCO_IFSH_IDENTIFIERS = {
	"VLAN": {'Vlan':2,},
	"TUNNEL": {'Tunnel':2,},
	"LOOPBACK": {'Loopback':2,} ,
	"AGGREGATED": {'Port-channel':2,},
	"PHYSICAL": {'Ethernet': 2, 
		'FastEthernet': 2,
		'GigabitEthernet': 2, 
		'TenGigabitEthernet': 3, 
		'FortyGigabitEthernet':2, 
		'TwentyFiveGigE':3, 
		'TwoGigabitEthernet': 2,
		'HundredGigE':3,
		'AppGigabitEthernet': 2,
		},
}
# ------------------------------------------------------------------------------
