import os
import stat
import time
import sys

###############################################################################
# Function: createDirTree
# Remarks.: 
#
def createDirTree(path):
  # Only continue if the path is not a directory already.
  if not os.path.isdir(path):
    try:
      os.makedirs(path)
    except OSError as exc:
      if exc.errno == errno.EEXIST:
        pass
      else: raise
  return

###############################################################################
# Function: sortDirs
# Remarks.: 
#
def sortDirs(srcDir):
  srcDir = srcDir.replace('\\', '/')
  dirListing = os.listdir(srcDir)
  for listing in iter(dirListing):
    try:
      fullPath = os.path.join(srcDir, listing)
      s = os.stat(fullPath)
      if stat.S_ISDIR(s[stat.ST_MODE]):
        baseName = os.path.basename(fullPath)
        cT = time.strftime("%Y%m%d", time.localtime(s[stat.ST_MTIME]))
        cTY = time.strftime("%Y", time.localtime(s[stat.ST_MTIME]))
        cTm = time.strftime("%m", time.localtime(s[stat.ST_MTIME]))
        
        if(len(baseName) == 2): continue
        tmpY = baseName[0:4]
        if int(tmpY) > 1900 and int(tmpY) < 2100:
          cTY = tmpY
          cTm = baseName[4:6]
          cTd = baseName[6:8]
        else:
          cTY = baseName[4:8]
          cTm = baseName[0:2]
          cTd = baseName[2:4]
        if cTY == os.path.basename(srcDir):
          newPath = os.path.join(srcDir, cTm,
            cTY + cTm + cTd)
        else:
          newPath = os.path.join(srcDir, cTY, cTm,
            cTY + cTm + cTd)
        print('old path: %s' % fullPath)
        print('new path: %s' % newPath)
        print('')
        os.renames(fullPath, newPath)
    except OSError as exc:
      print('OSError...')
  return

###############################################################################
# Function: sortFiles
# Remarks.: 
#
def sortFiles(ext, srcDir, recurse = False):
  i = 0
  # Convert all \\ to a forward slash, get rid of the headache.
  srcDir = srcDir.replace('\\', '/')
  # Find out the base name of the directory.
  baseName = os.path.basename(srcDir)
  print('Looking in srcDir: %s' % (srcDir))
  # Get a listing of the different files/directories in the source directory.
  dirListing = os.listdir(srcDir)
  # Validate params.
  if ext is None or srcDir is None:
    print('Invalid extension or source directory.')
    return
  # Then go through each listing.
  for listing in iter(dirListing):
    try:
      # Generate the full path to the file.
      fullFilePath = os.path.join(srcDir, listing)
      # Get a stat on the file.
      s = os.stat(fullFilePath)
      # Make sure we are not dealing with a directory.
      if not stat.S_ISDIR(s[stat.ST_MODE]):
        # Get the file name and the extension.
        fileName, fileExtension = os.path.splitext(listing)
        # We only want to deal with the extension specified by caller.
        if fileExtension is not None and fileExtension.lower() == ext.lower():
          # Get the modified time.
          cT = time.strftime("%Y%m%d", time.localtime(s[stat.ST_MTIME]))
          # The modified year.
          cTY = time.strftime("%Y", time.localtime(s[stat.ST_MTIME]))
          # The modified month.
          cTm = time.strftime("%m", time.localtime(s[stat.ST_MTIME]))
          # The modified day.
          cTd = time.strftime("%d", time.localtime(s[stat.ST_MTIME]))
          print('baseName != cTY: %s != %s' % (baseName, cTY))
          # see if we are inside a directory labeled as the "year".
          if baseName != cTY:
            path = os.path.join(srcDir, cTY, cTm, cT)
          else:
            path = os.path.join(srcDir, cTm, cT)
          # Generate the new file name.
          newFile = os.path.join(path, listing)
          # Create the directory tree.
          createDirTree(path)
          # Finally move the file to the new location.
          os.rename(fullFilePath, newFile)
          print('newFile: %s' % newFile)
          print('path: %s' % path)
          print(' File: %s' % listing)
          print('  state.st_mtime: %s' % (cT))
          print('    Year.: %s' % cTY)
          print('    Month: %s' % cTm)
          print('    Day..: %s' % cTd)
    except OSError as xxx_todo_changeme:
      (errno, strerror) = xxx_todo_changeme.args
      print(' OS Error ({0}): file {1}, error: {2}'.format(errno,listing,strerror))
  return

###############################################################################
# Function: usage
# Remarks.: 
#
def usage():
  print('python fileSort.py {ext} {dir}')
  print('')
  print('  ext - Extension to sort (e.g. .txt)')
  print('  dir - Directory to search.')
  print('')
  print('')
  return

###############################################################################
# Function: __main__
# Remarks.: 
#
if __name__ == "__main__":
  if len(sys.argv) <= 2:
    usage()
    exit()
  sortFiles(sys.argv[1], sys.argv[2])
