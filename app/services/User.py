import uuid
import bcrypt
from app.interfaces.User import Login_PM, SignUp_PM, UserModelTH
from app.ioc.ioc import SingletonMeta
from app.repositories.User import UserRepository


class UserService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.user_repo = UserRepository()

    def user_signup(self, payload: SignUp_PM):
        user = self.user_repo.get_user_by_email(payload.email)
        if user:
            raise Exception("User Already  Exist.")
        hashed_password = bcrypt.hashpw(
            payload.password.encode("utf-8"), bcrypt.gensalt()
        )

        user_data = UserModelTH(
            name=payload.name,
            userId=str(uuid.uuid4()),
            email=payload.email,
            password=hashed_password.decode(
                "utf-8"
            ),  # Store as string if DB expects string
        )
        self.user_repo.add_user(user_data)

    def login_user(self, payload: Login_PM) -> UserModelTH:
        user = self.user_repo.get_user_by_email(payload.email)
        if not user:
            raise Exception("User Does Not Exist.")
        bcrypt.checkpw(
            payload.password.encode("utf-8"), user["password"].encode("utf-8")
        )
        return user
