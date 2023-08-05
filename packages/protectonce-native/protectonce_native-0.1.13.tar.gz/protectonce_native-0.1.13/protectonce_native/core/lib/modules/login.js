const RestAPI = require('../backend/restAPI');
const Constants = require('../utils/constants');
const Config = require('../utils/config');
const RulesManager = require('../rules/rules_manager');
const Logger = require('../utils/logger');
const startHeartbeatTimer = require('../modules/sync');

function login(runtimeInfo) {
    return new Promise((resolve, reject) => {
        Config.runtimeInfo = runtimeInfo;
        const restApi = new RestAPI(Constants.REST_API_LOGIN, Config.info);

        if (RulesManager.isAppDeleted()) {
            Logger.write(Logger.ERROR && `Deletion triggered from PO dashboard, this app is no longer protected.`);
            resolve([]);
            return;
        }

        restApi.post().then((rulesData) => {
            Logger.write(Logger.DEBUG && `Login returned: ${JSON.stringify(rulesData)}`);
            RulesManager.handleIncomingRules(rulesData);
            resolve(RulesManager.runtimeRules);
            startHeartbeatTimer();
        }).catch((e) => {
            Logger.write(Logger.ERROR && `Failed to login with error: ${e})`);

            resolve([]);
        });
    });
}

module.exports = login;
