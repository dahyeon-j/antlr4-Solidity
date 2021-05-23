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
