pragma solidity >=0.4.0 <0.6.0;

contract SimpleStorage {
    uint storedData = 2;
    enum FreshJuiceSize{ SMALL, MEDIUM, LARGE }
    mapping (int => string) myMap;
    function set(uint x) public {
        storedData = 1;
    }

}