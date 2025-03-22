# LICENTA
## MAIN
Aici mi-am pus aplicațiile pe care le-am parcurs separat, dar nu le-am integrat încă. Pe măsură ce le integrez, o să le mut în `ryudocs` și voi adăuga altele.
🌐 Full API Documentation
Below is a structured and clearly organized summary of every API you currently have available from your Ryu REST application:

🛡️ Firewall Management APIs
Method	Endpoint	Description
GET	/firewall/module/status	Get firewall status
PUT	/firewall/module/enable/{switchid}	Enable firewall
PUT	/firewall/module/disable/{switchid}	Disable firewall
GET	/firewall/log/status	Get firewall log status
PUT	/firewall/log/enable/{switchid}	Enable firewall logging
PUT	/firewall/log/disable/{switchid}	Disable firewall logging
GET	/firewall/rules/{switchid}	Get firewall rules
POST	/firewall/rules/{switchid}	Add firewall rule
DELETE	/firewall/rules/{switchid}	Delete firewall rule
GET	/firewall/rules/{switchid}/{vlanid}	Get firewall rules by VLAN
POST	/firewall/rules/{switchid}/{vlanid}	Add firewall rule by VLAN
DELETE	/firewall/rules/{switchid}/{vlanid}	Delete firewall rule by VLAN
📈 OpenFlow Switch Management APIs
Switch General Information
Method	Endpoint	Description
GET	/stats/switches	List all connected switches
GET	/stats/desc/{dpid}	Switch description info
Flow Management
Method	Endpoint	Description
POST	/stats/flowdesc/{dpid}	Get flow descriptions
GET	/stats/flow/{dpid}	Retrieve flow entries
POST	/stats/flow/{dpid}	Retrieve flow entries (with filter)
GET	/stats/aggregateflow/{dpid}	Get aggregated flow stats
POST	/stats/aggregateflow/{dpid}	Aggregated flow stats with filters
POST	/stats/flowentry/{cmd}	Modify (add/delete) flow entries
DELETE	/stats/flowentry/clear/{dpid}	Clear all flow entries
Table Management
Method	Endpoint	Description
GET	/stats/table/{dpid}	Get table stats
GET	/stats/tablefeatures/{dpid}	Get table features
Port Management
Method	Endpoint	Description
GET	/stats/port/{dpid}	Get port stats for switch
GET	/stats/port/{dpid}/{port}	Get specific port stats
GET	/stats/portdesc/{dpid}	Get port descriptions
GET	/stats/portdesc/{dpid}/{port_no}	Get specific port description
POST	/stats/portdesc/{cmd}	Modify port behavior
Queue Management
Method	Endpoint	Description
GET	/stats/queue/{dpid}	Get queue stats for switch
GET	/stats/queue/{dpid}/{port}	Get queue stats per port
GET	/stats/queue/{dpid}/{port}/{queue_id}	Get specific queue stats
GET	/stats/queueconfig/{dpid}	Queue configuration for switch
GET	/stats/queueconfig/{dpid}/{port}	Queue config per port
GET	/stats/queuedesc/{dpid}	Queue description for switch
GET	/stats/queuedesc/{dpid}/{port}	Queue description per port
GET	/stats/queuedesc/{dpid}/{port}/{queue_id}	Specific queue description
Meter Management
Method	Endpoint	Description
GET	/stats/meterfeatures/{dpid}	Get meter features
GET	/stats/meterconfig/{dpid}	Get meter configuration
GET	/stats/meterconfig/{dpid}/{meter_id}	Specific meter config
GET	/stats/meterdesc/{dpid}	Meter descriptions
GET	/stats/meterdesc/{dpid}/{meter_id}	Specific meter description
GET	/stats/meter/{dpid}	Meter statistics
GET	/stats/meter/{dpid}/{meter_id}	Specific meter statistics
POST	/stats/meterentry/{cmd}	Modify meter entries
Group Management
Method	Endpoint	Description
GET	/stats/groupfeatures/{dpid}	Get group features
GET	/stats/groupdesc/{dpid}	Get group descriptions
GET	/stats/groupdesc/{dpid}/{group_id}	Specific group description
GET	/stats/group/{dpid}	Get group stats
GET	/stats/group/{dpid}/{group_id}	Specific group stats
POST	/stats/groupentry/{cmd}	Modify group entries
Role and Experimental
Method	Endpoint	Description
GET	/stats/role/{dpid}	Get controller role
POST	/stats/role	Set controller role
POST	/stats/experimenter/{dpid}	Send experimenter message

## RYUDOCS
Fișierele de aici sunt aplicațiile pe care le-am integrat în codul meu fără funcționalități schimbate.
## MYCODE
Această secțiune conține doar aplicațiile testate și funcționale. Aplicațiile netestate nu sunt incluse aici.
