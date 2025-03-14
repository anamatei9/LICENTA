import logging
import json
import ast

from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.lib import ofctl_v1_0, ofctl_v1_2, ofctl_v1_3, ofctl_v1_4, ofctl_v1_5
from ryu.ofproto import ofproto_v1_3,ofproto_v1_5
from ryu.app.wsgi import ControllerBase, Response, WSGIApplication
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.app.ofctl_rest import  supported_ofctl
from ryu.exception import RyuException

LOG = logging.getLogger('ryu.app.ofctl_rest')

# Custom exceptions
class CommandNotFoundError(RyuException):
    message = 'No such command: %(cmd)s'

class PortNotFoundError(RyuException):
    message = 'No such port info: %(port_no)s'
    
def stats_method(method):
    def wrapper(self, req, dpid, *args, **kwargs):
        try:
            dp = self.dpset.get(int(dpid, 16))
        except ValueError:
            LOG.exception('Invalid hexadecimal DPID: %s', dpid)
            return Response(status=400)
        if dp is None:
            LOG.error('No such Datapath: %s', dpid)
            return Response(status=404)

        try:
            ofctl = supported_ofctl.get(dp.ofproto.OFP_VERSION)
        except KeyError:
            LOG.exception('Unsupported OF version: %s', dp.ofproto.OFP_VERSION)
            return Response(status=501)

        try:
            ret = method(self, req, dp, ofctl, *args, **kwargs)

            if isinstance(ret, Response):
                return ret

            # Explicit formatting WITHOUT "0x"
            if isinstance(ret, dict):
                formatted_ret = {f"{int(k):016x}": v for k, v in ret.items()}
                return Response(content_type='application/json', body=json.dumps(formatted_ret))

            return Response(content_type='application/json', body=json.dumps(ret))
        except (ValueError, AttributeError) as e:
            LOG.exception('Error processing request: %s', e)
            return Response(status=400)
    return wrapper



def command_method(method):
    def wrapper(self, req, *args, **kwargs):
        try:
            body = ast.literal_eval(req.body.decode('utf-8')) if req.body else {}
        except SyntaxError:
            LOG.exception('Invalid syntax in request body: %s', req.body)
            return Response(status=400)

        dpid = body.get('dpid', kwargs.pop('dpid', None))
        if not dpid:
            LOG.exception('DPID missing in request')
            return Response(status=400)

        try:
            dp = self.dpset.get(int(dpid, 16))  # Corrected hex parsing
        except ValueError:
            LOG.exception('Invalid hexadecimal DPID: %s', dpid)
            return Response(status=400)
        if dp is None:
            LOG.error('No such Datapath: %s', dpid)
            return Response(status=404)

        try:
            ofctl = supported_ofctl.get(dp.ofproto.OFP_VERSION)
        except KeyError:
            LOG.exception('Unsupported OF version: %s', dp.ofproto.OFP_VERSION)
            return Response(status=501)

        try:
            # Important: Call the method with 'dp' and 'ofctl' directly
            method(self, req, dp, ofctl, body, *args, **kwargs)
            return Response(status=200)
        except (ValueError, AttributeError, CommandNotFoundError, PortNotFoundError) as e:
            LOG.exception('Error executing command: %s', e)
            return Response(status=400)
    return wrapper


class MyStatsController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(MyStatsController, self).__init__(req, link, data, **config)
        self.dpset = data['dpset']
        self.waiters = data['waiters']

    def get_dpids(self, req, **_kwargs):
        dps = ["{:016x}".format(dpid) for dpid in self.dpset.dps.keys()]
        body = json.dumps(dps)
        return Response(content_type='application/json', body=body)


    @stats_method
    def get_desc_stats(self, req, dp, ofctl, **kwargs):
        return ofctl.get_desc_stats(dp, self.waiters)

    @stats_method
    def get_flow_desc(self, req, dp, ofctl, **kwargs):
        flow = req.json if req.body else {}
        return ofctl.get_flow_desc(dp, self.waiters, flow)

    @stats_method
    def get_flow_stats(self, req, dp, ofctl, **kwargs):
        flow = req.json if req.body else {}
        return ofctl.get_flow_stats(dp, self.waiters, flow)

    @stats_method
    def get_aggregate_flow_stats(self, req, dp, ofctl, **kwargs):
        flow = req.json if req.body else {}
        return ofctl.get_aggregate_flow_stats(dp, self.waiters, flow)

    @stats_method
    def get_table_stats(self, req, dp, ofctl, **kwargs):
        return ofctl.get_table_stats(dp, self.waiters)

    @stats_method
    def get_table_features(self, req, dp, ofctl, **kwargs):
        return ofctl.get_table_features(dp, self.waiters)

    @stats_method
    def get_port_stats(self, req, dp, ofctl, port=None, **kwargs):
        if port == "ALL":
            port = None

        return ofctl.get_port_stats(dp, self.waiters, port)

    @stats_method
    def get_queue_stats(self, req, dp, ofctl,
                        port=None, queue_id=None, **kwargs):
        if port == "ALL":
            port = None

        if queue_id == "ALL":
            queue_id = None

        return ofctl.get_queue_stats(dp, self.waiters, port, queue_id)

    @stats_method
    def get_queue_config(self, req, dp, ofctl, port=None, **kwargs):
        if port == "ALL":
            port = None

        return ofctl.get_queue_config(dp, self.waiters, port)

    @stats_method
    def get_queue_desc(self, req, dp, ofctl,
                       port=None, queue=None, **_kwargs):
        if port == "ALL":
            port = None

        if queue == "ALL":
            queue = None

        return ofctl.get_queue_desc(dp, self.waiters, port, queue)

    @stats_method
    def get_meter_features(self, req, dp, ofctl, **kwargs):
        return ofctl.get_meter_features(dp, self.waiters)

    @stats_method
    def get_meter_config(self, req, dp, ofctl, meter_id=None, **kwargs):
        if meter_id == "ALL":
            meter_id = None

        return ofctl.get_meter_config(dp, self.waiters, meter_id)

    @stats_method
    def get_meter_desc(self, req, dp, ofctl, meter_id=None, **kwargs):
        if meter_id == "ALL":
            meter_id = None

        return ofctl.get_meter_desc(dp, self.waiters, meter_id)

    @stats_method
    def get_meter_stats(self, req, dp, ofctl, meter_id=None, **kwargs):
        if meter_id == "ALL":
            meter_id = None

        return ofctl.get_meter_stats(dp, self.waiters, meter_id)

    @stats_method
    def get_group_features(self, req, dp, ofctl, **kwargs):
        return ofctl.get_group_features(dp, self.waiters)

    @stats_method
    def get_group_desc(self, req, dp, ofctl, group_id=None, **kwargs):
        if dp.ofproto.OFP_VERSION < ofproto_v1_5.OFP_VERSION:
            return ofctl.get_group_desc(dp, self.waiters)
        else:
            return ofctl.get_group_desc(dp, self.waiters, group_id)

    @stats_method
    def get_group_stats(self, req, dp, ofctl, group_id=None, **kwargs):
        if group_id == "ALL":
            group_id = None

        return ofctl.get_group_stats(dp, self.waiters, group_id)

    @stats_method
    def get_port_desc(self, req, dp, ofctl, port_no=None, **kwargs):
        if dp.ofproto.OFP_VERSION < ofproto_v1_5.OFP_VERSION:
            return ofctl.get_port_desc(dp, self.waiters)
        else:
            return ofctl.get_port_desc(dp, self.waiters, port_no)

    @stats_method
    def get_role(self, req, dp, ofctl, **kwargs):
        return ofctl.get_role(dp, self.waiters)

    @command_method
    def mod_flow_entry(self, req, dp, ofctl, flow, cmd, **kwargs):
        cmd_convert = {
            'add': dp.ofproto.OFPFC_ADD,
            'modify': dp.ofproto.OFPFC_MODIFY,
            'modify_strict': dp.ofproto.OFPFC_MODIFY_STRICT,
            'delete': dp.ofproto.OFPFC_DELETE,
            'delete_strict': dp.ofproto.OFPFC_DELETE_STRICT,
        }
        mod_cmd = cmd_convert.get(cmd, None)
        if mod_cmd is None:
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_flow_entry(dp, flow, mod_cmd)

    @command_method
    def delete_flow_entry(self, req, dp, ofctl, flow, **kwargs):
        if ofproto_v1_0.OFP_VERSION == dp.ofproto.OFP_VERSION:
            flow = {}
        else:
            flow = {'table_id': dp.ofproto.OFPTT_ALL}

        ofctl.mod_flow_entry(dp, flow, dp.ofproto.OFPFC_DELETE)

    @command_method
    def mod_meter_entry(self, req, dp, ofctl, meter, cmd, **kwargs):
        cmd_convert = {
            'add': dp.ofproto.OFPMC_ADD,
            'modify': dp.ofproto.OFPMC_MODIFY,
            'delete': dp.ofproto.OFPMC_DELETE,
        }
        mod_cmd = cmd_convert.get(cmd, None)
        if mod_cmd is None:
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_meter_entry(dp, meter, mod_cmd)

    @command_method
    def mod_group_entry(self, req, dp, ofctl, group, cmd, **kwargs):
        cmd_convert = {
            'add': dp.ofproto.OFPGC_ADD,
            'modify': dp.ofproto.OFPGC_MODIFY,
            'delete': dp.ofproto.OFPGC_DELETE,
        }
        mod_cmd = cmd_convert.get(cmd, None)
        if mod_cmd is None:
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_group_entry(dp, group, mod_cmd)

    @command_method
    def mod_port_behavior(self, req, dp, ofctl, port_config, cmd, **kwargs):
        port_no = port_config.get('port_no', None)
        port_no = int(str(port_no), 0)

        port_info = self.dpset.port_state[int(dp.id)].get(port_no)
        if port_info:
            port_config.setdefault('hw_addr', port_info.hw_addr)
            if dp.ofproto.OFP_VERSION < ofproto_v1_4.OFP_VERSION:
                port_config.setdefault('advertise', port_info.advertised)
            else:
                port_config.setdefault('properties', port_info.properties)
        else:
            raise PortNotFoundError(port_no=port_no)

        if cmd != 'modify':
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_port_behavior(dp, port_config)

    @command_method
    def send_experimenter(self, req, dp, ofctl, exp, **kwargs):
        ofctl.send_experimenter(dp, exp)

    @command_method
    def set_role(self, req, dp, ofctl, role, **kwargs):
        ofctl.set_role(dp, role)

class RESTApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    _CONTEXTS = {
        'dpset': dpset.DPSet,
        'wsgi': WSGIApplication
    }
    def __init__(self, *args, **kwargs):
        super(RESTApp, self).__init__(*args, **kwargs)
        self.dpset = kwargs['dpset']
        wsgi = kwargs['wsgi']
        self.waiters = {}
        self.data = {}
        self.data['dpset'] = self.dpset
        self.data['waiters'] = self.waiters

        wsgi.registory[MyStatsController.__name__] = self.data

        self.logger.info("StatsController registered with WSGI")

        
        mapper = wsgi.mapper
        self._setup_routes(mapper)


    def _setup_routes(self, mapper):
        path_stats = '/stats'
        requirements = {'switchid': '[0-9a-fA-F]{16}', 'vlanid': '[0-9]+'}

      # --- Rutele pentru API-ul OpenFlow (StatsController) ---
        routes = {
            "switches": ("get_dpids", "GET"),
            "desc/{dpid}": ("get_desc_stats", "GET"),
            "flowdesc/{dpid} POST": ("get_flow_desc", "POST"),
            "flow/{dpid}": ("get_flow_stats", "GET"),
            "flow/{dpid} POST": ("get_flow_stats", "POST"),
            "aggregateflow/{dpid}": ("get_aggregate_flow_stats", "GET"),
            "aggregateflow/{dpid} POST": ("get_aggregate_flow_stats", "POST"),
            "table/{dpid}": ("get_table_stats", "GET"),
            "tablefeatures/{dpid}": ("get_table_features", "GET"),
            "port/{dpid}": ("get_port_stats", "GET"),
            "port/{dpid}/{port}": ("get_port_stats", "GET"),
            "queue/{dpid}": ("get_queue_stats", "GET"),
            "queue/{dpid}/{port}": ("get_queue_stats", "GET"),
            "queue/{dpid}/{port}/{queue_id}": ("get_queue_stats", "GET"),
            "queueconfig/{dpid}": ("get_queue_config", "GET"),
            "queueconfig/{dpid}/{port}": ("get_queue_config", "GET"),
            "queuedesc/{dpid}": ("get_queue_desc", "GET"),
            "queuedesc/{dpid}/{port}": ("get_queue_desc", "GET"),
            "queuedesc/{dpid}/{port}/{queue_id}": ("get_queue_desc", "GET"),
            "meterfeatures/{dpid}": ("get_meter_features", "GET"),
            "meterconfig/{dpid}": ("get_meter_config", "GET"),
            "meterconfig/{dpid}/{meter_id}": ("get_meter_config", "GET"),
            "meterdesc/{dpid}": ("get_meter_desc", "GET"),
            "meterdesc/{dpid}/{meter_id}": ("get_meter_desc", "GET"),
            "meter/{dpid}": ("get_meter_stats", "GET"),
            "meter/{dpid}/{meter_id}": ("get_meter_stats", "GET"),
            "groupfeatures/{dpid}": ("get_group_features", "GET"),
            "groupdesc/{dpid}": ("get_group_desc", "GET"),
            "groupdesc/{dpid}/{group_id}": ("get_group_desc", "GET"),
            "group/{dpid}": ("get_group_stats", "GET"),
            "group/{dpid}/{group_id}": ("get_group_stats", "GET"),
            "portdesc/{dpid}": ("get_port_desc", "GET"),
            "portdesc/{dpid}/{port_no}": ("get_port_desc", "GET"),
            "role/{dpid}": ("get_role", "GET"),
            "flowentry/{cmd}": ("mod_flow_entry", "POST"),
            "flowentry/clear/{dpid}": ("delete_flow_entry", "DELETE"),
            "meterentry/{cmd}": ("mod_meter_entry", "POST"),
            "groupentry/{cmd}": ("mod_group_entry", "POST"),
            "portdesc/{cmd}": ("mod_port_behavior", "POST"),
            "experimenter/{dpid}": ("send_experimenter", "POST"),
            "role": ("set_role", "POST"),
        }
        for route, (action, method) in routes.items():
            if hasattr(MyStatsController, action):
                mapper.connect('stats', f"{path_stats}/{route}",
                               controller=MyStatsController, action=action,
                               conditions=dict(method=[method]))
            else:
                print(f"⚠️ Method '{action}' not found in StatsController, route {route} not registered.")

    @set_ev_cls([ofp_event.EventOFPStatsReply,
                 ofp_event.EventOFPDescStatsReply,
                 ofp_event.EventOFPFlowStatsReply,
                 ofp_event.EventOFPAggregateStatsReply,
                 ofp_event.EventOFPTableStatsReply,
                 ofp_event.EventOFPTableFeaturesStatsReply,
                 ofp_event.EventOFPPortStatsReply,
                 ofp_event.EventOFPQueueStatsReply,
                 ofp_event.EventOFPQueueDescStatsReply,
                 ofp_event.EventOFPMeterStatsReply,
                 ofp_event.EventOFPMeterFeaturesStatsReply,
                 ofp_event.EventOFPMeterConfigStatsReply,
                 ofp_event.EventOFPGroupStatsReply,
                 ofp_event.EventOFPGroupFeaturesStatsReply,
                 ofp_event.EventOFPGroupDescStatsReply,
                 ofp_event.EventOFPPortDescStatsReply
                 ], MAIN_DISPATCHER)
    def stats_reply_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath

        if dp.id not in self.waiters:
            return
        if msg.xid not in self.waiters[dp.id]:
            return
        lock, msgs = self.waiters[dp.id][msg.xid]
        msgs.append(msg)

        flags = 0
        if dp.ofproto.OFP_VERSION == ofproto_v1_0.OFP_VERSION:
            flags = dp.ofproto.OFPSF_REPLY_MORE
        elif dp.ofproto.OFP_VERSION == ofproto_v1_2.OFP_VERSION:
            flags = dp.ofproto.OFPSF_REPLY_MORE
        elif dp.ofproto.OFP_VERSION >= ofproto_v1_3.OFP_VERSION:
            flags = dp.ofproto.OFPMPF_REPLY_MORE

        if msg.flags & flags:
            return
        del self.waiters[dp.id][msg.xid]
        lock.set()

    @set_ev_cls([ofp_event.EventOFPSwitchFeatures,
                 ofp_event.EventOFPQueueGetConfigReply,
                 ofp_event.EventOFPRoleReply,
                 ], MAIN_DISPATCHER)
    def features_reply_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath

        if dp.id not in self.waiters:
            return
        if msg.xid not in self.waiters[dp.id]:
            return
        lock, msgs = self.waiters[dp.id][msg.xid]
        msgs.append(msg)

        del self.waiters[dp.id][msg.xid]
        lock.set()