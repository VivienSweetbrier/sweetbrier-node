// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

import "./AramaeusRexToken.sol";

/**
 * @title SolidarityRouter
 * @dev Gift Economy routing protocol enforcing Catholic Social Teaching (Subsidiarity).
 */
contract SolidarityRouter {
    AramaeusRexToken public token;

    struct PorchNode {
        address localSteward;
        string geographicOrRelationalId;
        bool isActive;
    }

    mapping(address => PorchNode) public porches;
    
    event PorchRegistered(address indexed steward, string id);
    event GiftRouted(address indexed from, address indexed toPorch, uint256 amount, string memo);

    constructor(address _tokenAddress) {
        token = AramaeusRexToken(_tokenAddress);
    }

    /**
     * @dev Register a local node (a "Porch").
     * Subsidiarity requires empowering the most local level.
     */
    function registerPorch(string memory _id) public {
        require(!porches[msg.sender].isActive, "Porch already active");
        porches[msg.sender] = PorchNode(msg.sender, _id, true);
        emit PorchRegistered(msg.sender, _id);
    }

    /**
     * @dev Route capital directly to a local porch as a gift.
     * Prevents centralized hoarding. Capital moves purely based on relational intent.
     */
    function routeGift(address _toPorch, uint256 _amount, string memory _memo) public {
        require(porches[_toPorch].isActive, "Target is not an active Porch");
        
        // Transfer relies on the token's Anti-Kanz transfer mechanism
        bool success = token.transfer(_toPorch, _amount);
        require(success, "Gift transfer failed");

        emit GiftRouted(msg.sender, _toPorch, _amount, _memo);
    }
}
