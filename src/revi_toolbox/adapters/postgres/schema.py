from pydantic import BaseModel, ConfigDict, SecretStr, computed_field

class PostgreAuth(BaseModel):
    model_config = ConfigDict(extra="ignore")

    username: str
    password: SecretStr
    hostname: str
    port: int
    db_name: str

    @computed_field
    @property
    def uri(self) -> SecretStr:
        return SecretStr(
            "postgresql://{username}:{password}@{hostname}:{port}/{db_name}".format(
                username = self.username,
                password = self.password.get_secret_value(),
                hostname = self.hostname,
                port = str(self.port),
                db_name = self.db_name
            )
        )
