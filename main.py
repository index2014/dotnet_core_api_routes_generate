import re
import os

def find_cs_files(directory, output, Unauthorized):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                print(os.path.join(root, file))
                get_routes(os.path.join(root, file), output=output, Unauhtorized=Unauthorized)

def get_routes(path, output, Unauhtorized):
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        file_content = file.read()
    controller_pattern = r'namespace\s+([\w.]+)\s*{[^{}]*public\s+class\s+(\w+)\s*:'
    matches = re.findall(controller_pattern, file_content)
    controller_name = matches[0][1] if matches else ''
    route_pattern = r'\[(HttpGet|HttpPost|HttpDelete|HttpPut|HttpHead|HttpOptions|HttpConnect|HttpTrace)\(\"([^"]+)\"\)\]'
    routes = re.findall(route_pattern, file_content)
    authorize_pattern = r'\[Authorize\]'
    authorize_present = re.search(authorize_pattern, file_content)
    for route in routes:
        http_method = route[0]
        route_path = route[1].replace('[controller]', controller_name).replace('[action]', 'ActionName')
        API_result = (f"{http_method[4:].upper()} /api/{controller_name}/{route_path}")
        API_result = re.sub(r'Controller', '', API_result)
        if not authorize_present:
            with open(Unauhtorized, 'a') as Unauhtorized_file:
                Unauhtorized_file.write(f"{API_result}\n")
        with open(output, 'a') as output_file:
            output_file.write(API_result+'\n')

def main():
    directory = "./"
    output_directory = './API_Summary.txt'
    Unauhtorized = './Unauthorized.txt'
    find_cs_files(directory=directory, output=output_directory, Unauthorized=Unauhtorized)

if __name__ == "__main__":
    main()
