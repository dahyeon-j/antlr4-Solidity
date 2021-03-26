pragma solidity >=0.4.0 <0.6.0;

contract SimpleStorage {
    uint storedData = 2;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }
}