pragma solidity ^0.4.25;

contract Dealer{
    address private _owner;
    mapping (address => mapping(string => int32[])) orders;
    mapping (address => mapping(string => int32[])) trades;
    uint32[] public mkt_prices;

    constructor() public {
        _owner = msg.sender;
    }

    modifier onlyByOwner() {
        require(
            msg.sender == _owner,
            "Sender not authorized"
            );
        _;
    }
    
    function getOwner() public view returns (address) {
        return _owner;
    }

    function setMktPrices(uint32[] new_mkt_prices) public onlyByOwner() {
        mkt_prices = new_mkt_prices;
    }

    function getMktPrices() public view returns (uint32[]) {
        return mkt_prices;
    }

}