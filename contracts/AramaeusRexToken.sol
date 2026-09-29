// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

/**
 * @title AramaeusRexToken
 * @dev Deflationary asset with hardcoded Islamic Finance (Zero Riba, Anti-Kanz) constraints.
 */
contract AramaeusRexToken {
    string public name = "Aramaeus Rex";
    string public symbol = "REX";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => uint256) public lastActivity; // For Anti-Kanz (hoarding) mechanics

    uint256 public constant DEMURRAGE_INTERVAL = 365 days;
    uint256 public constant DEMURRAGE_RATE = 25; // 2.5% Zakat-inspired decay if inactive

    event Transfer(address indexed from, address indexed to, uint256 value);
    event DemurrageApplied(address indexed account, uint256 amount);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        lastActivity[msg.sender] = block.timestamp;
    }

    /**
     * @dev Core transfer function. Enforces activity to prevent hoarding.
     */
    function transfer(address to, uint256 amount) public returns (bool) {
        require(to != address(0), "Cannot transfer to zero address");
        
        _applyDemurrage(msg.sender);
        
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");

        // Execute transfer
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;

        // Update activity timestamps
        lastActivity[msg.sender] = block.timestamp;
        lastActivity[to] = block.timestamp;

        emit Transfer(msg.sender, to, amount);
        return true;
    }

    /**
     * @dev Anti-Kanz constraint: Applies decay to idle capital.
     * Forces money to remain relational and active in the graph.
     */
    function _applyDemurrage(address account) internal {
        uint256 timeIdle = block.timestamp - lastActivity[account];
        if (timeIdle >= DEMURRAGE_INTERVAL && balanceOf[account] > 0) {
            uint256 intervals = timeIdle / DEMURRAGE_INTERVAL;
            uint256 decayAmount = (balanceOf[account] * DEMURRAGE_RATE * intervals) / 1000;
            
            if (decayAmount > balanceOf[account]) {
                decayAmount = balanceOf[account];
            }

            balanceOf[account] -= decayAmount;
            totalSupply -= decayAmount; // Burned (deflationary) or could be routed to Solidarity pool

            lastActivity[account] = block.timestamp;
            emit DemurrageApplied(account, decayAmount);
        }
    }

    // Notice: There is intentionally no 'approve' or 'transferFrom' standard ERC20 functions here 
    // to prevent automated DeFi protocols from building Usury/Yield-farming loops on top of this asset.
    // The asset must be moved peer-to-peer.
}
