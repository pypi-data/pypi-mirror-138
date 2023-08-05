const Config = require('../utils/config');
const Constants = require('../utils/constants');
const HeartbeatCache = require('../reports/heartbeat_cache');
const RestAPI = require('../backend/restAPI');
const RulesManager = require('../rules/rules_manager');
const Logger = require('../utils/logger');

let intervalId = null;

function stopHeartBeatTimer(statusCode) {
    if (intervalId === null || statusCode !== Constants.APP_DELETE_STATUS_CODE) {
        return;
    }

    Logger.write(Logger.ERROR && `Deletion triggered from PO dashboard, this app is no longer protected.`);
    clearInterval(intervalId);
    intervalId = null;
}

function syncRules() {
    return new Promise((resolve) => {
        const heartbeatInfo = {};
        heartbeatInfo[Constants.HEARTBEAT_HASH_KEY] = RulesManager.hash;
        const {reports, inventory} = HeartbeatCache.flush();
        heartbeatInfo[Constants.HEARTBEAT_REPORT_KEY] = reports;
        heartbeatInfo[Constants.HEARTBEAT_INVENTORY_KEY] = inventory;
        if (RulesManager.isAppDeleted()) {
            stopHeartBeatTimer(Constants.APP_DELETE_STATUS_CODE);
            resolve([]);
            return;
        }

        const restApi = new RestAPI(Constants.REST_API_HEART_BEAT, heartbeatInfo);
        Logger.write(Logger.DEBUG && `Sending heartbeat to backend: ${heartbeatInfo}`);
        restApi.post().then((rulesData) => {
            RulesManager.handleIncomingRules(rulesData);
            resolve(RulesManager.runtimeRules);
            stopHeartBeatTimer(rulesData.statusCode);
        }).catch((e) => {
            Logger.write(Logger.INFO && `Failed to send heartbeat with error: ${e}`);

            // Do a resolve here as we don't want the agent to fail if heartbeat fails
            // TODO: Should we stop sending heartbeat on 'n' consecutive failures
            resolve([]);
        })
    });
}


function startHeartbeatTimer() {
    // Send heartbeat every n seconds as defined by Config.syncInterval
    intervalId = setInterval(syncRules, Config.syncInterval);
    intervalId.unref();
}

module.exports = startHeartbeatTimer;
