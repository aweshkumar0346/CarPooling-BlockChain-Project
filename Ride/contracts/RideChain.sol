// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RideChain {
    struct Ride {
        uint id;
        address payable driver;
        string origin;
        string destination;
        uint fare;
        bool isBooked;
        address passenger;
    }

    uint public rideCount = 0;
    mapping(uint => Ride) public rides;

    event RideOffered(uint id, address driver, string origin, string destination, uint fare);
    event RideBooked(uint id, address passenger);

    // Offer a new ride to the platform
    function offerRide(string memory _origin, string memory _destination, uint _fare) public {
        rideCount++;
        rides[rideCount] = Ride(rideCount, payable(msg.sender), _origin, _destination, _fare, false, address(0));
        emit RideOffered(rideCount, msg.sender, _origin, _destination, _fare);
    }

    // Book an offered ride
    function bookRide(uint _id) public payable {
        Ride storage ride = rides[_id];
        require(!ride.isBooked, "Already booked");
        require(msg.value == ride.fare, "Incorrect fare amount");

        ride.driver.transfer(msg.value);
        ride.isBooked = true;
        ride.passenger = msg.sender;

        emit RideBooked(_id, msg.sender);
    }

    // Retrieve information of a specific ride
    function getRide(uint _id) public view returns (Ride memory) {
        return rides[_id];
    }

    // Get rides for a specific user (driver or passenger)
    function getUserRides(address user) public view returns (Ride[] memory) {
        uint count = 0;
        for (uint i = 1; i <= rideCount; i++) {
            if (rides[i].driver == user || rides[i].passenger == user) {
                count++;
            }
        }

        Ride[] memory result = new Ride[](count);
        uint index = 0;
        for (uint i = 1; i <= rideCount; i++) {
            if (rides[i].driver == user || rides[i].passenger == user) {
                result[index] = rides[i];
                index++;
            }
        }
        return result;
    }
}
