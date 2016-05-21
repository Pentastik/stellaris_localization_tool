# -*- coding: utf-8 -*-

import codecs
import glob
import pymongo
import os
import sys
import re
import json


class Stellaris:
    publish_dir = 'D:\\Documents\\Paradox Interactive\\Stellaris\\mod\\koreantranslation\\localisation'
    localization_dir = 'D:\\GoodGame\\Steam\\steamapps\\common\\Stellaris\\localisation'
    special_chars = ['£', '§!', '§']

    class Localisation:
        """
        default localization line text

        KEY:NUM "TEXT"
        """
        regex = '([\w\d\.\-]*)(?::)(\d{1})(?:\s{1}\")(.*)(?:\")'  # 1: key, 2: num, 3: text

        def __init__(self):
            pass

    class Tag:
        """
        using comment in localization as tag

        # Tag
        ## TAG  <<== (ignore parsing)
        """
        regex = '(?:\s?#\s{1,3})([\w\s\-]*)'  # 1: key

        def __init__(self):
            pass

    class Function:
        """
        [type:group.method]
        [group.method:group.method]
        """
        regex = '(?:\[)(([\w\.\-]*)(?::))?([\w\.]*)(?:\.)(\w*)(?:\])'  # 2:type, 3: group, 4: method

        def __init__(self):
            pass

    class Keyword:
        """
        you can use left side key of localization as keyword

        $keyword$
        $keyword|Modifier$
        """
        regex = '(?:\$)(\w*)((?:\|)([\d\w\-\+\=\%]*))?(?:\$)'  # 1: key, 3: modifier

        def __init__(self):
            pass

    class Section:
        """
        highlight text with color code
        color code can found in interface/fonts.gfx

        §[colorCode]text§!
        """
        regex = '(?:§)([A-Z]{1})(.*)(?:§!)'  # 1: color, 2: body

        def __init__(self):
            pass

    class Pound:
        """
        use for display icon image

        £iconName[space]
        """
        regex = '(?:£)([\w\|\$]*)(?:\s{1})'  # 1: key

        def __init__(self):
            pass

    class Plate:
        """
        don't know where it use
        but it looks like function

        <SomeThing>
        <Some Thing>
        <Some Thing number>
        """
        regex = '(?:\<)(\w*)(?:\>)'  # 1: key

        def __init__(self):
            pass

    def __init__(self, version_info):
        self.version, self.checksum = version_info
        self.yml = []
        self.localization = []
        self.tag = []
        self.function = []
        self.keyword = []
        self.section = []
        self.pound = []
        self.plate = []
        self.total = 0

        self.load()

    def load(self):
        yml_files = glob.glob1(Stellaris.localization_dir, "*l_english.yml")

        for yml_file in yml_files:
            file_name, file_extension = os.path.splitext(yml_file)
            self.yml.append({'file_name': file_name, 'version': self.version, 'checksum': self.checksum})

    def parse_all(self):
        for files in self.yml:
            self.parse(files['file_name'])

        print 'total: ' + str(self.total)

    def parse(self, file_name):
        """
        parse yml file

        :param file_name: full name with ext
        """
        if file_name is None:
            raise ValueError('file_name is not specified')

        with open(Stellaris.localization_dir + '\\' + file_name + '.yml') as yml:
            total_count = 0
            current_tag = None
            localisation_list = []

            for line in yml:
                stripped_text = line.replace('\u00a7', '§').strip()

                # find tag
                if stripped_text.startswith('#'):
                    m = re.search(Stellaris.Tag.regex, stripped_text)
                    if m:
                        temp = m.group(1).strip()
                        if temp == '':
                            continue

                        current_tag = temp

                        tag = Stellaris.Tag()
                        tag.file_name = file_name
                        tag.key = current_tag
                        tag.text = m.group(0)

                        self.tag.append(tag.__dict__)

                    # ignore comment
                    continue

                # validate
                m = re.search(Stellaris.Localisation.regex, stripped_text)

                # if stripped_text.count('engineering') > 0:
                #     print stripped_text

                if m is None:
                    continue

                localisation = Stellaris.Localisation()
                localisation.status = 'init'
                localisation.version = self.version
                localisation.checksum = self.checksum
                localisation.yml = file_name
                localisation.tag = current_tag
                localisation.text = m.group(0)
                localisation.key = m.group(1)
                localisation.num = m.group(2)
                localisation.en = m.group(3)
                localisation.ko = m.group(3)
                localisation.type = 'mixed'

                simple_type = True

                match = re.finditer(Stellaris.Plate.regex, localisation.text)
                for m in match:
                    plate = Stellaris.Plate()
                    plate.key = m.group(1)
                    plate.text = m.group(0)

                    self.plate.append(plate.__dict__)
                    simple_type = False

                match = re.finditer(Stellaris.Pound.regex, localisation.text)
                for m in match:
                    pound = Stellaris.Pound()
                    pound.key = m.group(1)
                    pound.ko = m.group(1)
                    pound.text = m.group(0)

                    self.pound.append(pound.__dict__)
                    simple_type = False

                match = re.finditer(Stellaris.Section.regex, localisation.text)
                for m in match:
                    section = Stellaris.Section()
                    section.color = m.group(1)
                    section.body = m.group(2)
                    section.text = m.group(0)

                    self.section.append(section.__dict__)
                    simple_type = False

                match = re.finditer(Stellaris.Keyword.regex, localisation.text)
                for m in match:
                    keyword = Stellaris.Keyword()
                    keyword.key = m.group(1)
                    keyword.modifier = m.group(2)
                    keyword.text = m.group(0)

                    self.keyword.append(keyword.__dict__)
                    simple_type = False

                match = re.finditer(Stellaris.Function.regex, localisation.text)
                for m in match:
                    function = Stellaris.Function()
                    function.type = m.group(2)
                    function.group = m.group(3)
                    function.method = m.group(4)
                    function.text = m.group(0)

                    self.function.append(function.__dict__)
                    simple_type = False

                if simple_type:
                    localisation.type = 'simple'

                total_count += 1

                localisation_list.append(localisation.__dict__)
                self.localization.append(localisation.__dict__)

            # self.write_json(file_name, item_info_list)

        self.total += total_count
        print '{0} parsed: {1}'.format(file_name, total_count)

    def write_json(self, yml_file_name, item_info_list):
        """
        test method. write parsed data to json file
        :param yml_file_name:
        :param item_info_list:
        :return:
        """
        file_name, file_extension = os.path.splitext(yml_file_name)

        with open('D:\\' + file_name + '.json', mode='w') as f:
            f.write(json.dumps(item_info_list, indent=2))

    def insert_db(self):
        """
        insert parsed data array to db
        """
        conn = pymongo.MongoClient(host='192.168.0.150')
        db = conn['stellaris_' + self.checksum]

        """
        self.yml = []
        self.localization = []
        self.tag = []
        self.function = []
        self.keyword = []
        self.section = []
        self.pound = []
        self.plate = []
        """
        if len(self.yml) > 0:
            print 'insert yml to db...'
            table = db['yml']
            table.drop()
            table.insert_many(self.yml)
            table.create_index('file_name', background=True)

        if len(self.localization) > 0:
            print 'insert localization to db...'
            table = db['localization']
            table.drop()
            table.insert_many(self.localization)
            table.create_index('key', background=True)

        if len(self.tag) > 0:
            print 'insert tag to db...'
            # for tag in self.tag:
            #     print tag

            table = db['tag']
            table.drop()
            table.insert_many(self.tag)
            table.create_index([("file_name", pymongo.ASCENDING), ("key", pymongo.ASCENDING)], background=True)

        if len(self.keyword) > 0:
            print 'insert keyword to db...'
            table = db['keyword']
            table.drop()
            table.insert_many(self.keyword)
            table.create_index('key', background=True)

        if len(self.section) > 0:
            print 'insert section to db...'
            table = db['section']
            table.drop()
            table.insert_many(self.section)
            table.create_index('color', background=True)

        if len(self.pound) > 0:
            print 'insert pound to db...'
            table = db['pound']
            table.drop()
            table.insert_many(self.pound)
            table.create_index('key', background=True)

        if len(self.plate) > 0:
            print 'insert plate to db...'
            table = db['plate']
            table.drop()
            table.insert_many(self.plate)
            table.create_index('key', background=True)

    def publish(self):
        """
        let's write translated yml from db
        """
        conn = pymongo.MongoClient(host='192.168.0.150')
        db = conn['stellaris_' + self.checksum]

        table = db['yml']
        yml_list = table.find({})

        for yml in yml_list:
            yml = yml['file_name']
            file_name = '{0}.yml'.format(yml)

            print '{0} writing...'.format(file_name)

            table = db['localization']
            localisation_list = table.find({"yml": yml})

            with open(Stellaris.publish_dir + '\\' + file_name, mode='wb') as yml_file:
                line_list = []

                line_list.append('l_english:\n')

                for localisation in localisation_list:
                    line = ' {0}:{1} "{2}"\n'.format(localisation['key'].encode('utf-8'), localisation['num'].encode('utf-8'), localisation['ko'].encode('utf-8'))
                    # line = ' ' + str(unicode(localisation['key'], 'utf-8')) +':'+ str(unicode(localisation['num'], 'utf-8')) +' "'+ str(unicode(localisation['ko'], 'utf-8')) +'"\n'
                    line_list.append(line)

                yml_file.write(codecs.BOM_UTF8)
                yml_file.writelines(line_list)

    def migrate_from(self, old_version_info):
        """
        simply migrate from old db to new db
        :param old_version_info: tuple data (version_name, version_checksum)
        :return:
        """
        old_version, old_checksum = old_version_info

        conn = pymongo.MongoClient(host='192.168.0.150')
        old_db = conn['stellaris_' + old_checksum]
        current_db = conn['stellaris_' + self.checksum]

        table = 'yml'
        print 'processing table: %s' % (table)

        old_table = old_db[table]
        current_table = current_db[table]

        old_cursor = old_table.find().sort([
            ('file_name', pymongo.ASCENDING)
        ])

        for yml_info in old_cursor:
            file_name = yml_info['file_name']

            count = current_table.count({
                'file_name': file_name
            })

            if count != 1:
                print '\tNot found file name: %s %d' % (file_name, count)

        table = 'localization'
        print 'processing table: %s' % (table)

        old_table = old_db[table]
        current_table = current_db[table]

        old_cursor = old_table.find().sort([
            ('yml', pymongo.ASCENDING),
            ('key', pymongo.ASCENDING)
        ])

        total = 0
        for localization_info in old_cursor:
            # update
            result = current_table.update_one({
                'yml': localization_info['yml'],
                'key': localization_info['key']
            }, {
                '$set': {
                    'ko': localization_info['ko']
                }
            }, upsert=False)

            # aready updated if modified_count is 0
            print 'yml: %s, key: %s, modified_count: %d' %(localization_info['yml'], localization_info['key'], result.modified_count)

            total += 1

        print 'total: %d' % (total)

    def validate(self):
        """
        simply check count of data with colol(:) from original yml and translated yml
        """
        rt = 0
        mt = 0
        tt = 0

        for file_name in glob.glob1(Stellaris.localization_dir, "*l_english.yml"):
            sys.stdout.write('[{0:35s}] '.format(file_name))
            sys.stdout.flush()

            real_total = 0
            mod_total = 0
            translated_total = 0

            real_keys = []
            mod_keys = []

            real_data = {}
            mod_data = {}

            with open(Stellaris.localization_dir + '\\' + file_name) as real:
                for line in real:
                    text = line.strip()

                    if text.startswith('#'):
                        continue

                    if text.count(':') > 0:
                        real_total += 1

                        splitted = text.split(':');

                        real_keys.append(splitted[0])

                        real_data[splitted[0]] = splitted[1]

            with open(Stellaris.publish_dir + '\\' + file_name) as mod:
                for line in mod:
                    text = line.strip()

                    if text.startswith('#'):
                        continue

                    if text.count(':') > 0:
                        mod_total += 1

                        splitted = text.split(':');

                        mod_keys.append(splitted[0])

                        mod_data[splitted[0]] = splitted[1]


            for real_key in real_keys:
                for mod_key in mod_keys:
                    if real_key == mod_key:
                        if real_data[real_key] != mod_data[real_key]:
                            translated_total += 1

                        mod_keys.remove(mod_key)
                        break

            print '[Real/Mod/Translated] {0:4d} {1:4d} {2:4d} {3:7.2%}'.format(real_total, mod_total, translated_total, (float(translated_total)/float(real_total)))

            if real_total != mod_total:
                raise ValueError('incorrect mode_keys: {0}'.format(mod_keys))

            rt += real_total
            mt += mod_total
            tt += translated_total

        print '{0:4d} / {1:4d} ({2:7.2%})'.format(tt, rt, (float(tt)/float(rt)))

    def dump_all(self):
        print json.dumps(self.yml_files, indent=2)
        print json.dumps(self.localization, indent=2)
        print json.dumps(self.tag_list, indent=2)
        print json.dumps(self.keyword_list, indent=2)
        print json.dumps(self.keyword_name_list, indent=2)

    def replace_all_from_db(self, str_to_find, str_to_replace):
        if (str_to_find is None or str_to_replace is None):
            pass

        print '{0} => {1}'.format(str_to_find, str_to_replace)

        conn = pymongo.MongoClient(host='192.168.0.150')
        db = conn['stellaris_' + self.checksum]
        table = db['localization']

        cursor = table.find({
            'ko': {
                '$regex': '{0}'.format(str_to_find),
                '$options': 'i'
            }
        }).sort([
            ('ko', pymongo.ASCENDING)
        ]).limit(1000)

        pattern = re.compile(re.escape(str_to_find.decode('utf-8')), re.IGNORECASE)

        total = 0
        for localization in cursor:
            ko = localization['ko']

            replaced_ko = re.sub(pattern, str_to_replace.decode('utf-8'), ko)

            table.update_one({
                '_id': localization['_id']
            }, {
                '$set': {
                    'ko': replaced_ko.encode('utf-8')
                }
            }, upsert=False)

            total += 1

        print 'replaced total: %d' % (total)

