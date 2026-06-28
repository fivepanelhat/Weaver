# Sovereign-Edge-Firmware/src/attestation_agent.py
import subprocess
import os
import tempfile


def generate_tpm_quote(nonce_hex):
    """
    Interfaces with the physical SPI TPM 2.0 chip to generate a cryptographic quote
    of the current system state, locked down with a server-provided nonce.
    """
    print(f"[TPM] Received attestation challenge nonce: {nonce_hex}")

    # Paths for temporary cryptographic structures
    tmp_dir = tempfile.gettempdir()
    nonce_bin_path = os.path.join(tmp_dir, "nonce.bin")
    quote_path = os.path.join(tmp_dir, "quote.bin")
    pcr_path = os.path.join(tmp_dir, "pcr.bin")
    sig_path = os.path.join(tmp_dir, "quote.sig")

    try:
        # 1. Write the incoming hex nonce to raw binary
        with open(nonce_bin_path, "wb") as f:
            f.write(bytes.fromhex(nonce_hex))

        # 2. Invoke the hardware TPM to capture the Platform Configuration Registers (PCRs)
        # We check PCR bank sha256, registers 0 through 7 (Core Boot Integrity
        # chain)
        tpm_cmd = [
            "tpm2_quote",
            # The persistent handle index of your Attestation Identity Key
            # (AIK)
            "-c",
            "0x81010002",
            "-l",
            "sha256:0,1,2,3,4,5,6,7",
            "-q",
            nonce_bin_path,  # The challenge injection
            "-m",
            quote_path,  # Output structural attest file
            "-s",
            sig_path,  # Output hardware cryptographic signature
            "-p",
            pcr_path,  # Output targeted PCR state values
            "-g",
            "sha256",
        ]

        subprocess.run(
            tpm_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # 3. Package the binary artifacts into hexadecimal transport payloads
        with open(quote_path, "rb") as q, open(sig_path, "rb") as s, open(
            pcr_path, "rb"
        ) as p:
            attestation_payload = {
                "quote": q.read().hex(),
                "signature": s.read().hex(),
                "pcr_values": p.read().hex(),
            }

        return attestation_payload

    except subprocess.CalledProcessError as e:
        print(
            f"[CRITICAL HARDWARE FAULT] TPM execution failed: "
            f"{e.stderr.decode()}"
        )
        return None
    finally:
        # Cleanup volatile staging files
        for path in [nonce_bin_path, quote_path, pcr_path, sig_path]:
            if os.path.exists(path):
                os.remove(path)
