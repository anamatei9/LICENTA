// Wait for document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the response area
    const responseArea = document.getElementById('api-response');
    
    /**
     * Common function to make API calls with proper error handling
     * @param {string} endpoint - API endpoint to call
     * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
     * @param {object|null} data - Request body data (for POST/PUT)
     */
    async function callApi(endpoint, method = 'GET', data = null) {
        // Show loading indicator
        responseArea.textContent = 'Loading...';
        responseArea.classList.add('loading');
        
        try {
            // Prepare request options
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                credentials: 'same-origin' // Important for cookie-based authentication
            };
            
            // Add request body for POST/PUT/DELETE requests
            if (data && ['POST', 'PUT', 'DELETE'].includes(method)) {
                options.body = JSON.stringify(data);
            }
            
            // Make the API call
            const response = await fetch(endpoint, options);
            
            // Check if response is OK
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`API Error (${response.status}): ${errorText}`);
            }
            
            // Parse and display response
            const responseData = await response.json();
            responseArea.textContent = JSON.stringify(responseData, null, 2);
            responseArea.classList.remove('loading');
            responseArea.classList.remove('error');
            
            return responseData;
        } catch (error) {
            // Display error message
            responseArea.textContent = `Error: ${error.message}`;
            responseArea.classList.remove('loading');
            responseArea.classList.add('error');
            console.error(error);
        }
    }
    
    /**
     * Helper to get value from an input element
     * @param {string} id - Element ID
     * @returns {string} - Element value or empty string if not found
     */
    function getValue(id) {
        const element = document.getElementById(id);
        return element ? element.value.trim() : '';
    }
    
    /**
     * Helper to get JSON from textarea
     * @param {string} id - Element ID
     * @returns {object|null} - Parsed JSON or null if invalid
     */
    function getJson(id) {
        try {
            const element = document.getElementById(id);
            if (!element || !element.value.trim()) return null;
            return JSON.parse(element.value.trim());
        } catch (error) {
            responseArea.textContent = `Error parsing JSON: ${error.message}`;
            responseArea.classList.add('error');
            return null;
        }
    }
    
    // ============= SWITCH INFORMATION =============
    
    // Get list of switches
    document.getElementById('get-switches').addEventListener('click', function() {
        callApi('/stats/switches');
    });
    
    // Get switch description
    document.getElementById('switch-desc').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/desc/${dpid}`);
    });
    
    // Get table stats
    document.getElementById('table-stats').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/table/${dpid}`);
    });
    
    // Table features
    document.getElementById('table-features').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/tablefeatures/${dpid}`);
    });
    
    // Port stats
    document.getElementById('port-stats').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/port/${dpid}`);
    });
    
    // Port description
    document.getElementById('port-desc').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/portdesc/${dpid}`);
    });
    
    // Queue stats
    document.getElementById('queue-stats').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/queue/${dpid}`);
    });
    
    // Queue config
    document.getElementById('queue-config').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/queueconfig/${dpid}`);
    });
    
    // Queue description
    document.getElementById('queue-desc').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/queuedesc/${dpid}`);
    });
    
    // Meter features
    document.getElementById('meter-features').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/meterfeatures/${dpid}`);
    });
    
    // Meter config
    document.getElementById('meter-config').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/meterconfig/${dpid}`);
    });
    
    // Meter description
    document.getElementById('meter-desc').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/meterdesc/${dpid}`);
    });
    
    // Meter stats
    document.getElementById('meter-stats').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/meter/${dpid}`);
    });
    
    // Group features
    document.getElementById('group-features').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/groupfeatures/${dpid}`);
    });
    
    // Group descriptions
    document.getElementById('group-desc').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/groupdesc/${dpid}`);
    });
    
    // Group stats
    document.getElementById('group-stats').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/group/${dpid}`);
    });
    
    // Controller role
    document.getElementById('controller-role').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/role/${dpid}`);
    });
    
    // Clear flow entries
    document.getElementById('clear-flows').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/flowentry/clear/${dpid}`, 'DELETE');
    });
    
    // ============= SPECIFIC PORT STATS =============
    
    // Get specific port stats
    document.getElementById('specific-port-stats').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        const port = getValue('port-number');
        if (!dpid || !port) {
            responseArea.textContent = 'Error: Please enter both Switch DPID and Port Number';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/port/${dpid}/${port}`);
    });
    
    // Get specific port description
    document.getElementById('specific-port-desc').addEventListener('click', function() {
        const dpid = getValue('switch-dpid');
        const port = getValue('port-number');
        if (!dpid || !port) {
            responseArea.textContent = 'Error: Please enter both Switch DPID and Port Number';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/portdesc/${dpid}/${port}`);
    });
    
    // ============= FLOW MANAGEMENT =============
    
    // Get all flows
    document.getElementById('get-flows').addEventListener('click', function() {
        const dpid = getValue('flow-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/stats/flow/${dpid}`);
    });
    
    // Add flow
    document.getElementById('submit-flow').addEventListener('click', function() {
        const dpid = getValue('flow-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        
        // Build flow data from form inputs
        const flow = {
            dpid: dpid,
            priority: getValue('flow-priority') || 100,
            match: {},
            actions: []
        };
        
        // Add match criteria if specified
        const inPort = getValue('flow-in-port');
        const srcMac = getValue('flow-src-mac');
        const dstMac = getValue('flow-dst-mac');
        const srcIp = getValue('flow-src-ip');
        const dstIp = getValue('flow-dst-ip');
        
        if (inPort) flow.match.in_port = parseInt(inPort);
        if (srcMac) flow.match.dl_src = srcMac;
        if (dstMac) flow.match.dl_dst = dstMac;
        if (srcIp) flow.match.nw_src = srcIp;
        if (dstIp) flow.match.nw_dst = dstIp;
        
        // Add output action if specified
        const outPort = getValue('flow-out-port');
        if (outPort) flow.actions.push({
            type: 'OUTPUT',
            port: parseInt(outPort)
        });
        
        // Send flow data to API
        callApi(`/stats/flowentry/add`, 'POST', flow);
    });
    
    // Delete flow
    document.getElementById('delete-flow').addEventListener('click', function() {
        const dpid = getValue('flow-dpid');
        if (!dpid) {
            responseArea.textContent = 'Error: Please enter a Switch DPID';
            responseArea.classList.add('error');
            return;
        }
        
        // Build flow data from form inputs (similar to add but for delete)
        const flow = {
            dpid: dpid,
            match: {}
        };
        
        // Add match criteria if specified
        const inPort = getValue('flow-in-port');
        const srcMac = getValue('flow-src-mac');
        const dstMac = getValue('flow-dst-mac');
        const srcIp = getValue('flow-src-ip');
        const dstIp = getValue('flow-dst-ip');
        
        if (inPort) flow.match.in_port = parseInt(inPort);
        if (srcMac) flow.match.dl_src = srcMac;
        if (dstMac) flow.match.dl_dst = dstMac;
        if (srcIp) flow.match.nw_src = srcIp;
        if (dstIp) flow.match.nw_dst = dstIp;
        
        // Send delete request
        callApi(`/stats/flowentry/delete`, 'POST', flow);
    });
    
    // ============= FIREWALL MANAGEMENT =============
    
    // Get firewall status
    document.getElementById('get-firewall-status').addEventListener('click', function() {
        callApi('/firewall/module/status');
    });
    
    // Get firewall rules
    document.getElementById('get-firewall-rules').addEventListener('click', function() {
        const switchId = getValue('switchid');
        if (!switchId) {
            responseArea.textContent = 'Error: Please enter a Switch ID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/firewall/rules/${switchId}`);
    });
    
    // Enable firewall
    document.getElementById('enable-firewall').addEventListener('click', function() {
        const switchId = getValue('switchid');
        if (!switchId) {
            responseArea.textContent = 'Error: Please enter a Switch ID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/firewall/module/enable/${switchId}`, 'PUT');
    });
    
    // Disable firewall
    document.getElementById('disable-firewall').addEventListener('click', function() {
        const switchId = getValue('switchid');
        if (!switchId) {
            responseArea.textContent = 'Error: Please enter a Switch ID';
            responseArea.classList.add('error');
            return;
        }
        callApi(`/firewall/module/disable/${switchId}`, 'PUT');
    });
    
    // Add firewall rule
    document.getElementById('submit-firewall-rule').addEventListener('click', function() {
        const switchId = getValue('switchid');
        if (!switchId) {
            responseArea.textContent = 'Error: Please enter a Switch ID';
            responseArea.classList.add('error');
            return;
        }
        
        // Build firewall rule data from form inputs
        const rule = {
            priority: 100,  // Default priority
            action: getValue('fw-action') || 'DENY'
        };
        
        // Add match criteria if specified
        const srcIp = getValue('fw-src-ip');
        const dstIp = getValue('fw-dst-ip');
        const protocol = getValue('fw-protocol');
        const srcPort = getValue('fw-src-port');
        const dstPort = getValue('fw-dst-port');
        
        if (srcIp) rule.nw_src = srcIp;
        if (dstIp) rule.nw_dst = dstIp;
        if (protocol) rule.nw_proto = protocol;
        
        // Add ports only if protocol is TCP or UDP
        if ((protocol === 'TCP' || protocol === 'UDP') && srcPort) {
            rule.tp_src = parseInt(srcPort);
        }
        if ((protocol === 'TCP' || protocol === 'UDP') && dstPort) {
            rule.tp_dst = parseInt(dstPort);
        }
        
        // Send rule data to API
        callApi(`/firewall/rules/${switchId}`, 'POST', rule);
    });
    
    // Delete firewall rule
    document.getElementById('delete-firewall-rule').addEventListener('click', function() {
        const switchId = getValue('switchid');
        if (!switchId) {
            responseArea.textContent = 'Error: Please enter a Switch ID';
            responseArea.classList.add('error');
            return;
        }
        
        // Get rule ID for deletion
        const ruleId = getValue('rule-id');
        if (!ruleId) {
            responseArea.textContent = 'Error: Please enter a Rule ID to delete';
            responseArea.classList.add('error');
            return;
        }
        
        // Send delete request
        callApi(`/firewall/rules/${switchId}`, 'DELETE', { rule_id: parseInt(ruleId) });
    });
    
    // ============= TOPOLOGY INFORMATION =============
    
    // Get network topology information
    document.getElementById('get-topology').addEventListener('click', function() {
        callApi('/stats/topology/switches');
    });
    
    // Get links information
    document.getElementById('get-links').addEventListener('click', function() {
        callApi('/stats/topology/links');
    });
    
    // Get hosts information
    document.getElementById('get-hosts').addEventListener('click', function() {
        callApi('/stats/topology/hosts');
    });
});