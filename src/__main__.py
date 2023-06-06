from deps.dependencies import file_splitter, file_merger_factory


def main():
    # Step 1) Split the raw file into several small files
    file_splitter.split_file()

    # Step 2) Merge resulted files into one
    file_merger = file_merger_factory(file_splitter.get_created_files_names())
    file_merger.merge_files()


main()
