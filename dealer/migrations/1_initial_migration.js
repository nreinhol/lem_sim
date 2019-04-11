const Migrations = artifacts.require("Migrations");
const Inbox = artifacts.require("Inbox");

module.exports = function(deployer) {
  deployer.deploy(Migrations).then(function() {
    return deployer.deploy(Inbox);
  })
};
