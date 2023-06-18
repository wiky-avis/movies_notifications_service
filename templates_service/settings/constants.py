import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_PUBLIC_KEY = """"
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIzi1aV7xG1BGjwf1ZsCxiMO5j
dYEPVfdPDLbBQtMD4VZlNb4ps2B6bExyLisOUxnlhEqdVn424EHIFRwNAV3eo0Gc
RrEGT4u57+Esqy9QQmvknJaA+oBFlzCpMLV3clQIm6ropbVtgqQtnLH19WJMfal3
nwB/v8Nle2XNQ7DJKwIDAQAB
-----END PUBLIC KEY-----
"""

TEST_TOKEN = "test"
UGC_SRV_TOKEN = os.getenv("UGC_SRV_TOKEN", default=TEST_TOKEN)
ADMIN_PANEL_SRV_TOKEN = os.getenv("ADMIN_PANEL_SRV_TOKEN", default=TEST_TOKEN)
