# -*- coding: utf-8 -*-

__author__ = 'http://steamcommunity.com/id/Pentastik/'

from stellaris import Stellaris

if __name__ == "__main__":
    v102 = ('v1.0.2', 'Fc5e')
    v103 = ('v1.0.3', '48f6')

    st = Stellaris(v103)

    '''
    parse all yml files
    '''
    # st.parse_all()
    # st.insert_db()

    '''
    read db then write translated yml files to target dir
    '''
    st.publish()
    st.validate()

    '''
    comment out when you run migration
    this will copy translated data from old table to current table
    currently only use 'ko' column for copy
    '''
    # st.migrate_from(v102)

    '''
    single parse method for test
    '''
    # st.parse('technology_l_english')

    '''
    dump parsed data to console for test
    '''
    # st.dump_all()

    '''
    simply replace keyword in "localization" table's "ko" column
    '''
    # st.replace_all_from_db('findString', 'replaceString')
