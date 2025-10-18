import os
import sys
import re
from typing import Optional, Dict
from urllib import request, error
from urllib.parse import urlparse, urlsplit, quote, urlunsplit
from crawler import analyse,save_analysation
from dnslookup import proces_dnslookup
from helper import get_page_detection_pattern, get_resource_detection_pattern, clear_feed
from proxy import get_proxies, request_through_proxy
from parser import build_parser
from request import read_response, get_file

curr_directory = ''
url = ''
args = None
domain = ''
output_dir = ''
proxies = get_proxies()
analyse_file = ''


def process_file(undergoing_files : set, processed_files : set, isHTML = False, isForAnalysing = False) -> str:
    global args
    global curr_directory
    global url
    global output_dir
    file_path = ''
    resource = (undergoing_files - processed_files).pop()
    processed_files |= {resource}
    if url not in resource:
        file_name = resource[resource.rfind('/') + 1::]
        resource = resource[:resource.rfind('/')]
    else:
        file_name = resource[resource.rfind('/') + 1::]
        resource = resource[len(url) + 1:resource.rfind('/')]
    if not curr_directory:
        file_path = resource.replace('../', '')
    else:
        curr_dir_dirs_count = len(curr_directory.split('/'))
        file_path_returns = resource.count('../')
        if file_path_returns > curr_dir_dirs_count:
            file_path = resource.replace('../', '', file_path_returns - curr_dir_dirs_count)
        file_path = resource
    file_path = file_path.replace('./', '')
    print('='*23,'resource' if not isHTML else 'page','='*23)
    print('resource:' if not isHTML else 'page:', file_path + '/' + file_name)
    file_content = get_file(url + '/' + file_path + '/' + file_name,headers=args.headers, timeout=args.timeout,use_proxy=args.use_proxy)
    #clear_feed(lines=4,timeout=1)
    if isForAnalysing and (isHTML or re.match(r'^.*(?:(?:\.json)|(?:\.js))$',file_name)):
        analyse(file_content,domain)
    if not file_content:
        return ''

    try:
        file_path = os.path.join(output_dir, file_path)
        os.makedirs(file_path, exist_ok=True)
        file_name = file_name if '?' not in file_name else file_name.replace('?', '_')
        file_name = file_name if file_name != '' else 'index.html' if isHTML else 'unknown'
        file_path = os.path.join(file_path, file_name)
        print('file path: ', file_path)
        if isinstance(file_content, str):
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(file_content)
        else:
            with open(file_path, 'wb') as f:
                f.write(file_content)

    except OSError as e:
        print('Unable to write file:', e)
        return ''
    return file_content


def main(argv=None) -> int:
    parser = build_parser()
    global args
    global curr_directory
    global url
    global output_dir
    global analyse_file
    global domain
    args = parser.parse_args(argv)
    curr_directory= urlparse(args.url).path
    url = urlparse(args.url).geturl()
    domain = urlparse(url).netloc
    output_dir= os.path.expanduser(f'~/{args.output or 'WebDrop/' + domain}/')
    analyse_file = os.path.join(output_dir, 'analyse.html')

    if args.nslook:
        proces_dnslookup(domain,args.timeout)
    processed_pages = set()
    saved_resources = set()
    pages_for_lookup = {curr_directory if curr_directory == '/' else ''}

    try:
        os.makedirs(output_dir, exist_ok=True)
        dirs = curr_directory.split('/')
        output_dir = os.path.join(output_dir, 'site',*dirs)
        os.makedirs(output_dir, exist_ok=True)
        while pages_for_lookup - processed_pages:
            file_content = process_file(pages_for_lookup,processed_pages,isHTML=True,isForAnalysing=args.analyse)
            if not file_content:
                continue
            anchors = re.findall(get_page_detection_pattern(domain), file_content)
            pages_for_lookup |= {anchor for anchor in anchors}
            curr_page_resources = re.findall(get_resource_detection_pattern(domain), file_content)
            new_resources = {resource for resource in curr_page_resources}
            unsaved_resources = new_resources - saved_resources
            while unsaved_resources - saved_resources:
                process_file(unsaved_resources,saved_resources,isForAnalysing=args.analyse)
        if args.analyse:
            save_analysation(analyse_file)
        print('\nCompleted successfully\n')
    except error.HTTPError as e:
        print(f"HTTP error {e.code} while fetching {args.url}: {e.reason}", file=sys.stderr)
        return 1
    except error.URLError as e:
        print(f"Network error while fetching {args.url}: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error while fetching {args.url}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
