from flask import Flask, jsonify

app = Flask(__name__)

SERVERS = [
    {"id": 1, "hostname": "web-prod-01", "ip": "10.0.0.1", "status": "up"},
    {"id": 2, "hostname": "db-prod-01", "ip": "10.0.0.2", "status": "down"}
]


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé"""
    return jsonify({"status": "OK", "version": "1.0"})


@app.route('/api/v1/servers', methods=['GET'])
def list_servers():
    """Endpoint pour lister tous les serveurs"""
    return jsonify({
        "servers": SERVERS,
        "count": len(SERVERS)
    })


@app.route('/api/v1/servers/<int:server_id>', methods=['GET'])
def get_server(server_id):
    """Endpoint pour obtenir un serveur par son ID"""
    server = next((s for s in SERVERS if s["id"] == server_id), None)
    
    if server is None:
        return jsonify({"error": "Server not found"}), 404
    
    return jsonify(server)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
