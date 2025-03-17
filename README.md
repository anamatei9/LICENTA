# RYUDOCS
## Endpoint-uri:
### ofctl_rest.py 
- interfață REST API pentru controlul și monitorizarea switch-urilor OpenFlow.

| Metodă | Endpoint | Descriere |
|--------|---------|-------------|
| `GET`  | `/stats/switches` | Listează toate switch-urile conectate |
| `GET`  | `/stats/desc/{dpid}` | Obține descrierea unui switch |
| `GET`  | `/stats/flow/{dpid}` | Obține intrările de flux ale unui switch |
| `POST` | `/stats/flowentry/add` | Adaugă o nouă intrare de flux |
| `POST` | `/stats/flowentry/delete` | Șterge o anumită intrare de flux |
| `POST` | `/stats/flowentry/modify` | Modifică o intrare de flux existentă |
| `GET`  | `/stats/port/{dpid}` | Obține statisticile pentru porturile unui switch |
| `GET`  | `/stats/queue/{dpid}/{port}` | Obține statisticile pentru coada unui port al switch-ului |
| `POST` | `/stats/groupentry/add` | Adaugă o nouă intrare de grup |
| `POST` | `/stats/groupentry/delete` | Șterge o intrare de grup |
| `POST` | `/stats/meterentry/add` | Adaugă o nouă intrare de metru |
| `POST` | `/stats/meterentry/delete` | Șterge o intrare de metru |



### rest_firewall.py 
- interfață REST API pentru gestionarea regulilor de firewall.

| Metodă | Endpoint | Descriere |
|--------|---------|-------------|
| `POST` | `/firewall/rules/{dpid}` | Adaugă o regulă de firewall pentru un switch |
| `GET`  | `/firewall/rules/{dpid}` | Obține regulile de firewall pentru un switch |
| `DELETE` | `/firewall/rules/{dpid}` | Șterge regulile de firewall pentru un switch |
| `POST` | `/firewall/module/enable/{dpid}` | Activează modulul de firewall pentru un switch |
| `POST` | `/firewall/module/disable/{dpid}` | Dezactivează modulul de firewall pentru un switch |
| `GET`  | `/firewall/module/status/{dpid}` | Obține starea modulului de firewall |


### rest_topology.py 
- interfață REST API pentru descoperirea și obținerea informațiilor despre topologia rețelei.

| Metodă | Endpoint | Descriere |
|--------|---------|-------------|
| `GET`  | `/v1.0/topology/switches` | Listează toate switch-urile descoperite |
| `GET`  | `/v1.0/topology/links` | Obține toate legăturile active din rețea |
| `GET`  | `/v1.0/topology/hosts` | Obține toate gazdele descoperite |

**Notă:**-`dpid` se referă la **identificatorul datapath** al unui switch OpenFlow./n- Endpoint-urile suportă cereri și răspunsuri bazate pe JSON.





