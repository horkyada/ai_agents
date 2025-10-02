#!/usr/bin/env python3
"""
Homework 2 N8N Workflow Deployment Script

Simplified deployment script that:
1. Deploys all workflows from the ./workflows folder to N8N
2. Uses Docker-based N8N instance (no API key needed for local)
3. Provides clear feedback on deployment status

Usage:
    python deploy.py              # Deploy all workflows from ./workflows folder
    python deploy.py --clean      # Delete all workflows first, then deploy

Requirements:
    - Docker Compose running (docker-compose up -d)
    - N8N accessible at http://localhost:5678
    - pip install requests (or run: pip install -r requirements.txt)
"""

import requests
import json
import os
import glob
import sys
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class N8NDeployment:
    def __init__(self, base_url: str = None):
        """Initialize N8N deployment client"""
        self.base_url = (base_url or os.getenv("N8N_BASE_URL", "http://localhost:5678")).rstrip("/")
        self.session = requests.Session()

        # Check for API key in environment
        api_key = os.getenv("N8N_API_KEY")
        if api_key:
            self.session.headers.update({"X-N8N-API-KEY": api_key})
            print(f"🔑 Using API key authentication")
        else:
            print(f"🔓 No API key provided (trying without authentication)")

        print(f"🚀 N8N Deployment Tool")
        print(f"📍 Target: {self.base_url}")

        # Test connection
        self._test_connection()

    def _test_connection(self) -> None:
        """Test connection to N8N"""
        try:
            # Try to access N8N (for Docker setup, no auth needed)
            response = self.session.get(f"{self.base_url}/api/v1/workflows?limit=1")
            if response.status_code == 200:
                print("✅ Connected to N8N successfully")
                return
            elif response.status_code == 401:
                print("⚠️  N8N requires authentication - you may need to configure API key")
                return
            else:
                print(f"⚠️  N8N responded with status {response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to N8N at {self.base_url}")
            print(f"   Make sure Docker Compose is running: docker-compose up -d")
            print(f"   Error: {e}")
            sys.exit(1)

    def clean_workflow_json(self, workflow_data: Dict) -> Dict:
        """Clean workflow JSON for import by removing problematic fields"""
        cleaned = {
            "name": workflow_data.get("name", "Deployed Workflow"),
            "nodes": [],
            "connections": workflow_data.get("connections", {}),
            "settings": workflow_data.get("settings", {}),
            "staticData": workflow_data.get("staticData", {}),
        }

        # Clean nodes by removing IDs that might conflict
        for node in workflow_data.get("nodes", []):
            cleaned_node = dict(node)
            if "id" in cleaned_node:
                del cleaned_node["id"]
            cleaned["nodes"].append(cleaned_node)

        return cleaned

    def deploy_workflow(self, workflow_data: Dict) -> Dict:
        """Deploy a single workflow to N8N"""
        url = f"{self.base_url}/api/v1/workflows"

        # Clean the workflow data
        cleaned_data = self.clean_workflow_json(workflow_data)

        response = self.session.post(url, json=cleaned_data)

        return {
            "success": response.status_code in [200, 201],
            "status_code": response.status_code,
            "workflow_name": cleaned_data["name"],
            "response": response.json() if response.status_code in [200, 201] else response.text,
        }

    def get_all_workflows(self) -> List[Dict]:
        """Get all current workflows"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/workflows")
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else data.get("data", [])
            return []
        except:
            return []

    def delete_all_workflows(self) -> int:
        """Delete all workflows (for clean deployment)"""
        workflows = self.get_all_workflows()
        deleted_count = 0

        for workflow in workflows:
            workflow_id = workflow.get("id")
            if workflow_id:
                response = self.session.delete(f"{self.base_url}/api/v1/workflows/{workflow_id}")
                if response.status_code == 200:
                    deleted_count += 1
                    print(f"🗑️  Deleted: {workflow.get('name', 'Unknown')}")

        return deleted_count

    def deploy_workflows_from_folder(self, folder_path: str, clean_first: bool = False) -> Dict:
        """Deploy all workflows from a folder"""
        if not os.path.exists(folder_path):
            print(f"❌ Folder '{folder_path}' does not exist")
            return {"total": 0, "success": 0, "failed": 0}

        # Find all JSON files in the folder
        json_files = glob.glob(os.path.join(folder_path, "*.json"))

        if not json_files:
            print(f"❌ No JSON files found in {folder_path}")
            return {"total": 0, "success": 0, "failed": 0}

        print(f"\n📁 Found {len(json_files)} workflow file(s) to deploy")

        # Clean existing workflows if requested
        if clean_first:
            print(f"\n🧹 Cleaning existing workflows...")
            deleted = self.delete_all_workflows()
            print(f"🗑️  Deleted {deleted} existing workflow(s)")

        # Deploy each workflow
        print(f"\n🚀 Starting deployment...")
        print("=" * 50)

        success_count = 0
        failed_count = 0
        results = []

        for file_path in sorted(json_files):
            filename = os.path.basename(file_path)
            print(f"\n📦 Deploying: {filename}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    workflow_data = json.load(f)

                # Deploy the workflow
                result = self.deploy_workflow(workflow_data)

                if result["success"]:
                    print(f"✅ Success: {result['workflow_name']}")
                    if isinstance(result["response"], dict) and "id" in result["response"]:
                        print(f"   Workflow ID: {result['response']['id']}")
                    success_count += 1
                else:
                    print(f"❌ Failed: {result['workflow_name']}")
                    print(f"   Error ({result['status_code']}): {result['response']}")
                    failed_count += 1

                results.append({
                    "file": filename,
                    "workflow_name": result["workflow_name"],
                    "success": result["success"],
                    "status_code": result["status_code"],
                })

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
                failed_count += 1
                results.append({
                    "file": filename,
                    "success": False,
                    "error": str(e),
                })

        # Summary
        print(f"\n{'=' * 50}")
        print("🎯 DEPLOYMENT SUMMARY")
        print(f"{'=' * 50}")
        print(f"📊 Total files: {len(json_files)}")
        print(f"✅ Successfully deployed: {success_count}")
        if failed_count > 0:
            print(f"❌ Failed: {failed_count}")
        print(f"🌐 N8N Interface: {self.base_url}")
        print(f"{'=' * 50}")

        return {
            "total": len(json_files),
            "success": success_count,
            "failed": failed_count,
            "results": results,
        }


def main():
    """Main deployment function"""
    # Parse command line arguments
    clean_first = "--clean" in sys.argv

    print("🎯 Homework 2 - N8N Workflow Deployment")
    print("=" * 50)

    if clean_first:
        print("🧹 Clean deployment mode: Will delete existing workflows first")

    # Initialize deployer
    try:
        deployer = N8NDeployment()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)

    # Deploy workflows from ./workflows folder
    workflows_folder = os.path.join(os.path.dirname(__file__), "workflows")
    result = deployer.deploy_workflows_from_folder(workflows_folder, clean_first)

    if result["success"] > 0:
        print(f"\n🎉 Deployment completed successfully!")
        print(f"💡 Open {deployer.base_url} to see your workflows")
    else:
        print(f"\n💥 Deployment failed - check errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()