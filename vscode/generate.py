#!/usr/bin/env python3

import jinja2
import argparse
import os
import yaml

default_template = os.path.join(os.path.dirname(__file__), "templates", "default")

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--template', nargs='+', default=default_template)
parser.add_argument('-r', '--report', required=True)
parser.add_argument('target')
args = parser.parse_args()

try:
    report = yaml.load(open(args.report).read(), Loader=yaml.SafeLoader)
except Exception as e:
    print("Failed to load PTXdist BSP report: " + e.strerror)
    exit(1)

loader = jinja2.FileSystemLoader(args.template)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)

for name in loader.list_templates():
    # ignore hidden files
    if os.path.basename(name)[0] == '.':
        continue
    template = env.get_template(name)
    target = os.path.join(args.target, name)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    template.stream(report).dump(target)
    if target.endswith('.sh'):
        os.chmod(target, 0o755)
