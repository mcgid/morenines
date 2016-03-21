def print_message(message):
    print message


def print_filelist(header, filelist, footer=None):
    print header

    for line in filelist:
        print "  {}".format(line)

    if footer:
        print footer


def print_filelists(new_files, changed_files, missing_files):
    if new_files:
        print_filelist("Added files (not in index):", new_files)

    if changed_files:
        print_filelist("Changed files (hash differs from index):", changed_files)

    if missing_files:
        print_filelist("Missing files:", missing_files)

    if not any([new_files, changed_files, missing_files]):
        print_message("Index is up-to-date (no changes)")
