pragma solidity ^0.5.0;

contract Inbox{
    string public message;

    constructor() public {
        message = "Hi there";
    }
    
    function setMessage(string memory newMessgae) public {
        message = newMessgae;
    }
    
    function getMessage() public view returns (string memory) {
        return message;
    }
}