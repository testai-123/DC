// CLIENT CODE 

import java.rmi.Naming;
import java.util.Scanner;

// Client class for the hotel booking application
public class HotelClient {
    public static void main(String[] args) {
        try {
            HotelServerInterface hotelServer = (HotelServerInterface) Naming.lookup("rmi://localhost/HotelServer");
            Scanner scanner = new Scanner(System.in);

            int choice;
            do {
                System.out.println("Hotel Booking System");
                System.out.println("1. Book Room");
                System.out.println("2. Cancel Booking");
                System.out.println("3. Exit");
                System.out.print("Enter your choice: ");
                choice = scanner.nextInt();

                switch (choice) {
                    case 1:
                        System.out.print("Enter guest name: ");
                        String guestName = scanner.next();
                        System.out.println("Available rooms: 1 to 10");
                        System.out.print("Enter room number: ");
                        int roomNumber = scanner.nextInt();

                        boolean booked = hotelServer.bookRoom(guestName, roomNumber);
                        if (booked) {
                            System.out.println("Room booked successfully.");
                            System.out.println("Hotel: Ocean Paradise");
                        } else {
                            System.out.println("Failed to book the room. Room may be already booked or invalid room number.");
                        }
                        break;

                    case 2:
                        System.out.print("Enter guest name: ");
                        guestName = scanner.next();

                        String cancellationMessage = hotelServer.cancelBooking(guestName);
                        System.out.println(cancellationMessage);

                        if (cancellationMessage.contains("room number")) {
                            System.out.print("Enter 'yes' to confirm cancellation, 'no' to keep the booking: ");
                            String confirmation = scanner.next().toLowerCase();

                            if (confirmation.equals("yes")) {
                                System.out.print("Enter room number to cancel booking: ");
                                int roomNumToCancel = scanner.nextInt();

                                boolean canceled = hotelServer.cancelBooking(guestName, roomNumToCancel);
                                if (canceled) {
                                    System.out.println("Booking canceled successfully.");
                                } else {
                                    System.out.println("Failed to cancel booking. Room may not be booked by the specified guest or invalid room number.");
                                }
                            } else {
                                System.out.println("Booking kept as per user choice.");
                            }
                        }
                        break;

                    case 3:
                        System.out.println("Exiting the Hotel Booking System.");
                        break;

                    default:
                        System.out.println("Invalid choice. Please enter a valid option.");
                }
            } while (choice != 3);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}



// SERVER CODE 

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.Map;

// Define the remote interface for the hotel server
interface HotelServerInterface extends Remote {
    boolean bookRoom(String guestName, int roomNumber) throws RemoteException;
    String cancelBooking(String guestName) throws RemoteException;
    boolean cancelBooking(String guestName, int roomNumber) throws RemoteException;
}

// Implement the remote interface
public class HotelServer extends UnicastRemoteObject implements HotelServerInterface {
    private static final int TOTAL_ROOMS = 10;
    private Map<Integer, String> roomBookingMap;

    public HotelServer() throws RemoteException {
        super();
        roomBookingMap = new HashMap<>();
    }

    @Override
    public synchronized boolean bookRoom(String guestName, int roomNumber) throws RemoteException {
        if (roomNumber < 1 || roomNumber > TOTAL_ROOMS) {
            return false; // Invalid room number
        }

        if (roomBookingMap.containsKey(roomNumber)) {
            return false; // Room is already booked
        }

        roomBookingMap.put(roomNumber, guestName);
        return true;
    }

    @Override
    public synchronized String cancelBooking(String guestName) throws RemoteException {
        for (Map.Entry<Integer, String> entry : roomBookingMap.entrySet()) {
            if (entry.getValue().equals(guestName)) {
                return "You had booked room number " + entry.getKey() + ". Would you like to cancel? (yes/no)";
            }
        }
        return "No booking found for the guest: " + guestName;
    }

    @Override
    public synchronized boolean cancelBooking(String guestName, int roomNumber) throws RemoteException {
        if (roomNumber < 1 || roomNumber > TOTAL_ROOMS) {
            return false; // Invalid room number
        }

        if (!roomBookingMap.containsKey(roomNumber)) {
            return false; // Room is not booked
        }

        String bookedGuest = roomBookingMap.get(roomNumber);
        if (bookedGuest.equals(guestName)) {
            roomBookingMap.remove(roomNumber);
            return true;
        } else {
            return false; // The room is not booked by the specified guest
        }
    }

    public static void main(String[] args) {
        try {
            HotelServer server = new HotelServer();
            java.rmi.registry.LocateRegistry.createRegistry(1099);
            java.rmi.Naming.rebind("rmi://localhost/HotelServer", server);
            System.out.println("HotelServer is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
