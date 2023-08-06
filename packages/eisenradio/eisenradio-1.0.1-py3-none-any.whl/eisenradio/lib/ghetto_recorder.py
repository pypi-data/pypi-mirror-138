# 0.1.2a
##################################################################################
#   MIT License
#
#   Copyright (c) [2021] [René Horn]
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
###################################################################################
import io
import os
import queue
import shutil
import threading
import urllib.parse
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from time import sleep, strftime, time
from urllib.error import URLError, HTTPError

import urllib3
from eisenradio.api import ghettoApi

# logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
# logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

version = '0.9.0'
print(f'{version} ghettorecorder (eisen_radio module)')  # ########## version #############


class GBase:
    # class attribute
    dict_exit = {}  # all "single" started (this time four, each station)
    dict_error = {}

    sleeper = 2  # for exit of all threads
    pool = ThreadPoolExecutor(200)
    radio_base_dir = os.path.dirname(os.path.abspath(__file__)) + '//radiostations'  # if not set set_radio_base_dir()
    settings_path = os.path.dirname(os.path.abspath(__file__)) + '//settings.ini'  # if not set in set_settings_path()
    path = os.getcwd()
    path_to = path + '//'
    timer = 0

    def __init__(self, radio_base_dir=None, settings_path=None):
        self.instance_attr_time = 0
        self.trigger = False
        self.radio_base_dir = radio_base_dir
        self.settings_path = settings_path

    @staticmethod
    def make_directory(str_path):
        try:
            os.mkdir(str_path)
        except FileExistsError:
            pass
        else:
            print('\t--> created directory: ' + str_path)

    @staticmethod
    def remove_special_chars(str_name):
        # cleanup for writing files and folders

        # my_str = "hey th~!ere. /\ coolleagues?! Straße"
        ret_value = str_name.translate({ord(string): "" for string in '"!@#$%^*()[]{};:,./<>?\|`~=+"""'})
        return ret_value

    @staticmethod
    def this_time():
        time = strftime("%Y-%m-%d %H:%M:%S")
        return time

    def countdown(self, instance_attr_time):
        t = 0
        while not t == instance_attr_time:
            sleep(1)
            self.timer = t
            print(self.timer)
            t += 1
            if t == 0:
                self.trigger = True
        print(f' done {instance_attr_time} {self.trigger}')
        return self.trigger


class GIni(GBase):  # remnant of command line version

    ini_keys = {}  # cls attribute to store selections from ini file, works because of key[key] = value, else not
    srv_param_dict = {}  # all ini keys plus short url, suffix, server type stuff
    start_stop_recording = {}  # ini key: 'start' , 'stop'; while loop check start, working check stop go upper while
    # ini_key + '_single_title', ini_key + '_rec_from_here'
    cost_current_ini = ''  # ini key for cost_dict calc / should be a dict
    cost_dict = {}  # stores len of received headers to calc amount of data searching strings per day
    fail_meta_dict = {}  # can not read metadata from stream, no data
    # list of search strings delimiter blank, first key is named 'STRINGS': Britney Phantom ไม่เคยจะจำ Elton Jim techno
    search_dict = {'STRINGS': 'Britney Spears ไม่เคยจะจำ Elton AC/DC techno Band feat. mix'}  # only show it is working
    list_items = []  # radio key names for display in terminal
    search_title_keys_list = []  # radio short keys, not start recording all streams, only searched titles
    content_type = {}  # header info audio/mpeg

    @staticmethod
    def parse_url_simple_url(radio_url):
        url = radio_url  # whole url is used for connection to radio server

        # 'http:' is first [0], 'ip:port/xxx/yyy' second item [1] in list_url_protocol
        list_url_protocol = url.split("//")
        list_url_ip_port = list_url_protocol[1].split("/")  # 'ip:port' is first item in list_url_ip_port
        radio_simple_url = list_url_protocol[0] + '//' + list_url_ip_port[0]
        return radio_simple_url


class GNet(GBase):
    http_pool = urllib3.PoolManager(num_pools=200)

    @staticmethod
    def load_url(url):
        # returns status code, if server is alive conn.getcode()
        # use urllib, urllib3 causes response to wait "forever" and timeout is not working either
        # print(f' load_url {url}')
        with urllib.request.urlopen(url, timeout=15) as response:
            return response.getcode()

    @staticmethod
    def is_server_alive(url, str_radio):
        # don't delete - urllib3 timeout=5, placebo, retries=None or =2, screw yourself, since half of conn. die
        # we have server up, but content not presented - zombie
        try:
            GNet.load_url(url)
        except HTTPError:  # lots of strange configured web server

            print('HTTPError')
            GBase.dict_error[str_radio] = 'HTTPError - check radio homepage'
            return True
        except URLError as error:  # <urlopen error timed out>
            print(f' ---> {str_radio} server failed: {error} (no recording) {url}')
            GBase.dict_error[str_radio] = error
            print('URLError')
            return False
        return True

    @staticmethod
    def stream_filetype_url(url, str_radio):
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                headers = response.getheader('Content-Type')
        except Exception as ex:
            print(ex)
            return False

        content_type = ''
        if headers == 'audio/aacp' or headers == 'application/aacp':
            content_type = '.aacp'
        if headers == 'audio/aac':
            content_type = '.aac'
        if headers == 'audio/ogg' or headers == 'application/ogg':
            content_type = '.ogg'
        if headers == 'audio/mpeg':
            content_type = '.mp3'
        if headers == 'audio/x-mpegurl' or headers == 'text/html':
            content_type = '.m3u'
        # application/x-winamp-playlist , audio/scpls , audio/x-scpls ,  audio/x-mpegurl

        try:
            GIni.content_type[str_radio] = headers
            if len(headers) <= 5:
                GIni.content_type[str_radio] = 'audio/mpeg'
            # print(f' stream_filetype_url: {GIni.content_type[str_radio]}')
        except Exception as e:
            print(e)
            pass

        return content_type


class GRecorder:
    unknown_title_name = 'unknown_title'
    path_to_song_dict = {}  # {station : file path}
    current_song_dict = {}  # each thread writes the new title to the station key name {station : title}
    start_write_command = {}  # recorder head thread set command to copy first file
    search_pattern_found = {}

    record_active_dict = {}
    listen_active_dict = {}
    ghetto_measure = {}
    ghettoApi.init_ghetto_measurements(ghetto_measure)
    audio_stream_queue_dict = {}
    ghettoApi.init_ghetto_audio_stream(audio_stream_queue_dict)

    @staticmethod  # copy keep-alive timeout=3000
    def ghetto_recorder_display_title(url, str_radio):
        # print(f' ghetto_recorder_display_title: {str_radio}')
        update_terminal = ''
        stream_song_name = GRecorder.current_song_dict[str_radio]
        GIni.fail_meta_dict[url] = 'False'  # message display or not
        GRecorder.search_pattern_found[str_radio] = False

        while not GBase.dict_exit[str_radio]:

            if not len(stream_song_name) <= 2:
                #  GRecorder.current_song_dict[str_radio] = stream_song_name  # WRITE SONG NAME   # :DEACTIVATED:
                stream_song_name = GRecorder.current_song_dict[str_radio]  # :REVERSE:

                if not update_terminal == stream_song_name:
                    update_terminal = stream_song_name
                    try:
                        print(f'\t\t {GBase.this_time().split()[1]} title on {str_radio}: \t {update_terminal}')
                    except UnicodeEncodeError:
                        print('\t\t title on ' + str_radio + ':\t' + 'unicode error (check "$ localectl status")')
                        print('\t\t title on ' + str_radio + ':\t' + 'consider to add additional language support.')

                    except Exception as ex:
                        print('\t\t title on ' + str_radio + ':\t' + 'unknown error (print to your terminal)')
                        print(ex)
                    else:
                        pass
            # give recorder command to record, if we got a match from search gui
            #

            try:
                for _ in GIni.search_title_keys_list:
                    if _ == str_radio:
                        # search option was checked,
                        # call - def search_pattern_start_record, search string match?
                        got_it = GRecorder.search_pattern_start_record(stream_song_name, str_radio)
                        if got_it:
                            GIni.start_stop_recording[str_radio] = 'start'
                        else:
                            GIni.start_stop_recording[str_radio] = 'stop'
                            GRecorder.search_pattern_found[str_radio] = False

            except Exception as ex:
                print(ex)

            for sec in range(GBase.sleeper):
                sleep(1)
                if GBase.dict_exit[str_radio]:
                    # print(f' stop get title {str_radio}')
                    break

    @staticmethod
    def search_pattern_start_record(title, str_radio):
        # search title for strings to see if we should start recording this
        search_list = []  # chop the string

        try:
            strings = GIni.search_dict[str_radio]  # dict with user search strings
            search_list = strings.encode('utf-8').lower().split(b' ')
        except KeyError:
            pass

        for search_str in search_list:

            if not len(search_str) <= 1:  # b'' match problem

                if not title.encode('utf-8').lower().find(search_str) == -1:  # find() returns -1, if not found
                    if not GRecorder.search_pattern_found[str_radio]:
                        print(f'<<<< match station: {str_radio} phrase: {search_str}')
                        GRecorder.search_pattern_found[str_radio] = True
                    return True
        return False

    @staticmethod
    def ghetto_recorder_head(directory_save, stream_suffix, radio_short_key):
        # target: tail works without brain
        # print(f' ghetto_recorder_head -- {radio_short_key}')

        sleep(GBase.sleeper)
        # reader must work (conn. url) for writing the path from title name, can have a loop here
        fresh_song = 'False'
        first_record = True
        brake_loop = False
        GRecorder.start_write_command[radio_short_key] = False

        stream_song_name = GRecorder.current_song_dict[radio_short_key]

        try:
            GBase.make_directory(GBase.radio_base_dir)
        except FileNotFoundError:
            GRecorder.current_song_dict[radio_short_key] = '[{-_-}] ZZZzz zz z... Recorder Failure!'
            GBase.dict_exit[radio_short_key] = True  # all radio_short_key treads-will-stop
            print('\t---> Recorder Write Failure in : ' + GBase.radio_base_dir)
            return

        try:
            GBase.make_directory(GBase.radio_base_dir + '//' + radio_short_key)
        except OSError:
            # "heyth~!ere./\coolleagues?!Straße"
            GRecorder.current_song_dict[radio_short_key] = '[{-_-}] ZZZzz  Recorder Failure !!! DIRECTORY !!!'
            print('\t---> Recorder Write Failure in : ' + GBase.radio_base_dir + '//' + radio_short_key)
            sleep(5)
            GBase.dict_exit[radio_short_key] = True  # all radio_short_key treads-will-stop

            return

        while not brake_loop:
            i = 0
            while not GBase.dict_exit[radio_short_key]:
                if not fresh_song == stream_song_name:

                    if i == 5:
                        print(f' \t\t\t\t\t\t(  (  ( (Eisen Radio) )  )  ) )')
                        i = 0
                    i += 1

                    fresh_song = stream_song_name  # check if it can be removed, we look in a dict now
                    clean_name = GBase.remove_special_chars(stream_song_name)
                    if clean_name == GRecorder.unknown_title_name:  # init name of title on startup
                        clean_name = clean_name + radio_short_key + '_date_' + GBase.this_time()
                        clean_name = GBase.remove_special_chars(clean_name)

                    if first_record:
                        fresh_file_path = directory_save + '//' + '_incomplete_' + str(clean_name) + str(stream_suffix)
                        brake_loop = True
                        GRecorder.path_to_song_dict[radio_short_key] = fresh_file_path
                        GRecorder.start_write_command[radio_short_key] = True

                        first_record = False
                    else:
                        fresh_file_path = directory_save + '//' + str(clean_name) + str(stream_suffix)
                        GRecorder.path_to_song_dict[radio_short_key] = fresh_file_path  # NEW PATH ... ... ...

                    if GBase.dict_exit[radio_short_key]:
                        # print(f' exit head__ {radio_short_key}')
                        break

                    while not GBase.dict_exit[radio_short_key]:

                        stream_song_name = GRecorder.current_song_dict[radio_short_key]
                        if not fresh_song == stream_song_name:
                            break

                        for sec in range(5):
                            if GBase.dict_exit[radio_short_key]:
                                fresh_file_path = directory_save + '//' + '_incomplete_' + clean_name + stream_suffix
                                GRecorder.path_to_song_dict[radio_short_key] = fresh_file_path
                                # print(f' exit head_ {radio_short_key}')
                                break
                            sleep(1)

    @staticmethod
    def g_recorder_await_head(key):
        while not GBase.dict_exit[key]:
            try:
                if GRecorder.start_write_command[key]:
                    break
            except KeyError:
                pass
            else:
                sleep(.1)

    @staticmethod
    def g_recorder_check_dir(key):
        # if dir could not be made, no value
        try:
            file_write_path = GRecorder.path_to_song_dict[key]
            return file_write_path
        except KeyError:
            GRecorder.current_song_dict[key] = '[{-_-}] ZZZzz zz z... Recorder Failure!'
            GBase.dict_exit[key] = True  # all key treads-will-stop
            return False

    @staticmethod
    def g_recorder_request(url):
        # url was tested before in Gnet
        try:
            request = GNet.http_pool.request('GET', url,
                                             headers={'Connection': 'keep-alive'},
                                             timeout=3000,
                                             preload_content=False)
            return request
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def g_recorder_next_file(str_radio, full_file_path, record_file, ghetto_recorder, stream_request_size):
        # COMPLETE file path has changed, new file to write; got new metadata
        if not full_file_path == GRecorder.path_to_song_dict[str_radio]:
            try:
                if os.path.exists(full_file_path):
                    os.remove(full_file_path)
                record_file.flush()

                ghetto_size = os.path.getsize(ghetto_recorder)
                if int(ghetto_size) >= int(stream_request_size):
                    shutil.copyfile(ghetto_recorder, full_file_path)
            except Exception as ex:
                print(ex)

            record_file.seek(0)
            record_file.truncate()

        full_file_path = GRecorder.path_to_song_dict[str_radio]  # SET NEW PATH (title) after copy
        return full_file_path

    @staticmethod
    def g_recorder_teardown(str_radio, record_file, ghetto_recorder, stream_request_size):
        try:
            record_file.flush()
            ghetto_size = os.path.getsize(ghetto_recorder)

            if int(ghetto_size) >= int(stream_request_size):
                ghetto_copy = GRecorder.path_to_song_dict[str_radio]  # full path last file name
                print(f'\t "{str_radio}" last file (marked: _incomplete_): '
                      f'{GRecorder.current_song_dict[str_radio]} ')
                shutil.copyfile(ghetto_recorder, ghetto_copy)
            record_file.close()

            if os.path.exists(ghetto_recorder):
                os.remove(ghetto_recorder)
        except UnicodeEncodeError:
            print(f' {str_radio} copy last file (marked: _incomplete_):')
        except OSError as ex:
            print(ex)

    @staticmethod
    def g_recorder_write_queue(str_radio, chunk):
        if not GRecorder.audio_stream_queue_dict[str_radio + ',audio'].full():
            GRecorder.audio_stream_queue_dict[str_radio + ',audio'].put(chunk)

    @staticmethod
    def ghetto_recorder_tail(url, str_radio, path_to_save, suffix, str_action):

        stream_request_size = io.DEFAULT_BUFFER_SIZE * 4
        audio_stream_queue = queue.Queue(maxsize=20)  # 8KB * 4 * 20
        GRecorder.audio_stream_queue_dict[str_radio + ',audio'] = audio_stream_queue
        ghetto_recorder = path_to_save + '//__ghetto_recorder' + str(suffix)

        GRecorder.g_recorder_await_head(str_radio)

        # for thread in threading.enumerate():
        #     print(thread.name)

        full_file_path = GRecorder.g_recorder_check_dir(str_radio)
        if full_file_path:
            request = GRecorder.g_recorder_request(url)

            if str_action == "record":
                with open(ghetto_recorder, 'wb') as record_file:
                    for chunk in request.stream(stream_request_size):
                        record_file.write(chunk)
                        full_file_path = GRecorder.g_recorder_next_file(str_radio,
                                                                        full_file_path,
                                                                        record_file,
                                                                        ghetto_recorder,
                                                                        stream_request_size)

                        if not GRecorder.record_active_dict[str_radio]:
                            GRecorder.g_recorder_teardown(str_radio, record_file, ghetto_recorder, stream_request_size)
                            break

            if str_action == "listen":
                for chunk in request.stream(stream_request_size):
                    GRecorder.g_recorder_write_queue(str_radio, chunk)
                    if not GRecorder.listen_active_dict[str_radio]:
                        break

    @staticmethod
    def metadata_header_info(request, str_radio, request_time):
        try:
            GRecorder.ghetto_measure[str_radio + ',request_time'] = request_time
            GRecorder.ghetto_measure[str_radio + ',suffix'] = request.headers['content-type']
            GRecorder.ghetto_measure[str_radio + ",icy_genre"] = request.headers["icy-genre"]
            GRecorder.ghetto_measure[str_radio + ",icy_name"] = request.headers["icy-name"]
            GRecorder.ghetto_measure[str_radio + ",icy_br"] = request.headers["icy-br"]
        except KeyError:
            pass

    @staticmethod
    def metadata_icy_info(request):
        try:
            icy_metadata = request.headers['icy-metaint']
            icy_metadata = int(icy_metadata)

            request.read(icy_metadata)
            chunk_1b = request.read(1)
            chunk_1b = ord(chunk_1b)
            read_bytes = chunk_1b * 16
            read_bytes = int(read_bytes)
            metadata_content = request.read(read_bytes)
            return metadata_content
        except KeyError:
            return False

    @staticmethod
    def metadata_request(url):

        request = GNet.http_pool.request('GET', url,
                                         headers={'Icy-MetaData': '1'},
                                         preload_content=False)
        return request

    @staticmethod
    def metadata_get_display_extract(icy_info):
        # StreamTitle='X-Dream - Panic In Paradise * anima.sknt.ru';StreamUrl='';
        try:
            title_info = icy_info.split(";")
            if not len(title_info) > 1 or title_info is None:
                return    # empty list
            title_info = title_info[0].split("=")
            title = str(title_info[1])
            title = GBase.remove_special_chars(title)
            return title
        except IndexError:
            pass
        except OSError:
            pass

    @staticmethod
    def metadata_get_display_info(icy_info):
        # <class 'bytes'> decode to <class 'str'>
        title = ''
        try:
            title = GRecorder.metadata_get_display_extract(icy_info.decode('utf-8'))
        except AttributeError:
            pass
        if not title:
            return
        if title:
            return title

    @staticmethod
    def get_metadata_from_stream_loop(url, str_radio):
        icy_info = ''
        while not GBase.dict_exit[str_radio]:
            try:
                start_time = time()
                response = GRecorder.metadata_request(url)
                request_time = round((time() - start_time) * 1000)
                GRecorder.metadata_header_info(response, str_radio, request_time)
                icy_info = GRecorder.metadata_icy_info(response)
            except HTTPError:
                pass
            except URLError:
                """url was checked in is_server_alive. assume short conn error"""
                pass

            title = GRecorder.metadata_get_display_info(icy_info)
            if title:
                try:
                    if title[0] == "'" and title[-1] == "'":
                        GRecorder.current_song_dict[str_radio] = title[1:-1]   # sequence drop 0 and last char
                    else:
                        GRecorder.current_song_dict[str_radio] = title
                except KeyError:
                    pass
                except Exception as e:
                    print(e)
                    pass

            for sec in range(2):
                if GBase.dict_exit[str_radio]:
                    break     # while
                sleep(1)

    @staticmethod
    def playlist_m3u(url, str_radio):
        # returns the first server of the playlist (not only m3u)
        try:
            read_url = GNet.http_pool.request('GET', url, preload_content=False)
        except Exception as ex:
            print(ex)
        else:
            file = read_url.read().decode('utf-8')

            m3u_lines = file.split("\n")
            # print(' \n    m3u_lines    ' + file)
            m3u_lines = list(filter(None, m3u_lines))  # remove empty rows
            m3u_streams = []
            for row_url in m3u_lines:
                if row_url[0:4].lower() == 'http'.lower():
                    m3u_streams.append(row_url)  # not to lower :)
                    # print(len(m3u_streams))

            if len(m3u_streams) > 1:
                print(f' {str_radio} Have more than one server in playlist_m3u. !!! Take first stream available.')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 1:
                # print(' One server found in playlist_m3u')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 0:
                # print(' No http ... server found in playlist_m3u !!! -EXIT-')
                return False


def check_alive_playlist_container(str_radio, str_url):
    # playlist url?
    if str_url[-4:] == '.m3u' or str_url[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
        # take first from the list
        is_playlist_server = GRecorder.playlist_m3u(str_url, str_radio)

        if not is_playlist_server == '':
            if GNet.is_server_alive(str_url, str_radio):
                str_url = is_playlist_server
            else:
                print('   --> playlist_server server failed, no recording')
            return str_url
    else:
        GNet.is_server_alive(str_url, str_radio)
        return False


def record(str_radio, url, str_action):
    stream_suffix = GNet.stream_filetype_url(url, str_radio)
    GRecorder.current_song_dict[str_radio] = GRecorder.unknown_title_name
    GIni.start_stop_recording[str_radio] = 'start'  # remnant of hit keyword, start record in tk/tcl g.recorder
    # GIni.start_stop_recording[str_radio] = 'stop'   # init it here, checkbox user interface
    GIni.start_stop_recording[str_radio + '_adv'] = 'start_from_here'

    dir_save = GBase.radio_base_dir + '//' + str_radio

    threading.Thread(name=str_radio + '_' + str_action + "_show", target=GRecorder.ghetto_recorder_display_title,
                     args=(url, str_radio),
                     daemon=True).start()
    threading.Thread(name=str_radio + '_' + str_action + "_head", target=GRecorder.ghetto_recorder_head,
                     args=(dir_save, stream_suffix, str_radio),
                     daemon=True).start()
    threading.Thread(name=str_radio + '_' + str_action + "_tail", target=GRecorder.ghetto_recorder_tail,
                     args=(url, str_radio, dir_save, stream_suffix, str_action),
                     daemon=True).start()
    threading.Thread(name=str_radio + '_' + str_action + "_meta", target=GRecorder.get_metadata_from_stream_loop,
                     args=(url, str_radio),
                     daemon=True).start()

    # ################################## end ########################################
    # this version ends here. no loop
