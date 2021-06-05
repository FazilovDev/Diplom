import models.algorithms.ast_algorithm.astt as ast


def get_source_code_from_file(filename):
    file = open(filename, 'r')
    code = file.read()
    file.close()
    return code

def get_source_code_lines_from_file(filename):
    file = open(filename, 'r')
    code = file.readlines()
    file.close()
    return code

def get_plag_ast_all_files(filenames):
    print(filenames)

def get_plag_ast(file1, file2):
    code1 = get_source_code_from_file(file1)
    code2 = get_source_code_from_file(file2)

    results = ast.detect([code1, code2], diff_method=ast.UnifiedDiff, keep_prints=True, module_level=False)

    results_labels = []
    for index, func_ast_diff_list in results:
        print('ref: {}'.format(file1))
        print('candidate: {}'.format(file2))
        sum_plagiarism_percent, sum_plagiarism_count, sum_total_count = ast.summarize(func_ast_diff_list)
        print('{:.2f} % ({}/{}) of ref code structure is plagiarized by candidate.'.format(
            sum_plagiarism_percent * 100,
            sum_plagiarism_count,
            sum_total_count,
        ))

        output_count = 0
        for func_diff_info in func_ast_diff_list:
            if len(func_diff_info.info_ref.func_ast_lines) >= 1 and func_diff_info.plagiarism_percent >= 0.65:
                output_count = output_count + 1
                print(func_diff_info)
                results_labels.append([sum_plagiarism_percent, func_diff_info.info_ref.func_node, func_diff_info.info_candidate.func_node])

        if output_count == 0:
            print('<empty results>')

    return results_labels

def get_str_from_list_code(list_code, start, end):
    if start == end:
        return list_code[start]
    res = ''
    for i in range(start, end):
        res += list_code[i]
    return res

def get_source_code_from_ast_detect(filename1, filename2):
    result = get_plag_ast(filename1, filename2)
    code1 = get_source_code_lines_from_file(filename1)
    code2 = get_source_code_lines_from_file(filename2)

    point = result[0][1]
    point2 = result[0][2]

    text_code1 = ''
    text_code2 = ''
    current_index = 0
    current_index2 = 0
    code_1 = list()
    code_2 = list()

    for i in range(len(result)):
        point = result[i][1]
        point2 = result[i][2]
        text_code1 += '{}\033[31m{}\033[0m'.format(get_str_from_list_code(code1, current_index, point.lineno-1), get_str_from_list_code(code1, point.lineno-1, point.endlineno))
        text_code2 += '{}\033[31m{}\033[0m'.format(get_str_from_list_code(code2, current_index2, point2.lineno-1), get_str_from_list_code(code2, point2.lineno-1, point2.endlineno))

        code_1.append(get_str_from_list_code(code1, current_index, point.lineno-1))
        code_1.append(get_str_from_list_code(code1, point.lineno-1, point.endlineno))

        code_2.append(get_str_from_list_code(code2, current_index2, point2.lineno-1))
        code_2.append(get_str_from_list_code(code2, point2.lineno-1, point2.endlineno))

        current_index = point.endlineno
        current_index2 = point2.endlineno
    return result[0][0], code_1, code_2

#filename1 = 'Tests\\Python\\test3.py'
#filename2 = 'Tests\\Python\\test1.py'

#plag_percent, text1, text2 = get_source_code_from_ast_detect(filename1, filename2)

#print(text2)

