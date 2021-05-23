import sys


class DatabaseController:

    def __init__(self, file: str):
        self.database = file
        self.isTransaction = False
        self.transactions = []

        self.SIMPLE_COMMANDS = (
            '?', 'read', 'transaction', 'rollback', 'commit')

        self.commandswitch = {
            '?': self.__showHelp,
            'read': self.__readDatabase,
            'input': self.__writeLine,
            'remove': self.__removeLine,
            'transaction': self.__startTransaction,
            'rollback': self.__rollbackTransaction,
            'commit': self.__commitTransaction,
            'list': self.__transactionsList,
            'exit': self.__exit
        }

    def handleInput(self, command: str):
        if self.isTransaction:
            self.__addTransaction(command)
        else:
            try:
                self.__isValidCommand(command)
                split_command = command.split(":")
                if len(split_command) == 1:
                    self.commandswitch[split_command[0]]()
                else:
                    self.commandswitch[split_command[0]](split_command[1])
            except ValueError:
                print("Invalid command")

    def __showHelp(self):
        print(
            'read          -> returns all database lines in format [id]: [value]')
        print('input:[value] -> writes value as a new line into database')
        print(
            'remove:[id]   -> removes line from database that corresponds with writen id')
        print('transaction   -> starts transaction (batch of commands)')
        print('rollback      -> finishes transaction without executing commands')
        print('commit        -> finishes transaction and execute commands')
        print('list          -> shows list of commands in transaction')
        print('exit          -> ends programme')

    def __readDatabase(self):
        with open(self.database, "r") as db:
            for id, value in enumerate(db.readlines()):
                print(f"{id}: {value.strip()}")

    def __writeLine(self, line: str):
        with open(self.database, "a") as db:
            db.write(line + "\n")

    def __removeLine(self, lineNumberString: str):
        try:
            lineNumber = int(lineNumberString)
            if lineNumber+1 > self.__getDatabaseLength():
                raise ValueError
            with open(self.database, "r") as db:
                dbList = db.readlines()
                dbList.pop(lineNumber)
            with open(self.database, "w") as db:
                db.writelines(dbList)

        except ValueError:
            print("Invalid id")

    def __startTransaction(self):
        print("Transaction started")
        self.isTransaction = True

    def __rollbackTransaction(self):
        if self.isTransaction:
            self.isTransaction = False
            self.transactions = []
            print("Transaction rolledback")
        else:
            print('Transaction did not started')

    def __commitTransaction(self):
        if self.isTransaction:
            self.isTransaction = False
            for command in self.transactions:
                self.handleInput(command)
            self.transactions = []
            print('Transaction finnished')
        else:
            print('Transaction did not started')

    def __addTransaction(self, command: str):
        if command == "commit":
            self.__commitTransaction()
        elif command == "rollback":
            self.__rollbackTransaction()
        elif command == "list":
            self.__transactionsList()
        else:
            try:
                self.__isValidCommand(command)
                self.transactions.append(command)
            except ValueError:
                print("Invalid command")

    def __transactionsList(self):
        print("\n")
        print("TRANSACTIONS LIST")
        for command in self.transactions:
            print(command)
        print("\n")

    def __isValidCommand(self, command: str):
        split_command = command.split(":")
        if split_command[0] in self.commandswitch:
            if split_command[0] in self.SIMPLE_COMMANDS:
                if len(split_command) == 1:
                    if split_command[0] == "transaction" and self.isTransaction:
                        raise ValueError
                    return
                else:
                    raise ValueError
            return
        raise ValueError

    def __getDatabaseLength(self):
        with open(self.database, "r") as db:
            return len(db.readlines())

    def __exit(self):
        print("Goodbye")
        sys.exit()


def main():
    controller = DatabaseController("db.txt")
    print("Welcome to db programme!")
    print("Type '?' to show commands.\n")
    while True:
        controller.handleInput(input())


if __name__ == "__main__":
    main()
