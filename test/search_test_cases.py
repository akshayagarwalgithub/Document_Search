import pytest
import os
import json
from pathlib import Path
import glob
import sys
from main import simple_search,regex_search,index_search
import re


ROOT_DIR = Path(__file__).parent.parent
print("Root directory path is {}".format(str(ROOT_DIR)))
with open(ROOT_DIR / 'conf' / 'config.json') as json_conf_file:
    print("config file full path = {}".format(json_conf_file))
    conf_variables = json.load(json_conf_file)

src_files_path = conf_variables['src_files_base_path']['path']
src_data_folder = Path(src_files_path)
print("src_data_folder={}".format(src_data_folder))

search_text_file_names_list = [f for f in os.listdir(ROOT_DIR/src_data_folder) if f.endswith('.txt')]
#print("search files names list={}".format(search_text_file_names_list))
search_files_list = glob.glob(str(ROOT_DIR)+str(Path('/'))+str(src_data_folder) + '/*.txt')
#print("text files path = {}".format(str(ROOT_DIR)+str(src_data_folder) + '/*.txt'))
#print("search_file_list={}".format(search_files_list))
preprocessed_file = glob.glob(str(ROOT_DIR)+str(Path('/'))+str(src_data_folder) + '/*.json').pop()

with open(preprocessed_file, 'r') as fwc:
    files_word_counts = json.load(fwc)

file_name_data_dict_simple_search={}


for file in search_files_list:
    try:
        with open(file, 'r') as searchfile:
                # filedata_list =re.split(r'[^\w]',searchfile.read())
            file_name_data_dict_simple_search[file] = re.split(r'[^a-zA-Z0-9_.-]', searchfile.read())

    except IOError:
        print("File not found or path is incorrect")

# For matching words
file_name_data_dict_regex_search={}
for file in search_files_list:
    try:
        with open(file, 'r') as searchfile:
            # filedata_list =re.split(r'[^\w]',searchfile.read())
            file_name_data_dict_regex_search[file] = searchfile.read()

    except IOError:
        print("File not found or path is incorrect")

def test_search_methods_simple_regex_equality():
	search_word='of'


	assert simple_search.simple_search_word(search_word,file_name_data_dict_simple_search) == \
           regex_search.regex_search_word(search_word,file_name_data_dict_regex_search)

def test_search_methods_simple_index_equality():
    search_word = 'which'
    # assert cmp()
    assert simple_search.simple_search_word(search_word,file_name_data_dict_simple_search) == \
           index_search.index_search_word(search_word, search_text_file_names_list, files_word_counts)

def test_search_methods_regex_index_equality():
    search_word = 'and'

    assert regex_search.regex_search_word(search_word,file_name_data_dict_regex_search) == \
           index_search.index_search_word(search_word, search_text_file_names_list, files_word_counts)


# For non matching words
def test_search_methods_regex_index_inequality():
    search_word_regex = 'and'
    search_word_index = 'the'

    assert regex_search.regex_search_word(search_word_regex,file_name_data_dict_regex_search) != \
           index_search.index_search_word(search_word_index,search_text_file_names_list, files_word_counts)

def test_simple_search_result_validity():
    search_word='and'

    assert simple_search.simple_search_word(search_word,file_name_data_dict_simple_search) == {'french_armed_forces.txt': 27, 'hitchhikers.txt': 11, 'warp_drive.txt': 3}


def test_regex_search_result_validity():
    search_word = 'in'

    assert regex_search.regex_search_word(search_word, file_name_data_dict_regex_search) == {'french_armed_forces.txt': 28, 'hitchhikers.txt': 6, 'warp_drive.txt': 4}

def test_index_search_result_validity():
    search_word= 'they'

    assert index_search.index_search_word(search_word,search_text_file_names_list,files_word_counts) == {'french_armed_forces.txt': 1, 'hitchhikers.txt': 1, 'warp_drive.txt': 0}
