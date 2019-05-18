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

    // attributes for trade handling
    mapping(address => int256[]) private trades;
    mapping(address => uint256) public bills;
    mapping(address => uint256) public prepayments;
    mapping(address => uint256) public refunds;

    // attributes for the mmp
    int256[] public mmp_duals;
    int256[] public mmp_values;
    int256[] public mmp_target_coefs;
    int256[] public mmp_bounds;


    // events
    event ReceivedOrder(address from, int256[] bundle, uint256 bid, uint256 prepayment, uint32 index);
    event DeletedOrder(uint32 index);
    event StoredTrade(address receiver, int256[] trade, uint256 prepayment, uint256 bill, uint256 refund);
    event FetchedTrade(address receiver, int256[] trade, uint256 refund);
    event RejectedTrade(address receiver, int256[] trade, uint256 refund);

    constructor() public {
        _owner = msg.sender;
        order_count = 1;
    }

    modifier checkPrepayment(uint256 _prepayment) {
        require(
            _prepayment == msg.value,
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
        uint256 bid;
    }

    function setTrade(address _account, int256[] _trade, uint256 _prepayment, uint256 _bill, uint256 _refund) public onlyByOwner() {
        trades[_account] = _trade;
        bills[_account] = _bill;
        prepayments[_account] = _prepayment;
        refunds[_account] = _refund;

        emit StoredTrade(_account, _trade, _prepayment, _bill, _refund);
    }

    function getTrade(bool accept_trade) public returns (int256[]) {
        if(accept_trade) {
            msg.sender.transfer(refunds[msg.sender]);
            emit FetchedTrade(msg.sender, trades[msg.sender], refunds[msg.sender]);
            return trades[msg.sender];
        } else {
            msg.sender.transfer(prepayments[msg.sender]);
            emit RejectedTrade(msg.sender, trades[msg.sender], prepayments[msg.sender]);
        }

        
    }

    function setOrder(int256[] _bundle, uint256 _bid, uint256 _prepayment) public payable checkPrepayment(_prepayment) {

        Order memory new_order = Order(
            msg.sender,
            _bundle,
            _bid
        );

        orders[order_count] = new_order;
        order_indices.push(order_count);

        emit ReceivedOrder(new_order.account, new_order.bundle, new_order.bid, _prepayment, order_count);

        // increment order count
        order_count ++;
    }

    function getOrder(uint32 order_id) public view returns (address, int256[], uint256) {
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

    function setMMPAttributes(int256[] _mmp_values, int256[] _mmp_duals, int256[] _mmp_target_coefs, int256[] _mmp_bounds) public onlyByOwner() {
        mmp_values = _mmp_values;
        mmp_target_coefs = _mmp_target_coefs;
        mmp_bounds = _mmp_bounds;
        mmp_duals = _mmp_duals;
    }

    function getMMPAttributes() public view returns (int256[], int256[], int256[], int256[]) {
        return (mmp_values, mmp_duals, mmp_target_coefs, mmp_bounds);
    }

}