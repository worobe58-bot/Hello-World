import os
import sys
import re
import json
import base64
import zlib
import zipfile
import io
import argparse
import lzma
import codecs
from pathlib import Path

XK9M2N = r"(https://((ptb\.|canary\.|development\.)?)discord(app)?\.com/api/webhooks/[0-9]{19}/[a-zA-Z0-9\-_]{68})"
QW4T7V = r"(aHR0cHM6Ly9[\d\w]+==)"
ZX8B3C = r"([0-9]{10}:[a-zA-Z0-9]{35})"
MN5L2K = r"zT([a-zA-Z0-9]+==)z"


def P7Q3R1(Y8U2I0):
    A5S4D6 = re.findall(QW4T7V, Y8U2I0)
    F3G2H1 = re.findall(XK9M2N, Y8U2I0)
    J9K8L7 = re.search(MN5L2K, Y8U2I0)
    N6B5V4 = re.search(ZX8B3C, Y8U2I0)
    
    if A5S4D6:
        C3X2Z1 = []
        for W1E2R3 in A5S4D6:
            try:
                W1E2R3 = base64.b64decode(W1E2R3).decode()
                if W1E2R3 not in C3X2Z1 and re.fullmatch(XK9M2N, W1E2R3) is not None:
                    C3X2Z1.append(W1E2R3)
            except:
                pass
        if C3X2Z1:
            return C3X2Z1 if len(C3X2Z1) > 1 else C3X2Z1[0]
    
    if F3G2H1:
        T4Y5U6 = []
        for I7O8P9 in F3G2H1:
            if I7O8P9[0] not in T4Y5U6:
                T4Y5U6.append(I7O8P9[0])
        return T4Y5U6 if len(T4Y5U6) > 1 else T4Y5U6[0]
    
    if J9K8L7:
        try:
            L2K3J4 = J9K8L7.group(1) + "="
            H5G6F7 = base64.b64decode(L2K3J4).decode()
            return f"${H5G6F7}"
        except:
            pass
    
    if N6B5V4:
        return f"${N6B5V4.group(1)}"
    
    return None


class D8S7A6:
    def __init__(self, Q1W2E3, R4T5Y6):
        self.Q1W2E3 = Q1W2E3
        self.R4T5Y6 = R4T5Y6


class U7I8O9:
    def __init__(self, P0O9I8, U7Y6T5, R4E3W2, Q1A2S3):
        self.P0O9I8 = P0O9I8
        self.U7Y6T5 = U7Y6T5
        self.R4E3W2 = R4E3W2
        self.Q1A2S3 = Q1A2S3


def D4F5G6(H6J7K8):
    try:
        with open(H6J7K8, "rb") as L9Z0X1:
            C2V3B4 = L9Z0X1.read()
        
        C2V3B4 = C2V3B4.split(b"stub-oz,")[-1].split(b"\x63\x03")[0].split(b"\x10")
        
        if len(C2V3B4) < 2:
            return None
        
        N5M6Q7 = C2V3B4[0].split(b"\xDA")[0].decode('latin1', errors='ignore')
        W8E9R0 = C2V3B4[-1].decode('latin1', errors='ignore')
        
        N5M6Q7 = re.sub(r'[^a-zA-Z0-9+/=]', '', N5M6Q7)
        W8E9R0 = re.sub(r'[^a-zA-Z0-9+/=]', '', W8E9R0)
        
        N5M6Q7 = N5M6Q7 + '=' * ((4 - len(N5M6Q7) % 4) % 4)
        W8E9R0 = W8E9R0 + '=' * ((4 - len(W8E9R0) % 4) % 4)
        
        T1Y2U3 = base64.b64decode(N5M6Q7)
        I4O5P6 = base64.b64decode(W8E9R0)
        
        return D8S7A6(T1Y2U3, I4O5P6)
        
    except Exception as A7S8D9:
        print(f"[-] Key extraction failed: {A7S8D9}", file=sys.stderr)
        return None


def F9G8H7(J4K5L6, M3N2B1, V6C5X4):
    try:
        from Crypto.Cipher import AES
        
        if len(V6C5X4) < 16:
            return None
        
        Z8X7C6 = V6C5X4[:-16]
        Q5W4E3 = M3N2B1 + b'\x00\x00\x00\x02'
        R2T1Y0 = int.from_bytes(Q5W4E3, byteorder='big')
        
        U9I8O7 = bytearray()
        P6A5S4 = Q5W4E3
        D3F2G1 = AES.new(J4K5L6, AES.MODE_ECB)
        
        for H7J6K5 in range(0, len(Z8X7C6), 16):
            L4M3N2 = D3F2G1.encrypt(P6A5S4)
            B1V2C3 = Z8X7C6[H7J6K5:H7J6K5+16]
            for X4Z5Q6 in range(len(B1V2C3)):
                U9I8O7.append(B1V2C3[X4Z5Q6] ^ L4M3N2[X4Z5Q6])
            
            R2T1Y0 = int.from_bytes(P6A5S4, byteorder='big') + 1
            P6A5S4 = R2T1Y0.to_bytes(16, byteorder='big')
        
        return bytes(U9I8O7)
        
    except ImportError:
        print("[-] Install pycryptodome: pip install pycryptodome", file=sys.stderr)
        return None
    except Exception as W7E8R9:
        print(f"[-] AES decryption failed: {W7E8R9}", file=sys.stderr)
        return None


def T5Y6U7(I4O5P6):
    try:
        A3S4D5 = b"\xfd7zXZ\x00\x00" + I4O5P6.split(b"\xfd7zXZ\x00\x00")[1]
        F6G7H8 = lzma.decompress(A3S4D5)
        J9K0L1 = F6G7H8.decode().replace(";", "\n")
        J9K0L1 = re.sub(r"^__import__.*", "", J9K0L1, flags=re.M)
        
        M2N3B4 = re.search(r'^____="(.*)"$', J9K0L1, re.MULTILINE)
        V5C6X7 = re.search(r'^_____="(.*)"$', J9K0L1, re.MULTILINE)
        Z8A9S0 = re.search(r'^______="(.*)"$', J9K0L1, re.MULTILINE)
        D1F2G3 = re.search(r'^_______="(.*)"$', J9K0L1, re.MULTILINE)
        
        if M2N3B4 and V5C6X7 and Z8A9S0 and D1F2G3:
            return U7I8O9(
                M2N3B4.group(1),
                V5C6X7.group(1),
                Z8A9S0.group(1),
                D1F2G3.group(1)
            )
    except Exception as H4J5K6:
        print(f"[-] Stage 3 failed: {H4J5K6}", file=sys.stderr)
    
    return None


def L7K8J9(H6G5F4):
    try:
        D3S2A1 = codecs.decode(H6G5F4.P0O9I8, "rot13")
        Q1W2E3 = base64.b64decode(
            D3S2A1 + H6G5F4.U7Y6T5 + H6G5F4.R4E3W2[::-1] + H6G5F4.Q1A2S3
        )
        R5T6Y7 = Q1W2E3.decode('ascii', errors='ignore')
        return P7Q3R1(R5T6Y7)
    except Exception as U8I9O0:
        print(f"[-] Stage 4 failed: {U8I9O0}", file=sys.stderr)
    
    return None


def P0O9I8(U7Y6T5):
    U7Y6T5 = Path(U7Y6T5)
    
    print(f"[*] Processing: {U7Y6T5}")
    
    print("[*] Trying simple string scan...")
    for R4E3W2 in U7Y6T5.rglob("*"):
        if R4E3W2.is_file():
            try:
                if R4E3W2.stat().st_size > 10 * 1024 * 1024:
                    continue
                
                Q1A2S3 = R4E3W2.read_bytes()
                for D4F5G6 in ['utf-8', 'latin1', 'ascii']:
                    try:
                        H6J7K8 = Q1A2S3.decode(D4F5G6, errors='ignore')
                        L9Z0X1 = P7Q3R1(H6J7K8)
                        if L9Z0X1:
                            print(f"[+] Found webhook in: {R4E3W2.name}")
                            return L9Z0X1
                    except:
                        pass
            except:
                pass
    
    C2V3B4 = list(U7Y6T5.rglob("blank.aes"))
    
    if C2V3B4:
        N5M6Q7 = C2V3B4[0]
        print(f"[*] Found blank.aes: {N5M6Q7}")
        
        W8E9R0 = None
        
        for T1Y2U3 in ["loader-o.pyc", "loader.pyc"]:
            I4O5P6 = U7Y6T5 / T1Y2U3
            if I4O5P6.exists():
                W8E9R0 = I4O5P6
                break
        
        if W8E9R0 is None:
            for A7S8D9 in U7Y6T5.rglob("*.pyc"):
                if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[a-f0-9]{12}\.pyc$', A7S8D9.name):
                    W8E9R0 = A7S8D9
                    break
        
        if W8E9R0:
            print(f"[*] Extracting keys from: {W8E9R0.name}")
            F9G8H7 = D4F5G6(str(W8E9R0))
            
            if F9G8H7 and len(F9G8H7.Q1W2E3) == 32 and len(F9G8H7.R4T5Y6) == 12:
                print("[*] Successfully extracted AES keys")
                
                J4K5L6 = N5M6Q7.read_bytes()
                
                try:
                    M3N2B1 = J4K5L6[::-1]
                    V6C5X4 = zlib.decompress(M3N2B1)
                    J4K5L6 = V6C5X4
                except:
                    try:
                        V6C5X4 = zlib.decompress(J4K5L6)
                        J4K5L6 = V6C5X4
                    except:
                        pass
                
                Z8X7C6 = F9G8H7(F9G8H7.Q1W2E3, F9G8H7.R4T5Y6, J4K5L6)
                
                if Z8X7C6:
                    print(f"[*] Decrypted {len(Z8X7C6)} bytes")
                    
                    try:
                        with zipfile.ZipFile(io.BytesIO(Z8X7C6)) as Q5W4E3:
                            print(f"[*] ZIP contains {len(Q5W4E3.namelist())} files")
                            
                            R2T1Y0 = U7Y6T5 / "decrypted_zip"
                            Q5W4E3.extractall(R2T1Y0)
                            print(f"[*] Extracted ZIP to: {R2T1Y0}")
                            
                            for U9I8O7 in R2T1Y0.rglob("*"):
                                if U9I8O7.is_file():
                                    try:
                                        P6A5S4 = U9I8O7.read_bytes()
                                        
                                        for D3F2G1 in ['utf-8', 'latin1', 'ascii']:
                                            try:
                                                H7J6K5 = P6A5S4.decode(D3F2G1, errors='ignore')
                                                L4M3N2 = P7Q3R1(H7J6K5)
                                                if L4M3N2:
                                                    print(f"[+] Found webhook in: {U9I8O7.name}")
                                                    return L4M3N2
                                            except:
                                                pass
                                        
                                        B1V2C3 = T5Y6U7(P6A5S4)
                                        if B1V2C3:
                                            print(f"[*] Stage 3 successful for: {U9I8O7.name}")
                                            X4Z5Q6 = L7K8J9(B1V2C3)
                                            if X4Z5Q6:
                                                print(f"[+] Found webhook in stage 4 from: {U9I8O7.name}")
                                                return X4Z5Q6
                                        
                                    except Exception as W7E8R9:
                                        print(f"[-] Failed processing {U9I8O7.name}: {W7E8R9}")
                    
                    except zipfile.BadZipFile:
                        print("[-] Decrypted data is not a ZIP file")
                        
                        for T5Y6U7 in ['utf-8', 'latin1', 'ascii']:
                            try:
                                I4O5P6 = Z8X7C6.decode(T5Y6U7, errors='ignore')
                                A3S4D5 = P7Q3R1(I4O5P6)
                                if A3S4D5:
                                    print("[+] Found webhook in decrypted data")
                                    return A3S4D5
                            except:
                                pass
                        
                        F6G7H8 = T5Y6U7(Z8X7C6)
                        if F6G7H8:
                            J9K0L1 = L7K8J9(F6G7H8)
                            if J9K0L1:
                                print("[+] Found webhook in stage 4")
                                return J9K0L1
                else:
                    print("[-] Decryption failed")
            else:
                print("[-] Failed to extract valid AES keys")
        else:
            print("[-] No key file found")
    else:
        print("[-] No blank.aes file found")
    
    print("[*] Trying stub processing...")
    
    for M2N3B4 in U7Y6T5.rglob("*.pyc"):
        if 'pyi' not in M2N3B4.name:
            try:
                V5C6X7 = M2N3B4.read_bytes()
                
                Z8A9S0 = T5Y6U7(V5C6X7)
                if Z8A9S0:
                    print(f"[*] Stage 3 successful for: {M2N3B4.name}")
                    D1F2G3 = L7K8J9(Z8A9S0)
                    if D1F2G3:
                        print(f"[+] Found webhook in: {M2N3B4.name}")
                        return D1F2G3
            except:
                pass
    
    return None


def H4J5K6():
    L7K8J9 = argparse.ArgumentParser(description="BlankGrabber Deobfuscator")
    L7K8J9.add_argument("input", help="Extraction directory")
    L7K8J9.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    
    H6G5F4 = L7K8J9.parse_args()
    
    if not os.path.exists(H6G5F4.input):
        print(f"[-] Path does not exist: {H6G5F4.input}", file=sys.stderr)
        sys.exit(1)
    
    D3S2A1 = P0O9I8(H6G5F4.input)
    
    if D3S2A1:
        if H6G5F4.json:
            print(json.dumps({"type": "blankgrabber", "webhook": D3S2A1, "success": True}, indent=2))
        else:
            print(f"[+] Webhook: {D3S2A1}")
        sys.exit(0)
    else:
        if H6G5F4.json:
            print(json.dumps({"type": "blankgrabber", "webhook": None, "success": False}, indent=2))
        else:
            print("[-] No webhook found")
        sys.exit(1)


if __name__ == "__main__":
    H4J5K6()