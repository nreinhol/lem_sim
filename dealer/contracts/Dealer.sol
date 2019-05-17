pragma solidity ^0.4.25;

/*
1 wei = 1.000.000.000.000.000.000 ether (10^18)
*/

contract Dealer{ 
    address private _owner;
    int256[] public resource_inventory;
    int256[] public mkt_prices;

    // attributes for order handling
    uint32 public order_count;
    uint32[] public order_indices;
    mapping(uint32 => Order) public orders;

    // attributes for the mmp
    int256[] public mmp_duals;
    int256[] public mmp_values;
    int256[] public mmp_target_coefs;
    int256[] public mmp_bounds;

    // attributes for trade handling
    mapping(address => int256[]) private trades;
    mapping(address => uint256) public bills;

    // events
    event ReceivedOrder(address from, int256[] bundle, int256 bid, uint32 index);
    event DeletedOrder(uint32 index);
    event StoredTrade(address receiver, int256[] trade, uint256 payment);

    constructor() public {
        _owner = msg.sender;
        order_count = 1;
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

    function setMMPAttributes(int256[] _mmp_values, int256[] _mmp_duals, int256[] _mmp_target_coefs, int256[] _mmp_bounds) public onlyByOwner() {
        mmp_values = _mmp_values;
        mmp_target_coefs = _mmp_target_coefs;
        mmp_bounds = _mmp_bounds;
        mmp_duals = _mmp_duals;
    }

    function getMMPAttributes() public view returns (int256[], int256[], int256[], int256[]) {
        return (mmp_values, mmp_duals, mmp_target_coefs, mmp_bounds);
    }

    function setTrade(address _account, int256[] _trade, uint256 _payment) public onlyByOwner() {
        trades[_account] = _trade;
        bills[_account] = _payment;

        emit StoredTrade(_account, _trade, _payment);
    }

    function getTrade() public payable checkPayment() returns (int256[]) {
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

        emit ReceivedOrder(new_order.account, new_order.bundle, new_order.bid, order_count);

        // increment order count
        order_count ++;
    }

    function getOrder(uint32 order_id) public view returns (address, int256[], int256) {
        return (orders[order_id].account, orders[order_id].bundle, orders[order_id].bid);
    }

    function deleteOrder(uint32 index) public onlyByOwner() {
        delete orders[index];
        delete order_indices[index - 1];

        emit DeletedOrder(index);
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