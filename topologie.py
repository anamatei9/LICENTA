from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController

class SDNFirewallTopo(Topo):

    def build(self):
        # Adăugăm switch-ul central (Core-Firewall) cu dpid specific
        core_fw = self.addSwitch('s1', protocols='OpenFlow13', dpid="0000000000000001")

        # Adăugăm switch-urile Load Balancer cu dpids specifice
        lb1 = self.addSwitch('s2', protocols='OpenFlow13', dpid="0000000000000002")
        lb2 = self.addSwitch('s3', protocols='OpenFlow13', dpid="0000000000000003")

        # Adăugăm switch-urile pentru host-uri cu dpids specifice
        sw0 = self.addSwitch('s4', protocols='OpenFlow13', dpid="a000000000000004")
        sw1 = self.addSwitch('s5', protocols='OpenFlow13', dpid="0000000000000005")
        sw3 = self.addSwitch('s6', protocols='OpenFlow13', dpid="0000000000000006")
        sw4 = self.addSwitch('s7', protocols='OpenFlow13', dpid="0000000000000007")


        # Adăugăm host-urile (Laptop-uri)
        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/24")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/24")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4/24")
        h5 = self.addHost('h5', mac="00:00:00:00:00:05", ip="10.0.0.5/24")
        h6 = self.addHost('h6', mac="00:00:00:00:00:06", ip="10.0.0.6/24")
        h7 = self.addHost('h7', mac="00:00:00:00:00:07", ip="10.0.0.7/24")

        # Adăugăm serverele IDS, Ryu și un nod Internet simulat
        ids = self.addHost('ids', mac="00:00:00:00:00:08", ip="10.0.0.100/24")
        ryu = self.addHost('ryu', mac="00:00:00:00:00:09", ip="10.0.0.101/24")
        internet = self.addHost('internet', mac="00:00:00:00:00:10", ip="10.0.0.102/24")

        # Conectăm switch-ul Core-Firewall cu Load Balancer și servere
        self.addLink(core_fw, lb1)
        self.addLink(core_fw, lb2)
        self.addLink(core_fw, ids)
        self.addLink(core_fw, ryu)
        self.addLink(core_fw, internet)

        # Conectăm Load Balancer-urile la switch-uri de acces
        self.addLink(lb1, sw0)
        self.addLink(lb1, sw1)
        self.addLink(lb2, sw3)
        self.addLink(lb2, sw4)

        # Conectăm host-urile la switch-uri
        self.addLink(sw0, h1)
        self.addLink(sw0, h2)
        self.addLink(sw1, h3)
        self.addLink(sw1, h4)
        self.addLink(sw3, h5)
        self.addLink(sw3, h6)
        self.addLink(sw4, h7)

if __name__ == '__main__':
    setLogLevel('info')
    
    # Inițializăm topologia
    topo = SDNFirewallTopo()
    
    # Definim controlerul Ryu
    c0 = RemoteController('c0', ip='127.0.0.1', port=6633)
    
    # Creăm și pornim rețeaua
    net = Mininet(topo=topo, controller=c0, switch=OVSSwitch)
    net.start()

    print("\n=== Rețeaua SDN este activă! ===")
    CLI(net)  # Interfața CLI Mininet

    net.stop()

