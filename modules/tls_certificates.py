"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import os
import shutil
from prompt_toolkit import prompt
import requests
import hashlib
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import binascii
from modules.file_transfer import mobile_exists, upload_to_dest
from modules.utility import ip_and_port_from_user_input

def convert_der_to_pem(der_file_path: str):
    """
    Converts a DER-encoded certificate file to PEM format.

    Args:
        der_file_path (str): The path to the input DER certificate file.
        pem_file_path (str): The path for the output PEM certificate file.
    """
    try:
        with open(der_file_path, "rb") as der_file:
            der_data = der_file.read()

        # Load the DER-encoded certificate
        certificate = x509.load_der_x509_certificate(der_data, default_backend())

        # Serialize the certificate to PEM format
        pem_data = certificate.public_bytes(serialization.Encoding.PEM)

        pem_file_path = der_file_path.replace('.der', '.pem')
        with open(pem_file_path, "wb") as pem_file:
            pem_file.write(pem_data)

        print(f"Successfully converted '{der_file_path}' to '{pem_file_path}'")
        return pem_file_path
        
    except FileNotFoundError:
        print(f"Error: The file '{der_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def calculate_subject_hash_old_from_pem(cert_pem_path=None, cert_bytes=None):
    """
    Calculates the OpenSSL -subject_hash_old for a given PEM certificate.
    Can take either a file path to a PEM certificate or the certificate bytes directly.

    Args:
        cert_pem_path (str, optional): Path to the PEM-encoded certificate file.
        cert_bytes (bytes, optional): PEM-encoded certificate content as bytes.

    Returns:
        str: The 8-character hexadecimal subject hash (old style), or None if an error occurs.
    """
    if cert_pem_path:
        try:
            with open(cert_pem_path, "rb") as f:
                cert_data = f.read()
        except FileNotFoundError:
            print(f"Error: Certificate file not found at {cert_pem_path}")
            return None
    elif cert_bytes:
        cert_data = cert_bytes
    else:
        print("Error: Either cert_pem_path or cert_bytes must be provided.")
        return None

    try:
        # Suppress UserWarning related to attribute length (e.g., for non-standard Burp certs)
        certificate = x509.load_pem_x509_certificate(cert_data, default_backend())

            # Get the DER-encoded subject name
        subject_der = certificate.subject.public_bytes(serialization.Encoding.DER)

        # Calculate the MD5 hash
        md5_hash = hashlib.md5(subject_der).digest()

        # Take the first 4 bytes and reverse their order (little-endian)
        reversed_bytes = md5_hash[0:4][::-1]

        # Convert to hexadecimal string
        hex_hash = binascii.hexlify(reversed_bytes).decode('ascii')

        return cert_pem_path.replace(os.path.split(cert_pem_path)[1],f"{hex_hash}.0")

    except ValueError as e:
        print(f"Error loading certificate: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during hash calculation: {e}")
        return None

def download_burp_root_cert(domain_ip, port):
    proxy_url = f"http://{domain_ip}:{port}/cert" 
    print(f"[+] Downloading Burp root certificate from {proxy_url}")    
    
    try:
        response = requests.get(proxy_url)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch certificate: {e}")
        print(f"[!] Please ensure Burp Suite is running and proxy listener is active on {proxy_url}")
        return

    cert_der_bytes = response.content

    # Validate if it's a DER certificate by attempting to load it
    try:
        # Load DER to check validity and convert to PEM
        certificate = x509.load_der_x509_certificate(cert_der_bytes, default_backend())
    except ValueError as e:
        print(f"[!] Error: The downloaded content does not appear to be a valid DER certificate: {e}")
        return

    dest_folder = os.path.join("results", "tls_certificates")
    os.makedirs(dest_folder, exist_ok=True)
    der_filename = "burp_root_cert.der"

    # Save .der file (as bytes, not string)
    with open(os.path.join(dest_folder, der_filename), "wb") as f:
        f.write(cert_der_bytes)
    print(f"[+] Saved DER certificate to {os.path.join(dest_folder, der_filename)}")

    return os.path.join(dest_folder, der_filename)

def install_burp_root_cert(user_input):
    """
    Downloads the Burp Suite root certificate and installs it in the Android system's cacerts directory.
    """
    print(user_input)
    domain_ip, port = ip_and_port_from_user_input(user_input)

    # Download the Burp root certificate
    cert_der_path = download_burp_root_cert(domain_ip, port)

    if not cert_der_path:
        print("[!] Failed to download Burp root certificate.")
        return

    install_cert_on_cacerts(cert_der_path)

def rename_pem_cert_for_cacerts(filename):
    # Example usage of calculate_subject_hash_old
    cacerts_filename = calculate_subject_hash_old_from_pem(cert_pem_path=filename)

    if os.path.exists(cacerts_filename):
        print(f"[+] CA Certificate {cacerts_filename} already exists.")
    else:
        os.rename(filename, cacerts_filename)
        print(f"[+] CA Certificate renamed as {cacerts_filename}.")

    return cacerts_filename


def install_cert_on_cacerts(user_input):
    cacerts_filename = ""

    # Example usage of rename_perm_cert_for_cacerts
    while not (os.path.exists(user_input) and (user_input.endswith(".pem") or user_input.endswith(".der"))):
        print("[!] Error: The certificate file must be in PEM/DER format (.der).")
        user_input = prompt("Please enter the path of the certificate file on your PC: ")

    dest_folder = os.path.join("results", "tls_certificates")
    os.makedirs(dest_folder, exist_ok=True)
    
    try:
        shutil.copy(user_input, dest_folder)
    except shutil.SameFileError:
        print("[!] Error: The file already exists in the destination folder.")

    if user_input.endswith(".pem"):
        cacerts_filename = rename_pem_cert_for_cacerts(user_input)
    elif user_input.endswith(".der"):
        pem_filename = convert_der_to_pem(user_input)
        cacerts_filename = rename_pem_cert_for_cacerts(pem_filename)    
    else:
        print("[!] Error: The certificate file must be in PEM/DER format (.der).")
        return

    certificate_filename = os.path.split(cacerts_filename)[-1]
    if not mobile_exists([f"/system/etc/security/cacerts/{certificate_filename}"]):
        print(f"[+] Uploading CA Certificate {certificate_filename} to Android's /system/etc/security/cacerts/ directory...", end=' ')
        upload_to_dest(cacerts_filename, "/system/etc/security/cacerts/")
        print("DONE")

    else:
        print(f"[+] CA Certificate {cacerts_filename} already exists in Android's /system/etc/security/cacerts/ directory.")