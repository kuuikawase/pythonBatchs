import glob


# フォルダ内ファイル検索

# path：対象フォルダパス
# extension：対象拡張子
def search(path, extension):
    return glob.glob(path + '/*.' + extension)


# サブディレクトリ内も検索
def search_sub_folder(path, extension):
    return glob.glob(path + '/*.' + extension, recursive=True)


# 検索したファイルパスの検索ルートと拡張子を削除
def remove_path_search(path, extension):
    search_files = search(path, extension)
    replace_files = []
    for file in search_files:
        replace_file_name = file.replace(path + "\\", "")
        replace_file_name = replace_file_name.replace("." + extension, "")
        replace_files.append(replace_file_name)

    return replace_files


# 検索したファイルパスの検索ルートと拡張子を削除
def remove_path_search_sub_folder(path, extension):
    search_files = search_sub_folder(path, extension)
    replace_files = []
    for file in search_files:
        replace_file_name = file.replace(path + "\\", "")
        replace_file_name = replace_file_name.replace("." + extension, "")
        replace_files.append(replace_file_name)

    return replace_files


def search_keyword_file(path, extension, keyword):
    file_list = remove_path_search(path, extension)
    l_in = [s for s in file_list if keyword in s]
    print(l_in)
    return l_in
