class DB_Config:
    def __init__(self) -> None:
        self.__sqlalchemy_database_uri = self.set_SQLALCHEMY_DATABASE_URI()
        self.__sqlalchemy_track_modifications = False

    @property
    def SQLALCHEMY_TRACK_MODIFICATIONS(self) -> bool:
        return self.__sqlalchemy_track_modifications

    @SQLALCHEMY_TRACK_MODIFICATIONS.setter
    def set_SQLALCHEMY_TRACK_MODIFICATIONS(self, boolean=False):
        self.__sqlalchemy_track_modifications = boolean

    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.__sqlalchemy_database_uri

    def set_SQLALCHEMY_DATABASE_URI(self, USERNAME=None, PASSWORD=None, HOSTNAME=None, DATABASE=None) -> str:
        if None in [USERNAME,PASSWORD,HOSTNAME,DATABASE]:
            self.__sqlalchemy_database_uri = "mysql+mysqlconnector://braian:Santi15Beni19!@localhost/GESVEN"
        else:
            self.__sqlalchemy_database_uri = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}"
        return self.SQLALCHEMY_DATABASE_URI()


SQLALCHEMY_DATABASE_URI = DB_Config().SQLALCHEMY_DATABASE_URI()
SQLALCHEMY_TRACK_MODIFICATIONS = DB_Config().SQLALCHEMY_TRACK_MODIFICATIONS
