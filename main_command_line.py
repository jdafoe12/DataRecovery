
import read_journal
import recovery_journaled
import disks

def main():
    fileRecovery = recovery_journaled.FileRecoveryJournaled()

    print("select from availible disk file paths: ", end="")

    diskList = disks.getDisks()

    for disk in diskList:
        print(disk.diskPath, end=" ")
    print("\n")

    diskName = input("File path of disk: ")

    for disk in diskList:
        if disk.diskPath == diskName:
            currentDisk = disk

    readJournal = read_journal.ReadJournal(currentDisk)


    transactions = readJournal.readFileSystemJournal()
    transactions.sort(key=lambda transaction: -transaction.transactionNum)
    deletedInodes = fileRecovery.getDeletedInodes(currentDisk, transactions)

    numDeleted = len(deletedInodes)


    userChoice = input("%d deleted files found. Enter Y to recover all, and an integer N (1 to %d) to recover the N most recently deleted files: " % (numDeleted, numDeleted))

    numToRecover = 0
    if userChoice.upper() == "Y":
        numToRecover = numDeleted

    elif int(userChoice) <= numDeleted and int(userChoice) > 0:
        numToRecover = int(userChoice)

    filePath = input("please provide a file path for recovered files: ")

    numRecovered = fileRecovery.recoverFiles(currentDisk, transactions, deletedInodes, numToRecover, filePath)

    print("%d files were successfully recovered" % numRecovered)

if __name__ == "__main__":
    main()