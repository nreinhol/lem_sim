pragma solidity ^0.4.25;

/*
1 wei = 1.000.000.000.000.000.000 ether (10^18)
*/

contract Dealer{ 
    address private _owner;
    uint32 public order_count;
    uint32[] public order_indices;
    int256[] public mkt_prices;
    int256[] public resource_inventory;
    mapping(uint32 => Order) public orders;
    mapping(address => int256[]) private trades;
    mapping(address => uint256) public bills;

    constructor() public {
        _owner = msg.sender;
        order_count = 0;
    }

    modifier checkPayment() {
        require(
            bills[msg.sender] == msg.value,
            "Not enough wei"
            );
        _;
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
        int256[] bundle;
        int256 bid;
    }

    function setTrade(address _account, int256[] _trade, uint256 _payment) public onlyByOwner() {
        trades[_account] = _trade;
        bills[_account] = _payment;
    }

    function getTrade() checkPayment() payable public returns (int256[]) {
        return trades[msg.sender];
    }

    function setOrder(int256[] _bundle, int256 _bid) public {
        
        Order memory new_order = Order(
            msg.sender,
            _bundle,
            _bid
        );

        orders[order_count] = new_order;
        order_indices.push(order_count);
        // increment order count
        order_count ++;        
    }

    function getOrder(uint32 order_id) public view returns (address, int256[], int256) {
        return (orders[order_id].account, orders[order_id].bundle, orders[order_id].bid);
    }

    function setMktPrices(int256[] _mkt_prices) public onlyByOwner() {
        mkt_prices = _mkt_prices;
    }

    function getMktPrices() public view returns (int256[]) {
        return mkt_prices;
    }

    function getOrderIndices() public view returns (uint32[]) {
        return order_indices;
    }

    function deleteOrder(uint32 index) public onlyByOwner() {
        delete orders[index];
        if (index >= order_indices.length) {
            delete order_indices;
        }
        else {
            delete order_indices[index];
        
            for (uint i = index; i<order_indices.length-1; i++){
                order_indices[i] = order_indices[i+1];
            }
            order_indices.length--;        
        }
    }

    function setResourceInventory (int256[] _resource_inventory) public onlyByOwner() {
        resource_inventory = _resource_inventory;
    }

    function getResourceInventory() public view returns (int256[]) {
        return resource_inventory;
    }

    function getOwner() public view returns (address) {
        return _owner;
    }

    function getBill() public view returns (uint256) {
        return bills[msg.sender];
    }

}