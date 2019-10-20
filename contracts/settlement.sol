pragma solidity >=0.4.22 <0.6.0;
contract Settlement {

    address issuer;
    uint public totalDeposite;
    uint public currentTimeStamp;
    uint public rentalTimeStart;
    uint public depositeAmount;
    uint public pricePerMin;
    uint public latestTimeToLeave;
    address payable provider;
    bool public approvedByProvider = false;
    
    
    event ParkingSettlement(
        address Provider,
        address Issuer,
        uint amountPaid,
        uint minutesUsed
    );
    
    
    /// Create a new ballot with $(_numProposals) different proposals.
    constructor(uint _pricePerMin, uint _rentalTimeStart, address payable _provider) public payable {
        require(msg.value > 0);
        // require(_depositeAmount > 0 && _depositeAmount < msg.value);
        
        provider = _provider;
        issuer = msg.sender;
        totalDeposite = msg.value;
        
        currentTimeStamp = block.timestamp;
        rentalTimeStart = _rentalTimeStart;
        pricePerMin = _pricePerMin;
        
        uint minutesAvailable = totalDeposite / pricePerMin;
        latestTimeToLeave = rentalTimeStart + minutesAvailable * 60;
    }

    function providerApproval() public{
        require(msg.sender == provider);
        
        approvedByProvider = true;
    }
    
    function payToProvider() public {
        require(msg.sender == issuer);
        require(approvedByProvider==true);
        
        uint totalMinutesUsed = (block.timestamp - rentalTimeStart) / 60;
        uint paymentPerTotalMinutes = totalMinutesUsed * pricePerMin;
        
        provider.transfer(paymentPerTotalMinutes);
        
        emit ParkingSettlement(provider, issuer, paymentPerTotalMinutes, totalMinutesUsed);
    }
}
