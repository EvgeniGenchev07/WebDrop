from helper import get_analyser_pattern
import re

findings = dict()

def analyse(content:str,domain:str)-> None:
    pattern = get_analyser_pattern()
    results = re.finditer(pattern, content)
    for result in results:
        for key,value in result.groupdict().items():
            if value and not re.match(rf'(http|https)://{domain}',value):
                if not findings.__contains__(value):
                    findings.update({value:key})

def save_analysation(file_path:str):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for key,value in findings.items():
                f.write(f"<p>{value}:\t<a{f' href={key}' if value == 'link' else ''}>{key}</a></p>")
    except OSError as e:
        print('Unable to write to analyse.html:',e)