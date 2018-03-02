#!/usr/bin/python2

import shutil
import os
import sys
import time
import errno
import optparse
import os.path
import magic
import pathlib
import hashlib
import resource
import subprocess
from progress.bar import FillingSquaresBar
from distutils.dir_util import copy_tree
from colorama import Fore, Back, Style
from colorama import init

dir_exist = []


# Create a list of directories in a file
def more_directory_than_one(source_dir):
    try:
        path = source_dir + '/' + "dir.txt"
        with open(path, "r") as file_:
            lines = file_.readlines()
        return lines
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            "\nAn error occurred through opening or reading dir.txt.\nERROR message:%s") % e
        time.sleep(5)


# Delete source directory or duplicate files
def delete_file_dir(p, dir_path, *other_dir):
    # If p = 1 then you can delete source directory
    # or source directories
    if p == 1:
        try:
            if other_dir:
                for dir_ in other_dir:
                    for line in dir_:
                        split = line.split('\n')
                        target = split[0]
                        shutil.rmtree(target)
                        print Fore.YELLOW + Style.DIM + '\nSource directory: %s is deleted.' % line
                        time.sleep(5)
            else:
                shutil.rmtree(dir_path)
                print Fore.YELLOW + Style.DIM + '\nSource directory: %s is deleted.' % dir_path
                time.sleep(5)
        except OSError:
            pass
        except Exception, e:
            print Fore.RED + Back.BLACK + Style.BRIGHT + (
                '\nCan not delete source directory. ERROR message:\n %s') % e
    # If p = 2 then delete duplicate files

    elif p == 2:
        dup = dir_path
        for key, value in dup.iteritems():
            path_slice = value[1:]
            for path in path_slice:
                try:
                    os.remove(path)
                    print Fore.YELLOW + Style.DIM + '\nFile %s is deleted.' % path
                except Exception, e:
                    print Fore.RED + Back.BLACK + Style.BRIGHT + (
                        '\nAn error occurred during removing file. ERROR:\n %s') % e
    else:
        pass


# Make a list of all duplicate files in a text file
def duplicate_file_list(dupsdict, destination):
    results = list(filter(lambda x: len(x) > 1, dupsdict.values()))
    if len(results) > 0:
        os.system('clear')
        print Fore.MAGENTA + Back.YELLOW + Style.DIM + 'Duplicates Found and saved in duplicate_file_list.txt'
        try:
            path = destination + '/' + "duplicate_file_list.txt"
            table = open(path, "a")
            table.write("===================================" + os.linesep)
            table.write("===========| File Name |===========" + os.linesep)
            table.write("===================================" + os.linesep)
            for result in results:
                for subresult in result:
                    table.write("%s" % subresult + os.linesep)
                table.write("___________________" + os.linesep)
        except Exception, e:
            print Fore.RED + Back.BLACK + Style.BRIGHT + (
                'An error occurred through the listing of duplicate files. ERROR message:\n %s') % e
        finally:
            table.close()
    else:
        os.system('clear')
        print Fore.BLACK + Back.YELLOW + 'No duplicate files found.'


# Make a dictionary of all duplicate files
def findDup(destinationdir):
    # Dups in format {hash:[names]}
    dups = {}
    try:
        for dirName, subdirs, fileList in os.walk(destinationdir):
            os.system('clear')
            print('Scanning %s...' % dirName)
            for filename in fileList:
                # Get the path to the file
                path = os.path.join(dirName, filename)
                # Calculate hash
                file_hash = hashfile(path)
                # Add or append the file path
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        duplicate_file_list(dups, destinationdir)
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            "There is an error to find duplicate files:\n %s") % e

    return dups


# Hashing destination the files
def hashfile(path, blocksize=65536):
    try:
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            "There is an error to hashing the files:\n %s") % e


# Make a list of all source files
def source_file_list(source_files, destination):
    counter = 1
    try:
        path = destination + '/' + "soureFileList.txt"
        table = open(path, "a")
        table.write("===================================" + os.linesep)
        table.write("===========| File Name |===========" + os.linesep)
        table.write("===================================" + os.linesep)
        for root, dir, files in os.walk(source_files):
            for file_ in files:
                table.write("%d - %s" % (counter, file_) + os.linesep)
                table.write("-----------------------------------------------------------" + os.linesep)
                counter = counter + 1
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            'An error occurred through the list of source files. ERROR:\n %s') % e
    finally:
        table.close()


# Make a list of all destination files
def destination_file_list(destination, list_):
    counter = 1
    try:
        path = destination + '/' + "copiedOrMovedFileList.txt"
        table = open(path, "a")
        table.write("=======================================================================" + os.linesep)
        table.write("===========| File Name that copied or moved to destination |===========" + os.linesep)
        table.write("=======================================================================" + os.linesep)
        for file_ in list_:
            table.write("%d - %s" % (counter, file_) + os.linesep)
            table.write("-----------------------------------------------------------" + os.linesep)
            counter = counter + 1
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            'An error occurred through the list of source files. ERROR:\n %s') % e
    finally:
        table.close()


# Make a design for list of all files without
# extension in a text file.
def non_type_file_list_frame(destination):
    try:
        path = destination + '/' + "noneFileType.txt"
        table = open(path, "a")
        table.write("\t -------------------------------------------------------------------------" + os.linesep)
        table.write("\t ---------File name--------------------------Extension log----------------" + os.linesep)
        table.write("\t -------------------------------------------------------------------------" + os.linesep)
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            "Can not print the table in noneFileType.txt the ERROR is :\n %s") % e
    finally:
        table.close()


# list of all files without extension in a text file.
def non_type_file_list(destination, file_name, report):
    try:
        path = destination + '/' + "noneFileType.txt"
        msg = open(path, "a")
        msg.write("\t |\t%s\t|\t%s\t|" % (file_name, report) + os.linesep)
        msg.write("\t==========================================================================" + os.linesep)
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            '\nAn error occurred through the log file.\nERROR: %s') % e
    finally:
        msg.close()


# log file
def log_file(destination, log):
    try:
        path = destination + '/' + "log.txt"
        msg = open(path, "a")
        msg.write(log + os.linesep)
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            'An error occurred through the log file.\nERROR:%s') % e
        time.sleep(2)
    finally:
        msg.close()


# Find file formats by extension
def file_format_finder(filedest, file_name, destination_dir):
    try:
        ext_with_dot = pathlib.Path(file_name).suffix
        dot, ext = ext_with_dot.split('.')
        return ext
    except ValueError:
        try:
            file_path = filedest + '/' + file_name
            file_ext_report = magic.from_file(file_path)
            if file_ext_report == 'empty':
                e = 1
                return e
            else:
                non_type_file_list(destination_dir, file_name, file_ext_report)
                boolean = False
                return boolean
        except IOError:
            ioerror = 'NFOD'
            log = 'File format finder ERROR: %s ===> NOT SUCH A FILE TO FIND THE FORMAT.' % file_name
            log_file(destination_dir, log)
            return ioerror


# Make directory for file without any extension
def other_dir(destination_dir):
    directory = destination_dir + '/OTHER'
    try:
        os.mkdir(directory)
        return directory
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


# Make directories based on extensions
def making_dir(extension, destination):
    if extension.lower() in dir_exist:
        dest = destination + '/' + extension
        return dest
    else:
        try:
            dest = destination + '/' + extension
            os.mkdir(dest)
            dir_exist.append(extension.lower())
            return dest
        except OSError:
            pass


# Move files from source directory to destination directory
def file_mover(source_dir, dist_dir, destination_list, new_file):
    try:
        shutil.move(source_dir, dist_dir)
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            "An error occurred through moving files\n ERROR: %s") % e
    destination_list.append(new_file.lower())


# counting all files in source directory (for bar loading)
def bar_file_counter(source_dir):
    counter = 0
    for root, dir, files in os.walk(source_dir):
        for _ in files:
            counter = counter + 1
    return counter


# Copy files, directory and subdirectories from source to destination
def copy_tree_dir(to_directory, **source_dir):
    try:
        os.system('clear')
        if source_dir != None:
            for name, source in source_dir.iteritems():
                if source_dir[name] != None:
                    if type(source) == list:
                        source = source[:-1]
                    else:
                        source = [source]
                    for line in source:
                        d = line.splitlines()
                        for i in d:
                            new_d = i.split('/')
                        dir_name_as_list = new_d[-1:]
                        target = dir_name_as_list[0]
                        new_dir = to_directory + '/' + target
                        source = ''.join(d)

                        copy_tree(source, new_dir)
    except:
        pass


# If files are duplicate then rename them
def file_renamer(file_, destination_list, bool_):
    try:
        if bool_ == True:
            ext_with_dot = pathlib.Path(file_).suffix
            dot, ext = ext_with_dot.split('.')
            filename = os.path.splitext(file_)[0]
            count = 0
            boolean = True
            while boolean:
                count += 1
                new_file = '%s_%d.%s' % (filename, count, ext)
                boolean = new_file.lower() in destination_list
        else:
            filename = file_
            count = 0
            boolean = True
            while boolean:
                count += 1
                new_file = '%s_%d' % (filename, count)
                boolean = new_file.lower() in destination_list
        return new_file
    except Exception, e:
        print Fore.RED + Back.BLACK + Style.BRIGHT + (
            "An error occurred through renaming duplicated files.\nERROR:%s") % e


# Copy files from source to directory
def file_copier(source_dir, dist_dir, destination_list, new_file, destination_dir):
    try:
        shutil.copy2(source_dir, dist_dir)
        destination_list.append(new_file.lower())
    except IOError:
        log_1 = "File copy ERROR: %s ===> NOT SUCH A FILE OR DIRECTORY FOR COPYING file." % source_dir
        log_file(destination_dir, log_1)
        pass
    except TypeError:
        log_2 = "None type file Error: %s ===> None type found." % source_dir
        log_file(destination_dir, log_2)
    except shutil.Error:
        print Fore.RED + Back.BLACK + Style.BRIGHT + ("\nERROR:Your destination directory is in source "
                                                      "directory please change destination directory "
                                                      "and do in again!")
        time.sleep(5)


# Progress bar header design
def progressing_bar(type_):
    os.system('clear')
    print "=========================================="
    print "===========| %s Processing |============" % type_
    print "=========================================="


# Move files from directories (handler)
def move_file_from_directories(sourceDir, distDir):
    """Take files from directories and after make a directory
     named it as OTHER then check if is that file extension in
     the list or not if not then first make a directory in
     destinations directory and named it as that file extension
     then move files from that directory to destination directory
     that made based on file extension and if file extension is in
     the list so directory is already exist and file will transfer
     to that directory, but if same file name is in the directory
     then this file in a duplicate file and should be rename then
     transfer that and after renaming, and at the end bar progress
     will increase."""

    distlist = []
    boolean = True
    process_type = 'Move'
    counter = bar_file_counter(sourceDir)
    # Customizing bar progress
    bar = FillingSquaresBar('Processing', max=counter)
    for root, dir, files in os.walk(sourceDir):
        for ffile in files:
            file_format = file_format_finder(root, ffile, distDir)
            #  File for mat is not exist in the list
            if file_format == False or file_format == 1:
                lower_ffile = ffile.lower()
                # files with extension
                if lower_ffile in distlist:
                    boolean = False
                    new_file = file_renamer(ffile, distlist, boolean)
                    destdir = distDir + '/OTHER'
                    # OTHER directory for none type files
                    os.rename(os.path.join(root, ffile), os.path.join(destdir, new_file))
                    distlist.append(new_file)
                    log_1 = "'I couldn't recognize the file:=> %s <= type so it is moved to %s dir as %s'" \
                            % (ffile, destdir, new_file)
                    log_file(distDir, log_1)
                    progressing_bar(process_type)
                    # After finish every step bar will forward
                    bar.next()
                # File without extension
                else:
                    src = os.path.join(root, ffile)
                    destdir = distDir + '/OTHER'
                    log_2 = "'I couldn't recognize the file:=> %s <=type so it will been moved to %s dir'" \
                            % (ffile, destdir)
                    log_file(distDir, log_2)
                    file_mover(src, destdir, distlist, ffile)
                    progressing_bar(process_type)
                    bar.next()
            # File format exist in the list
            else:
                new_dir = making_dir(file_format.upper(), distDir)
                if new_dir != 'NFOD':
                    lower_ffile = ffile.lower()
                    if lower_ffile in distlist:
                        new_file = file_renamer(ffile, distlist, boolean)
                        os.rename(os.path.join(root, ffile), os.path.join(new_dir, new_file))
                        distlist.append(new_file)
                        progressing_bar(process_type)
                        bar.next()
                    else:
                        src = os.path.join(root, ffile)
                        file_mover(src, new_dir, distlist, ffile)
                        progressing_bar(process_type)
                        bar.next()
                else:
                    pass

    bar.finish()
    destination_file_list(distDir, distlist)
    print Fore.RED + "WARNING : check Error log file in (%s) as (%s) name." % (distDir, "log.txt")
    print Fore.BLUE + "You can find out files list without extension in (%s) as (%s) name" \
          % (distDir, "noneFileType.txt")
    print Fore.BLUE + "You can find out list of files of source directory in (%s) as (%s) name" \
          % (distDir, "sourceFileList.txt")
    print Fore.BLUE + "You can find out list of all files that moved to destination directory in (%s) as (%s) name" \
          % (distDir, "copiedOrMovedFileList.txt")
    time.sleep(20)


# Copy files from directories (handler)
def copy_file_from_directories(sourceDir, distDir):
    # Like Moving file but here will copying files
    distlist = []
    boolean = True
    process_type = 'Copy'
    counter = bar_file_counter(sourceDir)
    bar = FillingSquaresBar('Processing', max=counter)
    for root, dir, files in os.walk(sourceDir):
        for ffile in files:
            file_format = file_format_finder(root, ffile, distDir)
            #  Check for existing of a file in destination folder
            if file_format == False or file_format == 1:
                lower_ffile = ffile.lower()
                if lower_ffile in distlist:
                    boolean = False
                    new_file = file_renamer(ffile, distlist, boolean)
                    destdir = distDir + '/OTHER'
                    os.rename(os.path.join(root, ffile), os.path.join(root, new_file))
                    src = os.path.join(root, new_file)
                    file_copier(src, destdir, distlist, new_file, distDir)
                    log_1 = "'I couldn't recognize the file:=> %s <= type so it is copied to %s dir as %s'" \
                            % (ffile, destdir, new_file)
                    log_file(distDir, log_1)
                    progressing_bar(process_type)
                    bar.next()
                else:
                    src = os.path.join(root, ffile)
                    destdir = distDir + '/OTHER'
                    log_2 = "'I couldn't recognize the file:=> %s <=type so it will been copied to %s dir'" \
                            % (ffile, destdir)
                    log_file(distDir, log_2)
                    file_copier(src, destdir, distlist, ffile, distDir)
                    progressing_bar(process_type)
                    bar.next()
            else:
                new_dir = making_dir(file_format.upper(), distDir)
                if new_dir != 'NFOD':
                    lower_ffile = ffile.lower()
                    if lower_ffile in distlist:
                        new_file = file_renamer(ffile, distlist, boolean)
                        os.rename(os.path.join(root, ffile), os.path.join(root, new_file))
                        src = os.path.join(root, new_file)
                        file_copier(src, new_dir, distlist, new_file, distDir)
                        progressing_bar(process_type)
                        bar.next()
                    else:
                        src = os.path.join(root, ffile)
                        file_copier(src, new_dir, distlist, ffile, distDir)
                        progressing_bar(process_type)
                        bar.next()
                else:
                    pass

    bar.finish()
    destination_file_list(distDir, distlist)
    print Fore.RED + "WARNING : check Error log file in (%s) as (%s) name." % (distDir, "log.txt")
    print Fore.BLUE + "You can find out files list without extension in (%s) as (%s) name" \
          % (distDir, "noneFileType.txt")
    print Fore.BLUE + "You can find out list of files of source directory in (%s) as (%s) name" \
          % (distDir, "sourceFileList.txt")
    print Fore.BLUE + "You can find out list of all files that copied to destination directory in (%s) as (%s) name" \
          % (distDir, "copiedOrMovedFileList.txt")
    time.sleep(20)


# Options parser
def parsing_options():
    usage = "usage: %prog -s [source path] -d [destination path] [organizer options] [option]"
    parser = optparse.OptionParser(usage=usage, prog='File organizer program', version='1.0', )

    # Source and Destination switch
    parser.add_option('-s', '--source', dest='source', help='Source directory PATH')
    parser.add_option('-d', '--destination', dest='destination', help='Destination directory PATH')

    # Copy, Move, Copytree switch
    parser.add_option('-c', '--copy', action='store_true', dest='copy', help='Copy files from directories')
    parser.add_option('-m', '--move', action='store_true', dest='move', help='Moving files from directories')
    parser.add_option('-C', '--copytree', action='store_true', dest='copytree', help='Copy entire directory'
                                                                                     ' from specific directory')

    # Extra options
    parser.add_option('-M', '--more', dest='more', help='Insert the file path of all directory')
    parser.add_option('-f', '--duplicate', action='store_true', dest='duplicate', help='find all duplicate files from '
                                                                                       'destination directory')
    parser.add_option('-D', '--delete', dest='delete', action='store_true', help='delete file or directory tree')

    # Parsing Options and args together
    (options, args) = parser.parse_args()

    try:
        if options.copy:
            # Make an Other directory for Non-extension file
            other_dir(options.destination)
            non_type_file_list_frame(options.destination)
            source_file_list(options.source, options.destination)
            copy_file_from_directories(options.source, options.destination)

        elif options.move:
            # Make an Other directory for Non-extension file
            other_dir(options.destination)
            non_type_file_list_frame(options.destination)
            source_file_list(options.source, options.destination)
            move_file_from_directories(options.source, options.destination)

        elif options.copytree:
            p = 1
            if options.more:
                lines = more_directory_than_one(options.more)
                copy_tree_dir(options.destination, source=None, sourceMore=lines)
                if options.delete:
                    delete_file_dir(p, options.source, lines)
            else:
                copy_tree_dir(options.destination, source=options.source, sourceMore=None)
                if options.delete:
                    delete_file_dir(p, options.source)

        # Duplicate files content are really the same?
        # Answer find here with hashing files.
        if options.duplicate:
            p = 2
            dup = findDup(options.destination)
            if options.delete:
                delete_file_dir(p, dup)
    except:
        print "Please insert options truly."


# Show description on screen
def show_description():
    init(autoreset=True)
    ls_output = subprocess.check_output(['tput', 'cols'])
    size = '{:^' + ls_output + '}'
    strip = size.replace('\n', '')

    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|8888888888888888888888888888888|++============"))
    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|8888888888888888888888888888888|++============"))
    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|888      File Organizer     888|++============"))
    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|8888888888888888888888888888888|++============"))
    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|8888888888888888888888888888888|++============"))
    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|**|Developed By:Farzin Haque|**|++============"))
    print(Fore.BLUE + Back.WHITE + Style.DIM + strip.format(
        "============++|*********|Version 1.0|*********|++============"))
    # -------------------------------------------------------------------------------------------------------------------------
    print(Fore.BLUE + Back.MAGENTA + Style.BRIGHT + strip.format(
        "File organizer is actually for person like me that never"))
    print(Fore.BLUE + Back.MAGENTA + Style.BRIGHT + strip.format(
        "organize their files from first time :), you can copy all"))
    print(Fore.BLUE + Back.MAGENTA + Style.BRIGHT + strip.format(
        "files from directory and subdirectories or moving them and"))
    print(Fore.BLUE + Back.MAGENTA + Style.BRIGHT + strip.format("they will be organized based on extension ;)."))
    # --------------------------------------------------------------------------------------------------------------------------
    print(Fore.CYAN + Back.BLACK + Style.BRIGHT + strip.format("Main Switches:"))
    # --------------------------------------------------------------------------------------------------------------------------
    print(Fore.BLUE + Back.CYAN + Style.DIM + strip.format("-s or -M: Pass source directory path or "))
    print(Fore.BLUE + Back.CYAN + Style.DIM + strip.format("             dir.txt file path that you want copy"))
    print(Fore.BLUE + Back.CYAN + Style.DIM + strip.format("                 all files/directory/subdirectories from."))
    print(Fore.BLUE + Back.CYAN + Style.DIM + strip.format("                 Example: -M /dir_1/dir_2"))
    print(Fore.BLUE + Back.CYAN + Style.DIM + strip.format("-d: Pass destination directory that you"))
    print(Fore.BLUE + Back.CYAN + Style.DIM + strip.format("    want copy all files/directory to."))
    # ---------------------------------------------------------------------------------------------------------------------------
    print(Fore.CYAN + Back.BLACK + Style.BRIGHT + strip.format("Main Options:"))
    # ---------------------------------------------------------------------------------------------------------------------------
    print(Fore.BLUE + Back.GREEN + Style.DIM + strip.format("-c: Copy all files from directory and subdirectories."))
    print(Fore.BLUE + Back.GREEN + Style.DIM + strip.format("-m: Move all files from directory and subdirectories."))
    print(Fore.BLUE + Back.GREEN + Style.DIM + strip.format("-C: Move all files with subdirectories."))
    # --------------------------------------------------------------------------------------------------------------------------
    print(Fore.CYAN + Back.BLACK + Style.BRIGHT + strip.format("Optionals:"))
    # ---------------------------------------------------------------------------------------------------------------------------
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("-M: If you want to copy more than one directory with"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("    whole subdirectories from source directory"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("    to destination you just need to make a text file"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    and named it as (dir.txt), than copy all directory"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("   path that you want and paste line by line in the text"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    file and with -M option that comes with -C you can pass"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    your file to program and it will copy whole directory"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("    and subdirectories one by one."))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(""))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "-f: With this option if you have duplicated files in your -"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    destination directory so it could be look like foo_1.txt,"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    foo_2.txt ... so this means that your files are duplicated"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    by name but what about content? this option is for that case,"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(
        "    so it will find out your files with duplicate content and"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("    list them in a text file in destination directory."))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format(""))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("-D: This option come with -C either -c or -m:"))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("    will delete duplicate files from destination "))
    print(Fore.BLACK + Back.BLUE + Style.DIM + strip.format("    directory based on content."))
    # ----------------------------------------------------------------------------------------------------------------------------
    print(Fore.BLUE + Back.YELLOW + Style.DIM + strip.format(""))
    print(Fore.BLUE + Back.YELLOW + Style.DIM + strip.format("Attention:Usage:python File_organizer.py "
                                                             "-s [source path] -d [destination path] "
                                                             "[main options] [optional] "))
    print(Fore.BLUE + Back.YELLOW + Style.DIM + strip.format(""))
    # ----------------------------------------------------------------------------------------------------------------------------
    print(Fore.RED + Back.BLACK + Style.BRIGHT + strip.format("WARNING:"))
    print(Fore.RED + Back.BLACK + Style.BRIGHT + strip.format(
        "         Your destination directory could not be in source directory"))
    print(Fore.RED + Back.BLACK + Style.BRIGHT + strip.format("          This program tested "
                                                              "on Linux and it worked fine."))
    print(Fore.RED + Back.BLACK + Style.BRIGHT + strip.format(
        "        using this program is on you and it does not matter"))
    print(Fore.RED + Back.BLACK + Style.BRIGHT + strip.format(
        "        to me if this program does not work good on your system"))
    print(Fore.RED + Back.BLACK + Style.BRIGHT + strip.format("        or damage your files."))


def main():
    # Show some program description
    show_description()

    # Parsing Options
    parsing_options()


if __name__ == '__main__':
    main()