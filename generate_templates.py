import os

base_dir = r"c:\uknown\templates"

def write(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write("base.html", """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini SOC Platform</title>
    <!-- Modern Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --sidebar-bg: #1e293b;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.1);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.1);
            --border: #334155;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        .sidebar {
            width: 260px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 20px 0;
        }

        .sidebar h2 {
            padding: 0 20px;
            font-size: 1.25rem;
            color: var(--text-primary);
            margin-bottom: 30px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        
        .sidebar h2 span {
            color: var(--accent);
        }

        .nav-link {
            padding: 12px 20px;
            color: var(--text-secondary);
            text-decoration: none;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .nav-link:hover {
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--accent);
            border-left: 4px solid var(--accent);
        }

        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }

        .header {
            background-color: var(--card-bg);
            padding: 20px 30px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .content {
            padding: 30px;
        }

        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 24px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }

        h1, h2, h3 { margin-top: 0; }

        .btn {
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-block;
        }

        .btn:hover { background-color: var(--accent-hover); }
        .btn.danger { background-color: var(--danger); }
        .btn.danger:hover { background-color: #dc2626; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th, td {
            text-align: left;
            padding: 14px 16px;
            border-bottom: 1px solid var(--border);
        }

        th {
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        tr:hover { background-color: rgba(255, 255, 255, 0.02); }

        .badge {
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge.critical { background-color: var(--danger-bg); color: var(--danger); border: 1px solid var(--danger); }
        .badge.high { background-color: var(--danger-bg); color: var(--danger); border: 1px solid rgba(239,68,68,0.3); }
        .badge.medium { background-color: var(--warning-bg); color: var(--warning); border: 1px solid rgba(245,158,11,0.3); }
        .badge.low { background-color: var(--success-bg); color: var(--success); border: 1px solid rgba(16,185,129,0.3);}
        
        input, select, textarea {
            width: 100%;
            padding: 10px;
            background-color: var(--bg-color);
            border: 1px solid var(--border);
            color: var(--text-primary);
            border-radius: 6px;
            font-family: inherit;
            margin-bottom: 15px;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Mini <span>SOC</span></h2>
        <a href="{% url 'dashboard_index' %}" class="nav-link">Dashboard</a>
        <a href="{% url 'logs_index' %}" class="nav-link">Log Management</a>
        <a href="{% url 'detection_index' %}" class="nav-link">Detection Engine</a>
        <a href="{% url 'alerts_index' %}" class="nav-link">Alerts</a>
        <a href="{% url 'incidents_index' %}" class="nav-link">Incidents</a>
        <a href="{% url 'reports_index' %}" class="nav-link">Reports</a>
    </div>

    <div class="main-content">
        <div class="header">
            <h3>{% block page_title %}Overview{% endblock %}</h3>
            <div>
                User: {{ request.user.username }} | <a href="{% url 'admin:logout' %}?next=/" style="color: var(--accent);">Logout</a>
            </div>
        </div>
        <div class="content">
            {% block content %}
            {% endblock %}
        </div>
    </div>
</body>
</html>
""")

write("dashboard.html", """
{% extends 'base.html' %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}
<style>
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; margin-bottom: 30px; }
    .stat-value { font-size: 2.5rem; font-weight: 700; margin: 10px 0; }
    .stat-label { color: var(--text-secondary); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; }
</style>

<div class="grid">
    <div class="card" style="border-left: 4px solid var(--accent);">
        <div class="stat-label">Total Alerts</div>
        <div class="stat-value">{{ total_alerts }}</div>
    </div>
    <div class="card" style="border-left: 4px solid var(--danger);">
        <div class="stat-label">High/Critical Alerts</div>
        <div class="stat-value" style="color: var(--danger);">{{ high_alerts }}</div>
    </div>
    <div class="card" style="border-left: 4px solid var(--warning);">
        <div class="stat-label">Open Incidents</div>
        <div class="stat-value" style="color: var(--warning);">{{ open_incidents }}</div>
    </div>
</div>

<div class="card">
    <h3>Recent Alerts</h3>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>IP Address</th>
                <th>Attack Type</th>
                <th>Severity</th>
            </tr>
        </thead>
        <tbody>
            {% for alert in recent_alerts %}
            <tr>
                <td>{{ alert.timestamp|date:"Y-m-d H:i:s" }}</td>
                <td>{{ alert.ip_address }}</td>
                <td>{{ alert.attack_type }}</td>
                <td><span class="badge {{ alert.severity|lower }}">{{ alert.severity }}</span></td>
            </tr>
            {% empty %}
            <tr><td colspan="4" style="text-align: center; color: var(--text-secondary);">No recent alerts.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""")

write("logs.html", """
{% extends 'base.html' %}
{% block page_title %}Log Management{% endblock %}
{% block content %}
<div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3>Application Logs</h3>
        <div style="display: flex; gap: 10px;">
            <a href="{% url 'logs_index' %}" class="btn">Refresh</a>
            <form method="POST" style="margin: 0;">
                {% csrf_token %}
                <button type="submit" name="clear" class="btn danger">Clear Logs</button>
            </form>
        </div>
    </div>
    
    <div style="max-height: 600px; overflow-y: auto;">
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>IP Address</th>
                    <th>Event</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for log in logs %}
                <tr>
                    <td style="color: var(--text-secondary);">{{ log.timestamp }}</td>
                    <td style="font-family: monospace;">{{ log.ip }}</td>
                    <td>{{ log.event }}</td>
                    <td>
                        <span style="color: {% if log.status == 'Success' %}var(--success){% else %}var(--danger){% endif %}">
                            {{ log.status }}
                        </span>
                    </td>
                </tr>
                {% empty %}
                <tr><td colspan="4" style="text-align: center; color: var(--text-secondary);">No logs found in logs.txt.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
""")

write("detection.html", """
{% extends 'base.html' %}
{% block page_title %}Detection Engine{% endblock %}
{% block content %}
<div class="card">
    <h3>Threat Detection</h3>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">
        Run the detection engine to analyze logs and identify potential threats. 
        Current rules implemented: <strong>Brute Force Attack Detection</strong> (5+ failed logins from same IP).
    </p>
    
    <form method="POST">
        {% csrf_token %}
        <button type="submit" class="btn">Run Detection Analysis</button>
    </form>
    
    {% if results %}
    <div style="margin-top: 30px;">
        <h4>Analysis Results:</h4>
        <div style="background-color: var(--bg-color); border: 1px solid var(--border); border-radius: 8px; padding: 20px;">
            {% for r in results %}
                <div style="margin-bottom: 10px; display: flex; align-items: center;">
                    {% if 'Detected' in r %}
                        <span style="color: var(--danger); margin-right: 10px;">⚠️</span>
                    {% else %}
                        <span style="color: var(--success); margin-right: 10px;">✅</span>
                    {% endif %}
                    {{ r }}
                </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
""")

write("alerts.html", """
{% extends 'base.html' %}
{% block page_title %}Alerts{% endblock %}
{% block content %}
<div class="card">
    <h3>Generated Alerts</h3>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>IP Address</th>
                <th>Attack Type</th>
                <th>Severity</th>
            </tr>
        </thead>
        <tbody>
            {% for alert in alerts %}
            <tr>
                <td>#{{ alert.id }}</td>
                <td>{{ alert.timestamp|date:"Y-m-d H:i:s" }}</td>
                <td style="font-family: monospace;">{{ alert.ip_address }}</td>
                <td>{{ alert.attack_type }}</td>
                <td><span class="badge {{ alert.severity|lower }}">{{ alert.severity }}</span></td>
            </tr>
            {% empty %}
            <tr><td colspan="5" style="text-align: center; color: var(--text-secondary);">No alerts have been generated.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""")

write("incidents.html", """
{% extends 'base.html' %}
{% block page_title %}Incident Management{% endblock %}
{% block content %}
<div class="card">
    <h3>Active Incidents</h3>
    <table>
        <thead>
            <tr>
                <th>Incident ID</th>
                <th>Alert Info</th>
                <th>Created At</th>
                <th>Status</th>
                <th>Notes</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for incident in incidents %}
            <tr>
                <td>INC-{{ incident.id }}</td>
                <td>{{ incident.alert.attack_type }} ({{ incident.alert.ip_address }})</td>
                <td>{{ incident.created_at|date:"Y-m-d H:i" }}</td>
                <td>
                    <span style="color: {% if incident.status == 'Open' %}var(--danger){% elif incident.status == 'In Progress' %}var(--warning){% else %}var(--success){% endif %}">
                        {{ incident.status }}
                    </span>
                </td>
                <td style="max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {{ incident.notes|default:"No notes added." }}
                </td>
                <td>
                    <button class="btn" onclick="document.getElementById('modal-{{ incident.id }}').style.display='block'" style="padding: 6px 12px; font-size: 0.8rem;">Manage</button>
                    
                    <!-- Modal for Editing Incident -->
                    <div id="modal-{{ incident.id }}" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:100;">
                        <div style="background:var(--card-bg); width:400px; margin: 100px auto; padding: 25px; border-radius: 12px; border: 1px solid var(--border);">
                            <h3 style="margin-top: 0;">Update Incident INC-{{ incident.id }}</h3>
                            <form method="POST">
                                {% csrf_token %}
                                <input type="hidden" name="incident_id" value="{{ incident.id }}">
                                
                                <label style="display:block; margin-bottom:5px; color:var(--text-secondary);">Status</label>
                                <select name="status">
                                    {% for value, label in status_choices %}
                                    <option value="{{ value }}" {% if incident.status == value %}selected{% endif %}>{{ label }}</option>
                                    {% endfor %}
                                </select>
                                
                                <label style="display:block; margin-bottom:5px; color:var(--text-secondary);">Investigation Notes</label>
                                <textarea name="notes" rows="4">{{ incident.notes }}</textarea>
                                
                                <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 15px;">
                                    <button type="button" class="btn" style="background: transparent; border: 1px solid var(--border);" onclick="document.getElementById('modal-{{ incident.id }}').style.display='none'">Cancel</button>
                                    <button type="submit" class="btn">Save Changes</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </td>
            </tr>
            {% empty %}
            <tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No incidents tracked.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""")

write("reports.html", """
{% extends 'base.html' %}
{% block page_title %}Reports & Analytics{% endblock %}
{% block content %}
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
    <div class="card">
        <h3>Alerts by Severity</h3>
        <canvas id="severityChart"></canvas>
    </div>
    
    <div class="card">
        <h3>Top Attacking IPs</h3>
        <canvas id="ipChart"></canvas>
    </div>
</div>

<script>
    const severityLabels = JSON.parse('{{ severity_labels|safe }}');
    const severityData = JSON.parse('{{ severity_data|safe }}');
    const bgColors = [
        'rgba(16, 185, 129, 0.6)',  // Low
        'rgba(245, 158, 11, 0.6)',  // Medium
        'rgba(239, 68, 68, 0.6)',   // High
        'rgba(185, 28, 28, 0.6)'    // Critical
    ];

    const ctx = document.getElementById('severityChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: severityLabels,
            datasets: [{
                data: severityData,
                backgroundColor: bgColors,
                borderWidth: 0
            }]
        },
        options: {
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94a3b8' } }
            }
        }
    });

    const ipLabels = JSON.parse('{{ ips_labels|safe }}');
    const ipData = JSON.parse('{{ ips_data|safe }}');

    const ctx2 = document.getElementById('ipChart').getContext('2d');
    new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: ipLabels,
            datasets: [{
                label: 'Alert Count',
                data: ipData,
                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                borderRadius: 4
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, ticks: { color: '#94a3b8', stepSize: 1 }, grid: { color: '#334155' } },
                x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
</script>
{% endblock %}
""")

print("Done generating templates.")
