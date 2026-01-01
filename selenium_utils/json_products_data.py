import json
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
def save_results_to_json(text, results, filename= os.path.join(cur_dir, 'product_data', 'product_data.json')):
    with open(filename, 'a', encoding='utf-8') as json_file:
        # for result in results:
        results_dict = {text: results}
        json.dump(results_dict, json_file, ensure_ascii=False)  # Ensure ASCII is not forced
        json_file.write('\n')  # Write a new line after each JSON object
           
def load_results_from_json(filename= os.path.join(cur_dir, 'product_data', 'product_data.json')):
    results = []
    with open(filename, 'r', encoding='utf-8') as json_file:
        for line in json_file:
            # Parse each line as a JSON object and append to the results list
            results.append(json.loads(line))
    return results

def load_content_from_json(filename=os.path.join(cur_dir, 'product_data', 'product_data.json')):
    with open(filename, 'r', encoding='utf-8') as json_file:
        content = json_file.read()  # Read the entire file content as a string
    return content

def clean_json_file(filename=os.path.join(cur_dir, 'product_data', 'product_data.json')):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write('')  # Write an empty string to clear the file