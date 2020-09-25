import sqlite3
from sqlite3 import Error
import os

# sqlite date time
# https://www.tutorialspoint.com/sqlite/sqlite_date_time.htm


class DataBase:

    def __init__(self):
        self.absolutePath = os.path.dirname(__file__)
        self.dataPath = os.path.join(os.path.dirname(__file__), 'data')

    def ConexaoBanco(self):
        caminho = os.path.join(self.dataPath, 'data.sqlite')
        con = None
        # try:
        con = sqlite3.connect(caminho)
        # except Error as ex:
        #     print(ex)
        return con

    def createDatabase(self):

        vCon = self.ConexaoBanco()

        sqlDDL = """
        CREATE TABLE IF NOT EXISTS campaigns (
            id               INTEGER       PRIMARY KEY,
            name             VARCHAR (191) NOT NULL,
            start            DATE          NOT NULL,
            [end]            DATE          NOT NULL,
            start_monitoring DATETIME      NOT NULL,
            stop_monitoring  DATETIME      NOT NULL,
            description      TEXT,
            created_at       DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at       DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
                                           
        );

        CREATE TABLE IF NOT EXISTS segmentations (
            id           INTEGER       PRIMARY KEY,
            campaigns_id INTEGER       REFERENCES campaigns (id) NOT NULL,
            name         VARCHAR (191) NOT NULL,
            description  TEXT,
            created_at   DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at   DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wa_groups (
            id               INTEGER       PRIMARY KEY,
            segmentations_id INTEGER       REFERENCES segmentations (id) NOT NULL,
            name             VARCHAR (191) NOT NULL,
            image_url        VARCHAR (255),
            description      TEXT,
            edit_data        VARCHAR (20),
            send_message     VARCHAR (20),
            seats            INTEGER       NOT NULL,
            url              VARCHAR (255),
            created_at       DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at       DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wa_group_initial_members (
            id            INTEGER       PRIMARY KEY,
            wa_groups_id  INTEGER       REFERENCES wa_groups (id) NOT NULL,
            contact_name  VARCHAR (100) NOT NULL,
            administrator BOOLEAN       NOT NULL,
            created_at    DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at    DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wa_group_leads (
            id            INTEGER       PRIMARY KEY AUTOINCREMENT,
            wa_groups_id  INTEGER       REFERENCES wa_groups (id) NOT NULL,
            number        VARCHAR (25)  NOT NULL,
            sent_welcome  DATETIME,
            out           BOOLEAN       DEFAULT (false) NOT NULL,
            created_at    DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at    DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
        );

        CREATE UNIQUE INDEX IF NOT EXISTS idx_01_wa_group_leads ON wa_group_leads (
            number
        );

        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER       PRIMARY KEY
                                    NOT NULL,
            name       VARCHAR (255) NOT NULL
                                    UNIQUE,
            created_at DATETIME      NOT NULL
                                    DEFAULT (datetime('now', 'localtime') ),
            updated_at DATETIME      DEFAULT (datetime('now', 'localtime') ) 
                                    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS message_items (
            id          INTEGER      PRIMARY KEY
                                    NOT NULL,
            messages_id INTEGER      REFERENCES messages (id) ON DELETE CASCADE
                                    NOT NULL,
            type        VARCHAR (20) NOT NULL
                                    CHECK (type IN ('text', 'image', 'document', 'video', 'audio') ),
            value       TEXT,
            created_at  DATETIME     NOT NULL
                                    DEFAULT (datetime('now', 'localtime') ),
            updated_at  DATETIME     NOT NULL
                                    DEFAULT (datetime('now', 'localtime') ) 
        );

        CREATE TABLE IF NOT EXISTS campaign_messages (
            campaigns_id INTEGER  NOT NULL
                                UNIQUE,
            messages_id  INTEGER  NOT NULL
                                UNIQUE,
            created_at   DATETIME NOT NULL
                                DEFAULT (datetime('now', 'localtime') ),
            updated_at   DATETIME NOT NULL
                                DEFAULT (datetime('now', 'localtime') ) 
        );

        CREATE TRIGGER IF NOT EXISTS campaigns_updated_at
                AFTER UPDATE OF id,
                                name,
                                start,
                                [end],
                                start_monitoring,
                                stop_monitoring,
                                description
                    ON campaigns
        BEGIN
            UPDATE campaigns
            SET updated_at = datetime('now','localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS segmentations_updated_at
                AFTER UPDATE OF id,
                                campaigns_id,
                                name,
                                description
                    ON segmentations
        BEGIN
            UPDATE segmentations
            SET updated_at = datetime('now','localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS wa_groups_updated_at
                AFTER UPDATE OF id,
                                segmentations_id,
                                name,
                                image_url,
                                description,
                                edit_data,
                                send_message,
                                seats,
                                url
                    ON wa_groups
        BEGIN
            UPDATE wa_groups
            SET updated_at = datetime('now','localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS wa_group_initial_members_updated_at
                AFTER UPDATE OF id,
                                wa_groups_id,
                                contact_name,
                                administrator
                    ON wa_group_initial_members
        BEGIN
            UPDATE wa_group_initial_members
            SET updated_at = datetime('now','localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS wa_group_leads_updated_at
                AFTER UPDATE OF id,
                                wa_groups_id,
                                number,
                                sent_welcome,
                                out
                    ON WA_GROUP_LEADS
        BEGIN
            UPDATE wa_group_leads
            SET updated_at = datetime('now','localtime')
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS messages_updated_at
                AFTER UPDATE OF id
                    ON messages
        BEGIN
            UPDATE messages
            SET updated_at = datetime('now','localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS message_items_updated_at
                AFTER UPDATE OF id,
                                messages_id,
                                type,
                                value
                    ON message_items
        BEGIN
            UPDATE message_items
            SET updated_at = datetime('now', 'localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS campaign_messages_updated_at
                AFTER UPDATE OF campaigns_id,
                                messages_id
                    ON campaign_messages
        BEGIN
            UPDATE campaign_messages
            SET updated_at = datetime('now', 'localtime') 
            WHERE id = OLD.id;
        END;
        """
        cur = vCon.cursor()
        cur.executescript(sqlDDL)
        vCon.close()

    def __exists(self, id, tableName):
        c = self.ConexaoBanco().cursor()
        c.execute("SELECT count(id) FROM " +
                  tableName + " WHERE id = " + str(id))
        r = c.fetchone()
        return (r[0] > 0)

    def existsCampaign(self, id):
        return self.__exists(id, "campaigns")

    def existsSegmentation(self, id):
        return self.__exists(id, "segmentations")

    def existsGroup(self, id):
        return self.__exists(id, "wa_groups")

    def existsGroupInitialMembers(self, id):
        return self.__exists(id, "wa_group_initial_members")

    def campaignStore(self, id, name, start, end, start_monitoring, stop_monitoring, description):
        sql = """INSERT INTO campaigns (
            id,
            name,
            start,
            [end],
            start_monitoring,
            stop_monitoring,
            description
        )
        VALUES (
            """ + str(id) + """,
            '""" + name + """',
            '""" + start + """',
            '""" + end + """',
            '""" + start_monitoring + """',
            '""" + stop_monitoring + """',
            '""" + description + """'
        );
        """
        # try:
        con = self.ConexaoBanco()
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
        # except Error as ex:
        #     print(ex)

    def segmentationStore(self, id, campaigns_id, name, description):
        sql = """INSERT INTO segmentations (
            id,
            campaigns_id,
            name,
            description
        )
        VALUES (
            """ + str(id) + """,
            """ + str(campaigns_id) + """,            
            '""" + name + """',
            '""" + description + """'
        );
        """
        # try:
        con = self.ConexaoBanco()
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
        # except Error as ex:
        #     print(ex)

    def groupStore(self, id, segmentations_id, name, image_utl, description,
                   edit_data, send_message, seats, url):
        sql = """INSERT INTO wa_groups (
            id,
            segmentations_id,
            name,
            image_url,
            description,
            edit_data,
            send_message,
            seats,
            url
        )
        VALUES (
            """ + str(id) + """,
            """ + str(segmentations_id) + """,
            '""" + name + """',
            '""" + image_utl + """',
            '""" + description + """',
            '""" + edit_data + """',
            '""" + send_message + """',
            """ + str(seats) + """,
            '""" + url + """'
        );
        """
        # try:
        con = self.ConexaoBanco()
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
        # except Error as ex:
        #     print(ex)

    def groupInitialMembersStore(self, id, wa_groups_id, contact_name, administrator):
        sql = """INSERT INTO wa_group_initial_members (
            id,
            wa_groups_id,
            contact_name,
            administrator
        )
        VALUES (
            """ + str(id) + """,
            """ + str(wa_groups_id) + """,
            '""" + contact_name + """',
            """ + str(administrator) + """
        );
        """

        # try:
        con = self.ConexaoBanco()
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
        # except Error as ex:
        #     print(ex)

    def __dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def getGroupsToMonitor(self, dict=False):
        con = self.ConexaoBanco()
        if dict:
            con.row_factory = self.__dict_factory
        c = con.cursor()
        sql = """
        SELECT t2.campaigns_id,
            segmentations_id,
            t1.id,
            t1.name,
            image_url,
            t1.description,
            edit_data,
            send_message,
            seats,
            url
        FROM wa_groups t1,
            segmentations t2,
            campaigns t3
        WHERE t1.segmentations_id = t2.id
        AND t2.campaigns_id = t3.id
        AND datetime('now','localtime') BETWEEN t3.start_monitoring AND t3.stop_monitoring
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return r

    def getNumbersInTheGroup(self, group_id, dict=False):
        con = self.ConexaoBanco()
        if dict:
            con.row_factory = self.__dict_factory
        c = con.cursor()
        sql = """SELECT
            number
        FROM wa_group_leads
        WHERE wa_groups_id = """ + str(group_id) + """
        AND out = false;
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return r

    def getNumbersLeftTheGroup(self, group_id, dict=False):
        con = self.ConexaoBanco()
        if dict:
            con.row_factory = self.__dict_factory
        c = con.cursor()
        sql = """SELECT
            number
        FROM wa_group_leads
        WHERE wa_groups_id = """ + str(group_id) + """
        AND out = true;
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return r

    def setNumbersLeftTheGroup(self, group_id, numbersLeftTheGroup):
        con = self.ConexaoBanco()
        for number in numbersLeftTheGroup:
            sql = """UPDATE wa_group_leads
              SET out = 'true'
            WHERE wa_groups_id = '""" + group_id + """' AND 
                  number = '""" + number.strip() + """';
            """
            # try:
            c = con.cursor()
            c.execute(sql)
            con.commit()
            # except Error as ex:
            #     print(ex)
        con.close()

    def setNewNumbersInTheGroup(self, group_id, newNumbersInTheGroup):
        con = self.ConexaoBanco()
        for number in newNumbersInTheGroup:
            sql = """INSERT INTO wa_group_leads (
                wa_groups_id,
                number
            )
            VALUES (
                '""" + str(group_id) + """',
                '""" + number.strip() + """'
            )
            ON CONFLICT(number) 
            DO UPDATE SET out = false;
            """
            # try:
            c = con.cursor()
            c.execute(sql)
            con.commit()
            # except Error as ex:
            #     print(ex)
        con.close()


if __name__ == "__main__":
    # # Retorna os grupos da campanha que estão dentro do preríodo para sererm monitorados
    # groups = DataBase().getGroupsToMonitor()
    # print('--------------------------------')
    # for group in groups:
    #     print(group)
    #     print('--------------------------------')

    # # Retorna os números que estão do grupo
    # numbers_in_the_group = DataBase().getNumbersInTheGroup(1)
    # print('--------------------------------')
    # for number in numbers_in_the_group:
    #     print(number)

    # # Retorna os números que saíram do grupo
    # numbers_left_the_group = DataBase().getNumbersLeftTheGroup(1)
    # print('--------------------------------')
    # for number in numbers_left_the_group:
    #     print(number)

    # DataBase().getNumbersInTheGroupDict(1)
    # print(DataBase().getNumbersInTheGroup(group_id=1, dict=True))

    DataBase().createDatabase()
