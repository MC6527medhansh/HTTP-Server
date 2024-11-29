classDiagram
    InventoryManagementSystem --> Inventory : "1..1"
    InventoryManagementSystem --> JsonWriter : "1..1"
    InventoryManagementSystem --> JsonReader : "1..1"
    InventoryManagementSystemGUI --> Inventory : "1..1"
    InventoryManagementSystemGUI --> JsonWriter : "1..1"
    InventoryManagementSystemGUI --> JsonReader : "1..1"
    InventoryManagementSystemGUI --> WindowListenerClass : "1..1"
    Inventory --> Item : "1..*"
    EventLog --> Event : "1..*"

    class Writable {
        <<interface>>
    }

    class InventoryManagementSystem
    class Main
    class InventoryManagementSystemGUI {
        implements ActionListener
    }
    class WindowListenerClass {
        extends WindowAdapter
    }
    class Item {
        implements Writable
    }
    class Inventory {
        implements Writable
    }
    class JsonReader
    class JsonWriter
    class Event
    class EventLog {
        implements Iterable
    }

