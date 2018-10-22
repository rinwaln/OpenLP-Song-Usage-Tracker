
songs_db_location = 'F:\\Google Drive\\Church Music\\Music Sheets\\OpenLP Songs\\songs\\songs.sqlite'
song_usage_location = 'F:\\Google Drive\\Church Music\\Music Sheets\\OpenLP Songs\\songusage\\songusage.sqlite'
save_file = 'songlist.txt'

conn = sqlite3.connect(songs_db_location)
c = conn.cursor()
c.execute("SELECT title, create_date FROM songs")
song_list = c.fetchall()
conn.close

def usage_pull(song):
    conn = sqlite3.connect(song_usage_location)
    c = conn.cursor()
    c.execute("SELECT usagedate FROM songusage_data WHERE title=%s" % (song))
    usages = c.fetchall()
    conn.close
    return usages

def last_use(usages):
    last = 0
    today = datetime.datetime.today()
    if usages == []:
        last_date = 'not yet used'
    else:
        for each in usages:
            each = datetime.datetime.strptime(each[0], "%Y-%m-%d")
            check = today - each
            if last == 0:
                last = check
                last_date = each
            elif last > check:
                last = check
                last_date = each
    return last_date

def get_song(song_list, song_num):
    song = song_list[song_num][0]
    song_num += 1
    return song, song_num

def song_pad(song):
    pad = 40 - len(song)
    song = song + (pad * ' ')
    return song

song_num = 0

def write_line(song_num):
    song, song_num = get_song(song_list, song_num)
    song = json.dumps(song)
    usages = usage_pull(song)
    last_usage = last_use(usages)
    song = song_pad(song)
    line = "%s %s\n" % (song, last_usage)
    return line, song_num

list_len = len(song_list)

f = open(save_file, 'w')
f.write('                  Updates on Tuesdays at midnight\n')
f.write('Song Title                               Last use\n')
while song_num<list_len:
    line, song_num = write_line(song_num)
    f.write(line)
