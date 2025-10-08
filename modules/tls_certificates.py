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
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.exceptions import InvalidSignature
import warnings
from cryptography.utils import CryptographyDeprecationWarning

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

        pem_file_path = der_file_path+".pem"

        if der_file_path.endswith('.der'):
            pem_file_path = der_file_path.replace('.der', '.pem')

        with open(pem_file_path, "wb") as pem_file:
            pem_file.write(pem_data)

        print(f"Successfully converted '{der_file_path}' to '{pem_file_path}'")
        return pem_file_path
        
    except FileNotFoundError:
        print(f"Error: The file '{der_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_pkcs12_to_pem(pkcs12_file_path: str, password=None):
    """
    Converts a PKCS#12 (PFX) certificate file to PEM format.

    Args:
        pkcs12_file_path (str): The path to the input PKCS#12 certificate file.
    """
    try:
        # Load the PKCS#12 file
        with open(pkcs12_file_path, "rb") as f:
            pkcs12_data = f.read()

        # Load the key and certificates from the PKCS#12 file
        private_key, certificate, ca_certificates = pkcs12.load_key_and_certificates(
            pkcs12_data, password, default_backend()
        )

        # Convert the main certificate to PEM format and save it
        if not certificate:
            print("No certificate found in the PKCS#12 file.")
            return None

        certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)
        
        pem_file_path = pkcs12_file_path+".pem"

        if pkcs12_file_path.endswith('.pk12') or pkcs12_file_path.endswith('.pfx'):
            pem_file_path = pkcs12_file_path.replace('.pk12', '.pem').replace('.pfx', '.pem')

        with open(pem_file_path, "wb") as cert_file:
            cert_file.write(certificate_pem)
            print(f"Certificate converted and saved to {pem_file_path}")

        return pem_file_path

    except FileNotFoundError:
        print(f"Error: The file '{pkcs12_file_path}' was not found.")
    except (ValueError, TypeError, InvalidSignature) as e:
        print(f"An error occurred while loading the PKCS#12 file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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

def download_certificate(certificate_url, cert_filename, proxies):
    print(f"[+] Downloading Proxy root certificate from {certificate_url}")

    try:
        response = requests.get(certificate_url, proxies=proxies, verify=False, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch certificate: {e}")
        print(f"[!] Please ensure the proxy is running and proxy listener is active on {certificate_url}")
        return

    cert_der_bytes = response.content

    dest_folder = os.path.join("results", "tls_certificates")
    os.makedirs(dest_folder, exist_ok=True)

    # Save .der file (as bytes, not string)
    with open(os.path.join(dest_folder, cert_filename), "wb") as f:
        f.write(cert_der_bytes)
    print(f"[+] Saved certificate to {os.path.join(dest_folder, cert_filename)}")

    return os.path.join(dest_folder, cert_filename)

def download_and_install_certificate(certificate_url, cert_filepath, proxies=None):
    # Download the Burp root certificate
    certificate_path = download_certificate(certificate_url, cert_filepath, proxies=proxies)

    if not certificate_path:
        print("[!] Failed to download Proxy root certificate.")
        return

    install_cert_on_cacerts(certificate_path)

def download_and_install_burp_root_cert(user_input):
    """
    Downloads the Burp Suite root certificate and installs it in the Android system's cacerts directory.
    """
    domain_ip, port = ip_and_port_from_user_input(user_input)

    # Download the Burp root certificate
    certificate_url = f"http://{domain_ip}:{port}/cert"
    cert_filepath = "burp_root_cert"
    download_and_install_certificate(certificate_url, cert_filepath)

def download_and_install_zap_root_cert(user_input):
    """
    Downloads the ZAP root certificate and installs it in the Android system's cacerts directory.
    """
    domain_ip, port = ip_and_port_from_user_input(user_input)

    # Download the Burp root certificate
    certificate_url = f"http://{domain_ip}:{port}/OTHER/network/other/rootCaCert/"
    cert_filepath = "zap_root_cert"
    download_and_install_certificate(certificate_url, cert_filepath)

def download_and_install_mitmproxy_root_cert(user_input):
    """
    Downloads the Burp Suite root certificate and installs it in the Android system's cacerts directory.
    """
    domain_ip, port = ip_and_port_from_user_input(user_input)

    # Download the Mitmproxy root certificate
    proxies = {
        'http': f"http://{domain_ip}:{port}",
        'https': f"https://{domain_ip}:{port}",
    }
    certificate_url = "http://mitm.it/cert/cer"
    cert_filepath = "mitmproxy_root_cert"
    download_and_install_certificate(certificate_url, cert_filepath, proxies=proxies)

def rename_pem_cert_for_cacerts(filename):
    # Example usage of calculate_subject_hash_old
    cacerts_filename = calculate_subject_hash_old_from_pem(cert_pem_path=filename)

    if os.path.exists(cacerts_filename):
        print(f"[+] CA Certificate {cacerts_filename} already exists.")
    else:
        os.rename(filename, cacerts_filename)
        print(f"[+] CA Certificate renamed as {cacerts_filename}.")

    return cacerts_filename

def identify_cert_format(file_path):
    """
    Attempts to open a certificate file to determine its format.
    
    Args:
        file_path (str): The path to the certificate file.
        p12_password (bytes): The password for PKCS#12 files, if applicable.
    """
    try:
        with open(file_path, "rb") as f:
            cert_data = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None, None

    # Try PEM format first (most common)
    try:
        print("\nTrying PEM format...", end=' ')
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        print("OK")
        print(f"Subject: {cert.subject}")
        return "PEM", cert, None
    except ValueError as e:
        print("Not PEM format")
        
    # Try DER format
    try:
        print("\nTrying DER format...", end=' ')
        cert = x509.load_der_x509_certificate(cert_data, default_backend())
        print("OK")
        print(f"Subject: {cert.subject}")
        return "DER", cert, None
    except ValueError as e:
        print("Not DER format")

    # Try PKCS#12 (PFX) format
    try:
        print("\nTrying PKCS#12 (PFX) format...", end=' ')
        p12_password = input("Provide the password of the file if it is password protected:")

        _, cert, _ = pkcs12.load_key_and_certificates(cert_data, p12_password.encode(), default_backend())
        if cert:
            print("OK")
            print(f"Subject: {cert.subject}")
            return "PKCS#12", cert, p12_password.encode()
        else:
            print("Failed to load PKCS#12: Certificate not found in file.")
    except (ValueError, TypeError, InvalidSignature) as e:
        print("Not PKCS#12 format")

    print("\nCould not determine the certificate format.")
    return None, None, None

def install_cert_on_cacerts(user_input):
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    cacerts_filename = ""

    cert_type, cert, pwd_bytes = identify_cert_format(user_input)

    # Example usage of rename_perm_cert_for_cacerts
    while cert_type is None:
        print("[!] Error: The certificate file must be in PEM/DER/PKCS#12 format.")
        user_input = prompt("Please enter the path of the certificate file on your PC: ")
        cert_type, cert, pwd_bytes = identify_cert_format(user_input)

    dest_folder = os.path.join("results", "tls_certificates")
    os.makedirs(dest_folder, exist_ok=True)

    try:
        shutil.copy(user_input, dest_folder)
    except shutil.SameFileError:
        print("[!] Error: The file already exists in the destination folder.")

    if cert_type == "PEM":
        cacerts_filename = rename_pem_cert_for_cacerts(user_input)
    elif cert_type == "DER":
        pem_filename = convert_der_to_pem(user_input)
        cacerts_filename = rename_pem_cert_for_cacerts(pem_filename)    
    elif cert_type == "PKCS#12":
        pem_filename = convert_pkcs12_to_pem(user_input, password=pwd_bytes)
        cacerts_filename = rename_pem_cert_for_cacerts(pem_filename) 
    else:
        print("[!] Error: The certificate file must be in PEM/DER/PKCS#12 format.")
        return

    certificate_filename = os.path.split(cacerts_filename)[-1]
    if not mobile_exists([f"/system/etc/security/cacerts/{certificate_filename}"]):
        print(f"[+] Uploading CA Certificate {certificate_filename} to Android's /system/etc/security/cacerts/ directory...", end=' ')
        upload_to_dest(cacerts_filename, "/system/etc/security/cacerts/")
        print("DONE")

    else:
        print(f"[+] CA Certificate {cacerts_filename} already exists in Android's /system/etc/security/cacerts/ directory.")