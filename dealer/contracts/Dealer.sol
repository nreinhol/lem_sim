pragma solidity ^0.4.25;

contract Dealer{ 
    address private _owner;
    uint32 public order_count;
    uint32[] public mkt_prices;
    mapping(uint32 => Order) public orders;
    mapping(address => uint32[]) trades;
    
    constructor() public {
        _owner = msg.sender;
        order_count = 0;
    }

    modifier onlyByOwner() {
        require(
            msg.sender == _owner,
            "Sender not authorized"
            );
        _;
    }

    struct Order {
        address account;
        int32[] bundle;
        int32 bid;
    }

    function setTrade(address account, uint32[] trade) {
        
    }

    function setOrder(int32[] _bundle, int32 _bid) public {
        
        Order memory new_order = Order(
            msg.sender,
            _bundle,
            _bid
        );

        orders[order_count] = new_order;
        
        // increment order count
        order_count ++;        
    }

    function getOrder(uint32 order_id) public view returns (address, int32[], int32) {
        return (orders[order_id].account, orders[order_id].bundle, orders[order_id].bid);
    }

    function setMktPrices(uint32[] new_mkt_prices) public onlyByOwner() {
        mkt_prices = new_mkt_prices;
    }

    function getMktPrices() public view returns (uint32[]) {
        return mkt_prices;
    }

    function getOwner() public view returns (address) {
        return _owner;
    }

}