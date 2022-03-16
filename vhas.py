# Vhas (an acronym for video host auto store)
# a python library to facilitate the management of video files.
# Copyright (C) 2022 Dita Aji Pratama
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import mysql.connector as mariadb
import cv2

def CheckFileName(path):
    filename, file_extension = os.path.splitext(path)
    return filename

def CheckFileType(path):
    filename, file_extension = os.path.splitext(path)
    return file_extension

def CheckFileSize(path):
    # return in byte
    return os.path.getsize(path)

def CheckFileHeight(path):
    vid = cv2.VideoCapture(path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return height

def CheckFileWidth(path):
    vid = cv2.VideoCapture(path)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    return width

def CountDir(storage):
    return len(os.listdir(storage))

def CountDb(dbin, table):
    con = mariadb.connect(**dbin)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `"+table+"`;")
    result = cursor.fetchall()
    total = len(result)
    con.close()
    return total

def CountCompare(storage, dbin, table):
    storage_count = CountDir(storage)
    print('[DEBUG] Storage Count: '+str(storage_count))
    record_count = CountDb(dbin, table)
    print('[DEBUG] Record Count: '+str(record_count))
    if storage_count == record_count:
        print('[DEBUG] Sync well!')
        return 'ok'
    elif storage_count > record_count:
        print('[DEBUG] New file detected!')
        return 'new'
    elif storage_count < record_count:
        print('[DEBUG] Warning: Some videos is missing!')
        return 'miss'
    else:
        print('[DEBUG] Unknown Error!')
        return 'error'

def NewFileDetector(storage, dbin, table):
    # cek for list dari directori
    new_file_count  = 0
    new_file        = []
    content         = os.listdir(storage)
    for row1 in content:
        con     = mariadb.connect(**dbin)
        cursor  = con.cursor()
        cursor.execute("SELECT * FROM `"+table+"` WHERE id = '"+row1+"';")
        result      = cursor.fetchall()
        detected    = len(result)
        con.close()
        if detected == 0:
            new_file_count += 1
            info = {
                "file": row1,
                "name"     : CheckFileName      (row1),
                "type"     : CheckFileType      (row1),
                "size"     : CheckFileSize      (storage+row1),
                "height"   : CheckFileHeight    (storage+row1),
                "width"    : CheckFileWidth     (storage+row1)
            }
            new_file.append(info)

    result = {
        "count" : new_file_count,
        "info"  : new_file
    }
    return result

def MissingFileDetector(storage, dbin, table):
    # cek for list dari database
    pass

def NewFileInsertData():
    pass

def MissingFileRemoveData():
    pass
