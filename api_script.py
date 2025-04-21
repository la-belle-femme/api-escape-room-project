#!/usr/bin/env python3

import requests
import json
import csv
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
BASE_URL = "https://2os8c32q80.execute-api.us-east-1.amazonaws.com/prod"
LOGIN_ENDPOINT = "/login"
COMPLIANCE_ENDPOINT = "/compliance/posture"

# Credentials - these should be passed as environment variables
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID", "testuser")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY", "testpassword")

def make_login_request():
    """
    Make a login request to obtain an authentication token.
    """
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    
    # Request payload
    payload = {
        "username": ACCESS_KEY_ID,
        "password": SECRET_ACCESS_KEY
    }
    
    logger.info("Making login request...")
    
    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response and extract the token
        response_data = response.json()
        logger.info(f"Login response: {response_data}")
        token = response_data.get("token")
        
        if not token:
            raise ValueError("Token not found in the response")
        
        logger.info("Login successful, token received")
        return token
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Login request failed: {e}")
        # Print response content if available
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        raise

def make_compliance_request(token):
    """
    Make a request to the compliance endpoint using the authentication token.
    """
    # Add query parameters
    params = {
        "timeType": "relative",
        "timeAmount": "15",
        "timeUnit": "minute"
    }
    
    compliance_url = f"{BASE_URL}{COMPLIANCE_ENDPOINT}"
    
    # Headers based on the curl command
    headers = {
        "token": token,
        "content-type": "application/json",
        "accept": "application/json; charset=UTF-8"
    }
    
    logger.info("Making compliance request...")
    logger.info(f"Using URL: {compliance_url}")
    logger.info(f"Using params: {params}")
    logger.info(f"Using headers: {headers}")
    
    try:
        response = requests.get(compliance_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        compliance_data = response.json()
        logger.info("Compliance data received successfully")
        return compliance_data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Compliance request failed: {e}")
        # Print response content if available
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        raise

def save_to_csv(data, filename="compliance_data.csv"):
    """
    Save the compliance data to a CSV file.
    """
    # Ensure output directory exists
    output_dir = os.environ.get("OUTPUT_DIR", "/data")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    
    # Ensure the data is a list of dictionaries
    if not isinstance(data, list):
        if isinstance(data, dict):
            data = [data]
        else:
            raise ValueError("Data must be a dictionary or a list of dictionaries")
    
    # Get the fieldnames from the first item if data is not empty
    if data:
        fieldnames = data[0].keys()
    else:
        logger.warning("No data to save")
        return None
    
    logger.info(f"Saving data to {file_path}...")
    
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Data successfully saved to {file_path}")
        return file_path
    
    except Exception as e:
        logger.error(f"Error saving data to CSV: {e}")
        raise

def main():
    """
    Main function to orchestrate the API calls and save the data.
    """
    try:
        # Step 1: Get the authentication token
        token = make_login_request()
        
        # Step 2: Get the compliance data
        compliance_data = make_compliance_request(token)
        
        # Step 3: Save the compliance data to a CSV file
        csv_file = save_to_csv(compliance_data)
        
        logger.info(f"Process completed successfully. Data saved to {csv_file}")
        return csv_file
    
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")
        raise

if __name__ == "__main__":
    main()
