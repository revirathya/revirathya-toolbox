from pydantic import BaseModel, ConfigDict, SecretStr, computed_field


class MongoAuth(BaseModel):
    model_config = ConfigDict(extra="ignore")

    username: str
    password: SecretStr
    hostname: str
    port: int

    @computed_field
    @property
    def uri(self) -> SecretStr:
        return SecretStr(
            "mongodb://{username}:{password}@{hostname}:{port}".format(
                username = self.username,
                password = self.password.get_secret_value(),
                hostname = self.hostname,
                port = str(self.port),
            )
        )