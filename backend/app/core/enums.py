from enum import Enum


class CalendarType(str, Enum):
    SOLAR = 'SOLAR'
    LUNAR = 'LUNAR'


class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class ReminderChannel(str, Enum):
    IN_APP = 'IN_APP'


class ChatRole(str, Enum):
    USER = 'user'
    ASSISTANT = 'assistant'
