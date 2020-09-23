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

    def executeCommand(self, con, DDL):
        # try:
        c = con.cursor()
        c.executescript(DDL)
        # except Error as ex:
        #     print(ex)

    def createDatabase(self):

        vCon = self.ConexaoBanco()

        # CAMPAIGNS
        sqlDDL = """
        CREATE TABLE IF NOT EXISTS campaigns (
            id               INTEGER       PRIMARY KEY,
            name             VARCHAR (191) NOT NULL,
            start            DATETIME      NOT NULL,
            [end]            DATETIME      NOT NULL,
            start_monitoring DATETIME      NOT NULL,
            stop_monitoring  DATETIME      NOT NULL,
            description      TEXT,
            created_at       DATETIME      DEFAULT (datetime()) NOT NULL,
            updated_at       DATETIME      DEFAULT (datetime()) NOT NULL
                                           
        );
        """
        self.executeCommand(vCon, sqlDDL)

        # SEGMENTATIONS
        sqlDDL = """
        CREATE TABLE IF NOT EXISTS segmentations (
            id           INTEGER       PRIMARY KEY,
            campaigns_id INTEGER       REFERENCES campaigns (id) NOT NULL,
            name         VARCHAR (191) NOT NULL,
            description  TEXT,
            created_at   DATETIME      DEFAULT (datetime()) NOT NULL,
            updated_at   DATETIME      DEFAULT (datetime()) NOT NULL
        );
        """
        self.executeCommand(vCon, sqlDDL)

        # WA_GROUPS
        sqlDDL = """
        CREATE TABLE IF NOT EXISTS wa_groups (
            id               INTEGER       PRIMARY KEY,
            segmentations_id INTEGER       REFERENCES segmentations (id) NOT NULL,
            name             VARCHAR (191) NOT NULL,
            image_url        VARCHAR (255),
            description      TEXT,
            edit_data        VARCHAR (20),
            send_message     VARCHAR (20),
            seats            INTEGER       NOT NULL,
            occuped_seats    INTEGER,
            url              VARCHAR (255),
            created_at       DATETIME      DEFAULT (datetime()) NOT NULL,
            updated_at       DATETIME      DEFAULT (datetime()) NOT NULL
        );
        """
        self.executeCommand(vCon, sqlDDL)

        # WA_GROUP_INITIAL_MEMBERS
        sqlDDL = """
        CREATE TABLE IF NOT EXISTS wa_group_initial_members (
            id            INTEGER       PRIMARY KEY,
            wa_groups_id  INTEGER       REFERENCES wa_groups (id) NOT NULL,
            contact_name  VARCHAR (100) NOT NULL,
            administrator BOOLEAN       NOT NULL,
            created_at    DATETIME      DEFAULT (datetime()) NOT NULL,
            updated_at    DATETIME      DEFAULT (datetime()) NOT NULL
        );
        """
        self.executeCommand(vCon, sqlDDL)

        # WA_GROUP_LEADS
        sqlDDL = """
        CREATE TABLE IF NOT EXISTS wa_group_leads (
            id            INTEGER       PRIMARY KEY,
            wa_groups_id  INTEGER       REFERENCES wa_groups (id) NOT NULL,
            number        VARCHAR (25)  NOT NULL,
            sent_welcome  DATETIME,
            out           BOOLEAN       DEFAULT (false) NOT NULL,
            created_at    DATETIME      DEFAULT (datetime()) NOT NULL,
            updated_at    DATETIME      DEFAULT (datetime()) NOT NULL
        );
        """
        self.executeCommand(vCon, sqlDDL)

        # TRIGGER CAMPAIGNS_UPDATED_AT
        sqlDDL = """
        CREATE TRIGGER IF NOT EXISTS campaigns_updated_at
                AFTER UPDATE
                    ON campaigns
            FOR EACH ROW
        BEGIN
            UPDATE campaigns SET updated_at = datetime() WHERE id = OLD.id;
        END;
        """
        self.executeCommand(vCon, sqlDDL)

        # TRIGGER SEGMENTATIONS_UPDATED_AT
        sqlDDL = """
        CREATE TRIGGER IF NOT EXISTS segmentations_updated_at
                AFTER UPDATE
                    ON segmentations
            FOR EACH ROW
        BEGIN
            UPDATE segmentations SET updated_at = datetime() WHERE id = OLD.id;
        END;
        """
        self.executeCommand(vCon, sqlDDL)

        # TRIGGER WA_GROUPS_UPDATED_AT
        sqlDDL = """
        CREATE TRIGGER IF NOT EXISTS wa_groups_updated_at
                AFTER UPDATE
                    ON wa_groups
            FOR EACH ROW
        BEGIN
            UPDATE wa_groups SET updated_at = datetime() WHERE id = OLD.id;
        END;
        """
        self.executeCommand(vCon, sqlDDL)

        # TRIGGER WA_GROUP_INITIAL_MEMBERS_UPDATED_AT
        sqlDDL = """
        CREATE TRIGGER IF NOT EXISTS wa_group_initial_members_updated_at
                AFTER UPDATE
                    ON wa_group_initial_members
            FOR EACH ROW
        BEGIN
            UPDATE wa_group_initial_members SET updated_at = datetime() WHERE id = OLD.id;
        END;
        """
        self.executeCommand(vCon, sqlDDL)

        # TRIGGER WA_GROUP_LEADS_UPDATED_AT
        sqlDDL = """
        CREATE TRIGGER IF NOT EXISTS wa_group_leads_updated_at
                AFTER UPDATE
                    ON WA_GROUP_LEADS
            FOR EACH ROW
        BEGIN
            UPDATE WA_GROUP_LEADS SET updated_at = datetime() WHERE id = OLD.id;
        END;
        """
        self.executeCommand(vCon, sqlDDL)

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
                   edit_data, send_message, seats, occuped_seats, url):
        sql = """INSERT INTO wa_groups (
            id,
            segmentations_id,
            name,
            image_url,
            description,
            edit_data,
            send_message,
            seats,
            occuped_seats,
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
            """ + str(occuped_seats) + """,
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


if __name__ == "__main__":
    DataBase().createDatabase()
