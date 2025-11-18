#!/usr/bin/env python3
"""
Flask API Integration Example

Demonstrates how to integrate ISO 27001 Toolkit into a Flask REST API.
Provides endpoints for risks, controls, and audit readiness.

Install:
    pip install flask flask-cors

Run:
    python flask_api.py
    # API available at http://localhost:5000

Endpoints:
    GET  /api/health              - API health check
    GET  /api/risks               - List all risks
    POST /api/risks               - Create new risk
    GET  /api/risks/<id>          - Get risk by ID
    GET  /api/controls            - List all controls
    GET  /api/controls/stats      - Control statistics
    GET  /api/audit/readiness     - Audit readiness assessment
    GET  /api/dashboard           - Dashboard data
"""

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from datetime import datetime
import logging

# Import ISO 27001 Toolkit
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.audit_helper import AuditHelper
from iso27001_toolkit.utils.validators import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize ISO 27001 managers
risk_manager = RiskManager()
controls_tracker = ControlsTracker()
audit_helper = AuditHelper()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'error': str(error)}), 422

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.0'
    })

# Risks endpoints
@app.route('/api/risks', methods=['GET'])
def get_risks():
    """
    Get all risks
    
    Query parameters:
        level (optional): Filter by level (critical, high, medium, low)
        category (optional): Filter by category
    """
    risks = risk_manager.get_all_risks()
    
    # Filter by level
    level = request.args.get('level')
    if level:
        risks = [r for r in risks if r.get('level') == level]
    
    # Filter by category
    category = request.args.get('category')
    if category:
        risks = [r for r in risks if r.get('category') == category]
    
    return jsonify({
        'count': len(risks),
        'risks': risks
    })

@app.route('/api/risks/<risk_id>', methods=['GET'])
def get_risk(risk_id):
    """Get a specific risk by ID"""
    risk = risk_manager.get_risk(risk_id)
    
    if not risk:
        abort(404, description=f"Risk {risk_id} not found")
    
    return jsonify(risk)

@app.route('/api/risks', methods=['POST'])
def create_risk():
    """
    Create a new risk
    
    Request body (JSON):
        {
            "title": "Risk title",
            "description": "Description",
            "probability": 3,
            "impact": 4,
            "category": "confidentiality"
        }
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'probability', 'impact', 'category']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")
    
    try:
        risk_id = risk_manager.add_risk(
            title=data['title'],
            description=data['description'],
            probability=data['probability'],
            impact=data['impact'],
            category=data['category'],
            treatment=data.get('treatment'),
            controls=data.get('controls', [])
        )
        
        risk = risk_manager.get_risk(risk_id)
        
        logger.info(f"Risk created: {risk_id}")
        
        return jsonify(risk), 201
        
    except ValidationError as e:
        raise e

@app.route('/api/risks/stats', methods=['GET'])
def get_risk_stats():
    """Get risk statistics"""
    stats = risk_manager.get_statistics()
    return jsonify(stats)

# Controls endpoints
@app.route('/api/controls', methods=['GET'])
def get_controls():
    """
    Get all controls
    
    Query parameters:
        status (optional): Filter by status
        category (optional): Filter by category (A.5, A.6, A.7, A.8)
    """
    controls = controls_tracker.get_all_controls()
    
    # Filter by status
    status = request.args.get('status')
    if status:
        controls = {
            k: v for k, v in controls.items()
            if v.get('status') == status
        }
    
    # Filter by category
    category = request.args.get('category')
    if category:
        controls = {
            k: v for k, v in controls.items()
            if k.startswith(category)
        }
    
    return jsonify({
        'count': len(controls),
        'controls': controls
    })

@app.route('/api/controls/<control_id>', methods=['GET'])
def get_control(control_id):
    """Get a specific control by ID"""
    control = controls_tracker.get_control(control_id)
    
    if not control:
        abort(404, description=f"Control {control_id} not found")
    
    return jsonify(control)

@app.route('/api/controls/stats', methods=['GET'])
def get_control_stats():
    """Get control implementation statistics"""
    stats = controls_tracker.get_statistics()
    return jsonify(stats)

# Audit endpoints
@app.route('/api/audit/readiness', methods=['GET'])
def get_audit_readiness():
    """Get audit readiness assessment"""
    assessment = audit_helper.assess_readiness()
    return jsonify(assessment)

@app.route('/api/audit/gaps', methods=['GET'])
def get_gaps():
    """Get gap analysis"""
    gaps = audit_helper.perform_gap_analysis()
    return jsonify({
        'count': len(gaps),
        'gaps': gaps
    })

# Dashboard endpoint
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """
    Get dashboard summary data
    
    Returns comprehensive overview of:
    - Risk statistics
    - Control statistics
    - Audit readiness
    """
    risk_stats = risk_manager.get_statistics()
    control_stats = controls_tracker.get_statistics()
    readiness = audit_helper.assess_readiness()
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'risks': risk_stats,
        'controls': control_stats,
        'audit_readiness': readiness
    })

# Documentation endpoint
@app.route('/api/docs', methods=['GET'])
def get_docs():
    """API documentation"""
    return jsonify({
        'endpoints': {
            'health': {
                'path': '/api/health',
                'method': 'GET',
                'description': 'API health check'
            },
            'risks': {
                'list': {
                    'path': '/api/risks',
                    'method': 'GET',
                    'description': 'List all risks',
                    'params': ['level', 'category']
                },
                'create': {
                    'path': '/api/risks',
                    'method': 'POST',
                    'description': 'Create new risk',
                    'body': ['title', 'description', 'probability', 'impact', 'category']
                },
                'get': {
                    'path': '/api/risks/<id>',
                    'method': 'GET',
                    'description': 'Get risk by ID'
                }
            },
            'controls': {
                'list': {
                    'path': '/api/controls',
                    'method': 'GET',
                    'params': ['status', 'category']
                },
                'stats': {
                    'path': '/api/controls/stats',
                    'method': 'GET'
                }
            },
            'audit': {
                'readiness': {
                    'path': '/api/audit/readiness',
                    'method': 'GET'
                },
                'gaps': {
                    'path': '/api/audit/gaps',
                    'method': 'GET'
                }
            },
            'dashboard': {
                'path': '/api/dashboard',
                'method': 'GET'
            }
        }
    })

if __name__ == '__main__':
    # Initialize tracker
    controls_tracker.initialize()
    
    print("\n" + "="*50)
    print("ISO 27001 Toolkit - Flask API Server")
    print("="*50)
    print("\nAPI Endpoints:")
    print("  - Health:     http://localhost:5000/api/health")
    print("  - Risks:      http://localhost:5000/api/risks")
    print("  - Controls:   http://localhost:5000/api/controls")
    print("  - Dashboard:  http://localhost:5000/api/dashboard")
    print("  - Docs:       http://localhost:5000/api/docs")
    print("\n" + "="*50 + "\n")
    
    # Run server
    app.run(debug=True, host='0.0.0.0', port=5000)
