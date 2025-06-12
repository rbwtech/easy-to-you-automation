#!/usr/bin/env python3
"""
Legacy easy4us script (v1.0)
Original implementation for backward compatibility
Fixed: Browser compatibility and upload form detection
"""

import os
import codecs
import argparse
import shutil
import urllib
import zipfile
from io import BytesIO
import requests
import bs4
import time

parser = argparse.ArgumentParser(usage="easy4us", description="decode directories with easytoyou.eu")
parser.add_argument("-u", "--username", required=True, help="easytoyou.eu username")
parser.add_argument("-p", "--password", required=True, help="easytoyou.eu password")
parser.add_argument("-s", "--source", required=True, help="source directory")
parser.add_argument("-o", "--destination", required=True, help="destination directory", default="")
parser.add_argument("-d", "--decoder", help="decoder (default: ic11php72)", default="ic11php72")
parser.add_argument("-w", "--overwrite", help="overwrite", action='store_true', default=False)
base_url = "https://easytoyou.eu"
args = parser.parse_args()

# Updated headers to mimic modern browser
headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '"Chromium";v="120", "Google Chrome";v="120", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://easytoyou.eu"
}

not_decoded = []

def login(username, password):
    session = requests.session()
    # Set session headers
    session.headers.update(headers)
    
    try:
        # First, get the login page to establish session
        print("Getting login page...")
        login_page = session.get(base_url + "/login", timeout=30)
        time.sleep(1)  # Small delay to avoid being flagged as bot
        
        login_data = {"loginname": username, "password": password}
        print("Attempting login...")
        resp = session.post(
            base_url + "/login", 
            headers=dict(headers, **{"Content-Type": "application/x-www-form-urlencoded"}),
            data=login_data, 
            allow_redirects=True,
            timeout=30
        )
        
        if "/account" in resp.url or "account" in resp.text.lower():
            print("Login successful!")
            return session
        else:
            print("Login failed. Response URL:", resp.url)
            print("Response status:", resp.status_code)
            return False
            
    except Exception as e:
        print(f"Login error: {e}")
        return False

def copy(src, dest, files):
    for file in files:
        csrc = os.path.join(src, file)
        cdest = os.path.join(dest, file)
        shutil.copyfile(csrc, cdest)
        print("copied %s to %s" % (file, cdest))

def clear(session):
    print("clearing page", end='')
    c = 0
    while True:
        c += 1
        try:
            res = session.get(base_url + "/decoder/%s/1" % args.decoder, headers=headers, timeout=30)
            s = bs4.BeautifulSoup(res.content, features="lxml")
            inputs = s.find_all(attrs={"name": "file[]"})
            if len(inputs) < 1:
                print()
                break
            final = ""
            for i in inputs:
                final += "%s&" % urllib.parse.urlencode({i["name"]: i["value"]})
            session.post(base_url + "/decoder/%s/1" % args.decoder, data=final,
                         headers=dict(headers, **{"Content-Type": "application/x-www-form-urlencoded"}),
                         timeout=30)
            print("...%d" % c, end='')
            time.sleep(0.5)  # Small delay between requests
        except Exception as e:
            print(f"\nError during clear: {e}")
            break

def parse_upload_result(r):
    s = bs4.BeautifulSoup(r.content, features="lxml")
    success = []
    failure = []
    for el in s.find_all("div", {"class": "alert-success"}):
        res = [s.strip() for s in el.text.split()]
        if len(res) > 1:
            success.append(res[1])

    for el in s.find_all("div", {"class": "alert-danger"}):
        res = [s.strip() for s in el.text.split()]
        if len(res) > 3:
            failure.append(res[3])
    return success, failure

def upload(session, dir, files):
    try:
        print("Getting decoder page...")
        r = session.get(base_url + "/decoder/%s" % args.decoder, headers=headers, timeout=300)
        s = bs4.BeautifulSoup(r.content, features="lxml")
        
        # Try multiple selectors for upload form
        el = None
        selectors = [
            {"id": "uploadfileblue"},
            {"name": "uploadfile[]"},
            {"type": "file"},
            {"class": "form-control"},
            {"accept": ".php"}
        ]
        
        for selector in selectors:
            el = s.find("input", selector)
            if el:
                print(f"Found upload form with selector: {selector}")
                break
        
        if not el:
            # Try finding any file input
            file_inputs = s.find_all("input", {"type": "file"})
            if file_inputs:
                el = file_inputs[0]
                print("Found generic file input")
            else:
                print("Available forms and inputs:")
                forms = s.find_all("form")
                for i, form in enumerate(forms):
                    print(f"Form {i}: {form.get('action', 'No action')} - {form.get('method', 'No method')}")
                    inputs = form.find_all("input")
                    for inp in inputs:
                        print(f"  Input: name='{inp.get('name')}', type='{inp.get('type')}', id='{inp.get('id')}'")
                
                print("Raw page content (first 1000 chars):")
                print(r.text[:1000])
                print("error: couldnt find upload form")
                return None, None
        
        n = el.attrs.get("name", "uploadfile[]")
        print(f"Using input name: {n}")
        
        upload = []
        for file in files:
            if file.endswith(".php"):
                full = codecs.open(os.path.join(dir, file), 'rb')
                upload.append((n, (file, full, "application/x-php")))
        upload.append(("submit", (None, "Decode")))
        
        if len(upload) > 0:
            print("Submitting files...")
            r = session.post(base_url + "/decoder/%s" % args.decoder,
                             headers=headers,
                             files=upload,
                             timeout=300)
            return parse_upload_result(r)
        
    except Exception as e:
        print(f"Upload error: {e}")
        return None, None

def download_zip(session, outpath):
    try:
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        print("Downloading decoded files...")
        r = session.get(base_url + "/download.php?id=all", headers=headers, timeout=300)
        
        if r.status_code != 200:
            print(f"Download failed with status: {r.status_code}")
            return False
            
        bytes = BytesIO(r.content)
        zf = zipfile.ZipFile(bytes)
        for name in zf.namelist():
            data = zf.read(name)
            dest = os.path.join(outpath, os.path.basename(name))
            f = open(dest, 'wb+')
            wrote = f.write(data)
            f.close()
            print("wrote %d bytes to %s" % (wrote, dest))
        zf.close()
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def process_files(session, dir, dest, phpfiles):
    print("uploading %d files..." % len(phpfiles), end='', flush=True)
    res = upload(session, dir, phpfiles)
    if res and res[0] is not None:
        success, failure = res
        print("done. %d successful, %d failed." % (len(success), len(failure)))
        not_decoded.extend([os.path.join(dir, f) for f in failure])
        if len(success) > 0:
            if not download_zip(session, dest):
                print("couldn't download. copying originals and continuing")
                not_decoded.extend([os.path.join(dir, f) for f in phpfiles])
            clear(session)
    else:
        print("upload failed. copying originals and continuing")
        not_decoded.extend([os.path.join(dir, f) for f in phpfiles])

if __name__ == '__main__':
    if args.destination == "":
        args.destination = os.path.basename(args.source) + "_decoded"

    session = login(args.username, args.password)
    if session:
        clear(session)
        for dir, dirnames, filenames in os.walk(args.source):
            print("descended into %s" % dir)
            rel = os.path.relpath(dir, args.source)
            dest = os.path.join(args.destination, rel).strip(".")
            if not os.path.exists(dest):
                os.makedirs(dest)
            phpfiles = []
            other = []
            for f in filenames:
                csrc = os.path.join(dir, f)
                try:
                    if f.endswith(".php") and b"ionCube Loader" in open(csrc, "rb").read():
                        phpfiles.append(f)
                    else:
                        other.append(f)
                except Exception as e:
                    print(f"Error reading {csrc}: {e}")
                    other.append(f)

            copy(dir, dest, other)

            if not args.overwrite:
                needed = []
                for f in phpfiles:
                    csrc = os.path.join(dest, f)
                    if not os.path.exists(csrc):
                        needed.append(f)
                phpfiles = needed

            if len(phpfiles) > 0:
                for f in batch(phpfiles, 25):
                    process_files(session, dir, dest, f)
                    time.sleep(1)  # Delay between batches
        print("finished. ioncube files that failed to decode:")
        for f in not_decoded:
            print(f)
    else:
        print("Login failed. Please check your credentials.")