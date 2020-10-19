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
            campaign_id  INTEGER       REFERENCES campaigns (id) NOT NULL,
            name         VARCHAR (191) NOT NULL,
            description  TEXT,
            created_at   DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at   DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wa_groups (
            id               INTEGER       PRIMARY KEY,
            segmentation_id  INTEGER       REFERENCES segmentations (id) NOT NULL,
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
            wa_group_id   INTEGER       REFERENCES wa_groups (id) NOT NULL,
            contact_name  VARCHAR (100) NOT NULL,
            administrator BOOLEAN       NOT NULL,
            created_at    DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL,
            updated_at    DATETIME      DEFAULT (datetime('now','localtime')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wa_group_leads (
            id            INTEGER       PRIMARY KEY AUTOINCREMENT,
            wa_group_id   INTEGER       REFERENCES wa_groups (id) NOT NULL,
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
            message_id  INTEGER      REFERENCES messages (id) ON DELETE CASCADE
                                    NOT NULL,
            type        VARCHAR (20) NOT NULL
                                    CHECK (type IN ('text', 'image', 'document', 'video', 'audio') ),
            value       TEXT,
            created_at  DATETIME     NOT NULL
                                    DEFAULT (datetime('now', 'localtime') ),
            updated_at  DATETIME     NOT NULL
                                    DEFAULT (datetime('now', 'localtime') ) 
        );

        CREATE TABLE IF NOT EXISTS campaign_message (
            id             INTEGER      PRIMARY KEY,
            campaign_id    INTEGER      NOT NULL
                                        UNIQUE
                                        REFERENCES campaigns (id),
            message_id     INTEGER      NOT NULL
                                        UNIQUE
                                        REFERENCES messages (id),
            shot           STRING (20)  CHECK (shot IN ('immediate', 'date', 'relative') ),
            scheduler_date DATETIME,
            quantity       INTEGER,
            unit                        CHECK (unit IN ('minutes', 'hours', 'days') ),
            [trigger]      VARCHAR (10) CHECK ([trigger] IN ('before', 'after') ),
            moment         VARCHAR (20) CHECK (moment IN ('start_campaign', 'end_campaign', 'start_monitoring', 'stop_monitoring') ),
            created_at     DATETIME     NOT NULL
                                        DEFAULT (datetime('now', 'localtime') ),
            updated_at     DATETIME     NOT NULL
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
                                campaign_id,
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
                                segmentation_id,
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
                                wa_group_id,
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
                                wa_group_id,
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
                                message_id,
                                type,
                                value
                    ON message_items
        BEGIN
            UPDATE message_items
            SET updated_at = datetime('now', 'localtime') 
            WHERE id = OLD.id;
        END;

        CREATE TRIGGER IF NOT EXISTS campaign_message_updated_at
                AFTER UPDATE OF campaign_id,
                                message_id
                    ON campaign_message
        BEGIN
            UPDATE campaign_message
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

    def existsMessage(self, id):
        return self.__exists(id, "messages")

    def existsMessageItem(self, id):
        return self.__exists(id, "message_items")

    def campaignMessageDestroy(self, campaign_id, message_id):
        sql = """DELETE FROM campaign_message
        WHERE campaign_id = '""" + str(campaign_id) + """' AND 
                message_id = '""" + str(message_id) + """';
        """
        # try:
        con = self.ConexaoBanco()
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
        # except Error as ex:
        #     print(ex)

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

    def segmentationStore(self, id, campaign_id, name, description):
        sql = """INSERT INTO segmentations (
            id,
            campaign_id,
            name,
            description
        )
        VALUES (
            """ + str(id) + """,
            """ + str(campaign_id) + """,            
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

    def groupStore(self, id, segmentation_id, name, image_utl, description,
                   edit_data, send_message, seats, url):
        sql = """INSERT INTO wa_groups (
            id,
            segmentation_id,
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
            """ + str(segmentation_id) + """,
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

    def groupInitialMembersStore(self, id, wa_group_id, contact_name, administrator):
        sql = """INSERT INTO wa_group_initial_members (
            id,
            wa_group_id,
            contact_name,
            administrator
        )
        VALUES (
            """ + str(id) + """,
            """ + str(wa_group_id) + """,
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

    def __nullValue(self, value):
        if value.strip() == '':
            return 'null'
        else:
            return value

    def campaignMessageStore(self, campaign_id, message_id, shot, scheduler_date, quantity, unit, trigger, moment):
        sql = """INSERT INTO campaign_message (
                                 campaign_id,
                                 message_id,
                                 shot,
                                 scheduler_date,
                                 quantity,
                                 unit,
                                 [trigger],
                                 moment
                             )
                             VALUES (
                                 """ + str(campaign_id) + """,
                                 """ + str(message_id) + """,
                                 '""" + shot + """',
                                 """ + self.__nullValue(scheduler_date) + """,
                                 """ + self.__nullValue(str(quantity)) + """,
                                 """ + self.__nullValue(unit) + """,
                                 """ + self.__nullValue(trigger) + """,
                                 """ + self.__nullValue(moment) + """
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

    def messageStore(self, id, name):
        sql = """INSERT INTO messages (
            id,
            name
        )
        VALUES (
            """ + str(id) + """,
            '""" + name + """'
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

    def messageItemsStore(self, id, message_id, type, value):
        sql = """INSERT INTO message_items (
            id,
            message_id,
            type,
            value
        )
        VALUES (
            """ + str(id) + """,
            """ + str(message_id) + """,
            '""" + type + """',
            '""" + value + """'
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

    def groupsToMonitorIndex(self, dict=False):
        con = self.ConexaoBanco()
        if dict:
            con.row_factory = self.__dict_factory
        c = con.cursor()
        sql = """
        SELECT t2.campaign_id,
            segmentation_id,
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
        WHERE t1.segmentation_id = t2.id
        AND t2.campaign_id = t3.id
        AND datetime('now','localtime') BETWEEN t3.start_monitoring AND t3.stop_monitoring
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return r

    def numbersInTheGroupIndex(self, group_id):
        con = self.ConexaoBanco()
        c = con.cursor()
        sql = """SELECT
            number
        FROM wa_group_leads
        WHERE wa_group_id = """ + str(group_id) + """
        AND out = 0;
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return [number[0] for number in r]

    def numbersLeftTheGroupIndex(self, group_id):
        con = self.ConexaoBanco()
        c = con.cursor()
        sql = """SELECT
            number
        FROM wa_group_leads
        WHERE wa_group_id = """ + str(group_id) + """
        AND out = 1;
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return [number[0] for number in r]
    
    def numbersLeftTheGroupUpdate(self, group_id, numbersLeftTheGroup):
        con = self.ConexaoBanco()
        for number in numbersLeftTheGroup:
            sql = """UPDATE wa_group_leads
              SET out = 1
            WHERE wa_group_id = '""" + str(group_id) + """' AND 
                  number = '""" + number.strip() + """';
            """
            # try:
            c = con.cursor()
            c.execute(sql)
            con.commit()
            # except Error as ex:
            #     print(ex)
        con.close()
    
    def sentWelcomeMessageUpdate(self, group_id, number):
        con = self.ConexaoBanco()
        sql = """UPDATE wa_group_leads
            SET sent_welcome = datetime('now','localtime')
        WHERE wa_group_id = '""" + str(group_id) + """' AND 
                number = '""" + number + """';
        """
        # try:
        c = con.cursor()
        c.execute(sql)
        con.commit()
        # except Error as ex:
        #     print(ex)
        con.close()

    def welcomeMessageIndex(self, group_id, dict=True):
        con = self.ConexaoBanco()
        if dict:
            con.row_factory = self.__dict_factory
        c = con.cursor()
        sql = """select
            t5.type,
            t5.value
        from wa_groups t1,
            segmentations t2,
            campaigns t3,
            campaign_message t4,
            message_items t5
        where t1.id = """ + str(group_id) + """
        and t2.id = t1.segmentation_id
        and t3.id = t2.campaign_id
        and t4.campaign_id = t3.id
        and t4.shot = 'immediate'
        and t5.message_id = t4.message_id
        order by t5.id
         """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return r
    
    def newNumbersInTheGroupIndex(self, group_id, dict=True):
        con = self.ConexaoBanco()
        if dict:
            con.row_factory = self.__dict_factory
        c = con.cursor()
        sql = """SELECT
            id,
            number
        FROM wa_group_leads
        WHERE wa_group_id = """ + str(group_id) + """
        and sent_welcome is null
        and out = 0;
        """
        c.execute(sql)
        r = c.fetchall()
        con.close()
        return r

    def newNumbersInTheGroupStore(self, group_id, newNumbersInTheGroup):
        con = self.ConexaoBanco()
        for number in newNumbersInTheGroup:
            sql = """INSERT INTO wa_group_leads (
                wa_group_id,
                number
            )
            VALUES (
                '""" + str(group_id) + """',
                '""" + number.strip() + """'
            )
            ON CONFLICT(number) 
            DO UPDATE SET
               out = 0,
               sent_welcome = null;
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
    # groups = DataBase().groupsToMonitorIndex()
    # print('--------------------------------')
    # for group in groups:
    #     print(group)
    #     print('--------------------------------')

    # # Retorna os números que estão do grupo
    # numbers_in_the_group = DataBase().numbersInTheGroupIndex(1)
    # print('--------------------------------')
    # for number in numbers_in_the_group:
    #     print(number)

    # # Retorna os números que saíram do grupo
    # numbers_left_the_group = DataBase().numbersLeftTheGroupIndex(1)
    # print('--------------------------------')
    # for number in numbers_left_the_group:
    #     print(number)

    # DataBase().numbersInTheGroupDictIndex(1)
    # print(DataBase().numbersInTheGroupIndex(group_id=1, dict=True))

    DataBase().createDatabase()
