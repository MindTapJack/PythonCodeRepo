import time, random
from threading import Thread, current_thread, Condition

class SharedCell(object):
    """Shared data for the producer/consumer problem."""

    # Includes a wait list of consumers who have thus far read data,
    # a second condition on which these consumers must wait, and
    # the maximum number of consumers who will read each datum.

    # The condition for synchonizing the producer with the consumers
    # does not change.

    # getData looks for the current thread in the wait list of
    # consumers.  If it's there, that consumer has already read the
    # current datum and must wait on the new condition.  Otherwise,
    # the consumer reads the datum and is placed on the wait list.
    # If the list becomes full, all of the consumers are finished with
    # the current datum, so they can all be notofied and the writer can
    # be released.
    
    def __init__(self):
        self.data = -1
        self.writeable = True
        self.condition = Condition()
        
    def setData(self, data):
        """Producer's method to write to shared data."""
        self.condition.acquire()
        while not self.writeable:
            self.condition.wait()
            
        print("%s setting data to %d" % (current_thread().name, data))
        self.data = data
        self.writeable = False
        self.condition.notify()
        self.condition.release()
        # Reset the wait list, release the writer, and
        # release all readers
        
        
    def getData(self):
        """Consumer's method to read from shared data."""
        # Wait on consumer condition if you have
        # already consumed this datum
        
        self.condition.acquire()
        # Wait for writer to finish if datum has not been produced
        
        while self.writeable:
            self.condition.wait()
        print("%s accessing data %d " % (current_thread().name, self.data ))
        self.writeable = True
        self.condition.notify()
        self.condition.release()
        return self.data
        
class Producer(Thread):
    """Represents a producer."""
    
    """
    Create a producer with the given shared cell,
    number of accesses, and maximum sleep interval.
    """
    def __init__(self, cell, accessCount, sleepMax):
        
        Thread.__init__(self, name = "Producer")
        self.accessCount = accessCount
        self.cell = cell
        self.sleepMax = sleepMax
        
    def run(self):
         """
        Announce startup, sleep and write to shared cell
        the given number of times, and announce completion.
        """
        print("%s starting up: " % self.name )
        for count in range(self.accessCount):
            time.sleep(random.randint(1, self.sleepMax))
            self.cell.setData(count + 1)
            
        print("%s is done producing\n " % self.name)
                       
        
class Consumer(Thread):
    """Represents a consumer."""
    
    """
    Create a consumer with the given shared cell,
    number of accesses, and maximum sleep interval.
    """
    def __init__(self, name, cell, accessCount, sleepMax):
        Thread.__init__(self, name = "Consumer" + name)
        self.accessCount = accessCount
        self.sleepMax = sleepMax
        self.cell = cell
        
    def run(self):
        """
        Announce startup, sleep and read from shared cell
        the given number of times, and announce completion.
        """
        print("%s is starting up " % self.name)
        for count in range(self.accessCount):
            time.sleep(random.randint(1, self.sleepMax))
            value = self.cell.getData()
        print("%s is done consuming\n" % self.name)


def main():
    """
    Get numberof accesses from the user,
    get the number of Consumers from the user,
    create a shared cell with the number of Consumers,
    and create start up for a producer,
    create the start up for each of the consumers.
    """
    
    accessCount = int(input("Enter the number of accesses: "))
    sleepMax = 5
    cell = SharedCell()
    
    numConsumer = int(input("Enter the number of consumers: "))
    producer = Producer(cell, accessCount, sleepMax)
    
    consumers = []
    
    for count in range(numConsumer):
        consumers.append(Consumer(str(count),cell, accessCount, sleepMax))
    
    print("Starting a producer thread.")
    producer.start()         
                     
    for c in consumers:
        c.start()
        #print(c)
    
    
if __name__ == "__main__":
    main()
