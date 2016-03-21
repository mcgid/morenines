def print_message(message):
    print message


def print_filelist(header, filelist, footer=None):
    print header

    for line in filelist:
        print "  {}".format(line)

    if footer:
        print footer
