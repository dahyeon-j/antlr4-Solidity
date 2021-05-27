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

**차이점**
- constant: 컴파일할 때 값이 고정
- immutable: 생성시간에 값이 할당됨

state variable과 비교하여 constant variable, immutable variable의 가스 비용이 더 낮음

constant variable가 할당되는 표현식에는 모두 값이 복사되고, 매번 다시 평가되어 로컬 최적화






