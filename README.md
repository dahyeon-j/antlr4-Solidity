# antlr4-Solidity
This is Solidity visitor written by Python3

# Ether Units

-   접미사
-   Ether에서 더 작은 범위의 숫자를 표현하기 위해 사용
-   접미사가 없는 Ether은 Wei로 가정

#### Ethereum의 하위 유닛들

| Unit | wei value | wei | ether value |
| --- | --- | --- | --- |
| wei | 1 wei | 1 | 10^-18 ETH |
| kwei | 10^3 wei | 1,000 | 10^-15 ETH |
| mwei | 10^6 wei | 1,000,000 | 10^-12 ETH |
| gwei | 10^9 wei | 1,000,000,000 | 10^-9 ETH |
| microether | 10^12 wei | 1,000,000,000,000 | 10^-6 ETH |
| milliether | 10^15 wei | 1,000,000,000,000,000 | 10^-3 ETH |
| ether | 10^18 wei | 1,000,000,000,000,000,000 | 1 ETH |
| \`\`\` solidity |   |   |   |
| assert(1 wei == 1); |   |   |   |
| assert(1 gwei == 1e9); |   |   |   |
| assert(1 ether == 1e18); |   |   |   |
| \`\`\` |   |   |   |

# Time Units

-   시간 단위 표현에 사용
-   초가 기본 단위
-   리터럴 숫자 + 단위 조합으로 사용
-   변수에 사용이 불가능  
    _윤초(시간 보정을 위해 사용)가 발생할 수 있기 때문에 오라클로 calendar 라이브러리를 업데이트해야 함_

#### 단위

-   seconds
-   minutes
-   hourse
-   days
-   weeks  
    _years는 삭제됨_

```
    // 변수에 사용이 불가능 하기 대문에 1 days를 곱하여 적용
    if (block.timestamp >= start + daysAfter * 1 days) {
      // ...
    }
}
```

```
// 부호의 관계는 아래와 같음
assert(1 seconds == 1);
assert(1 minutes == 60 seconds);
assert(1 hours == 60 minutes);
assert(1 day == 24 hours);
assert(1 week == 7 days);
```

# Special Variables and Functions

-   global namespace에 존재
-   블록체인의 정보 제공
-   일반적으로 사용되는 유틸리티 함수 역할

**괄호 안은 리턴 값**

## Block and Transaction Properties

-   blockhash(uint blockNumber) returns (bytes32): 해당 블록의 hash 값 - 현재 블록을 제외한 가장 최근 256 블록에만 적용
-   block.chainid (int): 현재 체인의 id
-   block.coinbase (address payable): 현재 블록 채굴자의 address
-   block.difficulty (uint): 현재 블록 난이도
-   block.gaslimit (uint): 현재 블록의 gaslimit
-   block.number (uint): 현재 블록의 번호
-   block.timestamp (uint): unix epoch 이후의 현재 블록 타임스탬프
-   gasleft() returns (uint256): 잔여 gas
-   msg.data (bytes calldata): 완전한 calldata
-   msg.sender (address): 현재 호출 메시지 발신자
-   msg.sig (bytes4): calldata의 첫 4바이트(함수 식별자와 같음)
-   msg.value (uint): 메시지와 전송된 wei수
-   tx.gasprice (uint): 트랜잭션의 gas 가격
-   tx.origin (address): 트랜잭션의 발신자

#### Note

-   msg.sender와 msg.value를 포함한 msg의 모든 멤버의 값은 모든 외부 함수(라이브러리 함수도 포함) 호출에 의해 변경 가능
-   무엇을 하는지 모른다면, 랜덤 소스로 block.timestamp나 blockhash에 의존 하지 말 것
-   block hash는 범위 문제로 모든 블록에 적용할 수는 없음
-   block.blockhash가 blockhash로 변경
-   msg.gas가 gasleft로 변경
-   now가 사라짐

## ABI Encoding and Decoding Functions

-   abi.decode(bytes memory encodedData, (...)) returns (...): 데이터를 두번째 argument의 타입으로 ABI-decode
    
    ```
    // abi.decode 예제
    bytes4 sig = abiDecodeSig(_data); //can be replaced by abi.decode(_data, (bytes4));
    // 두번째 argument의 타입 순서대로 데이터가 decode
    (uint a, uint[2] memory b, bytes memory c) = abi.decode(data, (uint, uint[2], bytes))
    ```
    
-   abi.encode(...) returns (bytes memory): argument로 ABI-encode
-   abi.encodePacked(...) returns (bytes memory): packed encoding 수행
-   abi.encodeWithSelector(bytes4 selector, ...) returns (bytes memory): 두번째 argument부터 ABI-encode 수행하고 앞에 argument로 받은 4바이트 크기의 selector을 붙임
-   abi.encodeWithSignature(string memory signature, ...) returns (bytes memory): abi.encodeWithSelector와 같음

## Members of bytes

-   bytes.concat(...) returns (bytes memory) argument를 하나의 바이트 배열로 연결
    
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

contract C {  
  bytes s = "Storage";  
  function f(bytes calldata c, string memory m, bytes16 b) public view {  
    bytes memory a = bytes.concat(s, c, c\[:2\], "Literal", bytes(m), b);  
    // s.length: 문자열 s 길이  
    // c.length: 문자열 c 길이  
    // 2: 문자열 c에서 2 바이트만 슬라이싱  
    // 7: 문자열 "Literal"의 크기  
    // bytes(m).length: bytes(m)의 길이  
    // 16: b는 bytes16 타입  
    assert((s.length + c.length + 2 + 7 + bytes(m).length + 16) == a.length);  
  }  
}

```

## Error Handling
* assert(bool condition): 조건이 충족되지 않으면 에러 발생 - 내부 오류에 사용
* require(bool condition): 조건이 충족되지 않으면 되돌림 - 입력과 외부 구성요소에 사용
* require(bool condition, string memory message): 조건이 충족되지 않으면 되돌림 - 입력과 외부 구성요소에 사용 + 에러 메시지 제공
* revert(): 실행 중지 및 상태 변경 취소
* revert(string memory reason): 설명 문자열과 함께 실행 중지 및 상태 변경 취소

## Mathematical and Cryptographic Functions
* addmod(uint x, uint y, uint k) returns (uint): (x + y) % k 계산. 0.5.0 버전 이후부터 k != 0을 보장
* mulmod(uint x, uint y, uint k) returns (uint): (x * y) % k 계산. 0.5.0 버전 이후부터 k != 0을 보장
* keccak256(bytes memory) returns (bytes32): 입력값의 Keccak-256 해시값 계산.
* sha256(bytes memory) returns (bytes32): 입력값의 SHA-256 해시값 계산.
* ripemd160(bytes memory) returns (bytes20): 입력값의 RIPEMD-160 해시값 계산.
* ecrecover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) returns (address): 공개키와 연관된 주소 복원하거나 0을 리턴

## Members of Address Types
* \<address\>.balance (uint256): wei 주소의 잔고



#### Contract

-   객체 지향 언어의 클래스와 유사

# Creating Contracts

-   contract가 생성되면 생성자(`constructor`키워드와 선언된 함수)가 한 번 실행됨
-   constructor은 선택 사항 -> default constructor
-   constructor은 하나만 가능(오버로드가 지원되지 않음)
-   constructor가 실행된 후, contract의 최종 코드가 블록체인에 저장됨

```
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.9.0;


contract OwnedToken {
    TokenCreator creator;
    address owner;
    bytes32 name;

    // 생성자
    constructor(bytes32 _name) {
        owner = msg.sender;

        creator = TokenCreator(msg.sender);
        name = _name;
    }

    function changeName(bytes32 newName) public {
        if (msg.sender == address(creator))
            name = newName;
    }

    function transfer(address newOwner) public {
        if (msg.sender != owner) return;

        if (creator.isTokenTransferOK(owner, newOwner))
            owner = newOwner;
    }
}

// constructor가 있지 않음
// default constructor
contract TokenCreator {
    function createToken(bytes32 name)
        public
        returns (OwnedToken tokenAddress)
    {새
        return new OwnedToken(name);
    }

    function changeName(OwnedToken tokenAddress, bytes32 name) public {
        tokenAddress.changeName(name);
    }

    function isTokenTransferOK(address currentOwner, address newOwner)
        public
        pure
        returns (bool ok)
    {
        return keccak256(abi.encodePacked(currentOwner, newOwner))[0] == 0x7f;
    }
}
```

# Visibility and Getters

#### Solidity의 함수 호출 종류

-   내부 호출: 실제 EVM 호출을 생성하지 않음
-   외부 호출: 내부 호출을 실행

#### Visibility 종류

|   | Fuction | State Variable | note |
| :-: | :-: | :-: | - |
| external | O | X | `external function`: 다른 contract나 transaction을 통해 호출 가능<br />external function `f`는 `this.f()`를 통해 호출(`f()`는 동작하지 않음|
| public | O | O | `public function`: 내부적으로 호출하거나 메시지를 통해서 호출 가능<br />`public state variable`: 자동적으로 getter 함수가 생성됨 |
| internal | O | O | State Variable의 기본 가시성 수준.<br />현재 contract나 파생된 contract에서 접근 가능. |
| private | O | O | 정의된 contract에서만 가시적. <br />파생 클래스에서는 비가시적. |

#### visibility 지정자 위치

-   상태 변수의 타입 뒤
-   매개변수 리스트와 리턴 매개변수 리스트 사이
    
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;
    
contract C {  
function f(uint a) private pure returns (uint b) { return a + 1; } // 매개변수 리스트와 리턴 매개변수 리스트 사이  
function setData(uint a) internal { data = a; } // 매개변수 리스트와 리턴 매개변수 리스트 사이  
uint public data; // 상태 변수 타입 뒤  
}  
```

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.8.0;

contract C {
    uint private data;

    function f(uint a) private pure returns(uint b) { return a + 1; }
    function setData(uint a) public { data = a; }
    function getData() public view returns(uint) { return data; }
    function compute(uint a, uint b) internal pure returns (uint) { return a + b; }
}

// This will not compile
contract D {
    function readData() public {
        C c = new C();
        uint local = c.f(7); // error: member `f` is not visible -> f는 private
        c.setData(3);
        local = c.getData();
        local = c.compute(3, 5); // error: member `compute` is not visible -> compute는 internal이기 때문에 contract C나 혹은 contract C에서 파생된 contract에서만 접근 가능
    }
}

contract E is C {
    function g() public {
        C c = new C();
        uint val = compute(3, 5); // access to internal member (from derived to parent contract) -> E는 derived contract이기 때문에 접근 가능
    }
}
```

## Getter Functions
- public state variable에 대해 컴파일러가 자동으로 생성하는 함수
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.8.0;

contract C {
    uint public data = 42;
}

contract Caller {
    C c = new C();
    function f() public view returns (uint) {
        return c.data(); // data(): return state variable "data"
    }
}
```
- getter function은 external 수준으로 가시성을 가짐
    - this.data(): 외부 접근
    - data(): 내부 접근
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.0 <0.9.0;

contract C {
    uint public data;
    function x() public returns (uint) {
        data = 3; // internal access
        return this.data(); // external access
    }
}
```
- `public` state variable인 array 타입은 getter function으로 배열의 요소에 접근 가능
    - 전체 array를 리턴할 때 높은 gas 비용을 방지
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.8.0;

contract arrayExample {
    // public state variable
    uint[] public myArray;

    // 컴파일러에 의해 자동으로 생성되는 getter 
    /*
    function myArray(uint i) public view returns (uint) {
        return myArray[i];
    }
    */

    // 전체 array를 리턴하는 function
    function getArray() public view returns (uint[] memory) {
        return myArray;
    }
}
```

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.0 <0.8.0;

contract Complex {
    struct Data {
        uint a;
        bytes3 b;
        mapping (uint => uint) map;
    }
    mapping (uint => mapping(bool => Data[])) public data; // ??
}
```
위의 코드는 아래와 같은 funtion을 생성한다.
``` solidity
function data(uint arg1, bool arg2, uint arg3) public returns (uint a, bytes3 b) {
    a = data[arg1][arg2][arg3].a;
    b = data[arg1][arg2][arg3].b;
}
```

# Function Modifiers
- 함수의 동작을 변경하기 위해 사용
- contract에서 상속 가능
- virtual인 경우에만 derived contract에서 재정의 가능
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >0.7.0 <0.9.0;

contract owned {
    constructor() { owner = payable(msg.sender); }
    address payable owner;

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "Only owner can call this function."
        );
        _;
    }
}

contract destructible is owned {
    // owned에서 onlyOwner modifier  상속받아 destroy에 적용
    // 
    function destroy() public onlyOwner {
        selfdestruct(owner);
    }
}

contract priced {
    // modifier은 arguement를 받을 수 있음
    modifier costs(uint price) {
        if (msg.value >= price) {
            _;
        }
    }
}

contract Register is priced, destructible {
    mapping (address => bool) registeredAddresses;
    uint price;

    constructor(uint initialPrice) { price = initialPrice; }

    // payable 키워드가 없다면 Ether가 보내는 것을 모두 거절
    function register() public payable costs(price) {
        registeredAddresses[msg.sender] = true;
    }

    function changePrice(uint _price) public onlyOwner {
        price = _price;
    }
}

contract Mutex {
    bool locked;
    modifier noReentrancy() {
        require(
            !locked,
            "Reentrant call."
        );
        locked = true;
        _;
        locked = false;
    }

    // 
    function f() public noReentrancy returns (uint) {
        (bool success,) = msg.sender.call("");
        require(success);
        return 7;
    }
}
```
- contract C에 정의된 modifier m에 접근하려면, C.m으로 참조 가능
- 공백으로 구분된 리스트로 여러 개의 modifier을 function에 적용 가능
- 수정한 argument나 함수의 반환 값에 암묵적으로 접근하거나 변경할 수 없음
- modifier나 funtion으로부터 명시적인 반환으로 현재 modifier과 function의 본문만 남음. 반환 변수가 할당되고 `_` 뒤에 제어 흐름이 지속.
- modifier은 함수의 body가 실행되지 않도록 할 수 있으며, 이 경우 function의 body가 없는 것 처럼 반환 값이 기본 값으로 설정됨.

# Constant and Immutable State Variables
### constant, immutable
**공통점**
- state variable 선언에 사용
- contract가 생성된 뒤에 변경 불가  
- 컴파일러는 변수에 대한 저장 공간을 예약 하지 않음 -> 이 말은 어셈블리어에서 실제 값이 들어간다는 말? 
- state variable과 비교하여 가스 비용이 더 낮음

**차이점**
- constant
    - 컴파일할 때 값이 고정
    - 접근될 때마다 평가됨
- immutable
    - 생성시간에 값이 할당됨
    - contruction time에 평가됨
    - constant보다 제한적


``` solidity
pragma solidity >=0.7.4;

uint constant X = 32**22 + 8;

contract C {
    string constant TEXT = "abc";
    bytes32 constant MY_HASH = keccak256("abc");
    uint immutable decimals;
    uint immutable maxBalance;
    address immutable owner = msg.sender;

    constructor(uint _decimals, address _reference) {
        decimals = _decimals;
        // Assignments to immutables can even access the environment.
        maxBalance = _reference.balance;
    }

    function isBalanceTooHigh(address _other) public view returns (bool) {
        return _other.balance > maxBalance;
    }
}
```

# Functions
- 함수는 contract의 안과 밖에 선언될 수 있음
- free functions
    - contract 밖의 함수
    - 암묵적으로 internal visibitlisy를 가짐
    - 호출하는 contract에 코드가 포함됨
    - storage variable과 범위에 포함되지 않은 function에 직접 접근이 불가능


``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >0.7.0 <0.9.0;

// free function
function sum(uint[] memory _arr) pure returns (uint s) {
    for (uint i = 0; i < _arr.length; i++)
        s += _arr[i];
}

contract ArrayExample {
    bool found;
    function f(uint[] memory _arr) public {
        // free function 호출
        // 컴파일러는 이 코드를 contract에 추가
        uint s = sum(_arr);
        require(s >= 10);
        found = true;
    }
}
```

## Function Parameters and Return Variable
- 함수의 파라미터는 타입을 가짐
- 임의 개수의 값을 반환

### Function Parameter
- 변수과 같은 방식으로 선언됨
- 사용되지 않는 매개변수의 이름은 생략 가능

``` solidity
function func(uint k, uint ) returns(uint myValue) {
  myValue=404;
}
```

- 지역 변수로 사용 가능
- 할당 가능
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract Simple {
    uint sum;
    function taker(uint _a, uint _b) public {
        sum = _a + _b;
    }
}
```
### Return Variable
- `returns` 키워드 다음에 선언되는 문장

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract Simple {
    function arithmetic(uint _a, uint _b)
        public
        pure
        returns (uint o_sum, uint o_product)
    {
        // 2개의 리턴값
        o_sum = _a + _b;
        o_product = _a * _b;
    }
}
```

- 리턴 값의 이름은 생략될 수 있음
- 다른 지역 변수로 사용 가능
- 다시 할당 될 대 default 값으로 초기화
- return문을 사용하여 값을 반환할 수 있음

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract Simple {
    function arithmetic(uint _a, uint _b)
        public
        pure
        returns (uint o_sum, uint o_product)
    {
        /*
            o_sum = _a + _b;
            o_product = _a * _b;
        */
        return (_a + _b, _a * _b); // return 사용
    }
}
```

### Returning Multiple Values
- `return (v0, v1, ..., vn)`
- 개수와 타입이 일치해야 함

## View Functions
- `view`: 상태를 수정하지 않겠다고 약속
- 상태를 수정하는 문장
    1. state variable에 쓰기
    2. event
    3. 다른 contract 생성
    4. `selfdestruct`사용
    5. 호출을 통해 Ether 전송
    6. `view` 혹은 `pure`가 없는 함수 호출
    7. low-level의 호출 사용
    8. 특정 opcode가 포함된 inline assembly 사용

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.5.0 <0.9.0;

contract C {
    function f(uint a, uint b) public view returns (uint) {
        return a * (b + 42) + block.timestamp;
    }
}
```

- getter 메서드는 자동적으로 view로 표시됨

## Pure Functions
- `pure`로 선언된 함수
- 읽거나 상태를 변경하지 않음을 약속
- 읽는 것으로 간주되는 상황
    1. state variable 읽기
    2. `address(this).balance` 혹은 `<address>.balance` 접근
    3. `block`, `tx`, `msg` 멤버들에 접근
    4. `pure`로 표기되지 않은 함수 호출
    5.  특정 opcode가 포함된 inline assembly 사용

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.5.0 <0.9.0;

contract C {
    function f(uint a, uint b) public pure returns (uint) {
        return a * (b + 42);
    }
}
```

- 에러 발생시에 발생할 수 있는 잠재적인 상태변화를 되돌리기 위해 `revert()`와 `require()` 사용 가능

## Receive Ether Function
- contract는 최대 한 개의 `receive` function을 가질 수 있음
    - `function` 키워드 없이 `receive() external payable { ... }` 사용
- argument를 가질 수 없고 아무것도 반환할 수 없음
- `external` visibility와 `payable` 상태를 반드시 가짐
- 가상일 수 있고, 재정의 될수 있고, modifier을 가질 수 있음

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.0 <0.9.0;

// This contract keeps all Ether sent to it with no way
// to get it back.
contract Sink {
    event Received(address, uint);
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }
}
```

## Fallback Function
- contract는 최대 한 개의 fallback 함수를 가질 수 있음
    - function 키워드 없이 `fallback () external [payable]`사용
    - function 키워드 없이 `fallback (bytes calldata _input) external [payable] returns (bytes memory)` 사용
- 반드시 external visibility를 가짐
- 가상일 수 있고, 재정의 될 수 있고, modifier를 가질 수 있음
- 주어진 function signature과 일치하는 함수가 없거나 receive Ether function이 없는 계약을 호출할 때 실행
- 항상 data를 수신하지만, Ether을 받기 위해서는 payable를 반드시 표시

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.2 <0.9.0;

contract Test {
    // This function is called for all messages sent to
    // this contract (there is no other function).
    // Sending Ether to this contract will cause an exception,
    // because the fallback function does not have the `payable`
    // modifier.
    fallback() external { x = 1; }
    uint x;
}

contract TestPayable {
    // This function is called for all messages sent to
    // this contract, except plain Ether transfers
    // (there is no other function except the receive function).
    // Any call with non-empty calldata to this contract will execute
    // the fallback function (even if Ether is sent along with the call).
    fallback() external payable { x = 1; y = msg.value; }

    // This function is called for plain Ether transfers, i.e.
    // for every call with empty calldata.
    receive() external payable { x = 2; y = msg.value; }
    uint x;
    uint y;
}

contract Caller {
    function callTest(Test test) public returns (bool) {
        (bool success,) = address(test).call(abi.encodeWithSignature("nonExistingFunction()"));
        require(success);
        // results in test.x becoming == 1.

        // address(test) will not allow to call ``send`` directly, since ``test`` has no payable
        // fallback function.
        // It has to be converted to the ``address payable`` type to even allow calling ``send`` on it.
        address payable testPayable = payable(address(test));

        // If someone sends Ether to that contract,
        // the transfer will fail, i.e. this returns false here.
        return testPayable.send(2 ether);
    }

    function callTestPayable(TestPayable test) public returns (bool) {
        (bool success,) = address(test).call(abi.encodeWithSignature("nonExistingFunction()"));
        require(success);
        // results in test.x becoming == 1 and test.y becoming 0.
        (success,) = address(test).call{value: 1}(abi.encodeWithSignature("nonExistingFunction()"));
        require(success);
        // results in test.x becoming == 1 and test.y becoming 1.

        // If someone sends Ether to that contract, the receive function in TestPayable will be called.
        // Since that function writes to storage, it takes more gas than is available with a
        // simple ``send`` or ``transfer``. Because of that, we have to use a low-level call.
        (success,) = address(test).call{value: 2 ether}("");
        require(success);
        // results in test.x becoming == 2 and test.y becoming 2 ether.

        return true;
    }
}
```


## Function Overloading

- contract는 같은 이름을 가지는 인자가 다른 함수를 가질 수 있음

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract A {
    function f(uint _in) public pure returns (uint out) {
        out = _in;
    }

    function f(uint _in, bool _really) public pure returns (uint out) {
        if (_really)
            out = _in;
    }
}
```

- external 인터페이스에 오버로드 된 함수가 있을 수 있음
- solidity type이 아니라 external 타입에 따라 다른 경우 에러가 발생

``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

// This will not compile
contract A {
    function f(B _in) public pure returns (B out) {
        out = _in;
    }

    function f(address _in) public pure returns (address out) {
        out = _in;
    }
}

contract B {
}
```


### Overload resolution and Argument matching
- 오버로드 함수는 argument에 따라 선택됨
- 오버로드 함수들 중 예상 타입으로 변경 가능하면 선택됨
- 선택할 수 있는 함수가 하나가 아니라면 실패
``` solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract A {
    function f(uint8 _in) public pure returns (uint8 out) {
        out = _in;
    }

    function f(uint256 _in) public pure returns (uint256 out) {
        out = _in;
    }
}
```
- `f(50)`을 호출한 경우 에러가 발생 -> 50은 `uint8`와 `uint256` 모두 변경 가능하기 때문




