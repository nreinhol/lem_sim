pragma solidity ^0.4.25;

contract Dealer{
    mapping (address => int32[]) orders;

    constructor() public {}

    function addOrder(int32[] newOrder) public {
        orders[msg.sender] = newOrder;
    }

    function getOrders(address agent) public view returns (int32[]) {
        return orders[agent];
    }
    
}