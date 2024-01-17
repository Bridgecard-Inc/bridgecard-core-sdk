from dataclasses import dataclass

@dataclass
class CoreWebhookDataContext:
    
    def __getatrr__(self, key):

        super().__getattribute__(key)

    def __setatrr__(self, key, value):

        self.__dict__[key] = value

    def __delatrr__(self, key):

        super().__delatrr__(key)

    def __contains__(self, key):

        return key in self.__dict__

    

core_webhook_data_context = CoreWebhookDataContext()
