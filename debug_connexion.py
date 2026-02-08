#!/usr/bin/env python3
import connexion
import os
import sys

os.chdir('/usr/src/app')
print(f"Working directory: {os.getcwd()}")
print(f"swagger_server/swagger/ exists: {os.path.isdir('swagger_server/swagger/')}")
print(f"swagger.yaml exists: {os.path.isfile('swagger_server/swagger/swagger.yaml')}")

app = connexion.App(__name__, specification_dir='./swagger_server/swagger/')
print("✓ App created")

try:
    app.add_api('swagger.yaml', pythonic_params=True)
    print("✓ API added successfully")
    
    # List all routes
    print("\nRegistered routes:")
    for rule in app.app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
        
except Exception as e:
    print(f"✗ Error adding API: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
