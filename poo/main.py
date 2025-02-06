#!/bin/python3



class NetworkPentestFramework:
    def __init__(self, targetip="0.0.0.0", targetport="80"):
        self.targetip = targetip
        self.targetport = targetport

    @staticmethod
    def get_definition():
        """ Give the manual of the framework """
        return (
            """
            This is a Framework for pentest network interface.

            """
        )



if __name__ == "__main__":
    print(NetworkPentestFramework.get_definition())