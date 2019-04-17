const Migrations = artifacts.require("Migrations");
const Inbox = artifacts.require("Inbox");
const Dealer = artifacts.require("Dealer");

module.exports = function(deployer) {
  deployer.deploy(Migrations).then(function() {
    return deployer.deploy(Inbox).then(function() {
    return deployer.deploy(Dealer);
    })
  })
};
