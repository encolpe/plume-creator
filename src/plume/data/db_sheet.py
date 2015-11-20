'''
Created on 8 aug. 2015

@author: Bardi9 + Cyril Jacquet
'''

import sqlite3
from .exceptions import DbErr
from .db_property import DbProperty

class DbSheet:
    #
    # A class to manipulate single sheets
    #
    def __init__(self, a_db: sqlite3.Connection, i_sheet_id: int, b_commit: bool):
        # You need a sheet id to access this class, with the exception of add()
        # b_commit - set True to have this class do the commit for you. Set False to do the commit
        # yourself (see set_commit() for details)
        #
        # Class variables (consts in UPPERCASE). All vars are considered private - use the setter / getter to access.
        self.a_db = a_db                # db connection
        self.a_err = DbErr()            # Error status
        self.i_sheet_id = i_sheet_id
        self.b_commit = b_commit        # auto commit

    def set_commit(self, b_commit: bool):
        #
        # If you are doing several sheet operations (or operations on several sheets) then you can set commit to
        # False to speed up execution. Sqlite is fast to execute, but slow to commit, so batch commits if you can.
        # (We only make the default True as a fail-safe for users who don't know the rules :) )
        #
        self.b_commit = b_commit

    def get_commit(self):
        #
        return self.b_commit

    def exists(self) -> bool:
        #
        # Returns True if the sheet id exists, False otherwise
        #
        s_sql = """
        select
            l_sheet_id
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """

        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})
        a_row = a_qry.fetchone()
        if a_row is None:
            return False
        else:
            return True

    def get_sort_order(self) -> int:
        #
        # Returns the sort_order of this sheet.
        # Returns R_ERROR (0) if the i_sheet_id is not found.
        #
        s_sql = """
        select
            l_sort_order
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """

        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        a_row = a_qry.fetchone()
        if a_row is None:
            # sheet does not exist
            self.a_err.set_status(DbErr.E_RECNOTFOU, 1, 'Sheet does not exist')
            return DbErr.R_ERROR  # Failed,
        else:
            return a_row[0]

    def set_sort_order(self, i_sort_order: int):
        #
        # Changes l_sort_order for the sheet. Does not check the version or the existence of the sheet.
        #
        s_sql = """
        update
            tbl_sheet
        set
            l_sort_order = :sort,
            dt_updated = CURRENT_TIMESTAMP
        where
            l_sheet_id = :sheet
            """

        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id, 'sort': i_sort_order})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def get_sheet(self):
        #
        # Returns the column (except m_content) of a sheet record as a dict. {'name': value}
        #
        pass
        s_sql = """
        select
            l_sheet_id,
            t_status_code,
            l_sort_order,
            l_indent,
            l_version_code,
            l_dna_code,
            t_title,
            t_badge,
            t_synopsis,
            l_char_count,
            l_word_count,
            dt_created,
            dt_updated,
            dt_content,
            b_deleted
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """
        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        a_row = a_qry.fetchone()
        if a_row is None:
            # sheet does not exist
            self.a_err.set_status(DbErr.E_RECNOTFOU, 1, 'Sheet does not exist')
            return DbErr.R_ERROR  # Failed,
        else:
            return a_row

    def get_content(self) -> str:
        #
        # Returns the content of the sheet
        #
        s_sql = """
        select
            m_content
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """
        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        a_row = a_qry.fetchone()
        if a_row is None:
            # sheet does not exist
            self.a_err.set_status(DbErr.E_RECNOTFOU, 1, 'Sheet does not exist')
            return DbErr.R_ERROR  # Failed,
        else:
            return a_row[0]

    def set_content(self, s_content: str, i_char_count: int = 0, i_word_count: int = 0):
        #
        # Updates the content of the sheet + the cword/char count + timestamp
        #
        s_sql = """
        update
            tbl_sheet
        set
            m_content = :content,
            l_char_count = :charc,
            l_word_count = :wordc,
            dt_content = CURRENT_TIMESTAMP
        where
            l_sheet_id = :sheet
            """

        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id, 'content': s_content, 'charc': i_char_count, 'wordc': i_word_count})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def get_title(self) -> str:
        s_sql = """
            SELECT
                t_title
            FROM
                tbl_sheet
            WHERE
                l_sheet_id=:id
        """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {"id": self.i_sheet_id})
        result = a_curs.fetchone()
        for row in result:
            title = row
        return title

    def set_title(self, s_title: str):
        s_sql = """
        update
            tbl_sheet
        set
            t_title = :title,
            dt_updated = CURRENT_TIMESTAMP
        where
            l_sheet_id = :sheet
            """

        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id, 'title': s_title})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def get_indent(self) -> str:
        s_sql = """
            SELECT
                l_indent
            FROM
                tbl_sheet
            WHERE
                l_sheet_id=:id
        """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {"id": self.i_sheet_id})
        result = a_curs.fetchone()
        for row in result:
            indent = row
        return indent

    def set_indent(self, i_indent: int):
        s_sql = """
        update
            tbl_sheet
        set
            l_indent = :indent,
            dt_updated = CURRENT_TIMESTAMP
        where
            l_sheet_id = :sheet
            """

        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id, 'indent': i_indent})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def set_version(self, i_version: int):
        s_sql = """
        update
            tbl_sheet
        set
            l_version_code = :version,
            dt_updated = CURRENT_TIMESTAMP
        where
            l_sheet_id = :sheet
            """

        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id, 'version': i_version})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def get_version(self) -> int:

        s_sql = """
            SELECT
                l_version_code
            FROM
                tbl_sheet
            WHERE
                l_sheet_id=:id
        """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {"id": self.i_sheet_id})
        result = a_curs.fetchone()
        for row in result:
            version = row
        return version

    def get_properties(self) -> list:
        s_sql = """
            SELECT
                t_name
            FROM
                tbl_sheet_property
            WHERE
                l_sheet_code = :sheet_code
                """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {"sheet_code": self.i_sheet_id})
        result = a_curs.fetchall()
        list_ = []
        for row in result:
            name = row[0]
            p = DbSheetProperty(self.a_db, self.i_sheet_id, name, False)
            list_.append(p.property())
        return list_

    def set_property(self, name, value):
        s_sql = """
            SELECT
                *
            FROM
                tbl_sheet_property
            WHERE
                l_sheet_code = :sheet_code
                and t_name = :name
                """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {"sheet_code": self.i_sheet_id, "name": name})
        a_row = a_curs.fetchone()
        if a_row is None:

            db_property = DbSheetProperty(self.a_db, self.i_sheet_id, name, False)
            db_property.add()
            db_property.value = value

        else:

            db_property = DbSheetProperty(self.a_db, self.i_sheet_id, name, False)
            db_property.value = value

        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def remove_property(self, name):
        s_sql = """
            DELETE FROM
                tbl_sheet_property
            WHERE
                l_sheet_code = :sheet_code
                and t_name = :name
                """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {"sheet_code": self.i_sheet_id, "name": name})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def change_property_name(self, old_name, new_name):

        db_property = DbSheetProperty(self.a_db, self.i_sheet_id, old_name, False)
        db_property.name = new_name
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def set_sheet(self, a_rec: dict):
        #
        # Changes multiple columns in the sheet. a_rec is a dict with one or more keys that are the column
        # names to change. You can't change l_sheet_id. dt_updated is set automatically
        #
        # Remove undesirable keys
        a_rec['l_sheet_id'] = self.i_sheet_id
        a_rec.pop('dt_updated', None)

        if len(a_rec) < 1:
            return DbErr.E_INVPARAM     # Nothing in dict!

        s_upd = ''
        # build update clause of the form t_col = :t_col,
        for s_col in a_rec:
            s_upd += s_col + ' = :' + s_col + ','

        # Remove final ',' before using - [:-1]

        s_sql = 'update tbl_sheet set dt_updated = CURRENT_TIMESTAMP, ' + s_upd[:-1] + ' where l_sheet_id = :l_sheet_id'
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, a_rec)

        if self.b_commit:
            self.a_db.commit()
        return DbErr.R_OK

    def get_count(self):
        #
        # Returns a tuple with the simple character and word counts for this sheet. (The values stored in the record)
        #
        s_sql = """
        select
            l_char_count,
            l_word_count
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """
        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        a_row = a_qry.fetchone()
        if a_row is None:
            # sheet does not exist
            self.a_err.set_status(DbErr.E_RECNOTFOU, 1, 'Sheet does not exist')
            return DbErr.R_ERROR  # Failed,
        else:
            return (a_row['l_char_count'], a_row['l_word_count'])

    def get_count_children(self):
        #
        # Returns a tuple with the character and word counts for all children of this sheet. If the sheets are sorted
        # sort order, then this is the sum of all values for any sheet with a higher indent that this sheet. The last
        # sheet added is the sheet that has the same indent level as this sheet.
        #
        # NOTE: We deliberately don't include the current sheet, since we expect this function to be called once,
        # (when the current sheet starts to be edited), and the count for the current sheet will either already be
        # known, or will be changing, so this functions returns the values needed to ADD to the current sheet to get
        # the total count.
        #

        # Get current sheet values. I'm sure you can do this in a single query...
        s_sql = """
        select
            l_indent,
            l_sort_order
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """

        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        a_row = a_qry.fetchone()
        if a_row is None:
            # sheet does not exist
            self.a_err.set_status(DbErr.E_RECNOTFOU, 1, 'Sheet does not exist')
            return DbErr.R_ERROR  # Failed,

        i_parent_order = a_row['l_sort_order']
        i_parent_indent = a_row['l_indent']

        # Now get children that appear AFTER this sheet (sort Order > current)
        s_sql = """
        select
            l_indent,
            l_char_count,
            l_word_count
        from
            tbl_sheet
        where
            l_sort_order > :sort
        order by
            l_sort_order
        """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sort': i_parent_order})


        i_char = 0
        i_word = 0
        for a_row in a_curs:
            if a_row['l_indent'] <= i_parent_indent:
                break       # No more children
            i_char += a_row['l_char_count']
            i_word += a_row['l_word_count']

        return (i_char, i_word)

    def get_list_of_child_id(self) -> list:
        children = []
        # Get current sheet values. I'm sure you can do this in a single query...
        s_sql = """
        select
            l_indent,
            l_sort_order
        from
            tbl_sheet
        where
            l_sheet_id = :sheet
        """

        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        a_row = a_qry.fetchone()
        if a_row is None:
            # sheet does not exist
            self.a_err.set_status(DbErr.E_RECNOTFOU, 1, 'Sheet does not exist')
            return DbErr.R_ERROR  # Failed,

        i_parent_order = a_row[1]
        i_parent_indent = a_row[0]

        # Now get children that appear AFTER this sheet (sort Order > current)
        s_sql = """
        select
            l_sheet_id,
            l_indent
        from
            tbl_sheet
        where
            l_sort_order > :sort
        order by
            l_sort_order
        """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sort': i_parent_order})

        for a_row in a_curs:
            if a_row[1] <= i_parent_indent:
                break       # No more children
            children.append(a_row[0])

        return children

    def add(self) -> int:
        #
        # Adds a blank sheet, Returns the sheet id, and sets the internal sheet id to the new one.
        #
        s_sql = """
            insert into
                tbl_sheet
            (
                t_title,
                dt_created,
                dt_updated,
                dt_content,
                l_version_code,
                l_dna_code,
                b_deleted
            )
            values(
                :title,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                :version_code,
                0,
                0
            )
            """

        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'title': 'new', 'version_code': 0})

        self.i_sheet_id = a_curs.lastrowid
        if self.b_commit:
            self.a_db.commit()
        return self.i_sheet_id

    def copy(self, s_title_prefix: str) -> int:
        #
        # Copy the current sheet to a new sheet.
        # If s_title_prefix is not blank then:
        #   The sheet title will have s_title_prefix added before, so if s_title _prefix = 'Copy of ' then the
        #           next title will be 'Copy of <old title>'
        #       The sort order will be original + 1.
        #   Sort order is NOT changed if title prefix = ''
        # Returns the sheet id of the new sheet id
        # Does NOT alter the internal sheet id (this instance remains for the original sheet)
        #

        # The columns will need updating if the schema changes!
        # We don't copy the key, nor the created date. We add the title prefix if requested, and
        # the sort_order increment
        s_sql = """
            insert into
                tbl_sheet
            (
                l_sort_order,
                l_indent,
                l_version_code,
                l_dna_code,
                t_title,
                m_content,
                t_synopsis,
                l_char_count,
                l_word_count,
                dt_created,
                dt_updated,
                dt_content,
                b_deleted
            )
            select
                l_sort_order + :incr,
                l_indent,
                :version_code,
                l_dna_code,
                :prefix || t_title,
                m_content,
                t_synopsis,
                l_char_count,
                l_word_count,
                CURRENT_TIMESTAMP,
                dt_updated,
                dt_content,
                b_deleted
            from
                tbl_sheet
            where
                l_sheet_id = :sheet
            """

        a_curs = self.a_db.cursor()

        if s_title_prefix == '':
            # No title prefix implies this is not a copy, so leave the sort order unchanged
            i_incr = 0
        else:
            # It's a copy, add 1 to sort order to position the new sheet under the old one
            i_incr = 1
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id, 'prefix': s_title_prefix,
                               'version_code': self.get_version(), 'incr': i_incr})

        i_new_sheet_id = a_curs.lastrowid

        if self.b_commit:
            self.a_db.commit()

        return i_new_sheet_id

    def version(self, i_version: int) -> int:
        #
        # Create a new version of the sheet:
        # 1. If the dna of the src sheet is null, set it to the sheet_id (if it isn't null it means the src sheet is
        #   is a version of another sheet. The dna is the sheet id of it's original ancestor)
        # 2. Copy the current (src) sheet to a new sheet (this also copies the dna.)
        #
        # DNA Note: Although the dna codde is originally a sheet id, it is not intended to be used as a sheet
        # id. Instead, it is simply a value that is the same for all versions of the same ancestor, even if the
        # ancestor is deleted.
        #
        # Returns the sheet id of the new sheet id
        # Does NOT alter the internal sheet id (this instance remains for the original sheet)
        #

        # Turn off commit until the end of this function
        b_commit = self.get_commit()
        self.set_commit(False)

        # change dna if null
        s_sql = """
        update
            tbl_sheet
        set
            l_dna_code = l_sheet_id
        where
            l_sheet_id = :sheet
            and l_dna_code = 0
            """
        a_curs = self.a_db.cursor()
        a_curs.execute(s_sql, {'sheet': self.i_sheet_id})

        # Now copy the sheet
        i_sheet_id = self.copy('')

        # Change the version of the new sheet
        s_sql = """
        update
            tbl_sheet
        set
            l_version_code = :ver
        where
            l_sheet_id = :sheet
            """
        a_curs.execute(s_sql, {'sheet': i_sheet_id, 'ver': i_version})

        # Restore commit
        self.set_commit(b_commit)  # May be True or False

        if self.b_commit:
            self.a_db.commit()

        return i_sheet_id

    def list_version(self):
        #
        #  Returns a list of all sheets that are a version of this sheet. Sorted by version number?
        #
        s_sql = """
        select
            l_sheet_id
        from
            tbl_sheet
        where
            l_dna_code = (
                select
                    l_dna_code
                from
                    tbl_sheet
                where
                    l_sheet_id = :sheet
                )
            and l_dna_code <> 0
        order by
            l_version_code
            """

        a_curs = self.a_db.cursor()
        a_qry = a_curs.execute(s_sql, {'sheet': self.i_sheet_id})
        a_list = []
        for a_row in a_qry:
            a_list.append(a_row['l_sheet_id'])

        return a_list

    def delete(self) -> int:
        #
        # Mark the sheet as deleted
        #
        s_sql = """
        update
            tbl_sheet
        set
            b_deleted = 1
        where
            l_sheet_id = :sheet
            """
        self.a_db.execute(s_sql, {'sheet': self.i_sheet_id})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def undelete(self) -> int:
        #
        # Mark the sheet as undeleted
        #
        s_sql = """
        update
            tbl_sheet
        set
            b_deleted = 0
        where
            l_sheet_id = :sheet
            """
        self.a_db.execute(s_sql, {'sheet': self.i_sheet_id})
        if self.b_commit:
            self.a_db.commit()

        return DbErr.R_OK

    def commit(self):
        #
        # Commits db. Only needed after all other calls if you set b_commit = False in __init__
        #
        self.a_db.commit()
        return DbErr.R_OK

########################################################################################################################


class DbSheetProperty(DbProperty):
    #
    # A class to manipulate single note properties
    #
    def __init__(self, a_db: sqlite3.Connection, i_sheet_id: int, t_name: str, b_commit: bool):
        super(DbSheetProperty, self).__init__(table_name="tbl_sheet_property", code_column_name="l_sheet_code",
                                             a_db=a_db, i_item_code=i_sheet_id, t_name=t_name, b_commit=b_commit)
