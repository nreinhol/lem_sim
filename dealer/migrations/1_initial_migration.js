const Migrations = artifacts.require("Migrations");
const Dealer = artifacts.require("Dealer"); 

module.exports = function(deployer, network, accounts) {
  deployer.deploy(Migrations)  
  deployer.deploy(Dealer, {from: accounts[0]})
};
